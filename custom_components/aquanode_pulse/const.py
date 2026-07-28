"""Constants for the AquaNode Pulse integration."""

from __future__ import annotations

from datetime import timedelta

from homeassistant.const import Platform

DOMAIN = "aquanode_pulse"
EVENT_CONNECTION_LOST = "aquanode_pulse_connection_lost"
EVENT_INTERRUPTION = "aquanode_pulse_interruption"
EVENT_VOLTAGE_LOW = "aquanode_pulse_voltage_low"
EVENT_VOLTAGE_RECOVERED = "aquanode_pulse_voltage_recovered"
MANUFACTURER = "AquaNode"
MODEL = "AquaNode Pulse"

PANEL_URL_PATH = "aquanode-pulse"
PANEL_COMPONENT_NAME = "aquanode-pulse-panel"
PANEL_TITLE = "AquaNode Pulse"
PANEL_ICON = "mdi:power-plug"
FRONTEND_PATH = "/aquanode_pulse_frontend/aquanode-pulse-panel.js"
FRONTEND_URL = f"{FRONTEND_PATH}?v=0.5.0"
DATA_FRONTEND_REGISTERED = "frontend_registered"
DATA_HISTORY = "history"
DATA_SETUP_LOCK = "setup_lock"
DATA_WEBSOCKET_REGISTERED = "websocket_registered"

CONF_PORT = "port"
CONF_PASSWORD = "password"
CONF_VOLTAGE_MINIMUM = "voltage_minimum"
CONF_NOTIFICATION_DELAY = "notification_delay"
CONF_AUTOMATIC_NOTIFICATIONS = "automatic_notifications"
CONF_DISPLAY_NAME = "display_name"

DEFAULT_PORT = 6053
DEFAULT_VOLTAGE_MINIMUM = 200.0
DEFAULT_NOTIFICATION_DELAY = 0.0
DEFAULT_AUTOMATIC_NOTIFICATIONS = True
REQUEST_TIMEOUT_SECONDS = 1.5
UPDATE_INTERVAL = timedelta(seconds=1)

PLATFORMS: list[Platform] = [
    Platform.BINARY_SENSOR,
    Platform.BUTTON,
    Platform.NUMBER,
    Platform.SENSOR,
    Platform.SWITCH,
    Platform.TEXT,
]
