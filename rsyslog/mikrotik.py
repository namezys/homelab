#!/usr/bin/env python3
"""
Parse syslog from Mikrotik routers, like:
> dhcp,info dhcp-smart deassigned 10.20.1.223 for 1C:90:FF:E7:25:5E wlan0
"""

import json
import sys


SEVERITIES = {
    'critical': (2, 'crit'),
    'error': (3, 'err'),
    'warning': (4, 'warning'),
    'info': (6, 'info'),
    'debug': (7, 'debug'),
}

SEVERITIES_SET = set(SEVERITIES.keys())

DEBUG = any(i == "--debug" for i in sys.argv)


def debug(msg: dict, changes: dict):
    if not DEBUG:
        return
    data = msg | changes

    with open("/syslog-debug", "a+") as f:
        f.write("=======\n")
        f.write(json.dumps(data, indent=2) + "\n")
        f.write(json.dumps(data) + "\n")


def process(raw_json: str) -> str:
    msg = json.loads(raw_json)
    debug(msg, {"type": "init"})
    changes = {}

    tags = set(msg["syslogtag"].split(","))
    severity_tags = SEVERITIES_SET.intersection(tags)
    assert len(severity_tags) == 1, "Expect only one severity tag"
    app = ",".join(sorted(tags.difference(SEVERITIES_SET)))
    changes["syslogseverity"], changes["syslogseverity-text"] = SEVERITIES[severity_tags.pop()]
    changes["msg"] = msg["msg"].strip()
    changes["$!"] = (msg.get("$!") or {}) | {"programname": app}

    debug(changes, {"type": "changes"})
    return json.dumps(changes)


def main():
    for line in sys.stdin:
        print(process(line), flush=True)


if __name__ == '__main__':
    main()