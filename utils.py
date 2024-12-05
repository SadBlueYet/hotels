import json
import os


def load_json(file_path: str):
    with open(file_path, "r", encoding="utf-8") as hotels_file:
        data = json.load(hotels_file)
    return data


def write_to_json(file_path: str, data: dict):
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            try:
                existing_data = json.load(file)
            except json.JSONDecodeError:
                existing_data = []
    else:
        existing_data = []

    existing_data.append(data)
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(existing_data, file, ensure_ascii=False, indent=4)
