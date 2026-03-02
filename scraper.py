aper · PY
Copy

import requests
import json
import os
import random
from hashlib import md5
import time

# =========================
# CONFIG
# =========================

MAX_RESULTS = 40
MAX_DURATION_SECONDS = 999  # ~15 min max
MAX_PAGE = 20

VIDEO_FILE_NORMAL = "videos.json"
VIDEO_FILE_KIDS   = "kids_videos.json"

# =========================
# SEARCH TERMS
# =========================

NORMAL_SEARCH_TERMS = [
    # Space & Astronomy
    "space documentary", "rocket launch", "astronomy", "planets", "solar system",
    "moon landing", "mars mission", "satellite footage", "space exploration", "cosmos",
    "nebula timelapse", "black holes documentary", "astronaut training", "space station life",
    "asteroid impact", "comet footage", "space telescopes", "exoplanets", "spacewalk",
    "galaxy formation", "orbital mechanics", "cosmic events", "meteor shower", "planetary geology",
    "space physics", "astronomy lecture", "space science", "space technology", "space shuttle history",
    "mars rover mission", "space probes", "satellite launches", "stellar evolution",
    "planetary atmospheres", "astronomy visualization", "cosmic rays", "telescope review",
    "space colonies", "rocket science tutorial", "moon phases explanation",
    "solar eclipse footage", "space simulation", "space mission documentary",
    "interstellar travel", "planetary motion", "astrochemistry", "life in space", "star clusters",
    "gravity experiments", "observatory tour",

    # Wildlife & Nature
    "wildlife documentary", "nature documentary", "forest wildlife", "jungle animals",
    "savannah animals", "ocean life", "underwater documentary", "marine biology",
    "birds documentary", "insects documentary", "animal behavior", "predator vs prey",
    "coral reef exploration", "deep sea creatures", "migratory birds", "endangered species",
    "tropical rainforest", "arctic wildlife", "desert ecosystem", "wildlife rescue",
    "animal adaptation", "nature timelapse", "river ecosystem", "mountain wildlife",
    "nature soundscape", "forest conservation", "bee documentary", "butterfly lifecycle",
    "wolves documentary", "big cats documentary", "penguin colony", "whale migration",
    "shark behavior", "elephant herd", "primate behavior", "ocean currents documentary",
    "volcano wildlife", "jungle exploration", "wildlife photography", "ecosystem balance",
    "animal tracking", "natural wonders", "botanical documentary",
    "tree species documentary", "forest ecosystem", "reptile documentary", "amphibian behavior",
    "birdsong compilation", "marine predator documentary",

    # Science & Technology
    "science film", "technology documentary", "physics documentary",
    "chemistry documentary", "biology documentary", "robotics documentary", "futuristic technology",
    "AI development", "quantum physics", "nanotechnology",
    "renewable energy", "3D printing tutorial", "engineering marvels", "mechanical design",
    "scientific experiments", "chemistry experiments", "biology experiments", "tech innovations",
    "computer science tutorial", "software development documentary",
    "cybersecurity documentary", "tech history", "electronics tutorial", "scientific breakthroughs",
    "mechanics tutorial", "materials science", "environmental tech",
    "medical technology", "robotics for beginners", "autonomous systems", "AI ethics",
    "machine learning tutorial", "tech inventions", "coding challenge", "scientific discoveries",
    "science communication", "technology trends", "future tech concepts", "science news",
    "technology analysis", "physics experiments", "research lab footage",
    "technology interviews", "science lectures", "tech DIY",

    # Calm & Sleep
    "calm relaxing scenery", "peaceful nature", "ambient forest", "ocean waves",
    "mountain scenery", "sunset timelapse", "river flowing", "meditation video",
    "rain sounds", "fireplace video", "night sky timelapse", "slow motion nature",
    "zen garden", "relaxing music video", "peaceful river", "waterfall timelapse",
    "forest sounds", "relaxation for sleep", "calming ocean", "candle meditation",
    "soft piano music", "relaxing beach video", "mountain lake", "foggy forest",
    "soothing waterfalls", "nature ASMR", "deep breathing guide", "relaxing timelapse",
    "rainforest sounds", "relaxing sunset", "gentle river", "sleep meditation",
    "peaceful ocean waves", "calm landscapes", "tranquil mountains", "ambient music",
    "forest walk", "starry night sky", "meditative visuals", "slow nature video",
    "relaxing forest stream", "ocean breeze", "water meditation", "chill scenery",
    "peaceful garden", "soft nature music", "calm drone footage", "serene beach",
    "forest sunrise", "relaxing autumn forest",

    # Historical / Educational
    "history documentary", "ancient civilizations", "world history", "educational film",
    "geography documentary", "cultural documentary", "human body documentary",
    "medieval history", "renaissance documentary", "industrial revolution", "world wars",
    "historical figures documentary", "civil rights history", "ancient Egypt",
    "ancient Greece", "Roman Empire", "historical architecture", "archaeology documentary",
    "history of science", "history of technology", "educational lectures",
    "historical events", "cultural traditions", "human evolution", "philosophy documentary",
    "history timeline", "famous battles", "exploration history", "documentary series",
    "historical reenactment", "anthropology documentary", "history of medicine",
    "world cultures", "historical inventions", "documentary biographies", "ancient art",
    "historical mysteries", "education video", "historical maps",
    "historical documentaries full", "world heritage sites", "ancient cities", "historical research",
    "history timeline video", "famous explorers",

    # Vehicles & Machines
    "train documentary", "airplane documentary", "boat documentary", "industrial machines",
    "car documentary", "motorcycle documentary", "heavy machinery", "space vehicles",
    "submarine documentary", "construction equipment", "vehicle engineering",
    "transportation history", "robotic machines", "drone technology", "vehicle repair tutorial",
    "boat building documentary", "train operations", "vehicle design", "engineering vehicles",
    "industrial robotics", "automobile history", "futuristic vehicles", "agriculture machinery",
    "aircraft design", "spacecraft engineering", "electric vehicles", "self-driving cars",
    "railway technology", "mechanical inventions",
    "vehicle manufacturing", "boat tours documentary",
    "heavy transport", "machine mechanics", "vehicle maintenance", "plane engineering",
    "train timelapse", "drone footage vehicles", "construction site documentary", "vehicle technology",
    "mechanical engineering", "innovative machines", "flying cars concept", "space rover vehicles",

    # Engineering
    "engineering documentary", "space engineering", "engineering challenges",
    "engineering marvels vehicles", "civil engineering", "structural engineering",
    "bridge building documentary", "architecture documentary", "engineering history",
    "engineering innovations", "aerospace engineering",

    # DIY & Life Skills
    "home improvement", "craft tutorial", "gardening tips", "mechanics repair",
    "technology hacks", "upcycling projects", "DIY furniture", "woodworking tutorial",
    "home decoration ideas", "cooking hacks", "cleaning tips", "organization tips",
    "painting tutorial", "sewing tutorial", "life hacks", "DIY electronics", "creative projects",
    "handmade gifts", "garden design", "house repair", "upcycling furniture", "diy gadgets",
    "painting techniques", "home renovation", "crafting for kids", "decor ideas",
    "DIY repair tutorial", "gardening DIY", "organization hacks", "DIY projects for home",
    "craft supplies tutorial", "tool usage tutorial", "gardening tools", "creative diy",
    "woodcraft tutorial", "diy holiday decor", "home maintenance", "crafting techniques",
    "upcycling clothing", "diy painting", "electronics repair",
    "craft ideas", "diy art", "home hacks", "life skill tutorials", "crafting tips",

    # Gaming & Esports
    "gaming tutorial", "esports tournament", "gameplay walkthrough", "strategy guide",
    "speedrun video", "game analysis", "lets play", "game review", "multiplayer gameplay",
    "game commentary", "video game documentary", "game lore", "esports analysis", "game physics",
    "board game tutorial", "puzzle game video", "roleplaying game guide", "simulation game",
    "mobile gaming", "retro gaming", "indie game review", "game development tutorial",
    "game mechanics explained", "game modding", "strategy gaming", "arcade game video",
    "speedrun challenge", "virtual reality game", "augmented reality gaming", "game design documentary",
    "competitive gaming", "game streaming", "gaming culture", "game walkthrough", "gameplay compilation",
    "video game lore", "gaming history", "game storytelling", "esports highlights",
    "multiplayer strategy", "gamer interviews", "game tech documentary",

    # Math & Brain Challenges
    "puzzle solving", "logic challenge", "brain teaser", "math challenge",
    "riddle video", "memory game", "IQ test", "strategy puzzle", "problem solving tutorial",
    "cognitive exercises", "critical thinking challenge", "memory exercises", "chess strategy",
    "sudoku tutorial", "rubik's cube solving", "mental math challenge", "crossword puzzles",
    "brain training", "logic puzzle challenge", "mathematics riddle", "memory improvement",
    "cognitive development", "brain games", "math tricks", "puzzle tutorial",
    "intelligence test", "reasoning challenge", "mathematical puzzles", "brain teasers compilation",
    "logic exercises", "mind exercises", "puzzle solving techniques",
    "math games for kids", "mental agility games", "IQ puzzles",
    "thinking skills", "strategy puzzle games", "critical thinking skills",
    "problem solving skills", "mind games",

    # Environment & Climate
    "climate change documentary", "eco-friendly living", "sustainable energy",
    "environmental science", "wildlife conservation", "global warming", "carbon footprint",
    "renewable energy documentary", "ocean conservation", "deforestation documentary",
    "plastic pollution", "recycling tutorial", "eco travel documentary", "environmental awareness",
    "climate solutions", "solar energy tutorial", "wind energy", "eco-friendly tips",
    "green technology", "sustainable living tips", "environmental policy", "eco documentaries",
    "wildlife protection", "environmental activism", "climate science", "nature conservation",
    "pollution solutions", "eco innovation", "forest protection", "clean energy tutorial",
    "environmental education", "water conservation", "green living", "eco-friendly lifestyle",
    "climate documentaries full", "renewable energy solutions",
    "sustainable farming", "eco architecture", "green building", "carbon reduction tips",

    # Travel & Geography
    "mountain trek documentary", "city tour", "cultural festival", "world landmarks",
    "travel vlog", "eco-tourism", "adventure travel", "historical city tour", "desert exploration",
    "tropical island tour", "mountain climbing", "river expedition", "world cultures",
    "travel documentary", "local traditions", "geography lecture", "travel tips",
    "backpacking guide", "cultural exchange documentary", "nature travel", "urban exploration",
    "hiking documentary", "glacier tour", "countryside tour", "ancient landmarks",
    "tourist attractions", "travel photography", "travel guide video", "hidden travel gems",
    "cultural sites", "world exploration", "world geography", "nature travel vlog",
    "mountain adventure", "travel routes", "travel experiences", "international travel documentary",
    "eco-travel vlog", "city landmarks", "remote locations documentary", "travel history documentary",
    "travel hacks", "adventure vlog", "geography documentary full",

    # Documentary (general)
    "full documentary", "documentary film", "award winning documentary",
    "documentary series", "investigative documentary", "social documentary",
    "science documentary series", "nature documentary series",
]

