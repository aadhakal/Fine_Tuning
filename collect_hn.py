"""
Collect top-level Hacker News comments into a CSV, ready to label.

    python collect_hn.py --search "claude code"        # find threads worth reading
    python collect_hn.py 47660925 43163011 ...         # pull comments from those threads

The second command writes hn_candidates.csv with the columns labels.csv needs
(text, label, note) plus `source`, the thread each comment came from. The label
column is left empty. Filling it in is your job, and reading every comment is
Milestone 1 — this only saves you the copying.

Why top-level only: a reply only makes sense next to what it's replying to, and
the model never sees that. A comment on the story itself mostly stands alone.

Why a cap per thread: if one thread supplies half your data, the model learns
that thread's topic instead of your labels.

No account and no key. It uses the public HN search API at hn.algolia.com.
"""

import argparse
import csv
import html
import json
import random
import re
import sys
import urllib.parse
import urllib.request
from pathlib import Path

API = "https://hn.algolia.com/api/v1"
OUT = "hn_candidates.csv"

# The notebook reads about the first 128 tokens of each post, which is roughly
# 90 words. Longer comments are kept, but counted, because the model only sees
# their beginning.
WORDS_THE_MODEL_SEES = 90


def fetch(url):
    request = urllib.request.Request(url, headers={"User-Agent": "takemeter-coursework"})
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)


def clean(raw):
    """HN comment HTML to plain text. Paragraph breaks become blank lines."""
    text = re.sub(r"<p>", "\n\n", raw)
    text = re.sub(r"<[^>]+>", "", text)
    text = html.unescape(text)
    return re.sub(r"[ \t]+", " ", text).strip()


def search(query, limit):
    """List stories matching the query, busiest first, so you can pick threads."""
    params = urllib.parse.urlencode({"query": query, "tags": "story", "hitsPerPage": limit})
    hits = fetch(f"{API}/search?{params}")["hits"]
    hits.sort(key=lambda h: h.get("num_comments") or 0, reverse=True)

    print(f"{'thread id':<10} {'comments':>8}  {'date':<10}  title")
    for h in hits:
        print(f"{h['objectID']:<10} {h.get('num_comments') or 0:>8}  "
              f"{h.get('created_at', '')[:10]:<10}  {h['title'][:70]}")
    print("\nRead a thread first: https://news.ycombinator.com/item?id=<thread id>")


def top_level_comments(thread_id):
    """Every non-empty comment posted directly on the story. No authors kept."""
    story = fetch(f"{API}/items/{thread_id}")
    comments = [clean(c["text"]) for c in story.get("children", []) if c.get("text")]
    return story.get("title", ""), [c for c in comments if c]


def collect(thread_ids, per_thread, seed, out, force):
    path = Path(out)
    # Refuse to overwrite: once you've labelled this file, rerunning the script
    # would silently wipe your labels.
    if path.exists() and not force:
        sys.exit(f"{out} already exists. If you've started labelling it, rename it "
                 f"before collecting again. To replace it anyway, pass --force.")

    rng = random.Random(seed)
    rows, seen = [], set()

    for thread_id in thread_ids:
        title, comments = top_level_comments(thread_id)

        # HN lists the most upvoted comments first. Taking the first N would
        # collect only the popular ones, so sample across the whole thread.
        rng.shuffle(comments)
        kept = 0
        for text in comments:
            if text in seen:
                continue
            seen.add(text)
            rows.append({"text": text, "label": "", "note": "", "source": f"hn:{thread_id}"})
            kept += 1
            if kept == per_thread:
                break

        print(f"{thread_id}: kept {kept} of {len(comments)} top-level  ·  {title[:60]}")

    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["text", "label", "note", "source"])
        writer.writeheader()
        writer.writerows(rows)

    long = sum(len(r["text"].split()) > WORDS_THE_MODEL_SEES for r in rows)
    print(f"\nWrote {len(rows)} comments to {out}.")
    print(f"{long} are longer than about {WORDS_THE_MODEL_SEES} words. The model reads only "
          f"their beginning, so when you label one of those, ask whether its label "
          f"is decided in the opening lines.")
    print("Collect more than you need. Some won't fit any label and some will need "
          "context you can't see, and you should skip both.")


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("threads", nargs="*", help="HN thread ids to collect from")
    parser.add_argument("--search", help="list threads matching a query instead of collecting")
    parser.add_argument("--limit", type=int, default=15, help="how many threads --search lists")
    parser.add_argument("--per-thread", type=int, default=40, help="most comments kept per thread")
    parser.add_argument("--seed", type=int, default=42, help="which comments get sampled")
    parser.add_argument("--out", default=OUT, help=f"output CSV (default {OUT})")
    parser.add_argument("--force", action="store_true", help="overwrite an existing output file")
    args = parser.parse_args()

    if args.search:
        search(args.search, args.limit)
    elif args.threads:
        collect(args.threads, args.per_thread, args.seed, args.out, args.force)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
