#!/usr/bin/env python3
"""
Clarence Gets a Bargain — bespoke outreach generator.

Reads the categorized FinLit contact spreadsheet and writes a personalized
EMAIL + LinkedIn message for every Tier-1 and Strong contact, grouped by the
10 bespoke email groups defined in the workbook.

Voice rules (see CLAUDE.md): Jonathan Bach's voice — punchy, declarative, warm,
self-aware. No marketing slop, no AI tells, no finance puns. Spoiler guard:
never reveal the Clarence/Clearance wordplay or explain the "Wyze" pun.

The spreadsheet holds real people's names/titles/locations and is intentionally
NOT committed to this repo. Pass its path on the command line:

    python3 outreach/generate_outreach.py /path/to/contacts.xlsx

Output (also git-ignored) lands in outreach/drafts/.
"""
import sys
import os
import csv
import re
import hashlib
from collections import defaultdict, Counter

import openpyxl

# Set this once and the signature drops into every draft.
BOOK = "Clarence Gets a Bargain"
SITE = "www.clarencegetsabargain.com"
AUTHOR = "Jonathan Bach"

# Outreach priority tiers, and the named sets you can target from the CLI.
TIER_TAG = {
    "Custom Email - Tier 1": "TIER 1",
    "Strong Personalized Outreach": "Strong",
    "Consider Custom Email": "Consider",
}
TIER_RANK = {"Custom Email - Tier 1": 0, "Strong Personalized Outreach": 1,
             "Consider Custom Email": 2}
TIER_SETS = {
    "core": {"Custom Email - Tier 1", "Strong Personalized Outreach"},
    "consider": {"Consider Custom Email"},
    "all": set(TIER_TAG),
}

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "drafts")

# --------------------------------------------------------------------------- #
# Per-group voice. Order matters: drives the NN- file prefixes.
# Each group: subjects[], email_bodies[], linkedin[], ask, role_default,
# plus optional opener patterns. {first}{opener}{opener_li}{ask}{fact}{sig}
# --------------------------------------------------------------------------- #

SIG = f"Thanks,\n{AUTHOR}\nAuthor, {BOOK}\n{SITE}"

FACTS = [
    "36 pages, 16+ money concepts, written for ages 6-10. Not one worksheet in sight.",
    "It teaches budgeting, comparison shopping, and markdowns inside the plot instead of bolting them on after.",
    "A K-5 teacher with 30+ years in the classroom helped shape the lessons, so it holds up in front of real kids.",
    "The whole financial education hides inside one Sea-Mart shopping trip.",
]

