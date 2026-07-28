"""Actions for AquaNode Pulse."""

from __future__ import annotations

from homeassistant.components.button import ButtonEntity, ButtonEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import EntityCategory
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from .coordinator import AquaNodePulseCoordinator
from .entity import AquaNodePulseEntity

BUTTONS: tuple[ButtonEntityDescription, ...] = (
    ButtonEntityDescription(
        key="identify",
        translation_key="identify",
        icon="mdi:led-on",
    ),
    ButtonEntityDescription(
        key="restart",
        translation_key="restart",
        icon="mdi:restart",
        entity_category=EntityCategory.CONFIG,
    ),
    ButtonEntityDescription(
        key="reset_calibration",
        translation_key="reset_calibration",
        icon="mdi:restore",
        entity_category=EntityCategory.CONFIG,
    ),
    ButtonEntityDescription(
        key="clear_history",
        translation_key="clear_history",
        icon="mdi:delete-sweep-outline",
        entity_category=EntityCategory.CONFIG,
    ),
    ButtonEntityDescription(
        key="test_notification",
        translation_key="test_notification",
        icon="mdi:bell-check-outline",
        entity_category=EntityCategory.CONFIG,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Add Pulse actions."""
    coordinator = entry.runtime_data.coordinator
    async_add_entities(
        AquaNodePulseButton(coordinator, description) for description in BUTTONS
    )


class AquaNodePulseButton(AquaNodePulseEntity, ButtonEntity):
    """A safe explicit action."""

    entity_description: ButtonEntityDescription

    def __init__(
        self,
        coordinator: AquaNodePulseCoordinator,
        description: ButtonEntityDescription,
    ) -> None:
        super().__init__(coordinator, description.key)
        self.entity_description = description

    async def async_press(self) -> None:
        """Run the requested action."""
        if self.entity_description.key == "identify":
            await self.coordinator.api.async_identify()
            return
        if self.entity_description.key == "restart":
            self.coordinator.suppress_connection_alerts()
            await self.coordinator.api.async_restart()
            return
        if self.entity_description.key == "reset_calibration":
            await self.coordinator.api.async_reset_voltage_calibration()
            await self.coordinator.async_request_refresh()
            return
        if self.entity_description.key == "test_notification":
            self.coordinator.send_test_notification()
            return
        await self.coordinator.history.async_clear_events(
            self.coordinator.serial,
        )
        await self.coordinator.async_request_refresh()
