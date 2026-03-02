# VOIDSCROLL

A zero-backend infinite scroll science video app.

## How It Works

- `scraper.py` pulls new public domain MP4 videos from Archive.org
- It appends new videos to `videos.json`
- `index.html` reads the JSON file and renders the scroll feed

## Setup

Install dependencies:

pip install -r requirements.txt

Run scraper:

python scraper.py

Open `index.html` in browser (or host on GitHub Pages)

## Expand Content

Run scraper again anytime to expand the pool.
Duplicates are automatically ignored.