GROUPS = {
    "Classroom, school, curriculum, and library practitioners": {
        "slug": "classroom-library-practitioners",
        "subjects": [
            "A money book your students might actually finish",
            "Built for your classroom, not bolted on after",
            "Would this work with your kids? Honest answer wanted.",
        ],
        "openers": [
            "Your work{org_clause} is exactly why your name is on my short list.",
            "Here's why I'm writing you specifically: {role}{org_clause}.",
            "You do this for real{org_clause}, so I want your read before anyone else's.",
        ],
        "openers_li": [
            "I noticed your work{org_clause}.",
            "You do this for real{org_clause}, so your read matters more than mine.",
        ],
        "email_bodies": [
            "Hi {first},\n\n{opener}\n\nI wrote a children's book called {BOOK}. It's a story first. A kid earns a robot for good grades and chores, then has to go shop for it and learns how money actually works along the way. {fact}\n\nWhat I can't tell from my desk is whether it lands where it counts: a classroom, a library shelf, or a backpack headed home. {ask}\n\n{sig}",
            "Hi {first},\n\n{opener}\n\nQuick why-I'm-writing: I wrote {BOOK}, a 36-page picture book that teaches kids real money skills without ever feeling like a lecture. A K-5 teacher with 30+ years in the classroom helped shape the lessons, so it's built to hold up in front of actual students.\n\n{ask}\n\n{sig}",
        ],
        "linkedin": [
            "Hi {first}, {opener_li} I wrote a kids' book, {BOOK}, that sneaks a real money education inside a story about a kid and a robot. Built with a 30-year K-5 teacher so it holds up in a classroom. Could I send you a copy and get your honest read on whether it'd work with your students?",
            "Hi {first}, quick one. I wrote {BOOK}, a picture book that teaches kids money skills through a story instead of a worksheet. You do this for real, so your opinion beats mine. Mind if I send a copy your way?",
        ],
        "ask": "Want a copy to look at? I'll send the book and the zero-prep educator toolkit, and all I want back is whether it'd actually work with your kids.",
        "role_default": "educator",
    },
    "Personal-finance media and broad-audience storytellers": {
        "slug": "personal-finance-media",
        "subjects": [
            "Story idea: the money book kids actually read",
            "A kid, a robot, and a sneaky financial education",
            "For your money coverage: quick pitch",
        ],
        "openers": [
            "I've been reading your work{org_clause}, so you already know the gap I'm trying to close.",
            "Here's why I'm writing you specifically: {role}{org_clause}.",
            "Your audience{org_clause} is exactly who this is for.",
        ],
        "openers_li": [
            "I've been following your work{org_clause}.",
            "Your money coverage{org_clause} is right in this lane.",
        ],
        "email_bodies": [
            "Hi {first},\n\n{opener}\n\nHere's the story in a sentence: I snuck a financial education inside a children's book about a kid and a robot. {BOOK} follows a 7-year-old who earns a robot, then has to actually shop for it. Budgeting, comparison shopping, markdowns, the works, and not one worksheet. {fact}\n\n{ask}\n\n{sig}",
            "Hi {first},\n\n{opener}\n\nMost money advice talks to adults. I wrote a children's book that makes the family money conversation concrete and a little funny instead of scary. It's called {BOOK}. A kid earns a robot, then learns what it actually costs to bring one home.\n\n{ask}\n\n{sig}",
        ],
        "linkedin": [
            "Hi {first}, {opener_li} I wrote a children's book, {BOOK}, that hides a real financial education inside a story about a kid and a robot. Might be a fun angle for your audience: the money book kids actually finish. Want a review copy or a quick summary?",
            "Hi {first}, story idea for you. {BOOK} is a picture book that teaches kids how money works through a robot-shopping trip, no worksheet in sight. Happy to send a review copy, or point me to whoever covers this if it's not you.",
        ],
        "ask": "Happy to send a review copy or a two-line summary. And if money-for-kids isn't your lane, no hard feelings. Is there someone there I should talk to instead?",
        "role_default": "storyteller",
    },
    "Financial wellness educators, coaches, and practitioners": {
        "slug": "financial-wellness-coaches",
        "subjects": [
            "Does this make the concepts stick? Your call.",
            "A kids' money book: practitioner gut-check",
            "You know behavior change better than I do",
        ],
        "openers": [
            "You spend your days getting money concepts to actually stick{org_clause}.",
            "Here's why I'm writing you specifically: {role}{org_clause}.",
            "Your work{org_clause} means you'll spot in five minutes whether this works.",
        ],
        "openers_li": [
            "I saw your work{org_clause}.",
            "You get money concepts to stick for a living{org_clause}.",
        ],
        "email_bodies": [
            "Hi {first},\n\n{opener}\n\nI wrote a children's book that tries to do the same thing for kids. It's called {BOOK}. It teaches budgeting, Wants vs. Needs, and comparison shopping through a story about a kid shopping for a robot, not through a lecture. {fact}\n\n{ask}\n\n{sig}",
            "Hi {first},\n\n{opener}\n\nI wrote {BOOK}, a picture book that teaches kids real money habits inside a story. A kid earns a robot, then has to shop for it. You know what makes this stuff stick better than most people do.\n\n{ask}\n\n{sig}",
        ],
        "linkedin": [
            "Hi {first}, {opener_li} I wrote {BOOK}, a kids' book that teaches money habits through a story instead of a lecture. You know what makes this stuff stick better than most. Would you take a look and tell me if it does? Happy to send a copy.",
            "Hi {first}, quick practitioner gut-check. {BOOK} teaches kids budgeting and Wants vs. Needs through a robot-shopping story. Would you read it and tell me if it'd help the families you work with? I'll send a copy.",
        ],
        "ask": "Would you take a look and tell me, practitioner to practitioner, whether it'd help the families and kids you work with? Glad to send a copy.",
        "role_default": "financial educator",
    },
    "Financial-literacy coalitions and curriculum organizations": {
        "slug": "finlit-coalitions-curriculum",
        "subjects": [
            "A family-friendly supplement for your programming",
            "Where might a kids' money book fit in what you run?",
            "Clarence Gets a Bargain: aligned to Jump$tart, CCM, CCELA, CEE",
        ],
        "openers": [
            "Your work{org_clause} puts you right where I'm trying to learn.",
            "Here's why I'm writing you specifically: {role}{org_clause}.",
            "Given what you run{org_clause}, you'll know fast whether there's a fit.",
        ],
        "openers_li": [
            "I saw your work{org_clause}.",
            "Given what you run{org_clause}, you'll know fast whether there's a fit.",
        ],
        "email_bodies": [
            "Hi {first},\n\n{opener}\n\nI wrote {BOOK}, a children's book that teaches 16+ money concepts inside a story. A kid earns a robot, then learns to shop for it. It lines up with Jump$tart, Common Core Math, Common Core ELA, and the CEE standards, and it comes with a zero-prep educator toolkit. {fact}\n\n{ask}\n\n{sig}",
            "Hi {first},\n\n{opener}\n\n{BOOK} is a 36-page picture book that snuck a real financial education into a story about a kid and a robot. It's standards-aligned (Jump$tart, Common Core Math and ELA, CEE) and built for classroom, family, or library use.\n\n{ask}\n\n{sig}",
        ],
        "linkedin": [
            "Hi {first}, {opener_li} I wrote {BOOK}, a kids' book that teaches money through story and lines up with Jump$tart, Common Core, and CEE. Wondering where something like this might fit in your programming. Could I send you a copy?",
            "Hi {first}, {opener_li} {BOOK} is a standards-aligned picture book that teaches kids money skills through a robot-shopping story. Is there a spot for it in what you run: classroom, family night, library giveaway? Happy to send a copy.",
        ],
        "ask": "Is there a spot for something like this in what you're already running: classroom supplement, family night, library giveaway, enrichment? I'd value your read, and I'm glad to send a copy.",
        "role_default": "program lead",
    },
    "Federal Reserve and policy/institutional connectors": {
        "slug": "fed-policy-connectors",
        "subjects": [
            "Quick question on youth/family financial education",
            "Looking for the right person{org_subject}",
            "A referral question on financial education",
        ],
        "openers": [
            "I see your work{org_clause}, so you may know exactly the right person.",
            "Given your role{org_clause}, you're better placed than most to point me.",
            "Your work{org_clause} is why I'm asking you instead of guessing.",
        ],
        "openers_li": [
            "I see your work{org_clause}.",
            "Given your role{org_clause}, you'd know better than I would.",
        ],
        "email_bodies": [
            "Hi {first},\n\n{opener}\n\nI'm not pitching you anything. I'm trying to find the right door. I wrote a children's book on family money skills, {BOOK}, and I'm looking for whoever handles youth or family financial education, consumer education, or community learning on your side.\n\nIf a name comes to mind, I'd be grateful for the pointer. And if it's you, even better.\n\n{sig}",
            "Hi {first},\n\n{opener}\n\nThis is a referral question, not a pitch. I wrote {BOOK}, a kids' book on family money skills, and I'm trying to reach whoever works on youth or family financial education, consumer education, or community learning where you are. Any pointer would mean a lot.\n\n{sig}",
        ],
        "linkedin": [
            "Hi {first}, not pitching anything, just hoping you can point me in a direction. I wrote a kids' book on family money skills, {BOOK}, and I'm trying to find who handles youth or family financial education on your side. Any idea who I should talk to?",
            "Hi {first}, quick referral question. {BOOK} is a children's book on family money skills. Do you know who handles youth/family or consumer financial education where you are? Grateful for any pointer.",
        ],
        "ask": "",
        "role_default": "your institution",
    },
    "Parent, PTA, and family advocates": {
        "slug": "parent-pta-family",
        "subjects": [
            "Making the money talk at home a little easier",
            "For your PTA families: a money book that's actually fun",
            "Would this help families start the money conversation?",
        ],
        "openers": [
            "Your work{org_clause} is exactly the audience I had in mind.",
            "Here's why I'm writing you specifically: {role}{org_clause}.",
            "You help families directly{org_clause}, which is why I'm writing you.",
        ],
        "openers_li": [
            "I saw your work{org_clause}.",
            "You work with families directly{org_clause}.",
        ],
        "email_bodies": [
            "Hi {first},\n\n{opener}\n\nThe money talk at home is awkward for most families. I wrote a children's book to give them an easier way in. It's called {BOOK}. A kid earns a robot, then has to shop for it, and parents get a story to read together instead of a lecture to give. {fact}\n\n{ask}\n\n{sig}",
            "Hi {first},\n\n{opener}\n\nI wrote {BOOK}, a picture book that turns the family money talk into a story a kid actually wants to read. A robot is involved. It's built to make that first conversation easy for parents.\n\n{ask}\n\n{sig}",
        ],
        "linkedin": [
            "Hi {first}, {opener_li} I wrote {BOOK}, a kids' book that gives families an easy, funny way into the money talk. A kid earns a robot, then learns to shop for it. Could I send you a copy?",
            "Hi {first}, quick one. {BOOK} helps families start the money conversation through a story instead of a lecture. Think it'd help your families? Happy to send a copy.",
        ],
        "ask": "Would something like this help the families you work with start the conversation? Glad to send a copy your way.",
        "role_default": "family advocate",
    },
    "Children's books, publishing, and educational storytelling": {
        "slug": "childrens-books-publishing",
        "subjects": [
            "Fellow kid-lit author looking for your read",
            "Positioning a financial-literacy picture book",
            "One author to another: quick ask",
        ],
        "openers": [
            "You've done the thing I'm in the middle of{org_clause}.",
            "Here's why I'm writing you specifically: {role}{org_clause}.",
            "Your work{org_clause} means you know this market far better than I do.",
        ],
        "openers_li": [
            "I saw your work{org_clause}.",
            "One kid-lit person to another{org_clause}.",
        ],
        "email_bodies": [
            "Hi {first},\n\n{opener}\n\nI wrote {BOOK}, a picture book that teaches kids real money skills through a story. A kid earns a robot, then learns to shop for it. {fact}\n\nAny read you have on positioning it, or getting it in front of the right people, would mean a lot. Happy to trade copies.\n\n{sig}",
            "Hi {first},\n\n{opener}\n\n{BOOK} is my picture book that sneaks a money education into a story about a kid and a robot. I'm at the positioning-and-distribution stage and would value the read of someone who's been there.\n\n{ask}\n\n{sig}",
        ],
        "linkedin": [
            "Hi {first}, one kid-lit author to another. I wrote {BOOK}, a picture book that sneaks a money education into a story about a kid and a robot. Would value any read you have on positioning or distribution. Happy to trade copies?",
            "Hi {first}, {opener_li} I just wrote {BOOK}, a financial-literacy picture book. Any wisdom on getting it in front of the right people? Happy to trade copies.",
        ],
        "ask": "Any read on positioning or distribution would mean a lot. Happy to trade copies.",
        "role_default": "author",
    },
    "Public-sector financial education / consumer protection": {
        "slug": "public-sector-fined",
        "subjects": [
            "A family-facing money book: where might it fit?",
            "Supporting public financial-education goals",
            "Youth/family financial education: quick question",
        ],
        "openers": [
            "Your work{org_clause} is exactly where I'm trying to learn.",
            "Here's why I'm writing you specifically: {role}{org_clause}.",
            "Given your role{org_clause}, you'll know whether there's any fit here.",
        ],
        "openers_li": [
            "I saw your work{org_clause}.",
            "Given your role{org_clause}, you'll know whether there's a fit.",
        ],
        "email_bodies": [
            "Hi {first},\n\n{opener}\n\nI wrote a children's book on family money skills, {BOOK}. A kid earns a robot, then learns budgeting, comparison shopping, and markdowns by shopping for it. {fact}\n\nI'm trying to understand where a family-facing book like this might support public financial-education work: a school, library, family, or consumer-education pathway. {ask}\n\n{sig}",
            "Hi {first},\n\n{opener}\n\n{BOOK} is a picture book that teaches kids real money skills through a story. I'm trying to learn where a family-facing book fits in public financial-education or consumer-education work, and who decides that.\n\n{ask}\n\n{sig}",
        ],
        "linkedin": [
            "Hi {first}, {opener_li} I wrote {BOOK}, a kids' book on family money skills. Trying to learn where a family-facing book like this might fit in public financial-education or consumer-education work. Could I send you a copy and get your read?",
            "Hi {first}, quick question. {BOOK} teaches kids money skills through a story. Is there a school, library, or consumer-education pathway where something like this fits on your side? Happy to send a copy.",
        ],
        "ask": "If there's a fit, or a better person to ask, I'd be grateful for your perspective. Glad to send a copy.",
        "role_default": "program analyst",
    },
    "Individual review / one-off custom": {
        "slug": "individual-one-off",
        "subjects": [
            "A kids' money book: your read?",
            "Financial education, in picture-book form",
        ],
        "openers": [
            "Your work{org_clause} is why your name is on a very short list.",
            "Given your work{org_clause}, I wanted to ask you directly.",
        ],
        "openers_li": [
            "I saw your work{org_clause}.",
            "Given your work{org_clause}, I wanted to ask directly.",
        ],
        "email_bodies": [
            "Hi {first},\n\n{opener}\n\nI wrote {BOOK}, a children's book that teaches real money skills through a story. A kid earns a robot, then has to shop for it. {fact}\n\nGiven your work in financial education, I'd value your honest read on whether it'd be useful for the families or learners you reach. Glad to send a copy.\n\n{sig}",
        ],
        "linkedin": [
            "Hi {first}, {opener_li} I wrote {BOOK}, a kids' book that teaches money skills through a story about a kid and a robot. Given your work in financial education, I'd value your read. Could I send you a copy?",
        ],
        "ask": "I'd value your honest read on whether it'd be useful for the families or learners you reach. Glad to send a copy.",
        "role_default": "financial educator",
    },
    "Community impact and nonprofit program leaders": {
        "slug": "community-nonprofit",
        "subjects": [
            "A family money book for community programs",
            "Could this be useful for a program or giveaway?",
        ],
        "openers": [
            "Your work{org_clause} is the kind of program I had in mind.",
            "Given your work{org_clause}, I wanted to ask whether this could be useful.",
        ],
        "openers_li": [
            "I saw your work{org_clause}.",
            "Given your work{org_clause}, I wanted to ask.",
        ],
        "email_bodies": [
            "Hi {first},\n\n{opener}\n\nI wrote {BOOK}, a children's book that teaches money skills through a story about a kid and a robot. I'm wondering whether a small, easy family-money book could be useful for a community program, giveaway, or workshop.\n\n{ask}\n\n{sig}",
        ],
        "linkedin": [
            "Hi {first}, {opener_li} I wrote {BOOK}, a kids' book that teaches money skills through a story. Could a small family-money book be useful for a community program or giveaway? Happy to send a copy.",
        ],
        "ask": "If there's a fit on your side, I'd be glad to send a copy.",
        "role_default": "program lead",
    },
}