# =========================
# BLACKLIST
# =========================
BLACKLIST = [
    # Explicit / Adult
    "adult", "sexy", "nude", "erotic", "nsfw", "porn", "bikini", "lingerie", "strip", "fetish",
    "nudity", "xxx", "sexual", "sex", "erotica", "escort", "camgirl", "pornography", "softcore", "hardcore",
    # Violence / Weapons
    "gun", "shooting", "weapon", "war", "combat", "soldier", "military", "blood", "gore",
    "murder", "death", "killed", "execution", "suicide", "fight", "assault", "terrorist",
    "terrorism", "explosion", "bomb", "knife", "fight scene", "crime scene", "homicide", "shootout",
    "violence", "attacked", "hostage", "battle", "militant", "bullet", "army", "grenade", "sniper",
    # Horror / Spooky
    "horror", "scary", "creepy", "spooky", "monster", "ghost", "demon", "vampire", "zombie",
    "thriller", "slasher", "jumpscare", "darkness", "skeleton", "haunted", "witch", "witchcraft",
    "analog horror", "backrooms", "creepypasta", "clown", "bloodcurdling", "poltergeist",
    "fear", "haunting", "dread", "paranormal", "possession", "cursed",
    # Medical / Disturbing
    "surgery", "medical", "injury", "accident", "crash", "disaster", "hospital", "operation",
    "blood loss", "amputation", "trauma", "pathology", "infection", "fatal", "autopsy", "emergency",
    "disease", "contagion", "epidemic", "plague", "dead", "cadaver", "burial", "funeral", "disfigurement",
    "traumatic", "graphic", "violently", "brutal", "abuse", "torture", "slaughter",
]

