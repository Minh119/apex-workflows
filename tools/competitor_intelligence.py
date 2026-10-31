"""
Agent 6: Competitor Reverse-Engineer & Teardown Intelligence Module
Analyzes competitor architectures (BTOD, Wirecutter, ErgonomicTrends)
to extract high-converting keyword gaps and product battle blueprints.
"""

import os
import sys
import json
from datetime import datetime

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT_DIR)

from core.gemini_writer import get_api_key, MODEL_NAME
import urllib.request

def run_competitor_teardown(target_competitor="BTOD.com & ErgonomicTrends.com"):
    print(f"[*] Agent 6 (Competitor Teardown AI): Đang mổ xẻ cấu trúc lưu lượng và doanh thu của {target_competitor}...")
    
    api_key = get_api_key()
    prompt = f"""You are Agent 6 (Competitor Intelligence Specialist) for 'The Apex Workflows'.
Analyze the monetization strategy of top US ergonomic affiliate publishers: '{target_competitor}'.

Identify:
1. Their Top 3 Highest Revenue Article Formats (e.g. Head-to-Head Battles, 1-Year Durability Updates, Price-Tier Roundups).
2. Their 3 Biggest Weaknesses / Blind Spots (e.g. outdated pricing, ignoring sub-$300 direct-to-consumer Amazon gems, bloated mobile pages).
3. The #1 'Sniper' Head-to-Head Product Comparison keyword they dominate that we can ethically beat in 2026 with better data and zero ad bloat.
4. A concrete title and angle for our attack article to steal targeted traffic.

Output strict valid JSON with keys:
{{
  "competitor_analyzed": "{target_competitor}",
  "estimated_monthly_traffic": "500k - 1.2M visits/mo",
  "top_revenue_formats": ["format 1", "format 2", "format 3"],
  "competitor_fatal_flaws": ["flaw 1", "flaw 2", "flaw 3"],
  "sniper_keyword_target": "keyword here",
  "recommended_attack_article": {{
    "title": "Headline",
    "meta_description": "Meta description",
    "strategic_advantage": "Why we will outrank/outconvert them"
  }}
}}
Only output JSON."""

    url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL_NAME}:generateContent?key={api_key}"
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers={"Content-Type": "application/json"})
    
    res = urllib.request.urlopen(req, timeout=30)
    raw = json.loads(res.read().decode("utf-8"))["candidates"][0]["content"]["parts"][0]["text"].strip()
    
    if raw.startswith("```json"):
        raw = raw[7:]
    if raw.startswith("```"):
        raw = raw[3:]
    if raw.endswith("```"):
        raw = raw[:-3]
        
    intel = json.loads(raw.strip())
    
    report_file = os.path.join(ROOT_DIR, "reports", f"Competitor_Teardown_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
    with open(report_file, "w", encoding="utf-8") as f:
        json.dump(intel, f, indent=2, ensure_ascii=False)
        
    print("[✔] Agent 6: Mổ xẻ đối thủ hoàn tất! Báo cáo lưu tại:", report_file)
    return intel

if __name__ == "__main__":
    teardown = run_competitor_teardown()
    print("\n[BÁO CÁO NHANH CHO CHỦ TỊCH]:")
    print("Đối thủ phân tích:", teardown.get("competitor_analyzed"))
    print("Từ khóa bắn tỉa chủ lực:", teardown.get("sniper_keyword_target"))
    print("Bài viết tấn công đề xuất:", teardown.get("recommended_attack_article", {}).get("title"))