GROUP_ORDER = list(GROUPS.keys())

GENERIC_ACCOUNTS = {
    "", "bank", "account", "self-employed", "self employed", "freelance",
    "n/a", "none", "retired", "various",
}
CRED_TOKENS = re.compile(
    r",?\s*\b(ph\.?d\.?|mba|m\.?ed\.?|ed\.?d\.?|cfp|cfei|cfa|afc|clu|cpa|aca|"
    r"cflp|apfi|ipa|la|cpffe|csc|cfe)\b\.?",
    re.I,
)


def first_name(name):
    n = re.sub(r"\(.*?\)", " ", name)              # drop parentheticals
    quoted = re.findall(r'"([^"]+)"', name)         # prefer a quoted nickname
    if quoted:
        return quoted[0].strip().title()
    n = CRED_TOKENS.sub(" ", n)
    n = n.split(",")[0]
    tok = n.strip().split()
    if not tok:
        return "there"
    f = tok[0]
    if f.isupper() or f.islower():
        f = f.title()
    return f


# LinkedIn-bio slop we refuse to parrot back into an opener (see CLAUDE.md).
SLOP = re.compile(
    r"\b(empower\w*|unlock\w*|leverag\w*|transform\w*|elevat\w*|supercharg\w*|"
    r"passionate|thought leader|guru|ninja|rockstar|visionary|game.?chang\w*|"
    r"disrupt\w*|synerg\w*)\b",
    re.I,
)
# Institution names that read better with a leading "the".
THE_ORG = re.compile(
    r"^(federal|consumer|council|department|office|national|board|bureau|"
    r"division|u\.s\.|united states|center|centre|institute|coalition)\b",
    re.I,
)


