"""AquaNode Pulse local integration."""

from __future__ import annotations

import asyncio
from dataclasses import dataclass
from pathlib import Path
from typing import TypeAlias

from homeassistant.components import frontend, panel_custom
from homeassistant.components.http import StaticPathConfig
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST, EVENT_HOMEASSISTANT_STOP
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .api import AquaNodePulseApi
from .const import (
    CONF_PASSWORD,
    CONF_PORT,
    DATA_FRONTEND_REGISTERED,
    DATA_HISTORY,
    DATA_SETUP_LOCK,
    DATA_WEBSOCKET_REGISTERED,
    DEFAULT_PORT,
    DOMAIN,
    FRONTEND_PATH,
    FRONTEND_URL,
    PANEL_COMPONENT_NAME,
    PANEL_ICON,
    PANEL_TITLE,
    PANEL_URL_PATH,
    PLATFORMS,
)
from .coordinator import AquaNodePulseCoordinator
from .history import PulseHistory
from .websocket import async_register as async_register_websocket

AquaNodePulseConfigEntry: TypeAlias = ConfigEntry["AquaNodePulseRuntimeData"]


@dataclass(slots=True)
class AquaNodePulseRuntimeData:
    """Objects shared by all entity platforms."""

    api: AquaNodePulseApi
    coordinator: AquaNodePulseCoordinator
    history: PulseHistory


async def async_setup_entry(
    hass: HomeAssistant,
    entry: AquaNodePulseConfigEntry,
) -> bool:
    """Set up a discovered Pulse device."""
    domain_data = hass.data.setdefault(DOMAIN, {})
    setup_lock = domain_data.setdefault(DATA_SETUP_LOCK, asyncio.Lock())
    async with setup_lock:
        history = await _async_get_history(hass)
        _async_register_websocket_once(hass)
        await _async_register_panel(hass)
    api = AquaNodePulseApi(
        async_get_clientsession(hass),
        entry.data[CONF_HOST],
        entry.data.get(CONF_PORT, DEFAULT_PORT),
        entry.data[CONF_PASSWORD],
    )
    coordinator = AquaNodePulseCoordinator(hass, entry, api, history)
    await coordinator.async_config_entry_first_refresh()
    entry.runtime_data = AquaNodePulseRuntimeData(api, coordinator, history)
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def _async_get_history(hass: HomeAssistant) -> PulseHistory:
    """Load the shared persistent journal once."""
    domain_data = hass.data.setdefault(DOMAIN, {})
    if (history := domain_data.get(DATA_HISTORY)) is not None:
        return history

    history = PulseHistory(hass)
    await history.async_load()
    domain_data[DATA_HISTORY] = history

    async def _async_save_history(_event) -> None:
        await history.async_save()

    hass.bus.async_listen_once(
        EVENT_HOMEASSISTANT_STOP,
        _async_save_history,
    )
    return history


def _async_register_websocket_once(hass: HomeAssistant) -> None:
    """Expose saved graph data to the bundled panel once."""
    domain_data = hass.data.setdefault(DOMAIN, {})
    if domain_data.get(DATA_WEBSOCKET_REGISTERED):
        return
    async_register_websocket(hass)
    domain_data[DATA_WEBSOCKET_REGISTERED] = True


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
                FRONTEND_PATH,
                str(Path(__file__).parent / "frontend" / "aquanode-pulse-panel.js"),
                False,
            )
        ]
    )
    if PANEL_URL_PATH not in hass.data.get(frontend.DATA_PANELS, {}):
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
