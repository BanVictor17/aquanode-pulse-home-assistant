"""AquaNode Pulse local integration."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TypeAlias

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .api import AquaNodePulseApi
from .const import CONF_PASSWORD, CONF_PORT, DEFAULT_PORT, PLATFORMS
from .coordinator import AquaNodePulseCoordinator

AquaNodePulseConfigEntry: TypeAlias = ConfigEntry["AquaNodePulseRuntimeData"]


@dataclass(slots=True)
class AquaNodePulseRuntimeData:
    """Objects shared by all entity platforms."""

    api: AquaNodePulseApi
    coordinator: AquaNodePulseCoordinator


async def async_setup_entry(
    hass: HomeAssistant,
    entry: AquaNodePulseConfigEntry,
) -> bool:
    """Set up a discovered Pulse device."""
    api = AquaNodePulseApi(
        async_get_clientsession(hass),
        entry.data[CONF_HOST],
        entry.data.get(CONF_PORT, DEFAULT_PORT),
        entry.data[CONF_PASSWORD],
    )
    coordinator = AquaNodePulseCoordinator(hass, entry, api)
    await coordinator.async_config_entry_first_refresh()
    entry.runtime_data = AquaNodePulseRuntimeData(api, coordinator)
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(
    hass: HomeAssistant,
    entry: AquaNodePulseConfigEntry,
) -> bool:
    """Unload one Pulse device."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
