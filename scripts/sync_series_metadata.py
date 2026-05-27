import json

series_mapping = {
    "SANGRE DE CRISTOS SERIES": ["Sangre De Cristos — Neon", "Sangre De Cristos — Night", "Sangre De Cristos — Blanca", "Sangre De Cristos — Blanca at Dusk", "Sangre De Cristos — Colorado", "Sangre De Cristos — Midnight", "Sangre De Cristos — Midnight/Dawn", "Sangre De Cristos — Circuits", "Sangre De Cristos — Dreamsicle"],
    "CASE STUDY 42 — BROBOTICUS": ["Broboticus — The Original (March of the Robots, 2024)", "Vitruvian Broboticus", "Brobotosaurus Wrex", "Guitarbot (Brobassicus)", "Brobarticus — The Artist", "Iron Chef (Chefboticus)", "The Bolts and Nutcracker (Balletboticus)", "Karateboticus", "There's a Star-Bot Waiting in the Sky", "Rancher Broboticus", "Sunflowerboticus", "Night-Fishing the Arkansas River", "Fishboticus Glitched", "Brobot Noir"],
    "MASTERS REMIXED": ["Vitruvian Broboticus", "Screambot", "Sunflowerboticus", "Marilyn Monbroe", "American Gothbotic", "Cubist Chef"],
    "PUP FICTION": ["Pup Fiction — Crash (Diner Robbery Prologue)"],
    "CYBER SAVANNA": ["Lion (Cyber Savanna series)", "Elephant (Cyber Savanna series)", "Giraffey Taffy (Cyber Savanna series)", "Cheetah (Cyber Savanna series)", "Waterbuck (Cyber Savanna series)", "Pachydermis (psychedelic maximalist variant — elephant)"],
    "PACHYDERMIS TRIPTYCH": ["Pachydermis (psychedelic maximalist variant — elephant)", "Pachydermis — Phish Edition", "Pachydermis — Phish Edition Inked"],
    "SPIRAL STUDIES": ["Monopattern (Spiral Studies — Original)", "Spiral Geometry (Fire Variant)", "Color Pattern (Spiral Studies — Acid)", "Floral (Spiral Studies — Dusk Variant)"],
    "SKULLASTIC ENDEAVOR": ["Psylent Skulls", "Skullastic Endeavor"],
    "MYCOLOGY SERIES": ["A Mycological Phenomenon", "Mycology Yourcology"],
    "GAIA DIPTYCH": ["Gaia of the Wasteland", "Dust to Dust"],
    "HAND-DRAWN INK": ["Squid", "Henna Tree", "Unfinished Business", "Discworld"],
    "PERSONAL / AUTOBIOGRAPHICAL": ["Inner Child", "Love of the Game"]
}

with open('assets/data/gallery.json', 'r', encoding='utf-8') as f:
    gallery = json.load(f)

for item in gallery:
    item['series'] = []
    for series, titles in series_mapping.items():
        if item['title'] in titles:
            item['series'].append(series)
    if item['title'] == 'Brobotosaurus Wrex':
        item['series'].append('FIELD REPORT 00')

with open('assets/data/gallery.json', 'w', encoding='utf-8') as f:
    json.dump(gallery, f, indent=2)
