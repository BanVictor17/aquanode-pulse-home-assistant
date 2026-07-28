"""UI setup and automatic discovery for AquaNode Pulse."""

from __future__ import annotations

import asyncio
import logging
import time
from collections.abc import Mapping
from ipaddress import ip_address, ip_network
from typing import Any

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.config_entries import ConfigFlowResult
from homeassistant.const import CONF_HOST
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.selector import (
    NumberSelector,
    NumberSelectorConfig,
    NumberSelectorMode,
    SelectSelector,
    SelectSelectorConfig,
    SelectSelectorMode,
    TextSelector,
    TextSelectorConfig,
    TextSelectorType,
)
from homeassistant.helpers.service_info.zeroconf import ZeroconfServiceInfo

from .api import (
    AquaNodePulseApi,
    AquaNodePulseApiError,
    AquaNodePulseCannotConnect,
    AquaNodePulseInvalidAuth,
    AquaNodePulseInvalidResponse,
)
from .const import CONF_PASSWORD, CONF_PORT, DEFAULT_PORT, DOMAIN

_LOGGER = logging.getLogger(__name__)

SERVICE_TYPE = "_aquanode-pulse._tcp.local."
DISCOVERY_SECONDS = 6.0
SWEEP_CONCURRENCY = 64
SWEEP_TIMEOUT = 2.0
MANUAL = "manual"


async def _async_scan(hass: HomeAssistant) -> dict[str, dict[str, Any]]:
    """Look for Pulse boards on the LAN, keyed by serial.

    Home Assistant announces devices it discovered on its own as a separate card
    on the integrations page. Picking the integration from the Add Integration
    list always starts the user step instead, which is why this used to open a
    bare form asking for an IP address that nobody knows by heart.

    The browser exists to put a question on the wire; the answers are read out
    of Home Assistant's own zeroconf cache, which is the same place its built-in
    discovery looks. Reading the cache rather than counting on a callback means
    a board that answered before this flow opened is found immediately, and one
    that answers while it is open is picked up on the next poll.
    """
    from homeassistant.components import zeroconf as ha_zeroconf
    from zeroconf import DNSPointer
    from zeroconf.asyncio import AsyncServiceBrowser, AsyncServiceInfo
    from zeroconf.const import _CLASS_IN, _TYPE_PTR

    aiozc = await ha_zeroconf.async_get_async_instance(hass)
    zc = aiozc.zeroconf
    # The browser is only here to put a question on the wire; the answers come
    # from the cache below. It still needs a handler: constructing one without
    # any raises "You need to specify at least one handler".
    browser = AsyncServiceBrowser(
        zc,
        [SERVICE_TYPE],
        handlers=[lambda **kwargs: None],
    )
    found: dict[str, dict[str, Any]] = {}
    try:
        deadline = time.monotonic() + DISCOVERY_SECONDS
        while True:
            for record in zc.cache.async_all_by_details(
                SERVICE_TYPE, _TYPE_PTR, _CLASS_IN
            ):
                if not isinstance(record, DNSPointer):
                    continue
                info = AsyncServiceInfo(SERVICE_TYPE, record.alias)
                if not info.load_from_cache(zc):
                    await info.async_request(zc, 2000)
                if (device := _extract(info)) is None:
                    continue
                serial, host, port = device
                found[serial] = {
                    CONF_HOST: host,
                    CONF_PORT: port,
                    "name": f"AquaNode Pulse {serial.removeprefix('AP-')}",
                }
            if found or time.monotonic() >= deadline:
                # An empty cache here means Home Assistant never received the
                # board's announcement at all, which is a network problem
                # (usually a container without host networking, or a router
                # that does not forward multicast) rather than a parsing one.
                _LOGGER.info(
                    "AquaNode Pulse scan: %d in the zeroconf cache, %d usable",
                    len(
                        zc.cache.async_all_by_details(
                            SERVICE_TYPE, _TYPE_PTR, _CLASS_IN
                        )
                    ),
                    len(found),
                )
                return found
            await asyncio.sleep(0.5)
    finally:
        await browser.async_cancel()


def _candidate_networks(hass: HomeAssistant) -> list[str]:
    """Guess which /24 the boards live on, without asking.

    mDNS is multicast and multicast does not cross a Docker bridge, so on a
    containerised Home Assistant discovery cannot work no matter how the browse
    is written. Unicast does cross it, which is how every other local
    integration reaches its device, so their addresses are the one hint
    available from inside the container about the real network.
    """
    networks: list[str] = []
    for entry in hass.config_entries.async_entries():
        host = str(entry.data.get(CONF_HOST) or "")
        try:
            address = ip_address(host)
        except ValueError:
            continue
        if address.version != 4 or not address.is_private:
            continue
        network = str(ip_network(f"{host}/24", strict=False))
        if network not in networks:
            networks.append(network)
    return networks


