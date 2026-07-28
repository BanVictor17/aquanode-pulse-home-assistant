"""Controls for AquaNode Pulse."""

from __future__ import annotations

from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from .coordinator import AquaNodePulseCoordinator
from .entity import AquaNodePulseEntity


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Add the online LED control."""
    async_add_entities(
        [AquaNodePulseIdleLedSwitch(entry.runtime_data.coordinator)],
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
