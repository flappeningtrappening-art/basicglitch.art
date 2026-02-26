
import json
import re

def extract_first_paragraph(html_text):
    if not html_text:
        return None
    # Find the first <p>...</p> content
    match = re.search(r'<p>(.*?)</p>', html_text, re.DOTALL)
    if match:
        # Strip internal HTML tags and clean up
        clean_text = re.sub(r'<[^>]+>', '', match.group(1))
        # Ensure it's not too long for a short description, but longer than the placeholder
        return clean_text.strip()
    return None

def update_gallery():
    file_path = '/home/blitz/monetization/basic-glitch-art/assets/data/gallery.json'
    with open(file_path, 'r') as f:
        data = json.load(f)

    updated_count = 0
    for item in data:
        # Check if it has the placeholder description
        if "New forensic entry" in item.get('description', '') and item.get('forensic_analysis'):
            new_desc = extract_first_paragraph(item['forensic_analysis'])
            if new_desc and "pending deeper scrutiny" not in new_desc:
                item['description'] = new_desc
                updated_count += 1
                print(f"Updated description for: {item['title']}")

    if updated_count > 0:
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"Successfully updated {updated_count} descriptions.")
    else:
        print("No eligible descriptions found for update.")

if __name__ == "__main__":
    update_gallery()