# =========================
# KIDS WHITELIST
# =========================
KIDS_WHITELIST = [
    "classic cartoon", "silly symphony", "public domain animation", "merrie melodies",
    "vintage cartoon", "classic animation for kids", "felix the cat", "oswald rabbit",
    "public domain shorts", "animated fables", "classic animated series",
    "letter sounds", "alphabet song", "counting songs", "number recognition", "learning numbers",
    "shapes for kids", "colors for kids", "basic math for children", "early learning video", "ABC for kids",
    "phonics video", "spelling for kids", "vocabulary for kids", "educational animation", "learning letters",
    "kids learning video", "numbers and counting", "alphabet animation",
    "nature timelapse", "underwater world", "outer space for kids", "zoo animals", "butterfly life cycle",
    "forest animals", "ocean creatures", "birds for kids", "farm animals", "aquarium animals",
    "wildlife for children", "baby animals", "animal sounds", "jungle animals", "desert animals",
    "marine life for kids", "coral reef exploration", "reptiles for kids", "penguins for kids",
    "dolphins for kids", "whales for kids", "turtles for kids", "horses for children",
    "puppies for kids", "kittens for kids", "bee documentary for kids", "butterfly garden",
    "nature exploration kids", "animal documentaries for children", "underwater fish",
    "relaxing video", "calm scenery", "ambient forest", "ocean waves", "mountain scenery",
    "sunset timelapse", "river flowing", "peaceful nature", "meditation video", "clouds timelapse",
    "rain sounds for kids", "fireplace video", "gentle waterfall", "slow nature video",
    "tranquil beach", "serene forest", "gentle river", "soft piano for kids", "ambient music",
    "calm ocean", "river timelapse", "sunrise timelapse", "stars timelapse", "night sky for kids",
    "butterfly timelapse", "flower blooming timelapse", "meadow scenery", "field of flowers",
    "children songs", "nursery rhymes", "kids music video", "sing along songs", "dance for kids",
    "learning songs", "musical story for kids", "instrument sounds", "kids singing", "movement songs",
    "action songs for children", "rhythm games", "kids choir", "baby lullabies",
    "calm music for toddlers", "fun songs for preschool", "kids music animation",
    "how it's made", "science for kids", "kids experiments", "building blocks tutorial",
    "crafts for children", "drawing for kids", "painting for children", "coloring tutorial",
    "story time", "fairy tale video", "educational cartoons", "fun facts for kids", "kids quiz",
    "learning animals", "learning planets", "learning shapes", "learning colors", "kids exploration",
    "children activities", "interactive learning", "kids discovery", "safe adventure video",
    "kids tutorials", "beginner science for children", "storytelling for kids",
]

