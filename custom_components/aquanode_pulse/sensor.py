"""Sensors exposed by AquaNode Pulse."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    PERCENTAGE,
    SIGNAL_STRENGTH_DECIBELS_MILLIWATT,
    EntityCategory,
    UnitOfElectricPotential,
    UnitOfInformation,
    UnitOfTime,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback
from .coordinator import AquaNodePulseCoordinator
from .entity import AquaNodePulseEntity


@dataclass(frozen=True, kw_only=True)
class AquaNodePulseSensorDescription(SensorEntityDescription):
    """Describe a value inside the shared status payload."""

    value_fn: Callable[[dict[str, Any]], Any]


SENSORS: tuple[AquaNodePulseSensorDescription, ...] = (
    AquaNodePulseSensorDescription(
        key="voltage",
        translation_key="voltage",
        device_class=SensorDeviceClass.VOLTAGE,
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=1,
        value_fn=lambda data: (
            data["voltage"]["voltage_v"]
            if data["voltage"]["calibrated"]
            else None
        ),
    ),
    AquaNodePulseSensorDescription(
        key="wifi_signal",
        translation_key="wifi_signal",
        device_class=SensorDeviceClass.SIGNAL_STRENGTH,
        native_unit_of_measurement=SIGNAL_STRENGTH_DECIBELS_MILLIWATT,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda data: data["wifi"]["rssi_dbm"],
    ),
    AquaNodePulseSensorDescription(
        key="uptime",
        translation_key="uptime",
        device_class=SensorDeviceClass.DURATION,
        native_unit_of_measurement=UnitOfTime.SECONDS,
        entity_category=EntityCategory.DIAGNOSTIC,
        suggested_unit_of_measurement=UnitOfTime.HOURS,
        value_fn=lambda data: data["uptime_s"],
    ),
    AquaNodePulseSensorDescription(
        key="boot_count",
        translation_key="boot_count",
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
        value_fn=lambda data: data["boot_count"],
    ),
    AquaNodePulseSensorDescription(
        key="raw_voltage",
        translation_key="raw_voltage",
        native_unit_of_measurement=UnitOfElectricPotential.MILLIVOLT,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
        suggested_display_precision=1,
        value_fn=lambda data: data["voltage"]["raw_rms_mv"],
    ),
    AquaNodePulseSensorDescription(
        key="voltage_signal_level",
        translation_key="voltage_signal_level",
        native_unit_of_measurement=PERCENTAGE,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
        value_fn=lambda data: round(
            min(100, max(0, data["voltage"]["raw_rms_mv"] / 10)),
        ),
    ),
    AquaNodePulseSensorDescription(
        key="free_heap",
        translation_key="free_heap",
        device_class=SensorDeviceClass.DATA_SIZE,
        native_unit_of_measurement=UnitOfInformation.BYTES,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
        value_fn=lambda data: data["diagnostics"]["free_heap_bytes"],
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Add Pulse sensors."""
    coordinator = entry.runtime_data.coordinator
    async_add_entities(
        AquaNodePulseSensor(coordinator, description)
        for description in SENSORS
    )


class AquaNodePulseSensor(AquaNodePulseEntity, SensorEntity):
    """One measurement on the Pulse device page."""

    entity_description: AquaNodePulseSensorDescription

    def __init__(
        self,
        coordinator: AquaNodePulseCoordinator,
        description: AquaNodePulseSensorDescription,
    ) -> None:
        super().__init__(coordinator, description.key)
        self.entity_description = description

    @property
    def native_value(self) -> Any:
        """Return the latest coordinated value."""
        return self.entity_description.value_fn(self.coordinator.data)

    @property
    def extra_state_attributes(self) -> dict[str, Any] | None:
        """Explain why a voltage value is not yet available."""
        if self.entity_description.key != "voltage":
            return None
        voltage = self.coordinator.data["voltage"]
        return {
            "sensor_present": voltage["sensor_present"],
            "calibrated": voltage["calibrated"],
            "signal_clipped": voltage["clipped"],
        }
