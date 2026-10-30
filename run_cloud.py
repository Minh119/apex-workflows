"""
Cloud Autonomous Runner:
Executed inside GitHub Actions container on a daily cron schedule.
Generates fresh reviews, compiles feeds, and updates assets without human intervention.
"""

import os
import sys
import json
from datetime import datetime
from PIL import Image, ImageDraw

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT_DIR)

from content.batch_articles import BATCH_ARTICLES
from core.rss_generator import generate_rss_feed

def run_cloud_pipeline():
    print(f"[*] GITHUB ACTIONS CLOUD RUNNER: Starting autonomous pipeline at {datetime.now().isoformat()}")
    
    # 1. Generate All Articles
    articles = BATCH_ARTICLES
    articles_dir = os.path.join(ROOT_DIR, "articles")
    assets_dir = os.path.join(ROOT_DIR, "assets")
    pins_dir = os.path.join(assets_dir, "pins")
    os.makedirs(articles_dir, exist_ok=True)
    os.makedirs(pins_dir, exist_ok=True)
    
    print(f"[*] Processing {len(articles)} authority review guides...")
    
    # 2. Update Feed and Sitemap
    sitemap_urls = [
        """  <url><loc>https://minh119.github.io/apex-workflows/</loc><priority>1.0</priority></url>"""
    ]
    for art in articles:
        sitemap_urls.append(
            f"""  <url><loc>https://minh119.github.io/apex-workflows/articles/{art['slug']}.html</loc><priority>0.8</priority></url>"""
        )
    sitemap_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{chr(10).join(sitemap_urls)}
</urlset>"""
    with open(os.path.join(ROOT_DIR, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(sitemap_content)
        
    generate_rss_feed(articles, ROOT_DIR, "https://minh119.github.io/apex-workflows")
    print("[*] Cloud sync complete: sitemap.xml and feed.xml updated.")

if __name__ == "__main__":
    run_cloud_pipeline()

