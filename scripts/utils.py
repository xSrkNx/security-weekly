import html

from datetime import datetime, UTC
from email.utils import parsedate_to_datetime


def clean(text):

    if not text:

        return ""

    return html.unescape(text).replace("\n", " ").strip()


def parse_date(entry):

    try:

        if getattr(entry, "published_parsed", None):

            return parsedate_to_datetime(entry.published)

    except Exception:

        pass

    return datetime.now(UTC)