async def _async_sweep(hass: HomeAssistant, network: str) -> dict[str, dict[str, Any]]:
    """Ask every address on one /24 whether it is a Pulse.

    `/api/v1/info` needs no password, so this identifies boards without the
    label in hand. Two hundred and fifty four short requests in parallel take
    about as long as one timeout.
    """
    session = async_get_clientsession(hass)
    semaphore = asyncio.Semaphore(SWEEP_CONCURRENCY)

    async def probe(host: str) -> tuple[str, dict[str, Any]] | None:
        async with semaphore:
            try:
                async with asyncio.timeout(SWEEP_TIMEOUT):
                    response = await session.get(
                        f"http://{host}:{DEFAULT_PORT}/api/v1/info"
                    )
                    payload = await response.json(content_type=None)
            except Exception:  # noqa: BLE001 - an address that is not a Pulse
                return None
        if not isinstance(payload, dict) or payload.get("api_version") != 1:
            return None
        serial = str(payload.get("serial") or "").upper()
        if not serial.startswith("AP-"):
            return None
        return serial, {
            CONF_HOST: host,
            CONF_PORT: DEFAULT_PORT,
            "name": payload.get("name")
            or f"AquaNode Pulse {serial.removeprefix('AP-')}",
        }

    results = await asyncio.gather(
        *(probe(str(host)) for host in ip_network(network).hosts()),
    )
    return {serial: device for found in results if found for serial, device in [found]}


def _extract(info: Any) -> tuple[str, str, int] | None:
    """Pull serial, address and port out of one mDNS answer.

    `info.properties` is keyed by bytes; only Home Assistant's own
    ZeroconfServiceInfo normalises to str. Reading "serial" off the raw mapping
    returns nothing, which rejects every board as "not one of ours".
    """
    serial = str(info.decoded_properties.get("serial") or "").upper()
    addresses = info.parsed_scoped_addresses()
    if not addresses or not serial.startswith("AP-"):
        return None
    return serial, addresses[0], info.port or DEFAULT_PORT


def _property(properties: dict[str, Any], key: str) -> str:
    value = properties.get(key, "")
    if isinstance(value, bytes):
        return value.decode(errors="ignore")
    return str(value)


async def _async_validate(
    hass: HomeAssistant,
    host: str,
    port: int,
    password: str,
    expected_serial: str | None = None,
) -> dict[str, Any]:
    api = AquaNodePulseApi(
        async_get_clientsession(hass),
        host,
        port,
        password,
    )
    data = await api.async_status()
    if expected_serial and data["serial"] != expected_serial:
        raise AquaNodePulseInvalidResponse("serial changed")
    return data


class AquaNodePulseConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Set up a Pulse found on the local network."""

    VERSION = 1

    def __init__(self) -> None:
        self._host: str | None = None
        self._port = DEFAULT_PORT
        self._serial: str | None = None
        self._name: str | None = None
        self._found: dict[str, dict[str, Any]] = {}

    async def async_step_zeroconf(
        self,
        discovery_info: ZeroconfServiceInfo,
    ) -> ConfigFlowResult:
        """Receive the board's mDNS advertisement."""
        serial = _property(discovery_info.properties, "serial").upper()
        if not serial.startswith("AP-"):
            return self.async_abort(reason="invalid_discovery")

        self._host = discovery_info.host
        self._port = discovery_info.port or DEFAULT_PORT
        self._serial = serial
        self._name = f"AquaNode Pulse {serial.removeprefix('AP-')}"
        await self.async_set_unique_id(serial)
        self._abort_if_unique_id_configured(
            updates={CONF_HOST: self._host, CONF_PORT: self._port},
        )
        self.context["title_placeholders"] = {"name": self._name}
        return await self.async_step_confirm()

    async def async_step_confirm(
        self,
        user_input: dict[str, Any] | None = None,
    ) -> ConfigFlowResult:
        """Confirm a discovered device using the label password."""
        errors: dict[str, str] = {}
        if user_input is not None:
            try:
                data = await _async_validate(
                    self.hass,
                    self._host or "",
                    self._port,
                    user_input[CONF_PASSWORD],
                    self._serial,
                )
            except AquaNodePulseInvalidAuth:
                errors["base"] = "invalid_auth"
            except AquaNodePulseCannotConnect:
                errors["base"] = "cannot_connect"
            except AquaNodePulseApiError:
                errors["base"] = "unknown"
            else:
                return self.async_create_entry(
                    title=data.get("name", self._name),
                    data={
                        CONF_HOST: self._host,
                        CONF_PORT: self._port,
                        CONF_PASSWORD: user_input[CONF_PASSWORD],
                    },
                )

        return self.async_show_form(
            step_id="confirm",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_PASSWORD): TextSelector(
                        TextSelectorConfig(type=TextSelectorType.PASSWORD),
                    ),
                },
            ),
            errors=errors,
            description_placeholders={
                "serial": self._serial or "",
                "host": self._host or "",
            },
        )

    async def async_step_user(
        self,
        user_input: dict[str, Any] | None = None,
    ) -> ConfigFlowResult:
        """Offer the boards found on the network, or fall back to a manual IP."""
        if user_input is None:
            found = await _async_scan(self.hass)
            if not found:
                # Nothing answered the multicast question. On a containerised
                # Home Assistant that is expected rather than exceptional, so
                # fall back to asking every address on the networks the other
                # integrations already talk to.
                for network in _candidate_networks(self.hass):
                    found = await _async_sweep(self.hass, network)
                    _LOGGER.debug("swept %s, found %d", network, len(found))
                    if found:
                        break
            configured = {entry.unique_id for entry in self._async_current_entries()}
            self._found = {
                serial: device
                for serial, device in found.items()
                if serial not in configured
            }
            if self._found:
                return await self.async_step_pick()
        return await self.async_step_manual(user_input)

    async def async_step_pick(
        self,
        user_input: dict[str, Any] | None = None,
    ) -> ConfigFlowResult:
        """Let the customer choose one of the boards that answered."""
        if user_input is not None:
            choice = user_input["device"]
            if choice == MANUAL:
                return await self.async_step_manual()
            device = self._found[choice]
            self._host = device[CONF_HOST]
            self._port = device[CONF_PORT]
            self._serial = choice
            self._name = device["name"]
            await self.async_set_unique_id(choice, raise_on_progress=False)
            self._abort_if_unique_id_configured()
            return await self.async_step_confirm()

        options = [
            {"value": serial, "label": f"{device['name']} ({device[CONF_HOST]})"}
            for serial, device in self._found.items()
        ]
        options.append({"value": MANUAL, "label": "Enter an IP address manually"})
        return self.async_show_form(
            step_id="pick",
            data_schema=vol.Schema(
                {
                    vol.Required("device"): SelectSelector(
                        SelectSelectorConfig(
                            options=options,
                            mode=SelectSelectorMode.LIST,
                        ),
                    ),
                },
            ),
        )

    async def async_step_manual(
        self,
        user_input: dict[str, Any] | None = None,
    ) -> ConfigFlowResult:
        """Manual fallback when mDNS cannot cross a VLAN."""
        errors: dict[str, str] = {}
        if user_input is not None:
            host = user_input[CONF_HOST].strip()
            port = user_input[CONF_PORT]
            try:
                data = await _async_validate(
                    self.hass,
                    host,
                    port,
                    user_input[CONF_PASSWORD],
                )
            except AquaNodePulseInvalidAuth:
                errors["base"] = "invalid_auth"
            except AquaNodePulseCannotConnect:
                errors["base"] = "cannot_connect"
            except AquaNodePulseApiError:
                errors["base"] = "unknown"
            else:
                await self.async_set_unique_id(data["serial"])
                self._abort_if_unique_id_configured(
                    updates={CONF_HOST: host, CONF_PORT: port},
                )
                return self.async_create_entry(
                    title=data.get("name", "AquaNode Pulse"),
                    data={
                        CONF_HOST: host,
                        CONF_PORT: port,
                        CONF_PASSWORD: user_input[CONF_PASSWORD],
                    },
                )

        return self.async_show_form(
            step_id="manual",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_HOST): str,
                    vol.Required(CONF_PORT, default=DEFAULT_PORT): vol.All(
                        vol.Coerce(int),
                        vol.Range(min=1, max=65535),
                    ),
                    vol.Required(CONF_PASSWORD): TextSelector(
                        TextSelectorConfig(type=TextSelectorType.PASSWORD),
                    ),
                },
            ),
            errors=errors,
        )

    async def async_step_reauth(
        self,
        entry_data: Mapping[str, Any],
    ) -> ConfigFlowResult:
        """Ask for the new label password after an authentication error."""
        return await self.async_step_reauth_confirm()

    async def async_step_reauth_confirm(
        self,
        user_input: dict[str, Any] | None = None,
    ) -> ConfigFlowResult:
        """Validate and save replacement credentials."""
        errors: dict[str, str] = {}
        entry = self._get_reauth_entry()
        if user_input is not None:
            try:
                await _async_validate(
                    self.hass,
                    entry.data[CONF_HOST],
                    entry.data.get(CONF_PORT, DEFAULT_PORT),
                    user_input[CONF_PASSWORD],
                    entry.unique_id,
                )
            except AquaNodePulseInvalidAuth:
                errors["base"] = "invalid_auth"
            except AquaNodePulseCannotConnect:
                errors["base"] = "cannot_connect"
            except AquaNodePulseApiError:
                errors["base"] = "unknown"
            else:
                return self.async_update_reload_and_abort(
                    entry,
                    data_updates={CONF_PASSWORD: user_input[CONF_PASSWORD]},
                )

        return self.async_show_form(
            step_id="reauth_confirm",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_PASSWORD): TextSelector(
                        TextSelectorConfig(type=TextSelectorType.PASSWORD),
                    ),
                },
            ),
            errors=errors,
        )

    @staticmethod
    @callback
    def async_get_options_flow(
        config_entry: config_entries.ConfigEntry,
    ) -> config_entries.OptionsFlow:
        """Expose calibration actions under Configure."""
        return AquaNodePulseOptionsFlow()


