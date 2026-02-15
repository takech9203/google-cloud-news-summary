#!/usr/bin/env python3
"""
Google Cloud Blog Feed Parser

The Google Cloud Blog feed URL returns HTML (not Atom/XML).
This parser extracts blog article links from the HTML response
by scanning for <a> tags with href containing /blog/products/.

Since the HTML is JavaScript-rendered and does not contain
structured date information, this parser returns article URLs
without date filtering. The caller should manually check
article relevance.

Usage:
    python parse_gcp_blog.py [--days DAYS] [--feed PATH]

Options:
    --days DAYS    Ignored (kept for CLI compatibility)
    --feed PATH    Path to blog feed HTML file
                   (default: /tmp/gcp_blog_feed.xml)

Output:
    JSON object with extracted blog article links
"""

import argparse
import json
import re
import sys
from pathlib import Path


def extract_blog_links(html: str) -> list[dict]:
    """Extract unique blog article links from HTML content.

    Looks for href patterns like /blog/products/*/ARTICLE_SLUG
    that point to actual blog posts (not category pages).
    """
    # Match blog article URLs (must have at least 3 path segments)
    pattern = re.compile(
        r'href="(/blog/(?:products|topics)/[^"/]+/[^"]+)"'
    )
    seen = set()
    articles = []

    for match in pattern.finditer(html):
        path = match.group(1)
        # Skip feed, search, and category-only URLs
        if "/feed" in path or "/search" in path:
            continue
        # Skip if already seen
        if path in seen:
            continue
        seen.add(path)

        url = f"https://cloud.google.com{path}"
        # Extract slug from path for title hint
        slug = path.rstrip("/").split("/")[-1]
        title_hint = slug.replace("-", " ").title()

        articles.append({
            "title": title_hint,
            "url": url,
            "source": "gcp-blog",
        })

    return articles


def parse_feed(feed_path: Path) -> dict:
    """Parse Google Cloud Blog HTML and extract article links."""
    try:
        content = feed_path.read_text(encoding="utf-8")
    except Exception as e:
        print(f"Error reading feed: {e}", file=sys.stderr)
        return {
            "source": "gcp-blog",
            "total_items": 0,
            "items": [],
            "warning": "Could not read feed file",
        }

    if not content.strip():
        return {
            "source": "gcp-blog",
            "total_items": 0,
            "items": [],
            "warning": "Feed file is empty",
        }

    # Check if this is actually XML/Atom (future-proofing)
    if content.strip().startswith("<?xml"):
        return parse_atom_feed(content)

    # HTML mode: extract links
    articles = extract_blog_links(content)

    result = {
        "source": "gcp-blog",
        "total_items": len(articles),
        "items": articles,
    }

    if not articles:
        result["warning"] = (
            "No blog articles found. The feed URL returns "
            "JavaScript-rendered HTML; article data may not "
            "be available via static parsing."
        )

    return result


def parse_atom_feed(content: str) -> dict:
    """Parse Atom/XML feed if the response is actually XML."""
    import xml.etree.ElementTree as ET

    try:
        root = ET.fromstring(content)
    except ET.ParseError as e:
        print(f"Error parsing XML: {e}", file=sys.stderr)
        return {
            "source": "gcp-blog",
            "total_items": 0,
            "items": [],
            "warning": f"XML parse error: {e}",
        }

    ns = {"atom": "http://www.w3.org/2005/Atom"}
    entries = root.findall(".//atom:entry", ns)

    items = []
    for entry in entries:
        title_el = entry.find("atom:title", ns)
        link_el = entry.find("atom:link[@rel='alternate']", ns)
        published_el = entry.find("atom:published", ns)

        title = title_el.text if title_el is not None else ""
        link = ""
        if link_el is not None:
            link = link_el.get("href", "")
        published = ""
        if published_el is not None:
            published = published_el.text or ""

        items.append({
            "title": title,
            "url": link,
            "date": published[:10] if published else "",
            "source": "gcp-blog",
        })

    return {
        "source": "gcp-blog",
        "total_items": len(items),
        "items": items,
    }


def main():
    parser = argparse.ArgumentParser(
        description="Parse Google Cloud Blog feed"
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
        default=Path("/tmp/gcp_blog_feed.xml"),
        help="Path to blog feed file",
    )

    args = parser.parse_args()

    if not args.feed.exists():
        print(
            f"Error: Feed file not found: {args.feed}",
            file=sys.stderr,
        )
        sys.exit(1)

    result = parse_feed(args.feed)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
