"""
RSS 2.0 & Media Enclosure Feed Generator for Pinterest Auto-Publishing
Pinterest reads this feed directly to auto-create Pins without human intervention.
"""

import os
from datetime import datetime

def generate_rss_feed(articles, output_dir, site_url="https://minh119.github.io/apex-workflows"):
    items = []
    
    for art in articles:
        img_url = f"{site_url}/assets/pins/pin_{art['slug'].replace('best-', '').replace('-2026', '').replace('-', '_')}.png"
        # Match template naming convention
        if "chair" in art["slug"]:
            img_url = f"{site_url}/assets/pins/pin_ergonomic_chairs.png"
        elif "desk" in art["slug"]:
            img_url = f"{site_url}/assets/pins/pin_standing_desks.png"
        elif "mic" in art["slug"]:
            img_url = f"{site_url}/assets/pins/pin_podcasting_mics.png"
        elif "headphone" in art["slug"]:
            img_url = f"{site_url}/assets/pins/pin_anc_headphones.png"

        item_xml = f"""    <item>
      <title><![CDATA[{art['title']}]]></title>
      <link>{site_url}/articles/{art['slug']}.html</link>
      <guid isPermaLink="true">{site_url}/articles/{art['slug']}.html</guid>
      <pubDate>{datetime.now().strftime('%a, %d %b %Y 12:00:00 +0000')}</pubDate>
      <description><![CDATA[{art['meta_description']} Full lab review on ApexWorkflows.]]></description>
      <enclosure url="{img_url}" type="image/png" length="102400" />
      <media:content xmlns:media="http://search.yahoo.com/mrss/" url="{img_url}" medium="image" type="image/png" />
    </item>"""
        items.append(item_xml)

    rss_xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" 
     xmlns:content="http://purl.org/rss/1.0/modules/content/"
     xmlns:media="http://search.yahoo.com/mrss/">
  <channel>
    <title>ApexWorkflows | Lab Gear & Ergonomic Reviews</title>
    <link>{site_url}</link>
    <description>Independent workplace ergonomics and remote productivity gear tests.</description>
    <language>en-US</language>
    <lastBuildDate>{datetime.now().strftime('%a, %d %b %Y %H:%M:%S +0000')}</lastBuildDate>
{chr(10).join(items)}
  </channel>
</rss>"""

    feed_path = os.path.join(output_dir, "feed.xml")
    with open(feed_path, "w", encoding="utf-8") as f:
        f.write(rss_xml)
    return feed_path

