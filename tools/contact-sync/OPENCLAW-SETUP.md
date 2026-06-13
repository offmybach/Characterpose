# Wiring the clawbot — morning LinkedIn sync on Edge

This is the OpenClaw side: get the bot to open Edge each morning, check My Network
for new connections, and update the workbook. The skill is `SKILL.md`; the engine
it calls is `finlit_sync.py` (already built and tested). OpenClaw commands move
between versions — sanity-check each with `--help` if it doesn't behave.

## The one constraint to decide first

OpenClaw will **not** let an unattended/cron run drive your *real* logged-in Edge.
The "attach to your signed-in browser" mode requires you to approve an attach
prompt — so a fully hands-off cron can't use it. You pick one:

- **Attended (recommended).** Uses your real Edge + real LinkedIn login. Fires
  each morning, you approve one prompt, done. Lowest detection footprint, no
  re-login hassle. The "automation" is one click, which still beats exporting a
  CSV every time someone accepts.
- **Unattended (true zero-click cron).** A dedicated Edge automation profile you
  log into LinkedIn once. Cron fires hands-off each morning. Higher detection
  footprint (a persistent bot profile hitting LinkedIn daily) and you'll re-login
  whenever LinkedIn expires the session.

Everything below sets up both; use the section that matches your choice.

---

## 1. Install + gateway

Install OpenClaw and keep the **gateway running** (cron only fires while it's up —
set it to start with Windows). Then point it at Edge:

```bash
openclaw config set browser.executablePath "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe"
```

## 2. Install the skill

From this repo (the skill folder carries `finlit_sync.py` with it):

```bash
openclaw skills install ./tools/contact-sync --as linkedin-contact-sync
```

It lands in `~/.openclaw/skills/linkedin-contact-sync/` (so the engine path in
`SKILL.md` step 7 resolves). Confirm:

```bash
openclaw skills list
```

Install the engine's one dependency in the Python OpenClaw will call:

```bash
pip install openpyxl
```

## 3a. Attended mode — run it when you wake the PC and open LinkedIn (CHOSEN)

This matches "I wake the PC, open LinkedIn, and the bot updates the sheet."
Because *you* open LinkedIn, the session is already up and logged in — no timing
guesswork, and approving the one attach prompt is natural since you're right there.

Configure your real Edge as the `user` profile in `openclaw.json`:

```json5
{
  browser: {
    profiles: {
      user: { driver: "existing-session", attachOnly: true }
    }
  }
}
```

One-time in Edge: open `edge://inspect/#remote-debugging` and turn on remote
debugging.

Define the job once so you have a named trigger:

```bash
openclaw cron create "0 7 * * *" \
  "Run the linkedin-contact-sync skill: open Edge to LinkedIn, go to My Network -> Connections (Recently added), collect new connections (max 25, read-only), and append them with finlit_sync.py." \
  --name linkedin-sync --tz "America/New_York" --session isolated
```

The 7 AM time is a placeholder — in this mode you fire it by hand. (You can pause
the schedule so it only runs on demand; see `openclaw cron --help`. If it does
auto-fire while you're away it just finds no attachable session and stops.)

**Your morning:** wake PC → open Edge to LinkedIn → double-click `sync-now.cmd`
(pin it to the taskbar) → approve the attach prompt once. Done. `sync-now.cmd`
just runs `openclaw cron run linkedin-sync`. In an OpenClaw chat you can type
`/linkedin-contact-sync` instead.

**Want it to fire on its own at unlock?** Add a Windows Task Scheduler trigger
"On workstation unlock" that runs `sync-now.cmd` with a 1–2 minute delay (so Edge
and LinkedIn are open first). Less reliable than the one click — if LinkedIn isn't
up yet the run finds nothing and stops — so keep the shortcut as the fallback.

## 3b. Unattended mode (zero-click cron)

Use a dedicated managed Edge profile with its own data dir, logged into LinkedIn
once:

```json5
{
  browser: {
    profiles: {
      edge: {
        driver: "existing-session",
        attachOnly: true,
        userDataDir: "C:\\Users\\mdmen\\AppData\\Local\\Microsoft\\Edge\\ClawProfile"
      }
    }
  }
}
```

Log into LinkedIn in that profile once. Then schedule it:

```bash
openclaw cron create "0 7 * * *" \
  "Run the linkedin-contact-sync skill against the edge profile: open LinkedIn, go to My Network, collect new connections (max 25, read-only), append with finlit_sync.py." \
  --name linkedin-sync --tz "America/New_York" --session isolated
```

Check / manage it:

```bash
openclaw cron list
openclaw cron run linkedin-sync     # test now
```

Re-login in that profile whenever LinkedIn expires the session.

---

## What happens each run

The bot opens LinkedIn → My Network → Connections (Recently added), reads up to
25 new cards, writes them to `_new_connections.json`, and runs `finlit_sync.py`,
which classifies each person, routes them to the top of **Master** and their
category tab, copies the group's shared angle, **dedupes** against everyone
already in the sheet (so re-runs are safe), and **backs up** the workbook first.
You review the new rows (flagged `auto-added by contact-sync` in Parse Notes).

## If you'd rather skip OpenClaw entirely

The engine also runs off a LinkedIn CSV export with zero browser automation — see
`README.md`. Same result in the sheet, no account risk.

Sources: OpenClaw docs — [cron jobs](https://docs.openclaw.ai/automation/cron-jobs),
[skills](https://docs.openclaw.ai/tools/skills),
[browser](https://docs.openclaw.ai/tools/browser).
