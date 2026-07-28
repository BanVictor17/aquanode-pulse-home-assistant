#!/usr/bin/env python3
"""Fast repository checks that do not require a Home Assistant installation."""

from __future__ import annotations

import ast
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
COMPONENT = ROOT / "custom_components" / "aquanode_pulse"


def fail(message: str) -> None:
    print(f"FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)


def load_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text())
    except (OSError, json.JSONDecodeError) as err:
        fail(f"{path.relative_to(ROOT)}: {err}")


for path in sorted(COMPONENT.rglob("*.py")):
    try:
        ast.parse(path.read_text(), filename=str(path))
    except (OSError, SyntaxError) as err:
        fail(f"{path.relative_to(ROOT)}: {err}")


def check_imports() -> str:
    """Import every module for real, when Home Assistant is available.

    Parsing only proves the syntax is valid. It cannot see that a name has moved
    to another Home Assistant module, which is how `ConfigFlowResult` shipped
    imported from `data_entry_flow`: the file parsed, the import raised, the
    flow never registered, and the only symptom was "Invalid handler specified"
    in the browser.
    """
    try:
        import homeassistant  # noqa: F401
    except ImportError:
        return "SKIP: import check needs `pip install homeassistant`"

    import importlib

    sys.path.insert(0, str(ROOT))
    for module in sorted(path.stem for path in COMPONENT.glob("*.py")):
        name = f"custom_components.aquanode_pulse.{module}"
        try:
            importlib.import_module(name)
        except Exception as err:  # noqa: BLE001 - any failure is a failure
            fail(f"{name}: {type(err).__name__}: {err}")

    # Importing is not the same as registering. Subclassing ConfigFlow with
    # `domain=` is what puts the handler in HANDLERS, and an empty HANDLERS is
    # precisely what Home Assistant reports as "Invalid handler specified".
    from homeassistant.config_entries import HANDLERS

    if HANDLERS.get("aquanode_pulse") is None:
        fail("config flow did not register: Home Assistant would refuse to add it")

    # The mDNS record the board really advertises, straight from `dns-sd -L`.
    # Raw ServiceInfo properties are keyed by bytes, so reading them with a str
    # key returns nothing and every board is silently rejected as "not ours".
    import socket

    from zeroconf import ServiceInfo

    from custom_components.aquanode_pulse.config_flow import _extract

    info = ServiceInfo(
        "_aquanode-pulse._tcp.local.",
        "AquaNode Pulse 429385._aquanode-pulse._tcp.local.",
        addresses=[socket.inet_aton("192.168.1.42")],
        port=6053,
        properties={"serial": "AP-429385", "model": "pulse", "api": "1"},
        server="aquanode-pulse-429385.local.",
    )
    if _extract(info) != ("AP-429385", "192.168.1.42", 6053):
        fail(f"discovery would not recognise a real board: {_extract(info)}")

    stranger = ServiceInfo(
        "_aquanode-pulse._tcp.local.",
        "somebody else._aquanode-pulse._tcp.local.",
        addresses=[socket.inet_aton("192.168.1.43")],
        port=6053,
        properties={"model": "pulse"},
        server="stranger.local.",
    )
    if _extract(stranger) is not None:
        fail("discovery accepted a service with no serial")
    return "ok: imports, flow registration and mDNS parsing"


import_result = check_imports()

manifest = load_json(COMPONENT / "manifest.json")
hacs = load_json(ROOT / "hacs.json")
strings = load_json(COMPONENT / "strings.json")
english = load_json(COMPONENT / "translations" / "en.json")
romanian = load_json(COMPONENT / "translations" / "ro.json")

required_manifest = {
    "domain",
    "name",
    "version",
    "codeowners",
    "config_flow",
    "documentation",
    "issue_tracker",
    "integration_type",
    "iot_class",
    "zeroconf",
}
missing = required_manifest - manifest.keys()
if missing:
    fail(f"manifest keys missing: {sorted(missing)}")
if manifest["domain"] != "aquanode_pulse":
    fail("unexpected integration domain")
if "_aquanode-pulse._tcp.local." not in manifest["zeroconf"]:
    fail("mDNS service is not registered in manifest")
if not hacs.get("name"):
    fail("hacs.json has no name")
if strings != english:
    fail("strings.json and English translation differ")
if set(strings["entity"]) != set(romanian["entity"]):
    fail("Romanian entity groups do not match English")

firmware = (
    ROOT.parent
    / "AquaNode Pulse"
    / "Firmware"
    / "AquaNodePulse"
    / "pulse_home_assistant.cpp"
)
if firmware.exists():
    source = firmware.read_text()
    for contract in (
        'MDNS.addService("aquanode-pulse", "tcp"',
        '"/api/v1/status"',
        '"Authorization"',
        '\\"voltage_v\\"',
    ):
        if contract not in source:
            fail(f"firmware contract missing: {contract}")

print(import_result)
print("AquaNode Pulse Home Assistant checks: all passed")
