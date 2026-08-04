#!/usr/bin/env python3
"""
tidy_downloads.py — keep only the newest copy of each CGB file visible in Downloads.

Every older copy moves into  Downloads/CGB Outreach/<category>/  and every newest copy
stays where you can see it, even if only one version ever existed.

DOUBLE-CLICK IT. It shows you the plan, asks whether to go ahead, and waits before
closing so you can read what happened.

From a terminal, if you prefer:
    python tidy_downloads.py            # show the plan, then ask
    python tidy_downloads.py --go       # skip the question, just do it
    python tidy_downloads.py --go --downloads "D:/Stuff/Downloads"

Safe to run as often as you like. It never deletes, never overwrites, and never
touches a file it doesn't recognise as a CGB file.
"""
import argparse, os, re, shutil, sys
from pathlib import Path
from collections import defaultdict

FOLDER = "CGB Outreach"

# The only files worth having open. Everything else that is current but not in daily
# use is parked in CGB Outreach/current/ — still one click away, just not in your face.
WORKING_SET = [
    "send-queue.md",                    # the daily driver
    "cgb_master_outreach.xlsx",         # the database
    "handoff.md",                       # where things stand
    "heavy-hitters.md",                 # the voice
    "letters-new-aug.md",               # sending from these now
    "letter-erikk-bonner.md",
    "letters-whales-longform.md",
    "letters-grandparents-readalong.md",
]

# Which subfolder an older copy lands in. First match wins, so order matters.
RULES = [
    ("dbs",            r"^CGB_MASTER_outreach\.xlsx$|\.xlsx$|\.csv$"),
    ("packages",       r"\.zip$"),
    ("send-queue",     r"^SEND-QUEUE"),
    ("reference",      r"^(HANDOFF|heavy-hitters|phrasebank|deal-master-facts|reviews-of-record|pereira-review|voice-audit-humor|CLAUDE)"),
    ("contacts",       r"^(contacts-|organizations-target-list|parenting-orgs-target-list|mailing-list)"),
    ("person-letters", r"^letter-[a-z]"),                       # letter-erikk-bonner, letter-mia-russell
    ("new-additions",  r"^letters-(new-|grandparents-|whales-|top25-)"),
    ("letters",        r"^letters-|^jumpstart-clearinghouse|^roundup-outreach"),
    ("site-pages",     r"\.html?$"),
    ("playbooks",      r"^(marketing-blitz|disruptive-campaigns|seo-aeo|competitive-audit|outreach-playbook|linkedin-|research-)"),
]

# Only files matching one of these are touched at all.
KNOWN = re.compile(
    r"^(CGB[-_]|letters?-|jumpstart-|roundup-|contacts-|organizations-target|parenting-orgs|"
    r"mailing-list|HANDOFF|SEND-QUEUE|heavy-hitters|phrasebank|deal-master-facts|"
    r"reviews-of-record|pereira-review|voice-audit-humor|marketing-blitz|disruptive-campaigns|"
    r"seo-aeo|competitive-audit|outreach-playbook|linkedin-|vs-other-money-books|school-visits|"
    r"money-glossary|teaching-kids-about-money|grandparents-day-games|free-sample-print|"
    r"research-|clarence)", re.I)

# Never file these — they are the tool itself.
SELF = {"tidy_downloads.py", "tidy cgb downloads.bat"}

# Browser duplicate suffixes only: " (1)", " (2)", " copy", " copy 2".
# NOT "-1" — that would eat real names like letters-1-198.md and letters-199-396.md.
DUP = re.compile(r"(?:\s*\(\d+\)|\s+copy(?:\s+\d+)?)$", re.I)


PACKAGE = re.compile(r"^CGB[-_].*\.zip$", re.I)


def base_name(p: Path) -> str:
    """Strip browser duplicate suffixes so all copies of a file group together.

    Every CGB-*.zip is treated as one group: they are all 'the package', and only
    the newest one is worth having open."""
    if PACKAGE.match(p.name):
        return "__cgb_package__.zip"
    stem = p.stem
    prev = None
    while prev != stem:
        prev = stem
        stem = DUP.sub("", stem).rstrip()
    return (stem + p.suffix).lower()


def category(name: str) -> str:
    for folder, pat in RULES:
        if re.search(pat, name, re.I):
            return folder
    return "other"


