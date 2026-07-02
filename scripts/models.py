from dataclasses import dataclass
from datetime import datetime


@dataclass
class Article:

    title: str

    link: str

    source: str

    category: str

    published: datetime | None = None


@dataclass
class FeedHealth:

    source: str

    status: str

    message: str
