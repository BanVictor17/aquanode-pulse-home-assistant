"""Constants for the AquaNode Pulse integration."""

from __future__ import annotations

from datetime import timedelta

from homeassistant.const import Platform

DOMAIN = "aquanode_pulse"
MANUFACTURER = "AquaNode"
MODEL = "AquaNode Pulse"

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