PUBLIC_DOMAIN_SOURCES = ["archive.org", "wikimedia", "nasa"]

# =========================
# CATEGORY MAPPING
# Covers every id used in the frontend CATS array
# =========================
def categorize_kids(title, description=""):
    t = (title + " " + description).lower()
    if any(w in t for w in ["cartoon", "animation", "animated", "looney", "mickey", "felix", "silly symphony", "merrie"]):
        return "cartoons"
    if any(w in t for w in ["song", "music", "nursery", "lullaby", "singing", "choir", "rhyme", "dance"]):
        return "music"
    if any(w in t for w in ["alphabet", "letter", "number", "count", "shape", "color", "phonics", "learn", "spell", "quiz", "abc"]):
        return "learning"
    if any(w in t for w in ["sleep", "calm", "relax", "lullaby", "sooth", "gentle", "soft", "peaceful"]):
        return "sleep"
    if any(w in t for w in ["space", "rocket", "planet", "star", "moon", "cosmos", "astronaut"]):
        return "space"
    if any(w in t for w in ["animal", "wildlife", "zoo", "farm", "ocean", "bird", "insect", "fish", "pet", "puppy", "kitten"]):
        return "animals"
    if any(w in t for w in ["nature", "forest", "flower", "tree", "garden", "butterfly", "river", "mountain"]):
        return "nature"
    return "learning"  # safe fallback for kids
    t = title.lower()

    # Space / Astronomy
    if any(w in t for w in [
        "space", "rocket", "astronomy", "astronaut", "nasa", "orbit", "satellite",
        "planet", "solar system", "cosmos", "nebula", "galaxy", "comet", "asteroid",
        "telescope", "moon", "mars", "exoplanet", "spacewalk", "stellar", "cosmic",
        "interstellar", "astrophysics", "observatory", "star cluster", "black hole",
    ]):
        return "space"

    # Animals / Wildlife
    if any(w in t for w in [
        "wildlife", "animal", "ocean", "marine", "underwater", "coral reef",
        "deep sea", "shark", "whale", "dolphin", "elephant", "lion", "tiger",
        "bird", "insect", "reptile", "amphibian", "penguin", "primate", "predator",
        "savannah", "jungle animals", "forest animals", "zoo",
    ]):
        return "animals"

    # Nature (landscapes, plants, ecosystems — not animals)
    if any(w in t for w in [
        "nature", "forest", "mountain", "landscape", "botanical", "tree",
        "river", "waterfall", "rainforest", "arctic", "desert ecosystem",
        "natural wonder", "ecosystem", "volcano", "wilderness",
    ]):
        return "nature"

    # Sleep / Calm / Relaxing
    if any(w in t for w in [
        "sleep", "relax", "calm", "peaceful", "meditation", "ambient", "soothing",
        "tranquil", "zen", "asmr", "fireplace", "rain sound", "lo-fi", "lullaby",
        "slow motion", "serene", "gentle", "fog", "soft piano",
    ]):
        return "sleep"

    # Technology
    if any(w in t for w in [
        "technology", "tech", "computer", "software", "ai ", "artificial intelligence",
        "machine learning", "robotics", "coding", "programming", "cybersecurity",
        "electronics", "nanotechnology", "3d printing", "autonomous", "digital",
        "internet", "semiconductor", "circuit",
    ]):
        return "technology"

    # Engineering
    if any(w in t for w in [
        "engineering", "civil engineer", "structural", "bridge", "architecture",
        "construction", "aerospace", "mechanical engineer", "materials science",
    ]):
        return "engineering"

    # Vehicles & Machines
    if any(w in t for w in [
        "vehicle", "car", "train", "airplane", "aircraft", "boat", "ship",
        "submarine", "truck", "motorcycle", "heavy machinery", "drone", "helicopter",
        "electric vehicle", "railway", "locomotive", "transport", "automobile",
        "plane", "tractor", "excavator",
    ]):
        return "vehicles"

    # Environment & Climate
    if any(w in t for w in [
        "environment", "climate", "eco", "sustainable", "green energy", "solar energy",
        "wind energy", "renewable", "conservation", "pollution", "carbon", "recycle",
        "global warming", "deforestation", "ocean conservation",
    ]):
        return "environment"

    # History
    if any(w in t for w in [
        "history", "ancient", "medieval", "historical", "archaeology", "civilization",
        "empire", "renaissance", "revolution", "war history", "biography",
        "civil rights", "exploration history", "heritage",
    ]):
        return "history"

    # Travel & Geography
    if any(w in t for w in [
        "travel", "geography", "city tour", "landmark", "cultural", "festival",
        "adventure", "hiking", "expedition", "vlog", "tourism", "backpack",
        "country", "world tour", "glacier",
    ]):
        return "travel"

    # Math & Brain
    if any(w in t for w in [
        "math", "puzzle", "logic", "brain", "riddle", "chess", "sudoku", "rubik",
        "cognitive", "iq test", "memory game", "reasoning", "arithmetic",
        "problem solving", "mental math",
    ]):
        return "math"

    # Gaming
    if any(w in t for w in [
        "gaming", "esports", "gameplay", "video game", "speedrun", "game review",
        "lets play", "retro game", "indie game", "game lore", "board game",
        "strategy game",
    ]):
        return "gaming"

    # Documentary (generic long-form)
    if any(w in t for w in [
        "documentary", "full film", "award winning", "investigative", "doc series",
    ]):
        return "documentary"

    # DIY
    if any(w in t for w in [
        "diy", "craft", "woodwork", "home improvement", "gardening", "upcycling",
        "sewing", "painting tutorial", "life hack", "home renovation", "decor",
        "handmade", "how to make",
    ]):
        return "diy"

    # Science (fallback for anything left)
    return "science"

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

