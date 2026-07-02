import feedparser

from datetime import datetime

from email.utils import parsedate_to_datetime

from collections import defaultdict

import html

# ==========================================================
# Configuration
# ==========================================================

MAX_ARTICLES_PER_SOURCE = 5

MAX_TOP_STORIES = 10

seen_links = set()

summary = {}

top_stories = []

# ==========================================================
# RSS Sources
# ==========================================================

feeds = {

    "AI & GenAI": {

        "OpenAI":
        "https://openai.com/news/rss.xml",

        "Google AI":
        "https://blog.google/technology/ai/rss/",

        "NVIDIA":
        "https://blogs.nvidia.com/feed/",

        "Microsoft Security AI":
        "https://www.microsoft.com/en-us/security/blog/feed/",
    },

    "Cyber Security": {

        "Dark Reading":
        "https://www.darkreading.com/rss.xml",

        "Security Magazine":
        "https://www.securitymagazine.com/rss/topic/2236-security-news",

        "Microsoft Security":
        "https://www.microsoft.com/en-us/security/blog/feed/",
    },

    "Physical Security": {

        "ONVIF":
        "https://www.onvif.org/news/feed/",

        "SecurityInfoWatch":
        "https://www.securityinfowatch.com/rss",
    },

    "ITS & Smart Mobility": {

        "Traffic Technology Today":
        "https://www.traffictechnologytoday.com/feed",

        "Smart Cities Dive":
        "https://www.smartcitiesdive.com/feeds/news/",
    }

}

# ==========================================================
# Helper Functions
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


def article_block(entry):

    block = ""

    block += f"### {clean(entry.title)}\n"

    if hasattr(entry, "published"):

        block += f"Published: {entry.published}\n"

    block += f"[Read Article]({entry.link})\n\n"

    return block

# ==========================================================
# Report Header
# ==========================================================

content = f"""# Serkan TUNALI Executive Intelligence Report

Generated:
{datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}

---

## Executive Snapshot

This report provides a curated executive overview of the latest developments across:

- Artificial Intelligence
- Cyber Security
- Physical Security
- Intelligent Transportation Systems
- Smart Mobility

Only the most relevant headlines are included to support executive awareness and strategic decision making.

---

"""
# ==========================================================
# Collect RSS Feeds
# ==========================================================

for category, sources in feeds.items():

    content += f"""

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

            content += f"## {source_name}\n\n"

            content += f"Unable to read RSS feed.\n"

            content += f"{ex}\n\n"

            continue

        content += f"## {source_name}\n\n"

        if len(feed.entries) == 0:

            content += "⚠ No articles found.\n\n"

            continue

        added = 0

        for entry in feed.entries:

            link = getattr(entry, "link", "")

            if not link:

                continue

            if link in seen_links:

                continue

            seen_links.add(link)

            content += article_block(entry)

            category_total += 1

            added += 1

            top_stories.append({

                "category": category,

                "source": source_name,

                "title": clean(entry.title),

                "link": link,

                "date": get_date(entry)

            })

            if added >= MAX_ARTICLES_PER_SOURCE:

                break

    summary[category] = category_total
    # ==========================================================
# Sort Top Stories
# ==========================================================

top_stories = sorted(

    top_stories,

    key=lambda x: x["date"],

    reverse=True

)

top_stories = top_stories[:MAX_TOP_STORIES]
# ==========================================================
# Top Stories
# ==========================================================

content += """

--------------------------------------------------

# Top Stories This Week

--------------------------------------------------

"""

for article in top_stories:

    content += f"### {article['title']}\n"

    content += f"Category: {article['category']}\n"

    content += f"Source: {article['source']}\n"

    content += f"[Read Article]({article['link']})\n\n"

# ==========================================================
# Executive Summary
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

Total Headlines Collected : {total_articles}

Generated : {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}

"""

# ==========================================================
# Report Statistics
# ==========================================================

content += """

--------------------------------------------------

# Report Statistics

--------------------------------------------------

"""

content += f"""

Sources Configured : {sum(len(v) for v in feeds.values())}

Categories : {len(feeds)}

Unique Headlines : {len(seen_links)}

Top Stories : {len(top_stories)}

"""

# ==========================================================
# Footer
# ==========================================================

content += """

--------------------------------------------------

Prepared by

Serkan TUNALI Executive Intelligence Portal

https://intelligence.serkantunali.com

This report is automatically generated from trusted
industry sources including AI vendors,
cyber security organizations,
physical security vendors and
smart mobility publications.

© Serkan TUNALI

"""

# ==========================================================
# Write Report
# ==========================================================

with open(

    "weekly_report.md",

    "w",

    encoding="utf-8"

) as f:

    f.write(content)

print()

print("========================================")

print(" Executive Intelligence Report Created")

print("========================================")

print()

print(f"Unique Articles : {len(seen_links)}")

print(f"Top Stories     : {len(top_stories)}")

print(f"Categories      : {len(summary)}")

print()

for category, count in summary.items():

    print(f"{category:<25} {count}")

print()

print("Report saved to weekly_report.md")

print()
