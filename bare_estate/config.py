import os
import sys
import json


HOME = os.environ["HOME"]
XDG_CONFIG_HOME = os.environ.get("XDG_CONFIG_HOME", f"{HOME}/.config")
XDG_DATA_HOME = os.environ.get("XDG_DATA_HOME", f"{HOME}/.local/share")
CONFIG_FILE = "bare_estate.json"

DEFAULT_CONFIGS = {
    "history_location": os.path.join(XDG_DATA_HOME, "bare_estate"),
    "base_directory": HOME,
}


try:
    file = open(f"{XDG_CONFIG_HOME}/{CONFIG_FILE}")
    file_configs = json.load(file)
except FileNotFoundError:
    file_configs = DEFAULT_CONFIGS
finally:
    if file:
        file.close()


configs = {}
for key in DEFAULT_CONFIGS.keys():
    try:
        config_value = file_configs[key]
    except KeyError:
        config_value = DEFAULT_CONFIGS[key]

    configs[key] = os.environ.get(f"BARE_ESTATE_{key.upper()}", config_value)