def clean_role(title, default):
    if not title:
        return default
    # Split on real separators and on OCR'd pipes (" | " often scans as " I "/" l ").
    seg = re.split(r"[;|]|\s[IlL]\s", title)[0]
    seg = re.sub(r"^[^A-Za-z]+", "", seg).strip()
    seg = seg.strip(" -–—|;,")
    if len(seg.split()) > 9 or len(seg) < 3:
        return default
    if SLOP.search(seg):            # don't echo buzzword self-descriptions
        return default
    if seg.isupper():
        seg = seg.title()
    return seg or default


def org_phrase(org):
    """' at the Federal Reserve Board' vs ' at NPR'."""
    if not org:
        return ""
    article = "the " if THE_ORG.match(org) else ""
    return f" at {article}{org}"


def clean_org(account, name):
    if not account:
        return ""
    # Sales-Navigator exports often duplicate the org after a ';' with OCR
    # garbage ("Federal Reserve Bank of Cleveland; gpclpral Rank nf Cleveland").
    org = re.split(r"[;]", account)[0]
    org = re.sub(r"\(\+\s*[^)]*\)", "", org)        # drop "(+2)" / "(+ I)" tails
    org = org.split(",")[0]                          # drop ", Inc." etc.
    org = org.replace("®", "").replace("™", "").strip(" -–—|;,")
    low = org.lower()
    if low in GENERIC_ACCOUNTS or len(org) < 2:
        return ""
    if org and (org.lower() in name.lower() or name.split()[0].lower() in org.lower()):
        return ""   # account is really the person's own name
    return org


