#!/usr/bin/env python3
"""Read-only dependency gate: fail on a PyPI 404 or a first release under 30 days old."""
import json
import re
import sys
import tomllib
import urllib.error
import urllib.request
from datetime import datetime, timezone

MIN_AGE_DAYS = 30

deps = tomllib.load(open("pyproject.toml", "rb"))["project"]["dependencies"]
failed = False
for dep in deps:
    name = re.split(r"[\[<>=!~; ]", dep, maxsplit=1)[0]
    try:
        url = f"https://pypi.org/pypi/{name}/json"
        data = json.load(urllib.request.urlopen(url, timeout=20))
    except urllib.error.HTTPError as e:
        print(f"FAIL  {name}: not found on PyPI (HTTP {e.code})")
        failed = True
        continue
    uploads = [
        datetime.fromisoformat(f["upload_time_iso_8601"])
        for files in data["releases"].values()
        for f in files
    ]
    first = min(uploads)
    age = (datetime.now(timezone.utc) - first).days
    if age < MIN_AGE_DAYS:
        print(f"FAIL  {name}: first release {first.date()} ({age}d old, need >={MIN_AGE_DAYS}d)")
        failed = True
    else:
        print(f"PASS  {name}: first release {first.date()} ({age}d old)")
sys.exit(1 if failed else 0)
