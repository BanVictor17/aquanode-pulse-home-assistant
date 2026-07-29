"""Controls for AquaNode Pulse."""

from __future__ import annotations

from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import EntityCategory
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from .const import (
    CONF_AUTOMATIC_NOTIFICATIONS,
    CONF_DIAGNOSTIC_LOGGING,
    CONF_ROUTER_ON_UPS,
    DEFAULT_AUTOMATIC_NOTIFICATIONS,
    DEFAULT_DIAGNOSTIC_LOGGING,
    DEFAULT_ROUTER_ON_UPS,
)
from .coordinator import AquaNodePulseCoordinator
from .entity import AquaNodePulseEntity


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Add the online LED control."""
    coordinator = entry.runtime_data.coordinator
    async_add_entities(
        [
            AquaNodePulseIdleLedSwitch(coordinator),
            AquaNodePulseAutomaticNotificationsSwitch(coordinator, entry),
            AquaNodePulseRouterUpsSwitch(coordinator, entry),
            AquaNodePulseDiagnosticLoggingSwitch(coordinator, entry),
        ],
    )


class AquaNodePulseIdleLedSwitch(AquaNodePulseEntity, SwitchEntity):
    """Enable the steady LED without changing diagnostic blink patterns."""

    _attr_translation_key = "idle_led"
    _attr_icon = "mdi:led-on"

    def __init__(self, coordinator: AquaNodePulseCoordinator) -> None:
        super().__init__(coordinator, "idle_led")

    @property
    def is_on(self) -> bool:
        """Return the current board setting."""
        return self.coordinator.data["settings"]["idle_led_on"]

    async def async_turn_on(self, **kwargs) -> None:
        """Keep the LED on while the device is healthy."""
        await self.coordinator.api.async_set_idle_led(True)
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs) -> None:
        """Turn the healthy-state LED off."""
        await self.coordinator.api.async_set_idle_led(False)
        await self.coordinator.async_request_refresh()


class AquaNodePulseAutomaticNotificationsSwitch(
    AquaNodePulseEntity,
    SwitchEntity,
):
    """Enable the integration's automatic HA notification-center alerts."""

    _attr_translation_key = "automatic_notifications"
    _attr_icon = "mdi:bell-ring-outline"
    _attr_entity_category = EntityCategory.CONFIG

    def __init__(
        self,
        coordinator: AquaNodePulseCoordinator,
        entry: ConfigEntry,
    ) -> None:
        super().__init__(coordinator, "automatic_notifications")
        self._entry = entry

    @property
    def is_on(self) -> bool:
        return bool(
            self._entry.options.get(
                CONF_AUTOMATIC_NOTIFICATIONS,
                DEFAULT_AUTOMATIC_NOTIFICATIONS,
            ),
        )

    async def async_turn_on(self, **kwargs) -> None:
        self._set_enabled(True)

    async def async_turn_off(self, **kwargs) -> None:
        self._set_enabled(False)

    def _set_enabled(self, enabled: bool) -> None:
        options = dict(self._entry.options)
        options[CONF_AUTOMATIC_NOTIFICATIONS] = enabled
        self.hass.config_entries.async_update_entry(
            self._entry,
            options=options,
        )
        self.async_write_ha_state()


class AquaNodePulseDiagnosticLoggingSwitch(
    AquaNodePulseEntity,
    SwitchEntity,
):
    """Enable concise polling diagnostics in the Home Assistant log."""

    _attr_translation_key = "diagnostic_logging"
    _attr_icon = "mdi:bug-outline"
    _attr_entity_category = EntityCategory.DIAGNOSTIC

    def __init__(
        self,
        coordinator: AquaNodePulseCoordinator,
        entry: ConfigEntry,
    ) -> None:
        super().__init__(coordinator, "diagnostic_logging")
        self._entry = entry

    @property
    def is_on(self) -> bool:
        return bool(
            self._entry.options.get(
                CONF_DIAGNOSTIC_LOGGING,
                DEFAULT_DIAGNOSTIC_LOGGING,
            ),
        )

    async def async_turn_on(self, **kwargs) -> None:
        self._set_enabled(True)

    async def async_turn_off(self, **kwargs) -> None:
        self._set_enabled(False)

    def _set_enabled(self, enabled: bool) -> None:
        options = dict(self._entry.options)
        options[CONF_DIAGNOSTIC_LOGGING] = enabled
        self.hass.config_entries.async_update_entry(
            self._entry,
            options=options,
        )
        self.async_write_ha_state()
        self.coordinator.async_update_listeners()


class AquaNodePulseRouterUpsSwitch(
    AquaNodePulseEntity,
    SwitchEntity,
):
    """Treat disappearance as a power cut when network equipment has backup."""

    _attr_translation_key = "router_on_ups"
    _attr_icon = "mdi:router-wireless"
    _attr_entity_category = EntityCategory.CONFIG

    def __init__(
        self,
        coordinator: AquaNodePulseCoordinator,
        entry: ConfigEntry,
    ) -> None:
        super().__init__(coordinator, "router_on_ups")
        self._entry = entry

    @property
    def is_on(self) -> bool:
        return bool(
            self._entry.options.get(
                CONF_ROUTER_ON_UPS,
                DEFAULT_ROUTER_ON_UPS,
            ),
        )

    async def async_turn_on(self, **kwargs) -> None:
        self._set_enabled(True)

    async def async_turn_off(self, **kwargs) -> None:
        self._set_enabled(False)

    def _set_enabled(self, enabled: bool) -> None:
        options = dict(self._entry.options)
        options[CONF_ROUTER_ON_UPS] = enabled
        self.hass.config_entries.async_update_entry(
            self._entry,
            options=options,
        )
        self.async_write_ha_state()
        self.coordinator.async_update_listeners()
