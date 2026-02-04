import os
import json
import re

english_dir = "english"
telugu_dir = "telugu"

dictionary = {}

def parse_file(filepath):
    topic_data = {}
    current_sub = "General"
    topic_data[current_sub] = []

    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            # Detect subtopic
            if line.startswith("🔹"):
                current_sub = line.replace("🔹", "").strip()
                topic_data[current_sub] = []
                continue

            # Detect word-meaning
            parts = re.split(r"–|-|:", line)

            if len(parts) >= 2:
                word = parts[0].strip()
                meaning = "-".join(parts[1:]).strip()

                topic_data[current_sub].append({
                    "word": word,
                    "meaning": meaning
                })

    return topic_data


for filename in os.listdir(english_dir):

    if not filename.endswith(".txt"):
        continue

    topic_name = filename.replace(".txt", "")

    english_path = os.path.join(english_dir, filename)
    telugu_path = os.path.join(telugu_dir, filename)

    english_data = parse_file(english_path)
    telugu_data = parse_file(telugu_path) if os.path.exists(telugu_path) else {}

    dictionary[topic_name] = {}

    subtopics = set(english_data.keys()) | set(telugu_data.keys())

    for sub in subtopics:

        dictionary[topic_name][sub] = []

        eng_list = english_data.get(sub, [])
        tel_list = telugu_data.get(sub, [])

        max_len = max(len(eng_list), len(tel_list))

        for i in range(max_len):

            dictionary[topic_name][sub].append({
                "word": eng_list[i]["word"] if i < len(eng_list) else tel_list[i]["word"],
                "english": eng_list[i]["meaning"] if i < len(eng_list) else "",
                "telugish": tel_list[i]["meaning"] if i < len(tel_list) else ""
            })


with open("dictionary.json", "w", encoding="utf-8") as f:
    json.dump(dictionary, f, indent=2, ensure_ascii=False)

print("✅ dictionary.json created successfully")
