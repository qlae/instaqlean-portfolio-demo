import json

def load_usernames_from_file(file_path, key=None):
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    usernames = []

    if key:
        items = data.get(key, [])
    else:
        items = data

    for entry in items:
        string_list = entry.get("string_list_data", [])
        for s in string_list:
            if "value" in s:
                usernames.append(s["value"])
    
    return usernames
