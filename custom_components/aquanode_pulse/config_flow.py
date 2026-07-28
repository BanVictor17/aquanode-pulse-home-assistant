"""UI setup and automatic discovery for AquaNode Pulse."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.components import zeroconf
from homeassistant.const import CONF_HOST
from homeassistant.core import HomeAssistant, callback
from homeassistant.data_entry_flow import ConfigFlowResult
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.selector import (
    NumberSelector,
    NumberSelectorConfig,
    NumberSelectorMode,
    TextSelector,
    TextSelectorConfig,
    TextSelectorType,
)

from .api import (
    AquaNodePulseApi,
    AquaNodePulseApiError,
    AquaNodePulseCannotConnect,
    AquaNodePulseInvalidAuth,
    AquaNodePulseInvalidResponse,
)
from .const import CONF_PASSWORD, CONF_PORT, DEFAULT_PORT, DOMAIN


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

    async def async_step_zeroconf(
        self,
        discovery_info: zeroconf.ZeroconfServiceInfo,
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
            step_id="user",
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
                    vol.Required("reference_voltage", default=230.0):
                        NumberSelector(
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
