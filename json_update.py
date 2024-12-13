import json
import os

json_folder = r'C:\RecipeUpdater\Recipes'

def normalize_type(data):
    # Ensure the 'minecraft:' prefix is present if not already
    if not data["type"].startswith("minecraft:"):
        data["type"] = "minecraft:" + data["type"]
    return data

def transform_crafting_shaped(data):
    print("Transforming crafting_shaped recipe:")
    # Ensure every key entry is correctly formatted as a list of items
    for key, value in data["key"].items():
        # This assumes every value under "key" is a dictionary with an "item" field
        if isinstance(value, dict) and "item" in value:
            # Here you might want to do something with the value or just ensure it's correctly structured
            # For instance, you might want to wrap it in a list if your target format requires it
            data["key"][key] = [value["item"]]  # Example: wrapping the item in a list
    # Ensure the result field is properly updated
    if "item" in data["result"]:
        data["result"]["id"] = data["result"].pop("item")
    return data
def transform_crafting_shapeless(data):
    print("Transforming crafting_shapeless recipe:")
    transformed_ingredients = []
    for ingredient in data["ingredients"]:
        if "item" in ingredient:
            transformed_ingredients.append([ingredient["item"]])
    data["ingredients"] = transformed_ingredients
    if "item" in data["result"]:
        data["result"]["id"] = data["result"].pop("item")
    return data

def transform_smelting(data):
    print("Transforming smelting recipe:")
    if isinstance(data["ingredient"], dict):
        data["ingredient"] = [data["ingredient"]["item"]]
    elif isinstance(data["ingredient"], list) and all(isinstance(i, dict) for i in data["ingredient"]):
        data["ingredient"] = [i["item"] for i in data["ingredient"]]
    if isinstance(data["result"], str):
        data["result"] = {"id": data["result"]}
    data.setdefault("experience", 100)
    data.setdefault("cookingtime", 600)
    return data

def process_file(filename):
    file_path = os.path.join(json_folder, filename)
    try:
        with open(file_path, 'r', encoding='utf-8-sig') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON in file {filename}: {e}")
        return
    except Exception as e:
        print(f"An error occurred with file {filename}: {e}")
        return

    print(f"Processing {filename}")
    data = normalize_type(data)
    if data["type"] == "minecraft:crafting_shaped":
        transformed_data = transform_crafting_shaped(data)
    elif data["type"] == "minecraft:crafting_shapeless":
        transformed_data = transform_crafting_shapeless(data)
    elif data["type"] == "minecraft:smelting":
        transformed_data = transform_smelting(data)
    else:
        print(f"Unknown recipe type in {filename}")
        return

    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(transformed_data, f, indent=4)
        print(f"Updated {filename}")
    except Exception as e:
        print(f"Failed to write updated JSON to {filename}: {e}")

def main():
    for filename in os.listdir(json_folder):
        if filename.endswith(".json"):
            process_file(filename)

if __name__ == "__main__":
    main()
