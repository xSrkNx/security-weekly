import feedparser
from datetime import datetime

feeds = {
    "OpenAI": "https://openai.com/news/rss.xml",
    "Security Magazine": "https://www.securitymagazine.com/rss/topic/2236-security-news",
    "Dark Reading": "https://www.darkreading.com/rss.xml",
}

content = f"# Weekly Security Report\n\n"
content += f"Generated: {datetime.now()}\n\n"

for source, url in feeds.items():

    content += f"## {source}\n\n"

    feed = feedparser.parse(url)

    content += f"Feed URL: {url}\n\n"
    content += f"Entries found: {len(feed.entries)}\n\n"

    if len(feed.entries) == 0:
        content += "⚠ No entries found\n\n"

    for item in feed.entries[:5]:

        content += f"### {item.title}\n"

        if hasattr(item, "published"):
            content += f"Published: {item.published}\n"

        content += f"{item.link}\n\n"

with open("weekly_report.md", "w", encoding="utf-8") as f:
    f.write(content)

print("Report created")
