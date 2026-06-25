from pathlib import Path

reports_dir = Path("reports")

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
        Executive Intelligence Report
        </p>

        <a class="button"
           href="reports/{report}">
           Open Report
        </a>

    </div>
    """

latest_html = ""

if latest:

    latest_html = f"""
    <section class="hero">

        <h2>Latest Intelligence Briefing</h2>

        <p>
        Weekly insights covering AI,
        Cyber Security, Physical Security,
        Smart Cities and ITS.
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
<meta name="viewport" content="width=device-width, initial-scale=1">

<title>
Serkan TUNALI Intelligence Portal
</title>

<link rel="stylesheet" href="style.css">

</head>

<body>

<header>

<h1>Serkan TUNALI</h1>

<p class="subtitle">
Executive Intelligence Portal
</p>

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

{latest_html}

<section class="about">

<h2>About</h2>

<p>
Senior technology executive with 25+ years of experience
across Physical Security, ITS, Smart Cities,
Artificial Intelligence and Enterprise Technologies.
</p>

</section>

<section class="radar">

<div class="radar-card">
<h3>🤖 AI & GenAI</h3>
</div>

<div class="radar-card">
<h3>🔐 Cyber Security</h3>
</div>

<div class="radar-card">
<h3>📹 Physical Security</h3>
</div>

<div class="radar-card">
<h3>🚗 ITS & Smart Mobility</h3>
</div>

</section>

<section id="reports">

<h2>Reports Archive</h2>

<div class="report-grid">

{cards_html}

</div>

</section>

<footer>

© Serkan TUNALI

</footer>

</body>

</html>
"""

with open("index.html","w",encoding="utf-8") as f:
    f.write(html)

print("Portal generated")
