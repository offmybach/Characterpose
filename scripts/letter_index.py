#!/usr/bin/env python3
"""
Build an index of every letter in every letters-*.md / letter-*.md file, and
answer "does this person already have a letter?"

Why this exists
---------------
Three separate times this session, a naive matcher invented gaps that weren't
real and nearly caused duplicate letters to be written. The failures were:

1. Only matching "### N. Name" headings. Ten files use other formats — the
   MAESP/NAESP file uses "## N.", Delaware and the standalone letter-*.md
   files use "#", letters-consider-tier-64.md uses no headings at all, and
   the grandparents file uses sub-lettered numbers (3b, 7a). That hid roughly
   130 letters.
2. Dropping single-letter tokens. "J.J. McCorvey" and "R P Stevens" collapse
   to one token and vanished.
3. Name-form drift between the LinkedIn export and the letter files:
   pronouns "(he/him)", a trailing " SME", an appended " - Author of ...",
   an honorific "Mrs.", one more credential than the heading carries.

Use this instead of writing another one-off regex.

    from letter_index import build, find
    idx = build()
    hit = find(idx, "Mrs. Karima Onque, M.Ed, MA")   # -> ('letters-gap-educators.md', '930')
"""
import re, glob, os, unicodedata

# Credential and honorific tokens that are never part of a person's name.
CRED = set("""med mba phd edd ms msa mls mlis cpa cfp cfa afc cfei ccufc ncsp lssp psy jr sr
ii iii ceo mcom bsc cia cft cdfa ncpm cds crps cka ea dipfa cii mp cmt cfte nbct oct ma ph
eds ed d s cae sfo mpas ceft sme codc mat mse ded rn lcsw""".split())
HONORIFIC = re.compile(r'^\s*(mr|mrs|ms|miss|dr|prof|professor)\b\.?\s*', re.I)

# Headings that are section titles rather than people.
#
# NOTE: do NOT use re.X here. Verbose mode strips literal spaces from the
# pattern, which turned "the " into "the" and silently skipped every person
# whose name starts with those letters — Theresa, Theodore, Thelma. Two real
# letters went missing that way before it was caught. Keep the spaces literal
# and keep this on one line.
SKIP = re.compile(
    r'^(letters|whales|lane|top \d|the |why |on |correction|step \d|batch|'
    r'everything else|academic|gatekeeper|kids.finance|peer author|press|credit union|'
    r'district|media|educators|financial|government|nonprofit|other|authors|pta|'
    r'librarian|superintend|send |what|how|status|read me|these are|send these)', re.I)

HEAD  = re.compile(r'^#{1,3}\s+(?:[\U0001F400-\U0001FAFF☀-➿️]+\s*)*'
                   r'(?:(\d+[a-z]?)\.\s*)?(.+?)\s*$', re.M)
PLAIN = re.compile(r'^(\d+)\.\s+(.+?)\s+·', re.M)   # letters-consider-tier-64.md style


def _clean(s):
    s = str(s or '')
    s = re.sub(r'\([^)]*\)', '', s)          # (he/him), (She/Her)
    s = re.sub(r'\s+[-–—]\s+.*$', '', s)     # " - Author of 'The Sloth Investor'"
    s = HONORIFIC.sub('', s)
    return s.strip(' ,·|')


def norm(s):
    """Full normalised form, credentials and all."""
    s = unicodedata.normalize('NFKD', _clean(s))
    s = ''.join(c for c in s if not unicodedata.combining(c)).lower()
    return ' '.join(re.sub(r'[^a-z0-9 ]', ' ', s).split())


def base(s):
    """Just the name: everything before the first comma, credentials dropped."""
    n = norm(re.sub(r'\s*,.*$', '', _clean(s)))
    toks = [t for t in n.split() if t not in CRED]
    return ' '.join(toks)


def variants(name):
    """Every form worth indexing or looking up, longest first."""
    out = []
    for v in (norm(name), base(name)):
        if v and len(v.split()) >= 2 and v not in out:
            out.append(v)
    return out


def build(root='.'):
    idx = {}
    files = sorted(glob.glob(os.path.join(root, 'letters*.md')) +
                   glob.glob(os.path.join(root, 'letter-*.md')))
    for path in files:
        f = os.path.basename(path)
        text = open(path, encoding='utf-8').read()
        for m in HEAD.finditer(text):
            nm = m.group(2).strip()
            if SKIP.match(nm) or len(nm) < 4 or nm.startswith('|'):
                continue
            for v in variants(nm):
                idx.setdefault(v, (f, m.group(1) or ''))
        for m in PLAIN.finditer(text):
            for v in variants(m.group(2)):
                idx.setdefault(v, (f, m.group(1)))
    return idx


def find(idx, name):
    """Return (file, number) if this person already has a letter, else None."""
    for v in variants(name):
        if v in idx:
            return idx[v]
    return None


if __name__ == '__main__':
    import sys
    idx = build()
    print('%d indexed name forms across %d files'
          % (len(idx), len(set(v[0] for v in idx.values()))))
    for probe in sys.argv[1:]:
        print('%-46s -> %s' % (probe[:46], find(idx, probe) or 'NO LETTER'))