def pick(options, key):
    h = int(hashlib.md5(key.encode("utf-8")).hexdigest(), 16)
    return options[h % len(options)]


def build(contact):
    grp = contact["Bespoke Email Group"]
    g = GROUPS[grp]
    name = contact["Name"]
    first = first_name(name)
    role = clean_role(contact.get("Title", ""), g["role_default"])
    org = clean_org(contact.get("Account", ""), name)

    org_clause = org_phrase(org)
    # avoid "Director of X ... at X" duplication
    if org and org.split()[0].lower() in role.lower():
        org_clause = ""
    org_subject = org_phrase(org)

    opener = pick(g["openers"], name + "o").format(
        role=role, role_low=role[0].lower() + role[1:], org_clause=org_clause
    )
    opener_li = pick(g["openers_li"], name + "l").format(
        role=role, role_low=role[0].lower() + role[1:], org_clause=org_clause
    )
    fact = pick(FACTS, name + "f")

    subject = pick(g["subjects"], name + "s").format(org_subject=org_subject)
    body = pick(g["email_bodies"], name).format(
        first=first, opener=opener, ask=g["ask"], fact=fact, sig=SIG, BOOK=BOOK
    )
    li = pick(g["linkedin"], name + "li").format(
        first=first, opener_li=opener_li, BOOK=BOOK
    )
    # tidy any doubled spaces / stray "  " from empty clauses
    body = re.sub(r"[ \t]{2,}", " ", body)
    li = re.sub(r"[ \t]{2,}", " ", li)
    return {
        "first": first, "role": role, "org": org,
        "subject": subject, "email": body, "linkedin": li,
    }


