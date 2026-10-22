"""Keep the tool and story counts on index.html in step with the cards, so a new card never leaves a stale number.

The page has no JavaScript and no build, so this rewrites the HTML itself:
  <b data-count="tools">7</b>                          the number of tool cards (<article> in section#tools)
  <span data-count="tools" data-as="word">Seven</span>  the same number in words
  <span data-list="tools">...</span>                   each card's data-teaser, joined: "a, b, and c"
and the same for "stories" (each <a class="story">). Every card needs a data-teaser.

Run: python3 scripts/counts.py            rewrite index.html when a count or list is stale
     python3 scripts/counts.py --check    exit 1 when stale (the pre-commit hook and the GitHub check)
"""

import re
import sys
from pathlib import Path

PAGE = Path(__file__).resolve().parent.parent / "index.html"
WORDS = ["No", "One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten", "Eleven", "Twelve",
         "Thirteen", "Fourteen", "Fifteen", "Sixteen", "Seventeen", "Eighteen", "Nineteen", "Twenty"]


def teasers(html, cards):
    out = []
    for tag in cards:
        m = re.search(r'data-teaser="([^"]*)"', tag)
        if not m:
            raise ValueError(f"card without data-teaser: {tag[:80]}")
        out.append(m.group(1))
    return out


def found(html):
    """Teasers of the tool cards and of the story cards, in page order."""
    tools = re.search(r'<section id="tools".*?</section>', html, re.S)
    return {"tools": teasers(html, re.findall(r"<article\b[^>]*>", tools.group(0) if tools else "")),
            "stories": teasers(html, re.findall(r'<a class="story"[^>]*>', html))}


def joined(items):
    if len(items) < 3:
        return " and ".join(items)
    return ", ".join(items[:-1]) + ", and " + items[-1]


def sync(html):
    for kind, items in found(html).items():
        n = len(items)
        html = re.sub(rf'(<b data-count="{kind}">)[^<]*(</b>)', rf"\g<1>{n}\2", html)
        html = re.sub(rf'(<span data-count="{kind}" data-as="word">)[^<]*(</span>)',
                      lambda m: m.group(1) + (WORDS[n] if n < len(WORDS) else str(n)) + m.group(2), html)
        html = re.sub(rf'(<span data-list="{kind}">)[^<]*(</span>)', lambda m: m.group(1) + joined(items) + m.group(2), html)
    return html


def main():
    html = PAGE.read_text()
    new = sync(html)
    if new == html:
        return 0
    if "--check" in sys.argv:
        print("index.html: tool or story counts are stale; run python3 scripts/counts.py")
        return 1
    PAGE.write_text(new)
    print("index.html: counts and lists updated")
    return 0


if __name__ == "__main__":
    sys.exit(main())