# =========================
# FETCH FUNCTIONS
# =========================

def fetch_archive(query, kids_only=False):
    page = random.randint(1, MAX_PAGE)
    print(f"\nSearching Archive.org: '{query}' | page {page} | kids_only={kids_only}")
    results = []
    try:
        r = requests.get(
            "https://archive.org/advancedsearch.php",
            params={
                "q": query,
                "fl[]": ["identifier", "title", "description"],
                "output": "json",
                "rows": MAX_RESULTS,
                "page": page,
            },
            timeout=20,
        )
        r.raise_for_status()
    except Exception as e:
        print("Search failed:", e)
        return []

    docs = r.json().get("response", {}).get("docs", [])
    random.shuffle(docs)

    for doc in docs:
        identifier  = doc.get("identifier")
        title       = doc.get("title", "Untitled")
        description = doc.get("description", "")

        if isinstance(title, list):       title       = " ".join(title)
        elif not isinstance(title, str):  title       = str(title)
        if isinstance(description, list): description = " ".join(description)
        elif not isinstance(description, str): description = str(description)

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

        category = categorize_kids(title, description) if kids_only else categorize_normal(title)
        url = f"https://archive.org/download/{identifier}/{mp4['name']}"
        print(f"  Found [{category}]: {title}")
        results.append({
            "id":       generate_id(url),
            "title":    title,
            "url":      url,
            "category": category,
            "source":   "archive",
        })
    return results


