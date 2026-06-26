import feedparser
from datetime import datetime

# Aynı haber iki farklı kategoride tekrar gösterilmesin
seen_links = set()

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

# --------------------------------------------------

content = "# Serkan TUNALI Executive Intelligence Report\n\n"

content += (
    "Prepared for executive awareness across "
    "Artificial Intelligence, Cyber Security, "
    "Physical Security and Intelligent Transportation Systems.\n\n"
)

content += f"Generated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}\n\n"

content += "# Executive Snapshot\n\n"

content += (
    "This report highlights the most relevant developments "
    "across Artificial Intelligence, Cyber Security, "
    "Physical Security and Intelligent Transportation Systems.\n\n"
)

summary = {}

# --------------------------------------------------

for category, sources in feeds.items():

    content += "\n---\n\n"
    content += f"# {category}\n\n"

    category_total = 0

    for source_name, url in sources.items():

        feed = feedparser.parse(url)

        content += f"## {source_name}\n\n"

        if len(feed.entries) == 0:

            content += "_No recent articles found._\n\n"
            continue

        added = 0

        for item in feed.entries:

            link = getattr(item, "link", "")

            if link in seen_links:
                continue

            seen_links.add(link)

            added += 1

            if added > 5:
                break

            category_total += 1

            content += f"### {item.title}\n\n"

            if hasattr(item, "published"):
                content += f"**Published:** {item.published}\n\n"

            content += f"[Read Full Article]({link})\n\n"

    summary[category] = category_total

# --------------------------------------------------

content += "\n---\n\n"

content += "# Executive Summary\n\n"

for category, count in summary.items():

    content += f"- **{category}** : {count} curated headlines\n"

# --------------------------------------------------

with open("weekly_report.md", "w", encoding="utf-8") as f:

    f.write(content)

print("Executive report created successfully.")
