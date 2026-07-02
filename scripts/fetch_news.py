"""
==========================================================
Executive Intelligence Portal
V10 Phoenix

fetch_news.py

Main Report Generator

Responsibilities

- Load configured sources
- Run Source Engine
- Build Markdown report
- Save weekly_report.md
==========================================================
"""

from pathlib import Path
from datetime import datetime, UTC

from config import (
    REPORT_TITLE,
    OUTPUT_REPORT,
    MAX_TOP_STORIES
)

from feeds import feeds

from source_engine import SourceEngine

from intelligence import IntelligenceEngine

intel = IntelligenceEngine(articles)

intel.analyze()

content += intel.markdown()
# ==========================================================
# INITIALIZE ENGINE
# ==========================================================

engine = SourceEngine()

summary = engine.collect(feeds)

articles = engine.all_articles()

top_stories = engine.top_stories(MAX_TOP_STORIES)

feed_health = engine.health()

feed_stats = engine.feed_statistics()

vendor_stats = engine.vendor_statistics()

category_stats = engine.category_statistics()

# ==========================================================
# REPORT HEADER
# ==========================================================

content = f"""# {REPORT_TITLE}

Generated:
{datetime.now(UTC).strftime('%Y-%m-%d %H:%M UTC')}

---

## Executive Snapshot

This report is automatically generated from trusted
industry sources covering:

- Artificial Intelligence
- Cyber Security
- Physical Security
- Smart Mobility
- Intelligent Transportation Systems

The objective is to provide executive-level awareness
of important technology developments across strategic
domains.

---

"""

# ==========================================================
# EXECUTIVE INSIGHT
# ==========================================================

content += f"""

# Executive Insight

This edition includes **{len(articles)} curated articles**
from **{engine.source_count()} trusted sources**
covering **{engine.categories()} strategic domains**.

Feed Reliability Score:
**{feed_stats["reliability"]}%**

The most active technology vendors and organizations
are highlighted in this report together with the
latest industry announcements.

---

"""

# ==========================================================
# CATEGORY SECTIONS
# ==========================================================

for category in feeds.keys():

    content += f"""

==================================================

# {category}

==================================================

"""

    for article in articles:

        if article.category != category:

            continue

        content += f"### {article.title}\n"

        if article.published:

            content += (
                f"Published: "
                f"{article.published.strftime('%Y-%m-%d')}\n"
            )

        content += f"[Read Article]({article.link})\n\n"

# ==========================================================
# TOP STORIES
# ==========================================================

content += """

--------------------------------------------------

# Top Stories This Week

--------------------------------------------------

"""

for article in top_stories:

    content += f"### {article.title}\n"

    content += f"Category : {article.category}\n"

    content += f"Source   : {article.source}\n"

    content += f"[Read Article]({article.link})\n\n"

# ==========================================================
# VENDOR ACTIVITY
# ==========================================================

content += """

--------------------------------------------------

# Vendor Activity

--------------------------------------------------

"""

for vendor, count in vendor_stats.items():

    bar = "█" * min(count, 10)

    content += f"{vendor:<30} {bar} ({count})\n"

content += "\n"

# ==========================================================
# CATEGORY SUMMARY
# ==========================================================

content += """

--------------------------------------------------

# Category Summary

--------------------------------------------------

"""

for category, count in category_stats.items():

    content += f"- **{category}** : {count} articles\n"

content += "\n"

# ==========================================================
# REPORT HIGHLIGHTS
# ==========================================================

content += """

--------------------------------------------------

# Executive Highlights

--------------------------------------------------

"""

highest_vendor = next(iter(vendor_stats.items()), ("N/A", 0))

content += (
    f"- Most active vendor: "
    f"**{highest_vendor[0]}** "
    f"({highest_vendor[1]} articles)\n"
)

content += (
    f"- Total curated articles: "
    f"**{len(articles)}**\n"
)

content += (
    f"- Active sources: "
    f"**{engine.source_count()}**\n"
)

content += (
    f"- Feed Reliability Score: "
    f"**{feed_stats['reliability']}%**\n"
)

content += (
    f"- Strategic domains covered: "
    f"**{engine.categories()}**\n\n"
)

# ==========================================================
# TRENDING SOURCES
# ==========================================================

content += """

--------------------------------------------------

# Top Sources

--------------------------------------------------

"""

for vendor, count in list(vendor_stats.items())[:10]:

    content += f"- {vendor} ({count})\n"

content += "\n"

# ==========================================================
# FEED HEALTH
# ==========================================================

content += """

--------------------------------------------------

# Feed Health

--------------------------------------------------

"""

for health in feed_health:

    icon = {
        "OK": "✅",
        "WARNING": "⚠️",
        "ERROR": "❌"
    }.get(health.status, "•")

    content += (
        f"{health.source:<30} "
        f"{icon} {health.message}\n"
    )

content += f"""

Healthy Feeds     : {feed_stats['healthy']}

Warnings          : {feed_stats['warning']}

Errors            : {feed_stats['error']}

Feed Reliability  : {feed_stats['reliability']}%

"""

# ==========================================================
# REPORT STATISTICS
# ==========================================================

content += """

--------------------------------------------------

# Report Statistics

--------------------------------------------------

"""

content += f"""

Categories           : {engine.categories()}

Sources Configured   : {sum(len(v) for v in feeds.values())}

Healthy Sources      : {feed_stats['healthy']}

Unique Articles      : {engine.article_count()}

Top Stories          : {len(top_stories)}

Generated            : {datetime.now(UTC).strftime('%Y-%m-%d %H:%M UTC')}

"""

# ==========================================================
# FOOTER
# ==========================================================

content += """

--------------------------------------------------

Prepared by

Serkan TUNALI

Executive Intelligence Portal

https://intelligence.serkantunali.com

This report is automatically generated from trusted
industry sources covering Artificial Intelligence,
Cyber Security,
Physical Security,
Smart Mobility and
Intelligent Transportation Systems.

© Serkan TUNALI

"""

# ==========================================================
# WRITE REPORT
# ==========================================================

Path(OUTPUT_REPORT).write_text(

    content,

    encoding="utf-8"

)

# ==========================================================
# CONSOLE OUTPUT
# ==========================================================

print()

print("===================================================")
print(" Executive Intelligence Portal V10 Phoenix")
print("===================================================")

print()

print(f"Articles            : {engine.article_count()}")

print(f"Sources             : {engine.source_count()}")

print(f"Categories          : {engine.categories()}")

print(f"Healthy Feeds       : {feed_stats['healthy']}")

print(f"Warnings            : {feed_stats['warning']}")

print(f"Errors              : {feed_stats['error']}")

print(f"Feed Reliability    : {feed_stats['reliability']} %")

print()

print("Top Sources")

print("------------------------------------------")

for source, count in list(vendor_stats.items())[:10]:

    print(f"{source:<30} {count}")

print()

print(f"Report saved to {OUTPUT_REPORT}")

print()
