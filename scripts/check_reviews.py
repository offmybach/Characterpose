#!/usr/bin/env python3
"""Verify every review on the site against reference/reviews-of-record.md.

Full renderings must match the record exactly. Short renderings must be an exact
contiguous excerpt — clipping a sentence short or joining two sentences that were not
adjacent both fail, because both put words in a reviewer's mouth.

    python3 scripts/check_reviews.py
"""
import html
import re
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def norm(s: str) -> str:
    s = re.sub(r"<[^>]+>", " ", s)
    s = html.unescape(s)
    s = unicodedata.normalize("NFKC", s)
    s = s.replace("“", "").replace("”", "").replace("’", "'")
    s = s.replace("\\'", "'").replace('\\"', '"').replace("\\u2014", "—")
    s = re.sub(r"\s+", " ", s)
    s = re.sub(r"\s+([.,;:!?])", r"\1", s)
    return s.strip()


def records() -> dict:
    """Reviewer name -> canonical text, from the '## Name' + fenced block pairs."""
    txt = (ROOT / "reference" / "reviews-of-record.md").read_text()
    txt = txt.split("## Approved short forms")[0]
    out = {}
    for m in re.finditer(r"\n## ([^\n]+)\n(.*?)```\n(.*?)\n```", txt, re.S):
        out[m.group(1).strip()] = norm(m.group(3))
    return out


def key(name: str) -> str:
    """Identity is the first two name tokens, so 'Josie K.' == 'Josie K., Age 10'
    and 'Wally Luckeydoo, Ed.D.' == 'Wally Luckeydoo'."""
    toks = re.findall(r"[a-z]+", norm(name).lower())
    return "".join(toks[:2])


def renderings():
    out = []  # (surface, displayed_name, text, is_full)

    idx = (ROOT / "index.html").read_text()
    for m in re.finditer(r'"name": "([^"]+)",\s*"jobTitle": "[^"]*"\s*\},\s*"reviewBody": "(.*?)"', idx, re.S):
        out.append(("index.html JSON-LD", m.group(1), norm(m.group(2)), True))
    for m in re.finditer(r'<p class="t-quote">(.*?)</p>\s*<div class="t-author">([^<]+)</div>', idx, re.S):
        out.append(("index.html testimonials", norm(m.group(2)), norm(m.group(1)), False))
    for m in re.finditer(r"drawReview\(c, m, [^,]+, w - m\*2, cH,\s*'(.*?)',\s*'(.*?)'\s*\)", idx, re.S):
        who = norm(m.group(2)).lstrip("—").split("·")[0].split(",")[0].strip()
        out.append(("index.html magazine", who, norm(m.group(1)), False))

    rc = (ROOT / "review-cards.html").read_text()
    for m in re.finditer(r'\{name:"([^"]+)".*?text:"(.*?)",img:', rc, re.S):
        out.append(("review-cards.html", m.group(1), norm(m.group(2)), False))

    pk = (ROOT / "press-kit.html").read_text()
    m = re.search(r"Pam Pereira &mdash; Attorney.*?<div class=\"bio\"[^>]*>(.*?)\n</div>", pk, re.S)
    if m:
        out.append(("press-kit.html", "Pam Pereira", norm(m.group(1)), True))

    return out


def main() -> int:
    recs = records()
    by_key = {key(n): (n, t) for n, t in recs.items()}
    found = renderings()
    if not found:
        print("FAIL  no renderings found — did the markup change shape?")
        return 1

    failures = 0
    for surface, name, text, is_full in found:
        hit = by_key.get(key(name))
        if not hit:
            print(f"FAIL  {surface:<24} {name}  — no entry in reviews-of-record.md")
            failures += 1
            continue
        canon_name, canon = hit
        ok = (text == canon) if is_full else (text and text in canon)
        kind = "full" if is_full else "excerpt"
        print(f"{'PASS' if ok else 'FAIL'}  {surface:<24} {canon_name:<28} [{kind}]")
        if not ok:
            failures += 1
            print(f"    got: {text[:150]}")
            print(f"    ref: {canon[:150]}")

    print()
    if failures:
        print(f"{failures} rendering(s) do not match the record.")
        print("A short version must be an exact contiguous run of the canonical text.")
        print("Fix the page, not the record — unless the reviewer approved new wording.")
        return 1
    print(f"All {len(found)} renderings match. {len(recs)} reviewers on record.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
