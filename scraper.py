import requests
import json
import os
import random
from hashlib import md5

# =========================
# CONFIG
# =========================

MAX_RESULTS = 25
MAX_DURATION_SECONDS = 900  # 15 min max
MAX_PAGE = 20

VIDEO_FILE_NORMAL = "videos.json"
VIDEO_FILE_KIDS = "kids_videos.json"

# =========================
# SEARCH TERMS & FILTERS
# =========================

NORMAL_SEARCH_TERMS = [
    "space documentary", "wildlife documentary", "ocean life",
    "science film", "rocket launch", "astronomy",
    "nature documentary", "technology documentary"
]

KIDS_WHITELIST = [
    "cartoon", "storybook", "bedtime", "learning", "alphabet",
    "animals for kids", "nursery", "nature for children",
    "educational for children", "children's film", "public domain cartoon"
]

# Strict blacklist to keep adult/horror content out
BLACKLIST = [
    "adult", "horror", "sexy", "gore", "violence", "nude", "blood", 
    "thriller", "slasher", "nsfw", "erotic", "scary", "murder"
]

PUBLIC_DOMAIN_SOURCES = ["archive.org", "wikimedia", "nasa"]

# =========================
# HELPERS
# =========================

def load_existing(filename):
    if not os.path.exists(filename):
        return []
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []

def save_videos(filename, data):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def generate_id(url):
    return md5(url.encode()).hexdigest()

def is_clean(text):
    t = text.lower()
    return not any(bad_word in t for bad_word in BLACKLIST)

def is_safe_kids(title, description=""):
    text = (title + " " + description).lower()
    if not is_clean(text):
        return False
    return any(word in text for word in KIDS_WHITELIST)

def categorize_normal(title):
    t = title.lower()
    if "space" in t or "rocket" in t or "astronomy" in t: return "space"
    if "wildlife" in t or "animal" in t or "ocean" in t: return "animals"
    if "technology" in t or "computer" in t: return "technology"
    if "history" in t: return "history"
    return "science"

# =========================
# FETCH FUNCTIONS
# =========================

def fetch_archive(query, kids_only=False):
    page = random.randint(1, MAX_PAGE)
    print(f"\nSearching Archive.org: '{query}' | page {page} | kids_only={kids_only}")

    try:
        r = requests.get(
            "https://archive.org/advancedsearch.php",
            params={
                "q": query,
                "fl[]": ["identifier", "title", "description"],
                "output": "json",
                "rows": MAX_RESULTS,
                "page": page
            },
            timeout=20
        )
        r.raise_for_status()
    except Exception as e:
        print("Search failed:", e)
        return []

    docs = r.json().get("response", {}).get("docs", [])
    random.shuffle(docs)

    results = []
    for doc in docs:
        identifier = doc.get("identifier")
        title = doc.get("title", "Untitled")
        description = doc.get("description", "")

        # Strict filter before even fetching metadata
        if not is_clean(title + " " + description):
            continue
        if kids_only and not is_safe_kids(title, description):
            continue

        try:
            meta = requests.get(f"https://archive.org/metadata/{identifier}", timeout=10).json()
        except:
            continue

        files = meta.get("files", [])
        mp4 = next((f for f in files if f.get("name", "").endswith(".mp4")), None)
        if not mp4:
            continue

        duration = mp4.get("length")
        if duration:
            try:
                if float(duration) > MAX_DURATION_SECONDS:
                    continue
            except:
                pass

        category = "kids" if kids_only else categorize_normal(title)
        url = f"https://archive.org/download/{identifier}/{mp4['name']}"
        print(f"Found: {title}")
        results.append({
            "id": generate_id(url),
            "title": title,
            "url": url,
            "category": category,
            "source": "archive"
        })

    return results

def fetch_wikimedia(query, kids_only=False):
    print(f"\nSearching Wikimedia Commons: '{query}' | kids_only={kids_only}")
    url = "https://commons.wikimedia.org/w/api.php"
    params = {
        "action": "query",
        "generator": "search",
        "gsrsearch": query,
        "gsrlimit": MAX_RESULTS,
        "prop": "imageinfo",
        "iiprop": "url",
        "format": "json"
    }

    try:
        r = requests.get(url, params=params, timeout=15)
        r.raise_for_status()
    except:
        return []

    pages = r.json().get("query", {}).get("pages", {})
    results = []
    for page in pages.values():
        title = page.get("title", "Untitled")
        if not is_clean(title): continue
        if kids_only and not is_safe_kids(title): continue
        
        imageinfo = page.get("imageinfo", [])
        if not imageinfo: continue
        
        url = imageinfo[0].get("url")
        if not url: continue
        
        results.append({
            "id": generate_id(url),
            "title": title,
            "url": url,
            "category": "kids" if kids_only else "science",
            "source": "wikimedia"
        })
    return results

# =========================
# RANDOM FETCHER
# =========================

def random_fetch(kids_only=False):
    source = random.choice(PUBLIC_DOMAIN_SOURCES)
    term = random.choice(KIDS_WHITELIST) if kids_only else random.choice(NORMAL_SEARCH_TERMS)

    if source == "archive.org":
        query = f'{term} AND mediatype:movies'
        if kids_only:
            query += ' AND (subject:"children" OR subject:"cartoon" OR subject:"education")'
        return fetch_archive(query, kids_only=kids_only)

    if source == "wikimedia":
        return fetch_wikimedia(term, kids_only=kids_only)

    if source == "nasa":
        url = "https://images-api.nasa.gov/search"
        params = {"q": term, "media_type": "video", "page": random.randint(1, MAX_PAGE)}
        try:
            r = requests.get(url, params=params, timeout=15).json()
            items = r.get("collection", {}).get("items", [])
            random.shuffle(items)
            results = []
            for item in items:
                data = item.get("data", [{}])[0]
                title = data.get("title", "Untitled")
                
                if not is_clean(title): continue
                if kids_only and not is_safe_kids(title): continue

                links = item.get("links", [])
                video_link = next((l["href"] for l in links if l["render"]=="video"), None)
                if not video_link: continue
                
                results.append({
                    "id": generate_id(video_link),
                    "title": title,
                    "url": video_link,
                    "category": "kids" if kids_only else "space",
                    "source": "nasa"
                })
            return results
        except:
            return []

# =========================
# EXPAND POOL
# =========================

def expand_pool(filename, kids_only=False):
    existing = load_existing(filename)
    existing_ids = {v["id"] for v in existing}

    new_videos = random_fetch(kids_only=kids_only)
    added = 0
    
    for vid in new_videos:
        if vid["id"] not in existing_ids:
            existing.append(vid)
            existing_ids.add(vid["id"])
            added += 1

    save_videos(filename, existing)
    print(f"Added {added} new videos. Total: {len(existing)}")

if __name__ == "__main__":
    print("Fetching NORMAL videos...")
    expand_pool(VIDEO_FILE_NORMAL, kids_only=False)

    print("\nFetching KIDS videos...")
    expand_pool(VIDEO_FILE_KIDS, kids_only=True)

    print("\nDone.")