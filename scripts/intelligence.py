"""
==========================================================
Executive Intelligence Portal
V11 Intelligence Layer

intelligence.py

Analyzes collected articles and produces:

- Executive Insight
- Vendor Ranking
- Keyword Statistics
- Technology Focus
- Emerging Topics

This module never downloads feeds.
It only analyzes Article objects.
==========================================================
"""

from collections import Counter
import re

# ---------------------------------------------------------
# Default keywords
# ---------------------------------------------------------

DEFAULT_KEYWORDS = {

    "AI",
    "GENAI",
    "LLM",
    "GPT",
    "COPILOT",
    "AGENTIC",
    "RAG",
    "MCP",

    "CYBER",
    "ZERO",
    "TRUST",
    "XDR",
    "EDR",
    "SOC",
    "SIEM",

    "VIDEO",
    "SURVEILLANCE",
    "ANALYTICS",
    "CAMERA",
    "ONVIF",

    "ITS",
    "SMART",
    "CITY",
    "MOBILITY",
    "TRAFFIC",

    "EDGE",
    "CLOUD",
    "IOT",
    "DIGITAL",
    "TWIN"
}


# ---------------------------------------------------------
# Intelligence Engine
# ---------------------------------------------------------

class IntelligenceEngine:

    def __init__(self, articles):

        self.articles = articles

        self.keyword_counter = Counter()

        self.vendor_counter = Counter()

        self.category_counter = Counter()

        self.word_counter = Counter()

    # -----------------------------------------------------

    def tokenize(self, text):

        words = re.findall(

            r"[A-Za-z0-9\-]+",

            text.upper()

        )

        return words

    # -----------------------------------------------------

    def process_article(self, article):

        self.vendor_counter[article.source] += 1

        self.category_counter[article.category] += 1

        words = self.tokenize(article.title)

        for word in words:

            self.word_counter[word] += 1

            if word in DEFAULT_KEYWORDS:

                self.keyword_counter[word] += 1

    # -----------------------------------------------------

    def analyze(self):

        for article in self.articles:

            self.process_article(article)

        return self

      # -----------------------------------------------------
    # Top Keywords
    # -----------------------------------------------------

    def top_keywords(self, limit=15):

        return self.keyword_counter.most_common(limit)

    # -----------------------------------------------------
    # Top Vendors
    # -----------------------------------------------------

    def top_vendors(self, limit=10):

        return self.vendor_counter.most_common(limit)

    # -----------------------------------------------------
    # Technology Focus
    # -----------------------------------------------------

    def technology_focus(self):

        return sorted(

            self.category_counter.items(),

            key=lambda x: x[1],

            reverse=True

        )

    # -----------------------------------------------------
    # Executive Insight
    # -----------------------------------------------------

    def executive_insight(self):

        if not self.articles:

            return "No articles were collected this week."

        vendor = "Unknown"
        vendor_count = 0

        vendors = self.top_vendors(1)

        if vendors:

            vendor, vendor_count = vendors[0]

        categories = self.technology_focus()

        dominant_category = "Technology"
        dominant_count = 0

        if categories:

            dominant_category, dominant_count = categories[0]

        keywords = [

            keyword

            for keyword, count

            in self.top_keywords(5)

        ]

        insight = []

        insight.append(

            f"This week's intelligence report contains "

            f"{len(self.articles)} curated articles."

        )

        insight.append(

            f"The dominant technology area was "

            f"{dominant_category} "

            f"with {dominant_count} articles."

        )

        insight.append(

            f"The most active information source "

            f"was {vendor} "

            f"({vendor_count} articles)."

        )

        if keywords:

            insight.append(

                "Key technology themes included "

                + ", ".join(keywords)

                + "."

            )

        return "\n".join(insight)

    # -----------------------------------------------------
    # Executive Metrics
    # -----------------------------------------------------

    def metrics(self):

        return {

            "articles": len(self.articles),

            "vendors": len(self.vendor_counter),

            "categories": len(self.category_counter),

            "keywords": len(self.keyword_counter)

        }

      # -----------------------------------------------------
    # Emerging Topics
    # -----------------------------------------------------

    def emerging_topics(self, limit=10):

        ignored = {

            "THE", "AND", "FOR", "WITH", "FROM",
            "THIS", "THAT", "WILL", "NEW", "MORE",
            "ABOUT", "YOUR", "INTO", "OVER",
            "AFTER", "UNDER", "THROUGH",
            "USING", "THEIR", "THEY",
            "ANNOUNCES", "ANNOUNCED",
            "UPDATE", "UPDATES"
        }

        emerging = []

        for word, count in self.word_counter.items():

            if len(word) < 4:
                continue

            if word in ignored:
                continue

            if word in DEFAULT_KEYWORDS:
                continue

            if count >= 2:

                emerging.append((word, count))

        emerging.sort(

            key=lambda x: x[1],

            reverse=True

        )

        return emerging[:limit]

    # -----------------------------------------------------
    # Dashboard
    # -----------------------------------------------------

    def dashboard(self):

        return {

            "vendors": self.top_vendors(),

            "keywords": self.top_keywords(),

            "categories": self.technology_focus(),

            "emerging": self.emerging_topics(),

            "insight": self.executive_insight()

        }

    # -----------------------------------------------------
    # Markdown Builder
    # -----------------------------------------------------

    def markdown(self):

        dashboard = self.dashboard()

        md = ""

        md += """
--------------------------------------------------

# Intelligence Analysis

--------------------------------------------------

"""

        md += "## Executive Insight\n\n"

        md += dashboard["insight"]

        md += "\n\n"

        md += "## Technology Focus\n\n"

        for category, count in dashboard["categories"]:

            md += f"- **{category}** : {count} articles\n"

        md += "\n"

        md += "## Top Vendors\n\n"

        for vendor, count in dashboard["vendors"]:

            md += f"- {vendor} ({count})\n"

        md += "\n"

        md += "## Trending Keywords\n\n"

        for keyword, count in dashboard["keywords"]:

            md += f"- {keyword} ({count})\n"

        md += "\n"

        emerging = dashboard["emerging"]

        if emerging:

            md += "## Emerging Topics\n\n"

            for word, count in emerging:

                md += f"- {word} ({count})\n"

            md += "\n"

        return md

    # -----------------------------------------------------
    # Console Debug
    # -----------------------------------------------------

    def print_summary(self):

        print()

        print("========================================")
        print(" Intelligence Layer")
        print("========================================")

        print()

        print(self.executive_insight())

        print()

        print("Top Vendors")

        for vendor, count in self.top_vendors():

            print(f"{vendor:<30} {count}")

        print()

        print("Top Keywords")

        for keyword, count in self.top_keywords():

            print(f"{keyword:<20} {count}")

        print()

        print("Emerging Topics")

        for word, count in self.emerging_topics():

            print(f"{word:<20} {count}")

        print()

        print("========================================")
