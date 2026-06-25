import feedparser
from datetime import datetime

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

content = "# Serkan TUNALI Executive Intelligence Report\n\n"

content += f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}\n\n"

summary = {}

for category, sources in feeds.items():

    content += f"# {category}\n\n"

    category_total = 0

    for source_name, url in sources.items():

        feed = feedparser.parse(url)

        entry_count = len(feed.entries)

        category_total += min(entry_count, 5)

        content += f"## {source_name}\n\n"

        if entry_count == 0:
            content += "⚠ No entries found\n\n"
            continue

        for item in feed.entries[:5]:

            content += f"### {item.title}\n"

            if hasattr(item, "published"):
                content += f"Published: {item.published}\n"

            content += f"[Read Article]({item.link})\n\n"

    summary[category] = category_total

content += "\n---\n\n"
content += "# Executive Snapshot\n\n"

for category, count in summary.items():
    content += f"- {category}: {count} headlines collected\n"

with open("weekly_report.md", "w", encoding="utf-8") as f:
    f.write(content)

print("Report created")
