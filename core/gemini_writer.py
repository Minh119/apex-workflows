"""
Gemini Intelligence Writer Module:
Directly leverages Gemini AI to generate high-converting, E-E-A-T benchmark reviews.
"""

import os
import sys
import json
import urllib.request

def get_api_key():
    key = os.environ.get("GEMINI_API_KEY")
    if key:
        return key
    local_cfg = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "config", "local_keys.json")
    if os.path.exists(local_cfg):
        try:
            with open(local_cfg, "r", encoding="utf-8") as f:
                return json.load(f).get("gemini_api_key")
        except Exception:
            pass
    return None

MODEL_NAME = "gemini-3.5-flash"

def generate_review_content(product_name, category, price_range):
    """Sử dụng Gemini để sản xuất bài đánh giá chuyên sâu"""
    api_key = get_api_key()
    if not api_key:
        raise ValueError("GEMINI_API_KEY is not set.")

    prompt = f"""You are an elite workspace technology journalist writing for 'The Apex Workflows'.
Write an in-depth, hands-on lab benchmark review for: '{product_name}' in the category '{category}'.
Target Audience: Remote knowledge workers, developers, and corporate executives in the US.
Tone: Authoritative, objective, technical yet accessible, highlighting real-world trade-offs.

Output strict valid JSON with the following structure:
{{
  "title": "Compelling, high-CTR article headline (include 2026)",
  "meta_description": "Under 160 characters summary with high search intent",
  "read_time": "e.g. 8 min read",
  "rating": "e.g. 4.9",
  "author": "Dr. Elena Rostova, Ergonomics Consultant",
  "lead_box_html": "Quick Verdict / TL;DR text inside HTML tags",
  "why_it_matters_html": "2-3 paragraphs analyzing the underlying engineering problem",
  "pros": ["Pro 1", "Pro 2", "Pro 3"],
  "cons": ["Con 1", "Con 2"]
}}

Only respond with the JSON object. Do not wrap in markdown codeblocks if possible."""

    url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL_NAME}:generateContent?key={api_key}"
    payload = {
        "contents": [{"parts": [{"text": prompt}]}]
    }
    
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    
    res = urllib.request.urlopen(req, timeout=30)
    raw_text = json.loads(res.read().decode("utf-8"))["candidates"][0]["content"]["parts"][0]["text"].strip()
    
    if raw_text.startswith("```json"):
        raw_text = raw_text[7:]
    if raw_text.startswith("```"):
        raw_text = raw_text[3:]
    if raw_text.endswith("```"):
        raw_text = raw_text[:-3]
        
    return json.loads(raw_text.strip())

if __name__ == "__main__":
    test_res = generate_review_content("BenQ ScreenBar Pro Monitor Light Bar", "Workspace Lighting", "$140")
    print("Generated Title:", test_res.get("title"))
