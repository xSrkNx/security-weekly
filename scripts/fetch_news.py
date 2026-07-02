import feedparser
import html
import socket

from pathlib import Path
from datetime import datetime, UTC
from email.utils import parsedate_to_datetime

from feeds import feeds

# ==========================================================
# CONFIGURATION
# ==========================================================

REPORT_TITLE = "Serkan TUNALI Executive Intelligence Report"

MAX_ARTICLES_PER_SOURCE = 5
MAX_TOP_STORIES = 10

REQUEST_TIMEOUT = 20

socket.setdefaulttimeout(REQUEST_TIMEOUT)

# ==========================================================
# GLOBALS
# ==========================================================

seen_links = set()

summary = {}

top_stories = []

feed_health = []

report_sections = []

# ==========================================================
# HELPER FUNCTIONS
# ==========================================================

def clean(text):

    if not text:
        return ""

    return html.unescape(text).replace("\n", " ").strip()


def get_date(entry):

    try:

        if getattr(entry, "published_parsed", None):

            return parsedate_to_datetime(entry.published)

    except Exception:

        pass

    return datetime.now(UTC)


def make_article(entry):

    article = ""

    article += f"### {clean(getattr(entry,'title','No title'))}\n"

    if hasattr(entry, "published"):

        article += f"Published: {entry.published}\n"

    article += f"[Read Article]({entry.link})\n\n"

    return article


def feed_status(feed):

    """
    Returns:
        icon
        message
    """

    status = getattr(feed, "status", "Unknown")

    if getattr(feed, "bozo", False):

        return (
            "⚠️",
            f"HTTP {status} ({feed.bozo_exception})"
        )

    if len(feed.entries) == 0:

        return (
            "⚠️",
            f"HTTP {status} (Empty Feed)"
        )

    return (
        "✅",
        f"HTTP {status}"
    )


def add_top_story(category, source, entry):

    top_stories.append(

        {

            "category": category,

            "source": source,

            "title": clean(getattr(entry, "title", "")),

            "link": getattr(entry, "link", ""),

            "date": get_date(entry)

        }

    )

# ==========================================================
# REPORT HEADER
# ==========================================================

content = f"""# {REPORT_TITLE}

Generated:
{datetime.now(UTC).strftime('%Y-%m-%d %H:%M UTC')}

---

## Executive Snapshot

This report provides a curated executive overview of:

- Artificial Intelligence
- Cyber Security
- Physical Security
- Intelligent Transportation Systems
- Smart Mobility

Sources are automatically collected from trusted industry
vendors, standards organizations and technology leaders.

---

"""

# ==========================================================
# RSS COLLECTION
# ==========================================================

for category, sources in feeds.items():

    section = f"""

==================================================

# {category}

==================================================

"""

    category_total = 0

    for source_name, url in sources.items():

        print(f"Reading {source_name}...")

        try:

            feed = feedparser.parse(url)

        except Exception as ex:

            print(f"❌ {source_name}: {ex}")

            feed_health.append({
                "source": source_name,
                "icon": "❌",
                "message": str(ex)
            })

            section += f"## {source_name}\n\n"

            section += "Unable to read RSS feed.\n\n"

            continue

        # ----------------------------------------
        # Feed Health
        # ----------------------------------------

        icon, message = feed_status(feed)

        feed_health.append({

            "source": source_name,

            "icon": icon,

            "message": message

        })

        print(f"{icon} {source_name} -> {message}")

        section += f"## {source_name}\n\n"

        if len(feed.entries) == 0:

            section += "⚠ No articles found.\n\n"

            continue

        added = 0

        for entry in feed.entries:

            title = clean(getattr(entry, "title", ""))

            link = getattr(entry, "link", "")

            if not title or not link:

                continue

            uid = f"{title}|{link}"

            if uid in seen_links:

                continue

            seen_links.add(uid)

            section += make_article(entry)

            add_top_story(

                category,

                source_name,

                entry

            )

            category_total += 1

            added += 1

            if added >= MAX_ARTICLES_PER_SOURCE:

                break

    summary[category] = category_total

    report_sections.append(section)

# ==========================================================
# SORT TOP STORIES
# ==========================================================

top_stories.sort(

    key=lambda x: x["date"],

    reverse=True

)

top_stories = top_stories[:MAX_TOP_STORIES]

# ==========================================================
# BUILD REPORT
# ==========================================================

for section in report_sections:

    content += section

# ==========================================================
# TOP STORIES
# ==========================================================

content += """

--------------------------------------------------

# Top Stories This Week

--------------------------------------------------

"""

for article in top_stories:

    content += f"### {article['title']}\n"

    content += f"Category : {article['category']}\n"

    content += f"Source   : {article['source']}\n"

    content += f"[Read Article]({article['link']})\n\n"

# ==========================================================
# EXECUTIVE SUMMARY
# ==========================================================

content += """

--------------------------------------------------

# Executive Summary

--------------------------------------------------

"""

total_articles = sum(summary.values())

for category, count in summary.items():

    content += f"- **{category}** : {count} curated headlines\n"

content += f"""

Total Headlines : {total_articles}

Generated : {datetime.now(UTC).strftime('%Y-%m-%d %H:%M UTC')}

"""

# ==========================================================
# FEED HEALTH
# ==========================================================

content += """

--------------------------------------------------

# Feed Health

--------------------------------------------------

"""

healthy = 0
warning = 0
error = 0

for feed in feed_health:

    icon = feed["icon"]

    if icon == "✅":
        healthy += 1

    elif icon == "⚠️":
        warning += 1

    else:
        error += 1

    content += f"{feed['source']:<30} {icon} {feed['message']}\n"

total_feeds = len(feed_health)

score = 0

if total_feeds:

    score = round((healthy / total_feeds) * 100)

content += f"""

Healthy Feeds     : {healthy}

Warnings          : {warning}

Errors            : {error}

Feed Reliability  : {score}%

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

Categories           : {len(feeds)}

Sources Configured   : {sum(len(v) for v in feeds.values())}

Unique Headlines     : {len(seen_links)}

Top Stories          : {len(top_stories)}

Generated            : {datetime.now(UTC).strftime('%Y-%m-%d %H:%M UTC')}

"""

# ==========================================================
# FOOTER
# ==========================================================

content += """

--------------------------------------------------

Prepared by

Serkan TUNALI Executive Intelligence Portal

https://intelligence.serkantunali.com

Automatically generated from trusted AI,
Cyber Security, Physical Security,
Smart Mobility and ITS industry sources.

© Serkan TUNALI

"""

# ==========================================================
# WRITE REPORT
# ==========================================================

Path("weekly_report.md").write_text(

    content,

    encoding="utf-8"

)

# ==========================================================
# CONSOLE OUTPUT
# ==========================================================

print()

print("===============================================")
print(" Executive Intelligence Report Generated")
print("===============================================")

print()

print(f"Categories        : {len(summary)}")

print(f"Sources           : {sum(len(v) for v in feeds.values())}")

print(f"Unique Headlines  : {len(seen_links)}")

print(f"Top Stories       : {len(top_stories)}")

print(f"Healthy Feeds     : {healthy}")

print(f"Feed Reliability  : {score}%")

print()

for category, count in summary.items():

    print(f"{category:<28} {count}")

print()

print("weekly_report.md created successfully.")
