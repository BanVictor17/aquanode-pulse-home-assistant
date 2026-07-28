"""Sensors exposed by AquaNode Pulse."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime
from typing import Any, ClassVar

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
from homeassistant.util import dt as dt_util

from .coordinator import AquaNodePulseCoordinator
from .entity import AquaNodePulseEntity
from .interruptions import MAINTENANCE, NETWORK, POWER, UNKNOWN


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
            data["voltage"]["voltage_v"] if data["voltage"]["calibrated"] else None
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
        key="ip_address",
        translation_key="ip_address",
        icon="mdi:ip-network",
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda data: data["wifi"]["ip"],
    ),
    AquaNodePulseSensorDescription(
        key="boot_count",
        translation_key="boot_count",
        entity_category=EntityCategory.DIAGNOSTIC,
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
        value_fn=lambda data: data["diagnostics"]["free_heap_bytes"],
    ),
    AquaNodePulseSensorDescription(
        key="max_alloc_heap",
        translation_key="max_alloc_heap",
        device_class=SensorDeviceClass.DATA_SIZE,
        native_unit_of_measurement=UnitOfInformation.BYTES,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
        value_fn=lambda data: data["diagnostics"]["max_alloc_heap_bytes"],
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
        [
            *(AquaNodePulseSensor(coordinator, description) for description in SENSORS),
            AquaNodePulseLastInterruptionCause(coordinator),
            AquaNodePulseLastInterruptionStarted(coordinator),
            AquaNodePulseLastInterruptionEnded(coordinator),
            AquaNodePulseLastInterruptionDuration(coordinator),
            AquaNodePulsePowerOutageCount(coordinator),
            AquaNodePulseLastVoltage(coordinator),
        ]
    )


class AquaNodePulseHistorySensor(AquaNodePulseEntity, SensorEntity):
    """A saved value that remains readable while the board is offline."""

    @property
    def available(self) -> bool:
        return True


class AquaNodePulseLastInterruptionCause(AquaNodePulseHistorySensor):
    """What the most recent loss of contact turned out to be.

    Every other entity here is a diagnostic reading. This one answers the
    question the product exists for, in the two words the customer cares about:
    was it the power, or was it the network.
    """

    _attr_translation_key = "last_interruption_cause"
    _attr_device_class = SensorDeviceClass.ENUM
    _attr_options: ClassVar[list[str]] = [
        POWER,
        NETWORK,
        UNKNOWN,
        MAINTENANCE,
    ]

    def __init__(self, coordinator: AquaNodePulseCoordinator) -> None:
        super().__init__(coordinator, "last_interruption_cause")

    @property
    def native_value(self) -> str | None:
        last = self.coordinator.last_interruption
        return None if last is None else str(last["kind"])


class AquaNodePulseLastInterruptionStarted(AquaNodePulseHistorySensor):
    """When contact was first lost."""

    _attr_translation_key = "last_interruption_started"
    _attr_device_class = SensorDeviceClass.TIMESTAMP

    def __init__(self, coordinator: AquaNodePulseCoordinator) -> None:
        super().__init__(coordinator, "last_interruption_started")

    @property
    def native_value(self) -> datetime | None:
        last = self.coordinator.last_interruption
        if last is None:
            return None
        return dt_util.utc_from_timestamp(float(last["started_at"]))


class AquaNodePulseLastInterruptionEnded(AquaNodePulseHistorySensor):
    """When contact was restored."""

    _attr_translation_key = "last_interruption_ended"
    _attr_device_class = SensorDeviceClass.TIMESTAMP

    def __init__(self, coordinator: AquaNodePulseCoordinator) -> None:
        super().__init__(coordinator, "last_interruption_ended")

    @property
    def native_value(self) -> datetime | None:
        last = self.coordinator.last_interruption
        if last is None:
            return None
        return dt_util.utc_from_timestamp(float(last["ended_at"]))


class AquaNodePulseLastInterruptionDuration(AquaNodePulseHistorySensor):
    """How long the board was out of contact."""

    _attr_translation_key = "last_interruption_duration"
    _attr_device_class = SensorDeviceClass.DURATION
    _attr_native_unit_of_measurement = UnitOfTime.SECONDS
    _attr_suggested_display_precision = 0

    def __init__(self, coordinator: AquaNodePulseCoordinator) -> None:
        super().__init__(coordinator, "last_interruption_duration")

    @property
    def native_value(self) -> float | None:
        last = self.coordinator.last_interruption
        return None if last is None else float(last["duration_seconds"])


class AquaNodePulsePowerOutageCount(AquaNodePulseHistorySensor):
    """Number of real power outages retained in the local journal."""

    _attr_translation_key = "power_outage_count"
    _attr_icon = "mdi:power-plug-off"

    def __init__(self, coordinator: AquaNodePulseCoordinator) -> None:
        super().__init__(coordinator, "power_outage_count")

    @property
    def native_value(self) -> int:
        return self.coordinator.history.interruption_count(
            self.coordinator.serial,
        )


class AquaNodePulseLastVoltage(AquaNodePulseHistorySensor):
    """Last valid voltage, kept visible through an outage."""

    _attr_translation_key = "last_voltage"
    _attr_device_class = SensorDeviceClass.VOLTAGE
    _attr_native_unit_of_measurement = UnitOfElectricPotential.VOLT
    _attr_suggested_display_precision = 1

    def __init__(self, coordinator: AquaNodePulseCoordinator) -> None:
        super().__init__(coordinator, "last_voltage")

    @property
    def native_value(self) -> float | None:
        reading = self.coordinator.history.last_voltage(
            self.coordinator.serial,
        )
        return None if reading is None else float(reading["value"])

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        reading = self.coordinator.history.last_voltage(
            self.coordinator.serial,
        )
        attributes = super().extra_state_attributes
        if reading is None:
            return attributes
        return {
            **attributes,
            "measured_at": dt_util.utc_from_timestamp(float(reading["at"])),
        }


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
    def extra_state_attributes(self) -> dict[str, Any]:
        """Explain why a voltage value is not yet available."""
        attributes = super().extra_state_attributes
        if self.entity_description.key != "voltage":
            return attributes
        voltage = self.coordinator.data["voltage"]
        return {
            **attributes,
            "sensor_present": voltage["sensor_present"],
            "calibrated": voltage["calibrated"],
            "signal_clipped": voltage["clipped"],
        }
