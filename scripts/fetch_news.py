import feedparser
from datetime import datetime
from collections import Counter
import re

# ======================================================
# RSS SOURCES
# ======================================================

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

# ======================================================
# VARIABLES
# ======================================================

seen_links = set()

summary = {}

feed_status = {}

keyword_counter = Counter()

# ======================================================
# HEADER
# ======================================================

content = "# Serkan TUNALI Executive Intelligence Report\n\n"

content += (
    "Prepared for executive awareness across "
    "Artificial Intelligence, Cyber Security, "
    "Physical Security and Intelligent Transportation Systems.\n\n"
)

content += f"Generated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}\n\n"

content += "---\n\n"

content += "# Executive Snapshot\n\n"

content += (
    "This report contains curated headlines collected from "
    "trusted industry sources across AI, Cyber Security, "
    "Physical Security and Smart Mobility.\n\n"
)

# ======================================================
# COLLECT NEWS
# ======================================================

for category, sources in feeds.items():

    content += f"\n---\n\n# {category}\n\n"

    category_total = 0

    for source_name, url in sources.items():

        feed = feedparser.parse(url)

        entry_count = len(feed.entries)

        if entry_count > 0:
            feed_status[source_name] = "🟢 Online"
        else:
            feed_status[source_name] = "🔴 Offline"

        content += f"## {source_name}\n\n"

        if entry_count == 0:

            content += "⚠ No entries found.\n\n"

            continue

        added = 0

        for item in feed.entries:

            if item.link in seen_links:
                continue

            seen_links.add(item.link)

            if added >= 5:
                break

            added += 1
            category_total += 1

            title = item.title.strip()

            content += f"### {title}\n"

            if hasattr(item, "published"):
                content += f"Published: {item.published}\n"

            content += f"[Read Article]({item.link})\n\n"

            words = re.findall(r"[A-Za-z0-9\-\+]{4,}", title)

            keyword_counter.update(words)

    summary[category] = category_total

# ======================================================
# FEED HEALTH
# ======================================================

content += "\n---\n\n"

content += "# Feed Health\n\n"

for feed_name, status in feed_status.items():

    content += f"- {status} {feed_name}\n"

# ======================================================
# EXECUTIVE SUMMARY
# ======================================================

content += "\n---\n\n"

content += "# Executive Summary\n\n"

total_articles = 0

for category, count in summary.items():

    total_articles += count

    content += f"- **{category}** : {count} curated headlines\n"

content += f"\n**Total Headlines:** {total_articles}\n"

# ======================================================
# TRENDING TOPICS
# ======================================================

content += "\n---\n\n"

content += "# Trending Topics\n\n"

ignore = {

    "with",
    "from",
    "that",
    "this",
    "their",
    "into",
    "using",
    "will",
    "have",
    "after",
    "security",
    "technology",
    "report",
    "week",
    "latest",
    "news"

}

shown = 0

for word, count in keyword_counter.most_common():

    if word.lower() in ignore:
        continue

    if len(word) < 4:
        continue

    content += f"- {word} ({count})\n"

    shown += 1

    if shown == 10:
        break

# ======================================================
# SAVE REPORT
# ======================================================

with open("weekly_report.md", "w", encoding="utf-8") as f:
    f.write(content)

print("Weekly Executive Intelligence Report created successfully.")
