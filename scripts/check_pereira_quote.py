#!/usr/bin/env python3
"""Fail if Pam Pereira's review has drifted anywhere on the site.

Canonical text is section 2 of reference/pereira-review.md. Full renderings must match it
exactly; short renderings must be an exact contiguous excerpt of it. Nothing is allowed to
be paraphrased, restitched, or 'improved' by an editing pass.

Run after touching any review markup:  python3 scripts/check_pereira_quote.py
"""
import html
import re
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def norm(s: str) -> str:
    """Strip markup and typographic variation so only the words are compared."""
    s = re.sub(r"<[^>]+>", " ", s)
    s = html.unescape(s)
    s = unicodedata.normalize("NFKC", s)
    s = s.replace("“", "").replace("”", "").replace("’", "'")
    s = s.replace("\\'", "'").replace('\\"', '"')
    s = re.sub(r"\s+", " ", s)
    # stripping inline tags (<em>title</em>.) can leave a space before punctuation
    s = re.sub(r"\s+([.,;:!?])", r"\1", s)
    return s.strip()


def canonical() -> str:
    src = (ROOT / "reference" / "pereira-review.md").read_text()
    blocks = re.findall(r"```\n(.*?)\n```", src, re.S)
    if len(blocks) < 2:
        sys.exit("reference/pereira-review.md is missing its fenced text blocks")
    return norm(blocks[1])          # section 2 = the approved text


def renderings():
    out = []

    idx = (ROOT / "index.html").read_text()
    m = re.search(r'"name": "Pam Pereira".*?"reviewBody": "(.*?)"', idx, re.S)
    if m:
        out.append(("index.html JSON-LD", norm(m.group(1)), True))
    m = re.search(r'<p class="t-quote">(.*?)</p>\s*<div class="t-author">Pam Pereira', idx, re.S)
    if m:
        out.append(("index.html pull-quote", norm(m.group(1)), False))

    rc = (ROOT / "review-cards.html").read_text()
    m = re.search(r'name:"Pam Pereira".*?text:"(.*?)",img:', rc, re.S)
    if m:
        out.append(("review-cards.html", norm(m.group(1)), False))

    pk = (ROOT / "press-kit.html").read_text()
    m = re.search(r'Pam Pereira &mdash; Attorney.*?<div class="bio"[^>]*>(.*?)\n</div>', pk, re.S)
    if m:
        out.append(("press-kit.html full review", norm(m.group(1)), True))

    return out


def main() -> int:
    want = canonical()
    found = renderings()
    if not found:
        print("FAIL  no renderings found — did the markup change shape?")
        return 1

    failures = 0
    for label, got, is_full in found:
        ok = (got == want) if is_full else (got and got in want)
        print(("PASS  " if ok else "FAIL  ") + label + ("  [full]" if is_full else "  [excerpt]"))
        if not ok:
            failures += 1
            print("   got: " + got[:200])
            print("   ref: " + want[:200])

    if failures:
        print(f"\n{failures} rendering(s) no longer match her approved text.")
        print("Do not 'fix' the site to match a rewrite. Either revert the markup, or —")
        print("if she approved new wording — update section 2 of reference/pereira-review.md")
        print("and log it. Section 1 is what she wrote and never changes.")
        return 1

    print(f"\nAll {len(found)} renderings match. Quote intact.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
