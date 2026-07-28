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
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Add Pulse actions."""
    coordinator = entry.runtime_data.coordinator
    async_add_entities(
        AquaNodePulseButton(coordinator, description)
        for description in BUTTONS
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
        await self.coordinator.api.async_restart()
