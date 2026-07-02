import feedparser
import html
import socket

from pathlib import Path
from datetime import datetime
from email.utils import parsedate_to_datetime

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

feed_status = {}

report_sections = []

# ==========================================================
# RSS SOURCES
# ==========================================================

from feeds import feeds

# ==========================================================
# HELPER FUNCTIONS
# ==========================================================

def clean(text):

    if not text:
        return ""

    return html.unescape(text).replace("\n", " ").strip()


def get_date(entry):

    try:

        if hasattr(entry, "published_parsed") and entry.published_parsed:
            return parsedate_to_datetime(entry.published)

    except Exception:
        pass

    return datetime.utcnow()


def make_article(entry):

    article = ""

    article += f"### {clean(entry.title)}\n"

    if hasattr(entry, "published"):
        article += f"Published: {entry.published}\n"

    article += f"[Read Article]({entry.link})\n\n"

    return article


# ==========================================================
# REPORT HEADER
# ==========================================================

content = f"""# {REPORT_TITLE}

Generated:
{datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}

---

## Executive Snapshot

This report provides a curated executive overview
of the latest developments across:

- Artificial Intelligence
- Cyber Security
- Physical Security
- Intelligent Transportation Systems
- Smart Mobility

Only trusted industry sources are included.

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

        # -----------------------------
        # Feed diagnostics
        # -----------------------------

        status = getattr(feed, "status", "Unknown")

        print(f"{source_name:<30} HTTP: {status}")

        if feed.bozo:

        print(f"⚠ Parsing warning: {feed.bozo_exception}")

    except Exception as ex:

        content += f"## {source_name}\n\n"

        content += "Unable to read RSS feed.\n\n"

        content += f"{ex}\n\n"

        print(f"❌ {source_name}: {ex}")

        continue


        if getattr(feed, "bozo", False):

            feed_status[source_name] = "WARNING"

        else:

            feed_status[source_name] = "OK"


        section += f"## {source_name}\n\n"


        if len(feed.entries) == 0:

            section += "⚠ No articles found.\n\n"

            continue


        added = 0

        for entry in feed.entries:

            link = getattr(entry, "link", "")

            title = clean(getattr(entry, "title", ""))

            unique_id = f"{title}|{link}"


            if unique_id in seen_links:
                continue


            seen_links.add(unique_id)

            section += make_article(entry)

            category_total += 1

            added += 1


            top_stories.append({

                "category": category,

                "source": source_name,

                "title": title,

                "link": link,

                "date": get_date(entry)

            })


            if added >= MAX_ARTICLES_PER_SOURCE:
                break


    summary[category] = category_total

    report_sections.append(section)
    # ==========================================================
# SORT TOP STORIES
# ==========================================================

top_stories = sorted(
    top_stories,
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

total_articles = 0

for category, count in summary.items():

    total_articles += count

    content += f"- **{category}** : {count} curated headlines\n"

content += f"""

Total Headlines : {total_articles}

Generated : {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}

"""

# ==========================================================
# FEED STATUS
# ==========================================================

content += """

--------------------------------------------------

# Feed Health

--------------------------------------------------

"""

ok = 0
warning = 0
error = 0

for source, status in feed_status.items():

    if status == "OK":
        icon = "✅"
        ok += 1

    elif status == "WARNING":
        icon = "⚠️"
        warning += 1

    else:
        icon = "❌"
        error += 1

    content += f"{icon} {source}\n"

content += f"""

Healthy Feeds : {ok}

Warnings : {warning}

Errors : {error}

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

Generated            : {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}

"""

# ==========================================================
# FOOTER
# ==========================================================

content += """

--------------------------------------------------

Prepared by

Serkan TUNALI Executive Intelligence Portal

https://intelligence.serkantunali.com

This report is automatically generated from trusted
industry sources covering Artificial Intelligence,
Cyber Security, Physical Security,
Smart Cities and Intelligent Transportation Systems.

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

print("===========================================")
print(" Executive Intelligence Report Generated")
print("===========================================")

print()

print(f"Categories        : {len(summary)}")
print(f"Sources           : {sum(len(v) for v in feeds.values())}")
print(f"Unique Headlines  : {len(seen_links)}")
print(f"Top Stories       : {len(top_stories)}")

print()

for category, count in summary.items():
    print(f"{category:<25} {count}")

print()

print("weekly_report.md created successfully.")
