"""Constants for the AquaNode Pulse integration."""

from __future__ import annotations

from datetime import timedelta

from homeassistant.const import Platform

DOMAIN = "aquanode_pulse"
EVENT_INTERRUPTION = "aquanode_pulse_interruption"
MANUFACTURER = "AquaNode"
MODEL = "AquaNode Pulse"

PANEL_URL_PATH = "aquanode-pulse"
PANEL_COMPONENT_NAME = "aquanode-pulse-panel"
PANEL_TITLE = "AquaNode Pulse"
PANEL_ICON = "mdi:power-plug"
FRONTEND_URL = "/aquanode_pulse_frontend/aquanode-pulse-panel.js"
DATA_FRONTEND_REGISTERED = "frontend_registered"

CONF_PORT = "port"
CONF_PASSWORD = "password"
CONF_VOLTAGE_MINIMUM = "voltage_minimum"

DEFAULT_PORT = 6053
DEFAULT_VOLTAGE_MINIMUM = 200.0
UPDATE_INTERVAL = timedelta(seconds=3)

PLATFORMS: list[Platform] = [
    Platform.BINARY_SENSOR,
    Platform.BUTTON,
    Platform.NUMBER,
    Platform.SENSOR,
    Platform.SWITCH,
]
