"""Local alert threshold for AquaNode Pulse."""

from __future__ import annotations

from homeassistant.components.number import NumberDeviceClass, NumberEntity, NumberMode
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import EntityCategory, UnitOfElectricPotential
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from .const import CONF_VOLTAGE_MINIMUM, DEFAULT_VOLTAGE_MINIMUM
from .coordinator import AquaNodePulseCoordinator
from .entity import AquaNodePulseEntity


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Add the Home Assistant-side low-voltage threshold."""
    async_add_entities(
        [AquaNodePulseVoltageMinimum(entry.runtime_data.coordinator, entry)],
    )


class AquaNodePulseVoltageMinimum(AquaNodePulseEntity, NumberEntity):
    """Threshold used by the local low-voltage problem entity."""

    _attr_translation_key = "voltage_minimum"
    _attr_device_class = NumberDeviceClass.VOLTAGE
    _attr_native_unit_of_measurement = UnitOfElectricPotential.VOLT
    _attr_native_min_value = 0
    _attr_native_max_value = 260
    _attr_native_step = 1
    _attr_mode = NumberMode.BOX
    _attr_entity_category = EntityCategory.CONFIG

    def __init__(
        self,
        coordinator: AquaNodePulseCoordinator,
        entry: ConfigEntry,
    ) -> None:
        super().__init__(coordinator, "voltage_minimum")
        self._entry = entry

    @property
    def native_value(self) -> float:
        """Return the configured local threshold."""
        return float(
            self._entry.options.get(
                CONF_VOLTAGE_MINIMUM,
                DEFAULT_VOLTAGE_MINIMUM,
            ),
        )

    async def async_set_native_value(self, value: float) -> None:
        """Persist the threshold in Home Assistant."""
        options = dict(self._entry.options)
        options[CONF_VOLTAGE_MINIMUM] = round(value, 1)
        self.hass.config_entries.async_update_entry(
            self._entry,
            options=options,
        )
        self.async_write_ha_state()