class AquaNodePulseOptionsFlow(config_entries.OptionsFlow):
    """Calibrate the voltage sensor without any cloud dependency."""

    def _api(self) -> AquaNodePulseApi:
        entry = self.config_entry
        return AquaNodePulseApi(
            async_get_clientsession(self.hass),
            entry.data[CONF_HOST],
            entry.data.get(CONF_PORT, DEFAULT_PORT),
            entry.data[CONF_PASSWORD],
        )

    async def _async_refresh(self) -> None:
        runtime = getattr(self.config_entry, "runtime_data", None)
        if runtime is not None:
            await runtime.coordinator.async_request_refresh()

    async def async_step_init(
        self,
        user_input: dict[str, Any] | None = None,
    ) -> ConfigFlowResult:
        """Show explicit calibration actions."""
        return self.async_show_menu(
            step_id="init",
            menu_options=["calibrate", "reset_calibration"],
        )

    async def async_step_calibrate(
        self,
        user_input: dict[str, Any] | None = None,
    ) -> ConfigFlowResult:
        """Calibrate against a value measured at the same moment."""
        errors: dict[str, str] = {}
        if user_input is not None:
            try:
                await self._api().async_calibrate_voltage(
                    user_input["reference_voltage"],
                )
            except AquaNodePulseInvalidAuth:
                errors["base"] = "invalid_auth"
            except AquaNodePulseCannotConnect:
                errors["base"] = "cannot_connect"
            except AquaNodePulseApiError as err:
                errors["base"] = str(err)
            else:
                await self._async_refresh()
                return self.async_create_entry(title="", data={})

        return self.async_show_form(
            step_id="calibrate",
            data_schema=vol.Schema(
                {
                    vol.Required("reference_voltage", default=230.0): NumberSelector(
                        NumberSelectorConfig(
                            min=50,
                            max=280,
                            step=0.1,
                            mode=NumberSelectorMode.BOX,
                            unit_of_measurement="V",
                        ),
                    ),
                },
            ),
            errors=errors,
        )

    async def async_step_reset_calibration(
        self,
        user_input: dict[str, Any] | None = None,
    ) -> ConfigFlowResult:
        """Require a confirmation before removing calibration."""
        errors: dict[str, str] = {}
        if user_input is not None:
            try:
                await self._api().async_reset_voltage_calibration()
            except AquaNodePulseInvalidAuth:
                errors["base"] = "invalid_auth"
            except AquaNodePulseCannotConnect:
                errors["base"] = "cannot_connect"
            except AquaNodePulseApiError:
                errors["base"] = "unknown"
            else:
                await self._async_refresh()
                return self.async_create_entry(title="", data={})
        return self.async_show_form(
            step_id="reset_calibration",
            data_schema=vol.Schema({}),
            errors=errors,
        )
