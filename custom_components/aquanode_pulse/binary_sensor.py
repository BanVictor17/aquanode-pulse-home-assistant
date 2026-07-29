"""Binary status entities for AquaNode Pulse."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
    BinarySensorEntityDescription,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import EntityCategory
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from .const import CONF_VOLTAGE_MINIMUM, DEFAULT_VOLTAGE_MINIMUM
from .coordinator import AquaNodePulseCoordinator
from .entity import AquaNodePulseEntity


@dataclass(frozen=True, kw_only=True)
class AquaNodePulseBinaryDescription(BinarySensorEntityDescription):
    """Describe a boolean inside the shared payload."""

    value_fn: Callable[[dict[str, Any], float], bool]


BINARY_SENSORS: tuple[AquaNodePulseBinaryDescription, ...] = (
    AquaNodePulseBinaryDescription(
        key="cloud_connected",
        translation_key="cloud_connected",
        device_class=BinarySensorDeviceClass.CONNECTIVITY,
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda data, _threshold: data["cloud"]["connected"],
    ),
    AquaNodePulseBinaryDescription(
        key="voltage_sensor_problem",
        translation_key="voltage_sensor_problem",
        device_class=BinarySensorDeviceClass.PROBLEM,
        value_fn=lambda data, _threshold: (
            data["voltage"]["ready"] and not data["voltage"]["sensor_present"]
        ),
    ),
    AquaNodePulseBinaryDescription(
        key="voltage_clipped",
        translation_key="voltage_clipped",
        device_class=BinarySensorDeviceClass.PROBLEM,
        value_fn=lambda data, _threshold: data["voltage"]["clipped"],
    ),
    AquaNodePulseBinaryDescription(
        key="calibration_required",
        translation_key="calibration_required",
        device_class=BinarySensorDeviceClass.PROBLEM,
        value_fn=lambda data, _threshold: (
            data["voltage"]["sensor_present"] and not data["voltage"]["calibrated"]
        ),
    ),
    AquaNodePulseBinaryDescription(
        key="low_voltage",
        translation_key="low_voltage",
        device_class=BinarySensorDeviceClass.PROBLEM,
        value_fn=lambda data, threshold: (
            threshold > 0
            and data["voltage"]["calibrated"]
            and data["voltage"]["sensor_present"]
            and data["voltage"]["voltage_v"] < threshold
        ),
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Add Pulse binary sensors."""
    coordinator = entry.runtime_data.coordinator
    async_add_entities(
        [
            *(
                AquaNodePulseBinarySensor(coordinator, entry, description)
                for description in BINARY_SENSORS
            ),
            AquaNodePulseLocalConnection(coordinator),
        ],
    )


class AquaNodePulseLocalConnection(AquaNodePulseEntity, BinarySensorEntity):
    """A stable online/offline state that never becomes unavailable itself."""

    _attr_translation_key = "local_connection"
    _attr_device_class = BinarySensorDeviceClass.CONNECTIVITY

    def __init__(self, coordinator: AquaNodePulseCoordinator) -> None:
        super().__init__(coordinator, "local_connection")

    @property
    def available(self) -> bool:
        """Keep the entity readable while the physical device is offline."""
        return True

    @property
    def is_on(self) -> bool:
        """Return the result of the most recent one-second local poll."""
        return self.coordinator.last_update_success

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Expose planned maintenance and non-sensitive polling diagnostics."""
        return {
            **super().extra_state_attributes,
            "maintenance": self.coordinator.in_maintenance,
            "router_on_ups": self.coordinator.router_on_ups_enabled,
            **self.coordinator.poll_diagnostics,
        }


class AquaNodePulseBinarySensor(AquaNodePulseEntity, BinarySensorEntity):
    """A local condition or diagnostic."""

    entity_description: AquaNodePulseBinaryDescription

    def __init__(
        self,
        coordinator: AquaNodePulseCoordinator,
        entry: ConfigEntry,
        description: AquaNodePulseBinaryDescription,
    ) -> None:
        super().__init__(coordinator, description.key)
        self._entry = entry
        self.entity_description = description

    @property
    def is_on(self) -> bool:
        """Return the condition state."""
        threshold = float(
            self._entry.options.get(
                CONF_VOLTAGE_MINIMUM,
                DEFAULT_VOLTAGE_MINIMUM,
            ),
        )
        return self.entity_description.value_fn(
            self.coordinator.data,
            threshold,
        )
