import json
import os
from datetime import datetime, timedelta

# Find the path to your Django project's base directory
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Create the path to the 'Project/api/configs' directory within your project
configs_folder_path = os.path.join(base_dir, 'configs')
# Generate the full path to store_configs.json within the 'Project/api/configs' directory
store_config_path = os.path.join(configs_folder_path, 'store_configs.json')


def _generateStoreConfig(store_configs):
    with open(store_config_path, "w") as config_file:
        json.dump(store_configs, config_file, indent=2)


def update_store_config(store_name, new_store_infos):
    stores = _readStoreConfig()

    for store in stores:
        if store["name"] == store_name:
            if "openhours" in new_store_infos:
                store["openhours"].update(new_store_infos["openhours"])
            if "pretime" in new_store_infos:
                store["pretime"] = new_store_infos["pretime"]
            _generateStoreConfig({"stores": stores})
            break


def getStoreConfig(Storename):
    stores = _readStoreConfig()
    for store in stores:
        if store["name"] == Storename:
            return json.dumps(store)


def getAllStoresConfig():
    stores = _readStoreConfig()
    return json.dumps(stores)


def deleteStoreConfig(store_name):
    stores = _readStoreConfig()
    updated_stores = [store for store in stores if store["name"] != store_name]
    store_configs = {"stores": updated_stores}
    _generateStoreConfig(store_configs)


def getStoreNameFromJson(StoreJson):
    store = json.loads(StoreJson)
    return store['name']


def _readStoreConfig():
    try:
        with open(store_config_path, "r") as config_file:
            store_configs = json.load(config_file)
            return store_configs.get("stores", [])  # Get the "stores" key or return an empty list
    except FileNotFoundError:
        return []


def add_store(store_name):
    stores = _readStoreConfig()
    new_store = {
        "name": store_name,
        "openhours": {
            "mon": {
                "opened": True,
                "start": "%H:%M",
                "end": "%H:%M"
            },
            "tue": {
                "opened": True,
                "start": "%H:%M",
                "end": "%H:%M"
            },
            "wed": {
                "opened": True,
                "start": "%H:%M",
                "end": "%H:%M"
            },
            "thu": {
                "opened": True,
                "start": "%H:%M",
                "end": "%H:%M"
            },
            "fri": {
                "opened": True,
                "start": "%H:%M",
                "end": "%H:%M"
            },
            "sat": {
                "opened": True,
                "start": "%H:%M",
                "end": "%H:%M"
            },
            "sun": {
                "opened": True,
                "start": "%H:%M",
                "end": "%H:%M"
            },

        },
        "pretime": "%H:%M"

    }
    stores.append(new_store)

    store_configs = {"stores": stores}  # Wrap the list of stores in a dictionary with "stores" key

    _generateStoreConfig(store_configs)

import json

def _parse_opening_hours(openhours):
    days = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]
    parsed_hours = []
    current_group = []
    prev_hours = None

    for day in days:
        if openhours[day]["opened"]:
            hours = f"{openhours[day]['start']} - {openhours[day]['end']}"
            if hours == prev_hours:
                current_group.append(day)
            else:
                if current_group:
                    parsed_hours.append((current_group, prev_hours))
                current_group = [day]
                prev_hours = hours

    if current_group:
        parsed_hours.append((current_group, prev_hours))

    return parsed_hours

def format_opening_hours(store_name):
    store = json.loads(getStoreConfig(store_name))
    result = ""

    grouped_hours = _parse_opening_hours(store["openhours"])
    for day_group, hours in grouped_hours:
        if len(day_group) > 1:
            result += f"{', '.join([day.capitalize() for day in day_group])}: {hours}\n"
        else:
            day = day_group[0]
            result += f"{day.capitalize()}: {hours}\n"
    return result
