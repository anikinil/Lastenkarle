import json


class Store:
    def __init__(self, name):
        self.name = name


def _generateStoreConfig(store_configs):
    with open("store_configs.json", "w") as config_file:
        json.dump(store_configs, config_file, indent=2)


# def update_store_open_hours(store_name, new_open_hours):
#    store_configs = readStoreConfig()
#
#    for store_config in store_configs:
#        if store_config["name"] == store_name:
#            store_config["openhours"].update(new_open_hours)
#
#    _generateStoreConfig(store_configs)


def update_store_opening_hours(store_name, new_store_infos):
    stores = readStoreConfig()
    new_store_infos = json.load(new_store_infos)
    print(new_store_infos)
    for store in stores:
        if store["name"] == store_name:
            for new_store_info in new_store_infos:
               store["openhours"].update(new_store_infos)
    store_configs = {"stores": stores}  # Wrap the list of stores in a dictionary with "stores" key
    _generateStoreConfig(store_configs)


def readStoreConfig():
    try:
        with open("store_configs.json", "r") as config_file:
            store_configs = json.load(config_file)
            return store_configs.get("stores", [])  # Get the "stores" key or return an empty list
    except FileNotFoundError:
        return []


def add_store(store_name):
    stores = readStoreConfig()
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
            }
        },
        "pretime": "%H:%M"
    }
    stores.append(new_store)

    store_configs = {"stores": stores}  # Wrap the list of stores in a dictionary with "stores" key

    _generateStoreConfig(store_configs)


update_data_json = '''
    {
        "wed": {
            "opened": true,
            "start": "10:30",
            "end": "20:00"
        },
        "thu": {
            "opened": false,
           "start": "%H:%M",
            "end": "%H:%M"
        }
    }
    '''
# add_store("Store69")

add_store("Store2")
#update_data = json.loads(update_data_json)
#store_to_update = "Store2"
#update_store_opening_hours(store_to_update, update_data_json)
