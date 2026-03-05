import requests
import json
import random

# Giphy API Configuration
# This is a public beta key provided by Giphy for testing.
GIPHY_API_KEY = "dc6zaTOxFJmzC" 
SEARCH_ENDPOINT = "https://api.giphy.com/v1/gifs/search"

def get_giphy_gif(giphy_id):
    """Direct GIF URL for high reliability on mobile/web."""
    return f"https://media.giphy.com/media/{giphy_id}/giphy.gif"

def fetch_giphy_api(query, limit=25):
    """
    Fetches GIFs using the official Giphy API.
    Bypasses 403 Forbidden errors from scraping search pages.
    """
    params = {
        "api_key": GIPHY_API_KEY,
        "q": query,
        "limit": limit,
        "rating": "g"
    }
    
    try:
        r = requests.get(SEARCH_ENDPOINT, params=params, timeout=10)
        r.raise_for_status()
        data = r.json()
        
        results = []
        for gif in data.get("data", []):
            results.append({
                "id": gif["id"],
                "url": get_giphy_gif(gif["id"]),
                "title": query.upper()
            })
        return results
    except Exception as e:
        print(f"API Error for {query}: {e}")
        return []

if __name__ == "__main__":
    queries = [
        "backrooms", "liminal space", "psychedelic loop", "trippy fractal", 
        "hypnotic patterns", "glitch art loop", "kaleidoscope loop", 
        "vhs aesthetic", "optical illusion loop", "deep sky loop", 
        "retro sci-fi loop", "pixel art aesthetic loop"
    ]
    
    all_gifs = []
    seen_ids = set()
    
    print("🚀 Starting Giphy Void Scraper (API Mode)...")
    
    for q in queries:
        print(f"🔍 Searching: {q}...")
        found_gifs = fetch_giphy_api(q)
        for gif in found_gifs:
            if gif["id"] not in seen_ids:
                all_gifs.append(gif)
                seen_ids.add(gif["id"])
    
    random.shuffle(all_gifs)
    
    # Save to void_gifs.json
    try:
        with open('void_gifs.json', 'w') as f:
            json.dump(all_gifs, f, indent=2)
        print(f"✅ Finished! Saved {len(all_gifs)} GIFs to void_gifs.json")
    except Exception as e:
        print(f"File Error: {e}")
