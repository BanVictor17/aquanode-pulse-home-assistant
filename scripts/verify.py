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

print("AquaNode Pulse Home Assistant checks: all passed")
