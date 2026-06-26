from pathlib import Path
import re

reports_dir = Path("reports")

reports = sorted(
    reports_dir.glob("*.md"),
    reverse=True
)

latest = reports[0] if reports else None

cards = ""

for report in reports:

    report_name = report.stem

    cards += f"""
    <a class="report-card" href="reports/{report.name}">
        <h3>{report_name}</h3>
        <p>Executive Intelligence Report</p>
        <span>Read Report →</span>
    </a>
    """

latest_button = ""

if latest:

    latest_button = f"""
    <a class="hero-button"
       href="reports/{latest.name}">
       Read Latest Report →
    </a>
    """

html = f"""
<!DOCTYPE html>

<html>

<head>

<meta charset="utf-8">

<meta name="viewport"
content="width=device-width,initial-scale=1">

<title>

Serkan TUNALI Intelligence Portal

</title>

<link rel="stylesheet"
href="style.css">

</head>

<body>

<header>

<div>

<h1>Serkan TUNALI</h1>

<p>

Executive Intelligence Portal

</p>

</div>

<nav>

<a href="./">Home</a>

<a href="#reports">Reports</a>

<a href="https://www.serkantunali.com">
Website
</a>

<a href="https://www.linkedin.com/in/serkantunali/">
LinkedIn
</a>

</nav>

</header>

<section class="hero">

<h2>

Weekly Executive Intelligence

</h2>

<p>

Artificial Intelligence • Cyber Security • Physical Security • ITS

</p>

{latest_button}

</section>

<section class="dashboard">

<div class="dashboard-card">
<h3>🤖 AI</h3>
<p>Enterprise AI<br>LLMs<br>Agents</p>
</div>

<div class="dashboard-card">
<h3>🔐 Cyber</h3>
<p>Threats<br>CVEs<br>Zero Trust</p>
</div>

<div class="dashboard-card">
<h3>📹 Physical</h3>
<p>Video<br>ONVIF<br>Access Control</p>
</div>

<div class="dashboard-card">
<h3>🚗 ITS</h3>
<p>Mobility<br>Smart Cities<br>V2X</p>
</div>

</section>

<section class="about">

<h2>

About

</h2>

<p>

This portal automatically publishes curated weekly
executive intelligence reports focused on emerging
technologies and enterprise security.

</p>

</section>

<section id="reports">

<h2>

Reports Archive

</h2>

<div class="report-grid">

{cards}

</div>

</section>

<footer>

© Serkan TUNALI

</footer>

</body>

</html>
"""

Path("index.html").write_text(
    html,
    encoding="utf-8"
)

print("Portal generated")
