from pathlib import Path
import re

reports_dir = Path("reports")

reports = []

if reports_dir.exists():
    reports = sorted(
        [f.name for f in reports_dir.glob("*.md")],
        reverse=True
    )

latest = reports[0] if reports else None

cards_html = ""

for report in reports:

    report_date = report.replace(".md", "")

    cards_html += f"""
    <div class="report-card">
        <h3>{report_date}</h3>

        <p>
            Weekly Intelligence Report
        </p>

        <a class="button"
           href="reports/{report}">
           Open Report
        </a>

    </div>
    """

latest_banner = ""

if latest:
    latest_banner = f"""
    <section class="hero">

        <h2>Latest Intelligence Report</h2>

        <p>
            Latest automatically generated security,
            AI and technology intelligence briefing.
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
Serkan TUNALI | Intelligence Portal
</title>

<link rel="stylesheet" href="style.css">

</head>

<body>

<header>

<div class="logo-area">

<h1>Serkan TUNALI</h1>

<p class="subtitle">
Technology • AI • Security • ITS
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

{latest_banner}

<section class="about">

<h2>About</h2>

radar_section = """
<section class="radar">

<div class="radar-card">
<h3>AI Radar</h3>
<p>Generative AI, LLMs, Agents and Enterprise AI</p>
</div>

<div class="radar-card">
<h3>Cyber Security</h3>
<p>Threats, Vulnerabilities and Security Trends</p>
</div>

<div class="radar-card">
<h3>Physical Security</h3>
<p>Video Surveillance, Access Control and ONVIF</p>
</div>

<div class="radar-card">
<h3>ITS & Mobility</h3>
<p>Smart Cities, C-ITS and Transportation</p>
</div>

</section>
"""

<p>
Executive leader with 25+ years of experience in
Physical Security, Intelligent Transportation Systems,
Smart Cities, AI-enabled solutions and enterprise technologies.
</p>

<p>
This portal automatically publishes weekly intelligence reports
covering Cybersecurity, Artificial Intelligence,
Physical Security and Technology trends.
</p>

</section>

<section id="reports">

<h2>Reports Archive</h2>

<div class="report-grid">

{cards_html}

</div>

</section>

<footer>

<p>
© Serkan TUNALI
</p>

<p>
Weekly Intelligence Portal
</p>

</footer>

</body>

</html>
"""

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Professional portal generated")
