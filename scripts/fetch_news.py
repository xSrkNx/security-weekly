import feedparser
from datetime import datetime

feeds = {
    "OpenAI": "https://openai.com/news/rss.xml",
    "Security Magazine": "https://www.securitymagazine.com/rss/topic/2236-security-news",
    "Dark Reading": "https://www.darkreading.com/rss.xml",
}

content = "# Weekly Security Report\n\n"
content += f"Generated: {datetime.now()}\n\n"

summary = {}

for source, url in feeds.items():

    feed = feedparser.parse(url)

    summary[source] = len(feed.entries)

    content += f"## {source}\n\n"
    content += f"Feed URL: {url}\n\n"
    content += f"Entries found: {len(feed.entries)}\n\n"

    if len(feed.entries) == 0:
        content += "⚠ No entries found\n\n"
        continue

    for item in feed.entries[:5]:

        content += f"### {item.title}\n"

        if hasattr(item, "published"):
            content += f"Published: {item.published}\n"

        content += f"{item.link}\n\n"

content += "\n---\n\n"
content += "# Executive Summary\n\n"

for source, count in summary.items():
    content += f"- {source}: {count} entries found\n"

with open("weekly_report.md", "w", encoding="utf-8") as f:
    f.write(content)

print("Report created")
