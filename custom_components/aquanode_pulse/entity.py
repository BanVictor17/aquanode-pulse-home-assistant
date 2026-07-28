"""Shared entity model for AquaNode Pulse."""

from __future__ import annotations

from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, MANUFACTURER, MODEL
from .coordinator import AquaNodePulseCoordinator


class AquaNodePulseEntity(CoordinatorEntity[AquaNodePulseCoordinator]):
    """Base entity attached to one physical Pulse device."""

    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: AquaNodePulseCoordinator,
        key: str,
    ) -> None:
        super().__init__(coordinator)
        self._attr_unique_id = f"{coordinator.data['serial']}_{key}"

    @property
    def device_info(self) -> DeviceInfo:
        """Describe the device shown on the Home Assistant product page."""
        data = self.coordinator.data
        return DeviceInfo(
            identifiers={(DOMAIN, data["serial"])},
            manufacturer=MANUFACTURER,
            model=MODEL,
            name=data.get("name", MODEL),
            sw_version=data.get("firmware"),
            configuration_url=self.coordinator.api.base_url,
        )
