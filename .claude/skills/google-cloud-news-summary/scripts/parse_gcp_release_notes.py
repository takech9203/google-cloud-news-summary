#!/usr/bin/env python3
"""
Google Cloud Release Notes RSS Feed Parser

Parses the Google Cloud Release Notes RSS feed and outputs filtered items as JSON.

Usage:
    python parse_gcp_release_notes.py [--days DAYS] [--feed PATH]

Options:
    --days DAYS    Number of days to look back (default: 7)
    --feed PATH    Path to RSS feed XML file (default: /tmp/gcp_release_notes.xml)

Output:
    JSON object with filtered release notes items
"""

import argparse
import json
import sys
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
from pathlib import Path


def parse_date(date_str: str) -> datetime:
    """Parse ISO 8601 date string to datetime object."""
    # Google Cloud uses ISO 8601 format: 2026-01-15T00:00:00Z
    try:
        return datetime.fromisoformat(date_str.replace("Z", "+00:00"))
    except Exception:
        return datetime.now(timezone.utc)


def parse_feed(feed_path: Path, days: int) -> dict:
    """Parse Google Cloud Release Notes RSS feed."""
    try:
        tree = ET.parse(feed_path)
        root = tree.getroot()
    except Exception as e:
        print(f"Error parsing feed: {e}", file=sys.stderr)
        return {"source": "gcp-release-notes", "total_items": 0, "items": []}

    # Calculate cutoff date
    cutoff_date = datetime.now(timezone.utc) - timedelta(days=days)

    # Parse Atom feed
    ns = {"atom": "http://www.w3.org/2005/Atom"}
    entries = root.findall(".//atom:entry", ns)

    items = []
    for entry in entries:
        try:
            title_elem = entry.find("atom:title", ns)
            published_elem = entry.find("atom:published", ns)
            updated_elem = entry.find("atom:updated", ns)
            link_elem = entry.find("atom:link[@rel='alternate']", ns)
            summary_elem = entry.find("atom:summary", ns)
            category_elems = entry.findall("atom:category", ns)

            # Use published date if available, fall back to updated date
            date_elem = published_elem if published_elem is not None else updated_elem
            if title_elem is None or date_elem is None:
                continue

            title = title_elem.text or ""
            published_str = date_elem.text or ""
            published = parse_date(published_str)

            # Filter by date
            if published < cutoff_date:
                continue

            link = link_elem.get("href", "") if link_elem is not None else ""
            summary = summary_elem.text or "" if summary_elem is not None else ""
            categories = [cat.get("term", "") for cat in category_elems]

            items.append({
                "title": title,
                "date": published.strftime("%Y-%m-%d"),
                "url": link,
                "summary": summary,
                "categories": categories,
                "source": "gcp-release-notes",
            })

        except Exception as e:
            print(f"Error parsing entry: {e}", file=sys.stderr)
            continue

    # Sort by date (newest first)
    items.sort(key=lambda x: x["date"], reverse=True)

    return {
        "source": "gcp-release-notes",
        "total_items": len(items),
        "items": items,
    }


def main():
    parser = argparse.ArgumentParser(
        description="Parse Google Cloud Release Notes RSS feed"
    )
    parser.add_argument(
        "--days",
        type=int,
        default=7,
        help="Number of days to look back (default: 7)",
    )
    parser.add_argument(
        "--feed",
        type=Path,
        default=Path("/tmp/gcp_release_notes.xml"),
        help="Path to RSS feed XML file",
    )

    args = parser.parse_args()

    if not args.feed.exists():
        print(f"Error: Feed file not found: {args.feed}", file=sys.stderr)
        sys.exit(1)

    result = parse_feed(args.feed, args.days)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