def fetch_wikimedia(query, kids_only=False):
    print(f"\nSearching Wikimedia: '{query}' | kids_only={kids_only}")
    params = {
        "action":    "query",
        "generator": "search",
        "gsrsearch": query + " filetype:video",
        "gsrlimit":  MAX_RESULTS,
        "prop":      "imageinfo",
        "iiprop":    "url|mime",
        "format":    "json",
    }
    try:
        r = requests.get("https://commons.wikimedia.org/w/api.php", params=params, timeout=15)
        r.raise_for_status()
    except:
        return []

    pages = r.json().get("query", {}).get("pages", {})
    results = []
    for page in pages.values():
        title     = page.get("title", "Untitled")
        imageinfo = page.get("imageinfo", [])
        if not imageinfo:
            continue
        info = imageinfo[0]
        mime = info.get("mime", "")
        # Only accept actual video files
        if not mime.startswith("video/"):
            continue
        url = info.get("url")
        if not url:
            continue
        if not is_clean(title):
            continue
        if kids_only and not is_safe_kids(title):
            continue
        results.append({
            "id":       generate_id(url),
            "title":    title,
            "url":      url,
            "category": categorize_kids(title) if kids_only else categorize_normal(title),
            "source":   "wikimedia",
        })
    return results


def fetch_nasa(term, kids_only=False):
    print(f"\nSearching NASA: '{term}'")
    params = {"q": term, "media_type": "video", "page": random.randint(1, MAX_PAGE)}
    try:
        r = requests.get("https://images-api.nasa.gov/search", params=params, timeout=15).json()
        items = r.get("collection", {}).get("items", [])
        random.shuffle(items)
        results = []
        for item in items:
            data  = item.get("data", [{}])[0]
            title = data.get("title", "Untitled")
            if not is_clean(title):
                continue
            if kids_only and not is_safe_kids(title):
                continue
            links      = item.get("links", [])
            video_link = next((l["href"] for l in links if l.get("render") == "video"), None)
            if not video_link:
                continue
            results.append({
                "id":       generate_id(video_link),
                "title":    title,
                "url":      video_link,
                "category": categorize_kids(title) if kids_only else "space",
                "source":   "nasa",
            })
        return results
    except:
        return []