def load_contacts(path, priorities):
    wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    ws = wb["High Value Targets"]
    rows = list(ws.iter_rows(values_only=True))
    hdr = [str(c) if c else "" for c in rows[0]]
    idx = {h: i for i, h in enumerate(hdr)}
    out = []
    for r in rows[1:]:
        if not any(c is not None and str(c).strip() for c in r):
            continue
        rec = {h: ("" if r[i] is None else str(r[i]).strip()) for h, i in idx.items()}
        if rec.get("Custom Email Priority") in priorities:
            out.append(rec)
    return out


def main():
    import argparse
    ap = argparse.ArgumentParser(description="Generate bespoke outreach drafts.")
    ap.add_argument("xlsx", help="path to the FinLit contacts workbook")
    ap.add_argument("--tiers", choices=sorted(TIER_SETS), default="core",
                    help="which priority set to draft (default: core = Tier-1 + Strong)")
    ap.add_argument("--outdir", default=None,
                    help="output dir name under outreach/ (default: drafts / drafts-<tiers>)")
    args = ap.parse_args()

    path = args.xlsx
    priorities = TIER_SETS[args.tiers]
    out_name = args.outdir or ("drafts" if args.tiers == "core" else f"drafts-{args.tiers}")
    OUT = os.path.join(HERE, out_name)
    contacts = load_contacts(path, priorities)
    os.makedirs(os.path.join(OUT, "by-group"), exist_ok=True)

    by_group = defaultdict(list)
    for c in contacts:
        by_group[c["Bespoke Email Group"]].append(c)

    csv_rows = []
    total = 0
    for gi, grp in enumerate(GROUP_ORDER, start=1):
        items = by_group.get(grp, [])
        if not items:
            continue
        items.sort(key=lambda c: (TIER_RANK.get(c["Custom Email Priority"], 9), c["Name"]))
        slug = GROUPS[grp]["slug"]
        lines = [f"# {grp}", "",
                 f"_{len(items)} contacts — {GROUPS[grp].get('note','')}_".replace(" — _", "_"),
                 ""]
        for c in items:
            d = build(c)
            total += 1
            tag = TIER_TAG.get(c["Custom Email Priority"], c["Custom Email Priority"])
            deg = c.get("LI Connection Degree", "")
            geo = c.get("Geography", "")
            meta = " · ".join(x for x in [tag, f"{deg} degree" if deg else "", geo] if x)
            preview = re.split(r"[;|]|\s[IlL]\s", c.get("Title", ""))[0]
            preview = re.sub(r"^[^A-Za-z]+", "", preview).strip()[:120]
            lines += [
                f"## {c['Name']}",
                f"*{meta}*  ",
                f"*{preview}*",
                "",
                f"**Email — subject:** {d['subject']}",
                "",
                "```",
                d["email"],
                "```",
                "",
                "**LinkedIn:**",
                "",
                "```",
                d["linkedin"],
                "```",
                "",
                "---",
                "",
            ]
            csv_rows.append({
                "Priority": c["Custom Email Priority"],
                "Bespoke Group": grp,
                "Name": c["Name"],
                "First Name": d["first"],
                "Title": c.get("Title", "").split(";")[0],
                "Account": c.get("Account", ""),
                "Geography": geo,
                "LI Degree": deg,
                "Email Subject": d["subject"],
                "Email Body": d["email"],
                "LinkedIn Message": d["linkedin"],
            })
        with open(os.path.join(OUT, "by-group", f"{gi:02d}-{slug}.md"), "w") as f:
            f.write("\n".join(lines))

    # combined CSV
    fields = ["Priority", "Bespoke Group", "Name", "First Name", "Title", "Account",
              "Geography", "LI Degree", "Email Subject", "Email Body", "LinkedIn Message"]
    with open(os.path.join(OUT, "clarence_outreach_drafts.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(csv_rows)

    print(f"Generated {total} contacts across {len(by_group)} groups.")
    print("Group counts:", dict(Counter(c['Bespoke Email Group'] for c in contacts)))
    print("Output:", OUT)


if __name__ == "__main__":
    main()
