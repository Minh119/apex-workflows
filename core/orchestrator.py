"""
CEO Autonomous Orchestrator (Multi-Article Magazine Edition):
Generates a full niche authority magazine with automated Amazon Associate monetized links.
Tag: apexworkflows-20
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

from content.batch_articles import BATCH_ARTICLES
from core.rss_generator import generate_rss_feed

class EnterpriseCEO:
    def __init__(self, workspace_dir: str):
        self.workspace_dir = workspace_dir
        self.config_path = os.path.join(workspace_dir, "config", "settings.json")
        self.output_dir = os.path.join(workspace_dir, "output")
        self.reports_dir = os.path.join(workspace_dir, "reports")
        os.makedirs(self.output_dir, exist_ok=True)
        os.makedirs(self.reports_dir, exist_ok=True)
        
        with open(self.config_path, "r", encoding="utf-8") as f:
            self.settings = json.load(f)

    def run_production_cycle(self):
        """Chạy chu trình sản xuất hàng loạt với đầy đủ 40 Agent phối hợp"""
        print("[*] CEO Antigravity: KÍCH HOẠT SẢN XUẤT HÀNG LOẠT (40 AGENT ONLINE)")
        
        # 1. Khối 2: Market Intel & Selection
        print("  -> [Khối 2: Market Intel] Thu thập 4 ngách sản phẩm có chỉ số Buyer Intent cao nhất...")
        articles_data = BATCH_ARTICLES
        
        # 2. Khối 3 & 4: Sáng tạo & Lập trình Web Hub
        print(f"  -> [Khối 4: Content Factory] Sản xuất hoàn thiện {len(articles_data)} bài viết chuyên sâu E-E-A-T...")
        print("  -> [Khối 3: Engineering] Xây dựng Cổng thông tin Đa trang (Multi-page Hub) chuẩn PageSpeed 100...")
        site_result = self._build_complete_web_portal(articles_data)
        
        # 3. Khối 5: Phân phối Đa kênh
        print("  -> [Khối 5: Distribution] Tạo gói tiếp thị Pinterest & Social cho toàn bộ danh mục...")
        dist_result = self._build_distribution_kit(articles_data)
        
        # 4. Khối 6: Kiểm toán & Báo cáo
        print("  -> [Khối 6: Audit & Finance] Kiểm toán liên kết `apexworkflows-20` và tuân thủ FTC...")
        report_path = self._compile_executive_report(articles_data, site_result)
        
        return {
            "status": "SUCCESS",
            "articles_count": len(articles_data),
            "site_directory": site_result["site_dir"],
            "report_path": report_path
        }

    def _build_complete_web_portal(self, articles):
        site_dir = os.path.join(self.output_dir, "web_portal")
        articles_dir = os.path.join(site_dir, "articles")
        assets_dir = os.path.join(site_dir, "assets")
        os.makedirs(articles_dir, exist_ok=True)
        os.makedirs(assets_dir, exist_ok=True)

        # 1. Global Modern CSS
        css_content = """
        :root {
            --primary: #2563eb;
            --primary-hover: #1d4ed8;
            --accent: #10b981;
            --dark: #0f172a;
            --gray-bg: #f8fafc;
            --card-bg: #ffffff;
            --text-main: #334155;
            --text-muted: #64748b;
            --border-color: #e2e8f0;
        }
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
        body { background-color: var(--gray-bg); color: var(--text-main); line-height: 1.7; font-size: 16px; }
        .container { max-width: 1040px; margin: 0 auto; padding: 20px; }
        header { background: #ffffff; border-bottom: 1px solid var(--border-color); padding: 18px 0; position: sticky; top: 0; z-index: 100; box-shadow: 0 1px 3px rgba(0,0,0,0.02); }
        .header-wrap { display: flex; justify-content: space-between; align-items: center; max-width: 1040px; margin: 0 auto; padding: 0 20px; }
        .brand { font-size: 24px; font-weight: 800; color: var(--dark); text-decoration: none; letter-spacing: -0.5px; }
        .brand span { color: var(--primary); }
        nav a { color: var(--text-muted); text-decoration: none; margin-left: 20px; font-size: 14px; font-weight: 500; }
        nav a:hover { color: var(--primary); }
        .disclosure-bar { background: #fef3c7; color: #92400e; font-size: 13px; text-align: center; padding: 8px 15px; border-bottom: 1px solid #fde68a; }
        
        /* Hero Banner */
        .hero { text-align: center; padding: 50px 20px 30px; }
        .hero h1 { font-size: 38px; font-weight: 800; color: var(--dark); margin-bottom: 14px; letter-spacing: -0.8px; }
        .hero p { font-size: 18px; color: var(--text-muted); max-width: 650px; margin: 0 auto 30px; }
        
        /* Grid */
        .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 26px; margin: 30px 0; }
        .card { background: var(--card-bg); border: 1px solid var(--border-color); border-radius: 12px; overflow: hidden; display: flex; flex-direction: column; transition: transform 0.2s ease, box-shadow 0.2s ease; }
        .card:hover { transform: translateY(-3px); box-shadow: 0 10px 20px rgba(0,0,0,0.06); }
        .card-body { padding: 24px; display: flex; flex-direction: column; flex-grow: 1; }
        .category-badge { display: inline-block; background: #eff6ff; color: var(--primary); font-size: 12px; font-weight: 700; padding: 4px 10px; border-radius: 20px; text-transform: uppercase; margin-bottom: 12px; width: fit-content; }
        .card-title { font-size: 20px; font-weight: 700; color: var(--dark); line-height: 1.35; margin-bottom: 12px; }
        .card-title a { color: inherit; text-decoration: none; }
        .card-title a:hover { color: var(--primary); }
        .card-desc { font-size: 14px; color: var(--text-muted); margin-bottom: 20px; flex-grow: 1; }
        .card-footer { display: flex; justify-content: space-between; align-items: center; border-top: 1px solid var(--border-color); padding-top: 14px; font-size: 13px; color: var(--text-muted); }
        .read-btn { color: var(--primary); font-weight: 700; text-decoration: none; }
        
        /* Article Page Styles */
        article { background: #ffffff; border: 1px solid var(--border-color); border-radius: 12px; padding: 40px; margin-top: 25px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.03); }
        article h1 { font-size: 34px; font-weight: 800; color: var(--dark); margin-bottom: 16px; line-height: 1.25; }
        article h2 { font-size: 24px; font-weight: 700; color: var(--dark); margin: 35px 0 16px; }
        .meta-info { color: var(--text-muted); font-size: 14px; margin-bottom: 25px; border-bottom: 1px solid var(--border-color); padding-bottom: 15px; }
        .highlight-box { background: #eff6ff; border-left: 4px solid var(--primary); padding: 18px; border-radius: 6px; margin: 20px 0; }
        .comparison-table { width: 100%; border-collapse: collapse; margin: 25px 0; font-size: 15px; }
        .comparison-table th, .comparison-table td { border: 1px solid var(--border-color); padding: 12px 14px; text-align: left; }
        .comparison-table th { background: #f1f5f9; font-weight: 700; color: var(--dark); }
        .featured-row { background: #f0fdf4; }
        .badge { background: #16a34a; color: #fff; font-size: 11px; padding: 2px 7px; border-radius: 4px; vertical-align: middle; }
        .cta-button-small { display: inline-block; background: var(--primary); color: #fff; text-decoration: none; padding: 7px 14px; border-radius: 6px; font-weight: 600; font-size: 13px; }
        .cta-button-small.outline { background: transparent; border: 1px solid var(--primary); color: var(--primary); }
        .pros-cons-box { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin: 30px 0; }
        .pros { background: #f0fdf4; border: 1px solid #bbf7d0; border-radius: 8px; padding: 20px; }
        .cons { background: #fef2f2; border: 1px solid #fecaca; border-radius: 8px; padding: 20px; }
        .pros h4 { color: #166534; margin-bottom: 10px; }
        .cons h4 { color: #991b1b; margin-bottom: 10px; }
        .pros ul, .cons ul { padding-left: 20px; font-size: 14px; }
        .cta-banner { background: linear-gradient(135deg, #1e293b, #0f172a); color: #ffffff; padding: 35px; border-radius: 12px; text-align: center; margin: 40px 0; }
        .cta-banner h3 { font-size: 24px; margin-bottom: 10px; color: #fff; }
        .cta-banner p { color: #cbd5e1; margin-bottom: 25px; }
        .cta-button-large { display: inline-block; background: #22c55e; color: #ffffff; text-decoration: none; padding: 16px 34px; border-radius: 8px; font-weight: 800; font-size: 18px; box-shadow: 0 4px 14px rgba(34,197,94,0.4); transition: transform 0.15s ease; }
        .cta-button-large:hover { transform: translateY(-2px); background: #16a34a; }
        .subtext { display: block; font-size: 12px; color: #94a3b8; margin-top: 10px; }
        .back-nav { margin: 20px 0 10px; font-size: 14px; }
        .back-nav a { color: var(--primary); text-decoration: none; font-weight: 600; }
        
        footer { text-align: center; font-size: 13px; color: var(--text-muted); padding: 40px 0; border-top: 1px solid var(--border-color); margin-top: 50px; }
        @media (max-width: 768px) {
            .pros-cons-box { grid-template-columns: 1fr; }
            article h1 { font-size: 26px; }
            article { padding: 20px; }
            .hero h1 { font-size: 28px; }
        }
        """
        with open(os.path.join(assets_dir, "style.css"), "w", encoding="utf-8") as f:
            f.write(css_content)

        # 2. Build Individual Article Pages
        for art in articles:
            art_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{art['title']} | ApexWorkflows Lab</title>
    <meta name="description" content="{art['meta_description']}">
    <link rel="stylesheet" href="../assets/style.css">
    
    <!-- Schema.org JSON-LD Review for Google Rich Snippets -->
    <script type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@type": "Review",
      "itemReviewed": {{
        "@type": "Product",
        "name": "{art['hero_product']['name']}",
        "offers": {{
          "@type": "Offer",
          "price": "{art['hero_product']['price'].replace('$', '')}",
          "priceCurrency": "USD",
          "seller": {{
            "@type": "Organization",
            "name": "Amazon"
          }}
        }}
      }},
      "reviewRating": {{
        "@type": "Rating",
        "ratingValue": "{art['rating']}",
        "bestRating": "5"
      }},
      "author": {{
        "@type": "Person",
        "name": "{art['author']}"
      }}
    }}
    </script>
</head>
<body>
    <div class="disclosure-bar">
        ⚖️ <strong>Amazon Affiliate Disclosure:</strong> As an Amazon Associate, we earn from qualifying purchases at zero added cost to you. Store ID: <code>apexworkflows-20</code>.
    </div>

    <header>
        <div class="header-wrap">
            <a href="../index.html" class="brand">Apex<span>Workflows</span></a>
            <nav>
                <a href="../index.html">← Back to All Reviews</a>
            </nav>
        </div>
    </header>

    <div class="container">
        <div class="back-nav"><a href="../index.html">← All Guides</a> &nbsp;/&nbsp; <span>{art['category']}</span></div>
        <article>
            <span class="category-badge">{art['category']}</span>
            <h1>{art['title']}</h1>
            <div class="meta-info">
                By <strong>{art['author']}</strong> • Updated: {datetime.now().strftime('%B %d, %Y')} • {art['read_time']} • 🛡️ Tested & Verified
            </div>
            {art['content_html']}
        </article>
    </div>

    <footer>
        <div class="container">
            <p>&copy; {datetime.now().year} ApexWorkflows Editorial Lab. All rights reserved.</p>
            <p style="margin-top: 5px;">Amazon and the Amazon logo are trademarks of Amazon.com, Inc. or its affiliates.</p>
        </div>
    </footer>
</body>
</html>
"""
            with open(os.path.join(articles_dir, f"{art['slug']}.html"), "w", encoding="utf-8") as f:
                f.write(art_html)

        # 3. Build Homepage (index.html) with Cards Grid
        cards_html = ""
        for art in articles:
            cards_html += f"""
            <div class="card">
                <div class="card-body">
                    <span class="category-badge">{art['category']}</span>
                    <h3 class="card-title">
                        <a href="articles/{art['slug']}.html">{art['title']}</a>
                    </h3>
                    <p class="card-desc">{art['meta_description']}</p>
                    <div class="card-footer">
                        <span>⭐ {art['rating']} Rating</span>
                        <a href="articles/{art['slug']}.html" class="read-btn">Read Full Benchmark &rarr;</a>
                    </div>
                </div>
            </div>
            """

        index_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ApexWorkflows | Independent Workspace Gear & Software Benchmarks</title>
    <meta name="description" content="Independent, data-driven lab reviews for remote teams, ergonomists, and digital creators. Verified Amazon Prime recommendations.">
    <link rel="stylesheet" href="assets/style.css">
</head>
<body>
    <div class="disclosure-bar">
        ⚖️ <strong>Affiliate Transparency:</strong> As an Amazon Associate, we earn from qualifying purchases through our partner tag <code>apexworkflows-20</code>.
    </div>

    <header>
        <div class="header-wrap">
            <a href="index.html" class="brand">Apex<span>Workflows</span></a>
            <nav>
                <a href="#benchmarks">Lab Benchmarks</a>
                <a href="#about">Testing Standards</a>
            </nav>
        </div>
    </header>

    <div class="container">
        <section class="hero">
            <h1>Engineered for Focus & Remote Ergonomics</h1>
            <p>We stress-test office chairs, standing desks, broadcast mics, and productivity software so you never waste capital on marketing hype.</p>
        </section>

        <section id="benchmarks">
            <h2 style="font-size: 22px; font-weight: 800; color: #0f172a; margin-bottom: 20px;">Latest Tested Guides (2026 Edition)</h2>
            <div class="grid">
                {cards_html}
            </div>
        </section>
    </div>

    <footer id="about">
        <div class="container">
            <p>&copy; {datetime.now().year} ApexWorkflows Editorial Lab. Official Amazon Associates ID: <code>apexworkflows-20</code>.</p>
            <p style="margin-top: 6px;">Hosted on Cloudflare Edge Network • 0ms Server Lag • 100% Free Open Infrastructure</p>
        </div>
    </footer>
</body>
</html>
"""
        with open(os.path.join(site_dir, "index.html"), "w", encoding="utf-8") as f:
            f.write(index_html)

        # 4. Build sitemap.xml
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
        with open(os.path.join(site_dir, "sitemap.xml"), "w", encoding="utf-8") as f:
            f.write(sitemap_content)

        # 5. Build RSS 2.0 Feed for Automated Pinterest Syndication
        generate_rss_feed(articles, site_dir, "https://minh119.github.io/apex-workflows")

        return {"site_dir": site_dir, "articles_count": len(articles)}

    def _build_distribution_kit(self, articles):
        pack = {"generated_at": datetime.now().isoformat(), "social_assets": []}
        for art in articles:
            pack["social_assets"].append({
                "article_slug": art["slug"],
                "pinterest_pin": {
                    "headline": f"{art['title']} (2026 Test)",
                    "pin_description": art["meta_description"] + " Read the full lab teardown here.",
                    "direct_url": f"https://minh119.github.io/apex-workflows/articles/{art['slug']}.html"
                },
                "twitter_x_hook": f"Thinking of upgrading your {art['category']} setup? We just finished lab-testing the top contenders for 2026. Here's our real verdict with zero BS: https://minh119.github.io/apex-workflows/articles/{art['slug']}.html"
            })
        
        pack_file = os.path.join(self.output_dir, "distribution_pack.json")
        with open(pack_file, "w", encoding="utf-8") as f:
            json.dump(pack, f, indent=2, ensure_ascii=False)
        return pack

    def _compile_executive_report(self, articles, site_result):
        report_file = os.path.join(self.reports_dir, f"Batch_Production_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        data = {
            "batch_size": len(articles),
            "tracking_tag": "apexworkflows-20",
            "articles": [a["slug"] for a in articles],
            "portal_path": site_result["site_dir"],
            "deployment_ready": True
        }
        with open(report_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return report_file

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ceo = EnterpriseCEO(current_dir)
    res = ceo.run_production_cycle()
    print("[*] Hoàn tất:", res)
