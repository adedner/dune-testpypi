#!/usr/bin/env python3

import requests
import sys

try:
    package = sys.argv[1]
except IndexError:
    print(f"Usage: {sys.argv[0]} <package name>")
    sys.exit(1)

response  = requests.get(f'https://pypi.org/pypi/{package}/json')
try:
    latestVer = response.json()['info']['version']
except KeyError:
    print(f"Package {package} not found!")
    sys.exit(1)

print(f"Lastest version of {package} available:\n{latestVer}")
