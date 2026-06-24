from pathlib import Path

reports_dir = Path("reports")

reports = []

if reports_dir.exists():
    reports = sorted(
        [f.name for f in reports_dir.glob("*.md")],
        reverse=True
    )

latest = reports[0] if reports else None

archive_html = ""

for report in reports:
    archive_html += f'<li><a href="reports/{report}">{report.replace(".md","")}</a></li>\n'

latest_html = ""

if latest:
    latest_html = f"""
    <div class="card">
        <h2>Latest Report</h2>
        <a href="reports/{latest}">
            {latest.replace(".md","")}
        </a>
    </div>
    """

html = f"""
<!DOCTYPE html>
<html>

<head>

<meta charset="utf-8">

<title>Serkan TUNALI | Weekly Intelligence</title>

<link rel="stylesheet" href="style.css">

</head>

<body>

<header>

<h1>Serkan TUNALI</h1>

<p class="subtitle">
Technology • AI • Security • ITS
</p>

<nav>
<a href="./">Home</a> |
<a href="#reports">Weekly Intelligence</a> |
<a href="https://www.serkantunali.com">Website</a> |
<a href="https://www.linkedin.com/in/serkantunali/">LinkedIn</a>
</nav>

</header>

<div class="card">

<h2>About</h2>

<p>

Serkan TUNALI is a senior technology executive with more than 25 years of experience in Physical Security, Intelligent Transportation Systems (ITS), Smart Cities, AI-enabled solutions and enterprise technologies.

This portal provides weekly intelligence reports covering Artificial Intelligence, Cybersecurity, Physical Security, Video Surveillance, Smart Mobility and Emerging Technologies.

</p>

</div>

{latest_html}

<div class="card" id="reports">

<h2>Reports Archive</h2>

<ul>

{archive_html}

</ul>

</div>

<footer>

© Serkan TUNALI

</footer>

</body>

</html>
"""

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Index generated")
