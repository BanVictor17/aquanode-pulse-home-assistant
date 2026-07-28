"""AquaNode Pulse local integration."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import TypeAlias

from homeassistant.components import frontend, panel_custom
from homeassistant.components.http import StaticPathConfig
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .api import AquaNodePulseApi
from .const import (
    CONF_PASSWORD,
    CONF_PORT,
    DATA_FRONTEND_REGISTERED,
    DEFAULT_PORT,
    DOMAIN,
    FRONTEND_URL,
    PANEL_COMPONENT_NAME,
    PANEL_ICON,
    PANEL_TITLE,
    PANEL_URL_PATH,
    PLATFORMS,
)
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
    await _async_register_panel(hass)
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


async def _async_register_panel(hass: HomeAssistant) -> None:
    """Put the bundled dashboard in the sidebar.

    Registered once for the whole integration rather than per device: the panel
    lists every board, and a second registration of the same path fails.
    """
    domain_data = hass.data.setdefault(DOMAIN, {})
    if domain_data.get(DATA_FRONTEND_REGISTERED):
        return

    await hass.http.async_register_static_paths(
        [
            StaticPathConfig(
                FRONTEND_URL,
                str(Path(__file__).parent / "frontend" / "aquanode-pulse-panel.js"),
                False,
            )
        ]
    )
    if not frontend.async_panel_exists(hass, PANEL_URL_PATH):
        await panel_custom.async_register_panel(
            hass,
            frontend_url_path=PANEL_URL_PATH,
            webcomponent_name=PANEL_COMPONENT_NAME,
            sidebar_title=PANEL_TITLE,
            sidebar_icon=PANEL_ICON,
            module_url=FRONTEND_URL,
            require_admin=False,
        )
    domain_data[DATA_FRONTEND_REGISTERED] = True


async def async_unload_entry(
    hass: HomeAssistant,
    entry: AquaNodePulseConfigEntry,
) -> bool:
    """Unload one Pulse device."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
