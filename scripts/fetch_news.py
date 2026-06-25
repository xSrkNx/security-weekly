import feedparser
from datetime import datetime

feeds = {

    "AI & GenAI": {

        "OpenAI":
        "https://openai.com/news/rss.xml",

        "Microsoft AI":
        "https://blogs.microsoft.com/ai/feed/",

        "Google AI":
        "https://blog.google/technology/ai/rss/",

        "NVIDIA":
        "https://blogs.nvidia.com/feed/",
    },

    "Cyber Security": {

        "Dark Reading":
        "https://www.darkreading.com/rss.xml",

        "Security Magazine":
        "https://www.securitymagazine.com/rss/topic/2236-security-news",

        "AWS Security":
        "https://aws.amazon.com/blogs/security/feed/",

        "Microsoft Security":
        "https://www.microsoft.com/en-us/security/blog/feed/",
    },

    "Physical Security": {

        "Genetec":
        "https://www.genetec.com/blog/rss.xml",

        "Axis":
        "https://www.axis.com/blog/rss.xml",
    },

    "ITS & Smart Mobility": {

        "ITS International":
        "https://www.itsinternational.com/rss",

        "Smart Cities World":
        "https://www.smartcitiesworld.net/rss.xml",
    }
}

content = "# Weekly Executive Intelligence Report\n\n"
content += f"Generated: {datetime.now()}\n\n"

summary = {}

for category, sources in feeds.items():

    content += f"\n# {category}\n\n"

    category_total = 0

    for source_name, url in sources.items():

        feed = feedparser.parse(url)

        entry_count = len(feed.entries)

        category_total += min(entry_count, 5)

        content += f"## {source_name}\n\n"
        content += f"Entries found: {entry_count}\n\n"

        if entry_count == 0:
            content += "⚠ No entries found\n\n"
            continue

        for item in feed.entries[:5]:

            content += f"### {item.title}\n"

            if hasattr(item, "published"):
                content += f"Published: {item.published}\n"

            content += f"{item.link}\n\n"

    summary[category] = category_total

content += "\n---\n\n"
content += "# Executive Summary\n\n"

for category, count in summary.items():

    content += f"- {category}: {count} articles collected\n"

with open("weekly_report.md", "w", encoding="utf-8") as f:
    f.write(content)

print("Report created")
