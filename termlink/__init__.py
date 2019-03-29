import json

_PACKAGE_FILE = '../package.json'

with open(_PACKAGE_FILE, 'r') as file:
    package = json.load(file)

name = package['name']