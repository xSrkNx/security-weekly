from pathlib import Path
from datetime import datetime, UTC

REPORTS_DIR = Path("reports")
OUTPUT_FILE = Path("index.html")

reports = []

if REPORTS_DIR.exists():
    reports = sorted(REPORTS_DIR.glob("*.md"), reverse=True)

latest = reports[0].name if reports else None

# ---------------------------------------------------
# Statistics
# ---------------------------------------------------

report_count = len(reports)

today = datetime.now(UTC).strftime("%Y-%m-%d")

sources = 10
domains = 4

# ---------------------------------------------------
# Latest Report Card
# ---------------------------------------------------

latest_html = ""

if latest:

    latest_date = latest.replace(".md", "")

    latest_html = f"""
<section class="latest-section">

<div class="section-title">
Latest Intelligence
</div>

<div class="latest-card">

<h2>{latest_date}</h2>

<p>

Automatically generated executive intelligence briefing
covering AI, Cyber Security, Physical Security,
ITS and Smart Mobility.

</p>

<a class="primary-button"
href="reports/{latest}">
Read Report
</a>

</div>

</section>
"""

# ---------------------------------------------------
# Report Cards
# ---------------------------------------------------

cards = ""

for report in reports:

    date = report.name.replace(".md", "")

    cards += f"""
<div class="report-card">

<div class="report-date">

📅 {date}

</div>

<h3>Executive Intelligence Report</h3>

<p>

Weekly curated intelligence for technology leaders.

</p>

<a class="secondary-button"
href="reports/{report.name}">
Open Report
</a>

</div>
"""

# ---------------------------------------------------
# HTML
# ---------------------------------------------------

html = f"""
<!DOCTYPE html>

<html lang="en">

<head>

<meta charset="UTF-8">

<meta
name="viewport"
content="width=device-width, initial-scale=1">

<title>

Serkan TUNALI | Executive Intelligence Portal

</title>

<link rel="stylesheet" href="style.css">

<link rel="icon" href="assets/favicon.svg">

</head>

<body>

<header>

<div class="container header-flex">

<div>

<h1>

Serkan TUNALI

</h1>

<p class="subtitle">

Executive Intelligence Portal

</p>

</div>

<nav>

<a href="#">Home</a>

<a href="#latest">Latest</a>

<a href="#radar">Radar</a>

<a href="#archive">Reports</a>

<a href="https://www.serkantunali.com">

Website

</a>

<a href="https://www.linkedin.com/in/serkantunali/">

LinkedIn

</a>

</nav>

</div>

</header>

<!-- HERO -->

<section class="hero">

<div class="container">

<h2>

Trusted Weekly Executive Intelligence

</h2>

<p>

Curated weekly intelligence across Artificial Intelligence,
Cyber Security,
Physical Security,
Video Surveillance,
Smart Cities and Intelligent Transportation Systems.

</p>

<a class="primary-button"
href="#latest">

Latest Report

</a>

</div>

</section>

<!-- DASHBOARD -->

<section class="dashboard">

<div class="container dashboard-grid">

<div class="stat-card">

<h2>{report_count}</h2>

<p>Reports</p>

</div>

<div class="stat-card">

<h2>{sources}</h2>

<p>Sources</p>

</div>

<div class="stat-card">

<h2>{domains}</h2>

<p>Domains</p>

</div>

<div class="stat-card">

<h2>{today}</h2>

<p>Updated</p>

</div>

</div>

</section>

<!-- ABOUT -->

<section class="about">

<div class="container">

<h2>

About

</h2>

<p>

Serkan TUNALI is a senior technology executive with more
than 25 years of experience in Intelligent Transportation
Systems, Smart Cities, AI, Physical Security,
Enterprise Technologies and Digital Transformation.

</p>

</div>

</section>

<!-- RADAR -->

<section
class="radar"
id="radar">

<div class="container">

<h2>

Technology Radar

</h2>

<div class="radar-grid">

<div class="radar-box">

🤖

<h3>AI & GenAI</h3>

</div>

<div class="radar-box">

🔐

<h3>Cyber Security</h3>

</div>

<div class="radar-box">

📹

<h3>Physical Security</h3>

</div>

<div class="radar-box">

🚗

<h3>ITS & Smart Mobility</h3>

</div>

</div>

</div>

</section>

<a id="latest"></a>

{latest_html}

<section
class="archive"
id="archive">

<div class="container">

<h2>

Report Archive

</h2>

<div class="report-grid">

{cards}

</div>

</div>

</section>

<footer>

<div class="container">

<p>

© {datetime.utcnow().year}
Serkan TUNALI

</p>

<p>

Executive Intelligence Portal

</p>

</div>

</footer>

</body>

</html>
"""

OUTPUT_FILE.write_text(html, encoding="utf-8")

print("V7 Portal generated successfully.")
