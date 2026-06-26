from pathlib import Path

reports_dir = Path("reports")

reports = sorted(
    reports_dir.glob("*.md"),
    reverse=True
) if reports_dir.exists() else []

report_count = len(reports)
latest = reports[0].name if reports else ""

# Şimdilik sabit. İleride fetch_news.py bunları otomatik üretecek.
sources = 9
categories = 4

cards = ""

for report in reports:

    date = report.stem

    cards += f"""
    <div class="report-card">

        <h3>{date}</h3>

        <p>
        Executive Intelligence Report
        </p>

        <a class="button"
        href="reports/{report.name}">
        Read Report →
        </a>

    </div>
    """

hero = ""

if latest:

    hero = f"""
<section class="hero">

<h2>Executive Intelligence Briefing</h2>

<p>

Weekly curated intelligence covering Artificial Intelligence,
Cyber Security, Physical Security,
Smart Cities and Intelligent Transportation Systems.

</p>

<a class="hero-button"
href="reports/{latest}">

Read Latest Report

</a>

</section>
"""

html = f"""
<!DOCTYPE html>

<html>

<head>

<meta charset="utf-8">

<meta name="viewport"
content="width=device-width, initial-scale=1">

<title>

Serkan TUNALI | Executive Intelligence Portal

</title>

<link rel="stylesheet" href="style.css">

</head>

<body>

<header>

<h1>Serkan TUNALI</h1>

<p class="subtitle">

Technology • AI • Security • ITS

</p>

<nav>

<a href="./">Home</a>

<a href="#reports">Reports</a>

<a href="#radar">Technology Radar</a>

<a href="https://www.serkantunali.com">

Website

</a>

<a href="https://www.linkedin.com/in/serkantunali/">

LinkedIn

</a>

</nav>

</header>

{hero}

<section class="about">

<div class="card">

<h2>About</h2>

<p>

Executive leader with more than 25 years of experience in
Physical Security, AI, Intelligent Transportation Systems,
Critical Infrastructure, Smart Cities and Enterprise Technology.

</p>

</div>

</section>

<section>

<div class="dashboard">

<div class="dashboard-card">

<h3>Reports</h3>

<span>{report_count}</span>

</div>

<div class="dashboard-card">

<h3>Sources</h3>

<span>{sources}</span>

</div>

<div class="dashboard-card">

<h3>Categories</h3>

<span>{categories}</span>

</div>

<div class="dashboard-card">

<h3>Latest</h3>

<span>{latest.replace(".md","") if latest else "-"}</span>

</div>

</div>

</section>

<section id="radar">

<h2>Technology Radar</h2>

<div class="radar-grid">

<div class="radar-card">

<h3>🤖 AI & GenAI</h3>

<p>

Enterprise AI<br>
LLMs<br>
AI Agents

</p>

</div>

<div class="radar-card">

<h3>🔐 Cyber Security</h3>

<p>

Threat Intelligence<br>
CVE<br>
Cloud Security

</p>

</div>

<div class="radar-card">

<h3>📹 Physical Security</h3>

<p>

Video Analytics<br>
Access Control<br>
ONVIF

</p>

</div>

<div class="radar-card">

<h3>🚗 ITS & Mobility</h3>

<p>

Traffic Systems<br>
Smart Cities<br>
Connected Mobility

</p>

</div>

</div>

</section>

<section id="reports">

<h2>Reports Archive</h2>

<div class="report-grid">

{cards}

</div>

</section>

<footer>

<p>

© 2026 Serkan TUNALI

</p>

<p>

Executive Intelligence Portal

</p>

</footer>

</body>

</html>

"""

with open("index.html","w",encoding="utf-8") as f:
    f.write(html)

print("Portal generated successfully")