# =========================
# RANDOM FETCHER
# =========================

def random_fetch(kids_only=False):
    source = random.choice(PUBLIC_DOMAIN_SOURCES)
    term   = random.choice(KIDS_WHITELIST) if kids_only else random.choice(NORMAL_SEARCH_TERMS)

    if source == "archive.org":
        query = f'{term} AND mediatype:movies'
        if kids_only:
            query += ' AND (subject:"children" OR subject:"cartoon")'
        return fetch_archive(query, kids_only=kids_only)

    if source == "wikimedia":
        return fetch_wikimedia(term, kids_only=kids_only)

    if source == "nasa":
        return fetch_nasa(term, kids_only=kids_only)

    return []


# =========================
# EXPAND POOL (single run)
# =========================

def expand_pool(filename, kids_only=False):
    existing     = load_existing(filename)
    existing_ids = {v["id"] for v in existing}
    new_videos   = random_fetch(kids_only=kids_only)
    added = 0
    for vid in new_videos:
        if vid["id"] not in existing_ids:
            existing.append(vid)
            existing_ids.add(vid["id"])
            added += 1
    save_videos(filename, existing)
    print(f"Added {added} new videos. Total: {len(existing)}")


# =========================
# PERSISTENT SCRAPER LOOP
# =========================

def expand_pool_persistent(filename, kids_only=False, cycles=10000):
    """Runs the scraper in a long loop, saving after each successful batch."""
    existing     = load_existing(filename)
    existing_ids = {v["id"] for v in existing}

    for i in range(1, cycles + 1):
        print(f"\n{'='*50}")
        print(f"Cycle {i} of {cycles} | Library size: {len(existing)}")
        print('='*50)

        for attempt in range(20):
            new_videos = random_fetch(kids_only=kids_only)
            if not new_videos:
                print(f"  Attempt {attempt+1}: No results, retrying...")
                time.sleep(2)
                continue

            added = 0
            for vid in new_videos:
                if vid["id"] not in existing_ids:
                    existing.append(vid)
                    existing_ids.add(vid["id"])
                    added += 1

            if added > 0:
                print(f"  +{added} new videos saved.")
                save_videos(filename, existing)
                break
            else:
                print(f"  Attempt {attempt+1}: All duplicates, retrying...")

        if i < cycles:
            wait = random.randint(30, 60)
            print(f"\nWaiting {wait}s before next cycle...")
            time.sleep(wait)


# =========================
# ENTRY POINT
# =========================

if __name__ == "__main__":
    # Normal videos (all categories)
    expand_pool_persistent(VIDEO_FILE_NORMAL, kids_only=False, cycles=10000)

    # Uncomment to run kids scraper instead:
    # expand_pool_persistent(VIDEO_FILE_KIDS, kids_only=True, cycles=10000)

    print("\n[FINISH] Library updated.")