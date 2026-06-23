import feedparser
from datetime import datetime

feeds = {
    "ONVIF": "https://www.onvif.org/feed/",
    "OpenAI": "https://openai.com/news/rss.xml"
}

content = f"# Weekly Security Report\n\n"
content += f"Generated: {datetime.now()}\n\n"

for source, url in feeds.items():

    content += f"## {source}\n\n"

    feed = feedparser.parse(url)

    for item in feed.entries[:5]:

        content += f"### {item.title}\n"
        content += f"{item.link}\n\n"

with open("weekly_report.md", "w", encoding="utf-8") as f:
    f.write(content)

print("Report created")
