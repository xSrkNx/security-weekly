"""
==========================================================
Executive Intelligence Portal
V10 Phoenix
Source Engine
==========================================================

This module is responsible for:

- Reading RSS feeds
- Collecting articles
- Feed health monitoring
- Duplicate detection
- Top story collection

Future versions will also support:

- HTML parsing
- Press Release pages
- Vendor Newsrooms
- JSON APIs
"""

import feedparser
import socket

from datetime import datetime, UTC

from models import Article, FeedHealth

from utils import clean, parse_date

from config import (
    REQUEST_TIMEOUT,
    MAX_ARTICLES_PER_SOURCE
)

socket.setdefaulttimeout(REQUEST_TIMEOUT)


class SourceEngine:

    def __init__(self):

        self.articles = []

        self.feed_health = []

        self.seen = set()

    # -------------------------------------------------

    def feed_status(self, feed):

        status = getattr(feed, "status", "Unknown")

        if getattr(feed, "bozo", False):

            return FeedHealth(

                source="",

                status="WARNING",

                message=f"HTTP {status} ({feed.bozo_exception})"

            )

        if len(feed.entries) == 0:

            return FeedHealth(

                source="",

                status="WARNING",

                message=f"HTTP {status} (Empty Feed)"

            )

        return FeedHealth(

            source="",

            status="OK",

            message=f"HTTP {status}"

        )

    # -------------------------------------------------

    def parse_feed(

        self,

        category,

        source_name,

        url

    ):

        print(f"Reading {source_name}...")

        try:

            feed = feedparser.parse(url)

        except Exception as ex:

            self.feed_health.append(

                FeedHealth(

                    source=source_name,

                    status="ERROR",

                    message=str(ex)

                )

            )

            return []

        health = self.feed_status(feed)

        health.source = source_name

        self.feed_health.append(health)

        collected = []

        added = 0

          # ---------------------------------------------
        # Read Articles
        # ---------------------------------------------

        for entry in feed.entries:

            title = clean(
                getattr(entry, "title", "")
            )

            link = getattr(entry, "link", "")

            if not title or not link:

                continue

            uid = f"{title}|{link}"

            if uid in self.seen:

                continue

            self.seen.add(uid)

            article = Article(

                title=title,

                link=link,

                source=source_name,

                category=category,

                published=parse_date(entry)

            )

            self.articles.append(article)

            collected.append(article)

            added += 1

            if added >= MAX_ARTICLES_PER_SOURCE:

                break

        return collected

    # -------------------------------------------------

    def collect(self, feeds):

        """
        Collect articles from every configured source.
        """

        summary = {}

        for category, sources in feeds.items():

            category_total = 0

            for source_name, url in sources.items():

                articles = self.parse_feed(

                    category,

                    source_name,

                    url

                )

                category_total += len(articles)

            summary[category] = category_total

        return summary

    # -------------------------------------------------

    def top_stories(

        self,

        limit=10

    ):

        stories = sorted(

            self.articles,

            key=lambda x: x.published,

            reverse=True

        )

        return stories[:limit]

      # -------------------------------------------------
    # Feed Statistics
    # -------------------------------------------------

    def feed_statistics(self):

        healthy = 0
        warning = 0
        error = 0

        for feed in self.feed_health:

            if feed.status == "OK":

                healthy += 1

            elif feed.status == "WARNING":

                warning += 1

            else:

                error += 1

        total = len(self.feed_health)

        reliability = 0

        if total:

            reliability = round((healthy / total) * 100)

        return {

            "healthy": healthy,

            "warning": warning,

            "error": error,

            "total": total,

            "reliability": reliability

        }

    # -------------------------------------------------
    # Vendor Statistics
    # -------------------------------------------------

    def vendor_statistics(self):

        vendors = {}

        for article in self.articles:

            vendors.setdefault(article.source, 0)

            vendors[article.source] += 1

        return dict(

            sorted(

                vendors.items(),

                key=lambda x: x[1],

                reverse=True

            )

        )

    # -------------------------------------------------
    # Category Statistics
    # -------------------------------------------------

    def category_statistics(self):

        categories = {}

        for article in self.articles:

            categories.setdefault(article.category, 0)

            categories[article.category] += 1

        return categories

    # -------------------------------------------------
    # Export helpers
    # -------------------------------------------------

    def all_articles(self):

        return self.articles

    def health(self):

        return self.feed_health

    def article_count(self):

        return len(self.articles)

    def source_count(self):

        return len(

            {

                article.source

                for article in self.articles

            }

        )

    def categories(self):

        return len(

            {

                article.category

                for article in self.articles

            }

        )

    # -------------------------------------------------
    # Debug
    # -------------------------------------------------

    def print_summary(self):

        stats = self.feed_statistics()

        print()

        print("=======================================")
        print(" Executive Intelligence Source Engine")
        print("=======================================")

        print()

        print(f"Articles           : {self.article_count()}")

        print(f"Sources            : {self.source_count()}")

        print(f"Categories         : {self.categories()}")

        print(f"Healthy Feeds      : {stats['healthy']}")

        print(f"Warnings           : {stats['warning']}")

        print(f"Errors             : {stats['error']}")

        print(f"Reliability        : {stats['reliability']} %")

        print()

        print("Top Vendors")

        print("----------------------------")

        for vendor, count in self.vendor_statistics().items():

            print(f"{vendor:<30} {count}")

        print()

        print("=======================================")
