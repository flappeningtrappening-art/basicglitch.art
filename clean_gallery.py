import json

with open('assets/data/gallery.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

seen_ids = set()
unique_data = []
for item in data:
    if item['id'] not in seen_ids:
        unique_data.append(item)
        seen_ids.add(item['id'])
    else:
        print(f"Removing duplicate: {item['id']} ({item['title']})")

with open('assets/data/gallery.json', 'w', encoding='utf-8') as f:
    json.dump(unique_data, f, indent=2)

print(f"Cleaned gallery.json. Final count: {len(unique_data)} items.")
