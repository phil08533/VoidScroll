import requests
import json
import os
import random
from hashlib import md5

VIDEO_FILE = "videos.json"
MAX_RESULTS = 40

CATEGORY_MAP = {
    "space": ["space", "mars", "jupiter", "satellite", "rocket", "nasa"],
    "animals": ["animal", "wildlife", "ocean", "fish", "bird"],
    "science": ["experiment", "physics", "biology", "chemistry"],
    "movies": ["film", "movie", "television", "documentary"]
}

SEARCH_TERMS = [
    "space documentary",
    "wildlife",
    "ocean life",
    "science film",
    "rocket launch"
]

def load_existing():
    if not os.path.exists(VIDEO_FILE):
        return []
    with open(VIDEO_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_videos(data):
    with open(VIDEO_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def generate_id(url):
    return md5(url.encode()).hexdigest()

def categorize(title):
    t = title.lower()
    for cat, words in CATEGORY_MAP.items():
        if any(w in t for w in words):
            return cat
    return "science"

def fetch_archive():
    term = random.choice(SEARCH_TERMS)
    r = requests.get(
        "https://archive.org/advancedsearch.php",
        params={
            "q": f"{term} AND mediatype:movies",
            "output": "json",
            "rows": MAX_RESULTS
        },
        timeout=10
    )
    data = r.json()
    results = []

    for doc in data.get("response", {}).get("docs", []):
        identifier = doc.get("identifier")
        title = doc.get("title", "Untitled")

        meta = requests.get(f"https://archive.org/metadata/{identifier}", timeout=10).json()
        files = meta.get("files", [])

        mp4 = next((f for f in files if f["name"].endswith(".mp4")), None)
        if not mp4:
            continue

        url = f"https://archive.org/download/{identifier}/{mp4['name']}"
        results.append({
            "id": generate_id(url),
            "title": title,
            "url": url,
            "category": categorize(title),
            "source": "archive"
        })

    return results

def expand():
    existing = load_existing()
    existing_ids = {v["id"] for v in existing}

    new = fetch_archive()
    added = 0

    for vid in new:
        if vid["id"] not in existing_ids:
            existing.append(vid)
            existing_ids.add(vid["id"])
            added += 1

    save_videos(existing)
    print(f"Added {added} new videos. Total: {len(existing)}")

if __name__ == "__main__":
    expand()
