import json

class Store:
    def __init__(self, name):
        self.name = name

def readStoreConfig():
    try:
        with open("store_configs.json", "r") as config_file:
            store_configs = json.load(config_file)
            stores = [Store(store_config["name"]) for store_config in store_configs]
            return stores
    except FileNotFoundError:
        return []

def generateStoreConfig(stores):
    store_configs = []

    for store in stores:
        config = {
            "name": store.name,
            "openhours": {
                "mon": {
                    "opened": True,
                    "start": "%H:%M",
                    "end": "%H:%M"
                },
                # ... (same as before)
            },
            "pretime": "%H:%M"
        }
        store_configs.append(config)

    with open("store_configs.json", "w") as config_file:
        json.dump(store_configs, config_file, indent=2)

def add_store(store_name):
    stores = readStoreConfig()
    new_store = Store(store_name)
    stores.append(new_store)

    generateStoreConfig(stores)

# Example usage
add_store("Store1")
add_store("Store2")
add_store("Store3")
