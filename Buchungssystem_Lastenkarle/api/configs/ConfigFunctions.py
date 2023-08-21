import json
import random
import string


def _generateStoreConfig(store_configs):
    with open("store_configs.json", "w") as config_file:
        json.dump(store_configs, config_file, indent=2)


def update_store_config(store_name, new_store_infos):
    stores = _readStoreConfig()

    for store in stores:
        if store["name"] == store_name:
            if "openhours" in new_store_infos:
                store["openhours"].update(new_store_infos["openhours"])
            if "pretime" in new_store_infos:
                store["openhours"]["pretime"] = new_store_infos["pretime"]
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
        with open("store_configs.json", "r") as config_file:
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
            "pretime": "%H:%M"
        }

    }
    stores.append(new_store)

    store_configs = {"stores": stores}  # Wrap the list of stores in a dictionary with "stores" key

    _generateStoreConfig(store_configs)

#here btw the code to genreate random string from alma todo pls move this someewhere else
def generate_random_string(length):
    characters = string.ascii_letters + string.digits  # Combining letters and digits
    random_string = ''.join(random.choices(characters,k=length))
    return random_string


#todo  delete example interaction before merging
#add_store("Store1")
#add_store("Store2")
#add_store("Store27")
#add_store("Store69")
##Example usage
#new_store_data_json = '''
# {
#    "openhours": {
#        "wed": { "opened": true, "start": "20:00", "end": "21:00" },
#        "fri": { "opened": true, "start": "13:00", "end": "16:00" },
#        "sun": { "opened": false, "start": "%H:%M", "end": "%H:%M" }
#    },
#    "pretime": "20:00"
# }
# '''
#store_name = "Store2"

#new_store_data = json.loads(new_store_data_json)
#
#update_store_config(store_name, new_store_data)
#print(getStoreConfig("Store2"))
#print(getStoreNameFromJson(
#    '{"name": " HiddenStore", "openhours": {"mon": {"opened": true, "start": "%H:%M", "end": "%H:%M"}, "tue": {"opened": true, "start": "%H:%M", "end": "%H:%M"}, "wed": {"opened": true, "start": "20:00", "end": "21:00"}, "thu": {"opened": true, "start": "%H:%M", "end": "%H:%M"}, "fri": {"opened": true, "start": "13:00", "end": "16:00"}, "sat": {"opened": true, "start": "%H:%M", "end": "%H:%M"}, "sun": {"opened": false, "start": "%H:%M", "end": "%H:%M"}, "pretime": "20:00"}}'))
#print(getAllStoresConfig())
#deleteStoreConfig('Store27')
#print(getAllStoresConfig())
