"""Home Assistant-side device naming for AquaNode Pulse."""

from __future__ import annotations

from homeassistant.components.text import TextEntity, TextMode
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import EntityCategory
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from .const import CONF_DISPLAY_NAME
from .coordinator import AquaNodePulseCoordinator
from .entity import AquaNodePulseEntity


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Add the local display-name setting."""
    async_add_entities(
        [AquaNodePulseDisplayName(entry.runtime_data.coordinator, entry)],
    )


class AquaNodePulseDisplayName(AquaNodePulseEntity, TextEntity):
    """Name shown by the local dashboard and notification messages."""

    _attr_translation_key = "display_name"
    _attr_icon = "mdi:rename"
    _attr_entity_category = EntityCategory.CONFIG
    _attr_mode = TextMode.TEXT
    _attr_native_min = 1
    _attr_native_max = 40

    def __init__(
        self,
        coordinator: AquaNodePulseCoordinator,
        entry: ConfigEntry,
    ) -> None:
        super().__init__(coordinator, "display_name")
        self._entry = entry

    @property
    def native_value(self) -> str:
        """Return the name currently used by the integration."""
        return self.coordinator.display_name

    async def async_set_value(self, value: str) -> None:
        """Persist a concise, non-empty local name."""
        cleaned = " ".join(value.split())[: self.native_max]
        if not cleaned:
            return
        options = dict(self._entry.options)
        options[CONF_DISPLAY_NAME] = cleaned
        self.hass.config_entries.async_update_entry(
            self._entry,
            title=cleaned,
            options=options,
        )
        self.async_write_ha_state()