def find_downloads() -> Path:
    for c in [Path.home() / "Downloads", Path.home() / "Downloads",
              Path(os.environ.get("USERPROFILE", "")) / "Downloads"]:
        if c.exists():
            return c
    sys.exit("Could not find your Downloads folder — pass --downloads \"C:/path/to/Downloads\"")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--go", action="store_true", help="actually move files")
    ap.add_argument("--downloads", help="path to your Downloads folder")
    ap.add_argument("--no-pause", action="store_true", help="don't wait for Enter at the end")
    ap.add_argument("--keep-all", action="store_true",
                    help="leave every current file visible instead of parking the ones you are not using")
    a = ap.parse_args()
    interactive = not a.go            # double-clicked, or run with no flags

    dl = Path(a.downloads) if a.downloads else find_downloads()
    if not dl.exists():
        sys.exit(f"No such folder: {dl}")
    archive = dl / FOLDER

    groups = defaultdict(list)
    for f in dl.iterdir():
        if f.is_dir() or f.name.startswith("."):
            continue
        if f.name.lower() in SELF or not KNOWN.match(f.name):
            continue
        groups[base_name(f)].append(f)

    if not groups:
        print(f"No CGB files found in {dl}")
        return

    keep, move, park = [], [], []
    for base, files in sorted(groups.items()):
        files.sort(key=lambda p: p.stat().st_mtime, reverse=True)   # newest first
        newest = files[0]
        for older in files[1:]:                                     # genuinely outdated
            move.append((older, archive / "superseded" / category(older.name) / older.name))
        if a.keep_all or PACKAGE.match(newest.name) or base in WORKING_SET:
            keep.append(newest)
        else:                                                       # current, just not in use
            park.append((newest, archive / "current" / category(newest.name) / newest.name))

    print(f"\nDownloads: {dl}")
    print(f"Archive:   {archive}\n")
    print(f"STAYS VISIBLE — newest of each ({len(keep)}):")
    for f in sorted(keep, key=lambda p: p.name.lower()):
        n = len(groups[base_name(f)])
        print(f"   {f.name}" + (f"   [newest of {n}]" if n > 1 else "   [only copy]"))

    def show(title, items):
        if not items: return
        print(f"\n{title} ({len(items)}):")
        by_cat = defaultdict(list)
        for src, dst in items:
            by_cat[str(dst.parent.relative_to(archive))].append(src.name)
        for cat in sorted(by_cat):
            print(f"   {cat}/")
            for n in sorted(by_cat[cat]):
                print(f"      {n}")

    show(f"OUTDATED COPIES -> {FOLDER}/superseded/", move)
    show(f"CURRENT BUT NOT IN USE -> {FOLDER}/current/", park)
    if not move and not park:
        print("\nNothing to file — Downloads is already tidy.")

    move += park

    if interactive:
        if not move:
            hold(a); return
        print()
        try:
            answer = input(f"File those {len(move)} into '{FOLDER}'?  [y/N] ").strip().lower()
        except EOFError:
            answer = ""
        if answer not in ("y", "yes"):
            print("\nNothing moved.")
            hold(a); return
    elif not move:
        return

    # 1. archive the older copies first, so the clean name is free
    done = 0
    for src, dst in move:
        dst.parent.mkdir(parents=True, exist_ok=True)
        final, i = dst, 2
        while final.exists():                       # never overwrite
            final = dst.with_name(f"{dst.stem} ({i}){dst.suffix}")
            i += 1
        shutil.move(str(src), str(final))
        done += 1

    # 2. then give each survivor its clean name back
    #    letters-new-aug (2).md  ->  letters-new-aug.md
    renamed = 0
    for f in keep:
        if PACKAGE.match(f.name) or not f.exists():
            continue                      # packages keep their real, dated names
        want = f.with_name(DUP.sub("", f.stem).rstrip() + f.suffix)
        if want != f and not want.exists():
            f.rename(want)
            renamed += 1

    print(f"\nFiled {done} files into {archive}")
    if renamed:
        print(f"Renamed {renamed} survivors back to their clean names.")
    print(f"{len(keep)} current files left visible in Downloads.")
    hold(a)


def hold(a):
    """Keep the window open when the script was double-clicked."""
    if getattr(a, "no_pause", False) or a.go:
        return
    try:
        input("\nDone. Press Enter to close.")
    except EOFError:
        pass


if __name__ == "__main__":
    try:
        main()
    except Exception as e:                 # never flash-and-vanish on an error
        print(f"\nSomething went wrong: {e}")
        try:
            input("\nPress Enter to close.")
        except EOFError:
            pass
