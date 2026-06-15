# Windows install walkthrough — clawbot LinkedIn sync

Copy-paste each block into **Windows PowerShell**. Manual (non-PowerShell) steps
are marked 👉. Verify lines tell you what "good" looks like. If a command behaves
differently, your OpenClaw version may have renamed it — run it with `--help`.

Have ready: an **Anthropic API key** (OpenClaw's brain runs on Claude; the
onboarding wizard asks for it).

---

## Step 1 — Base tools (Git + Python)

```powershell
winget install --id Git.Git -e --source winget
winget install --id Python.Python.3.12 -e --source winget
```

👉 Close this PowerShell window and open a **new** one (so PATH picks up git +
python), then verify:

```powershell
git --version
python --version
```

## Step 2 — Get the project and the engine's dependency

```powershell
cd $HOME
git clone https://github.com/offmybach/Characterpose.git
cd Characterpose
git checkout claude/tender-pascal-e27bzj
python -m pip install openpyxl
```

👉 The first `git clone` opens a browser to sign in to GitHub — approve it. The
skill now lives at `$HOME\Characterpose\tools\contact-sync`.

## Step 3 — Install OpenClaw

```powershell
iwr -useb https://openclaw.ai/install.ps1 | iex
```

👉 An onboarding wizard runs (~2 min). Choose **Anthropic / Claude** as the model
provider and paste your API key. Then verify and set it to start with Windows:

```powershell
openclaw --version
openclaw doctor
openclaw gateway install
openclaw gateway status --json
```

`gateway status` should show it running on port 18789.

## Step 4 — Point OpenClaw at Edge

```powershell
openclaw config set browser.executablePath "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
```

Add your real Edge as the `user` profile. Open the config file:

```powershell
notepad "$HOME\.openclaw\openclaw.json"
```

👉 Add (or merge) this `browser` block, save, close. It's JSON5, so the comments
are fine:

```json5
{
  browser: {
    executablePath: "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe",
    profiles: {
      user: { driver: "existing-session", attachOnly: true }
    }
  }
}
```

The gateway watches this file and applies it automatically.

## Step 5 — Turn on Edge remote debugging (the fiddly one)

👉 In Edge, go to `edge://inspect/#remote-debugging` and enable remote debugging.
Keep Edge open and logged into LinkedIn. This is the step most likely to need a
tweak on your machine — if the bot later can't attach, run `openclaw doctor` and
check the browser section, and make sure Edge is actually open when you trigger
the sync.

## Step 6 — Install the skill

```powershell
cd $HOME\Characterpose
openclaw skills install .\tools\contact-sync --as linkedin-contact-sync
openclaw skills list
```

`skills list` should show **linkedin-contact-sync**. The engine `finlit_sync.py`
is copied in alongside it at `$HOME\.openclaw\skills\linkedin-contact-sync\`.

## Step 7 — Create the one-click job

```powershell
openclaw cron create "0 7 * * *" "Run the linkedin-contact-sync skill: open Edge to LinkedIn, go to My Network -> Connections (Recently added), collect new connections (max 25, read-only), and append them with finlit_sync.py." --name linkedin-sync --tz "America/New_York" --session isolated
openclaw cron list
```

The 7 AM time is just a placeholder — you trigger it by hand. (Adjust `--tz` to
your timezone.)

## Step 8 — Confirm the workbook path

The engine writes to
`C:\Users\mdmen\Downloads\finlit_contacts_categorized_bespoke_groups.xlsx`. Your
current file is named `..._updated_20260612.xlsx` — rename it to that exact name,
or tell me and I'll change the default in `finlit_sync.py`.

```powershell
Test-Path "C:\Users\mdmen\Downloads\finlit_contacts_categorized_bespoke_groups.xlsx"
```

Should print `True`.

---

## Daily use

1. Wake the PC, open Edge to LinkedIn (logged in).
2. Double-click `tools\contact-sync\sync-now.cmd` (pin it to your taskbar). Or, in
   an OpenClaw chat, type `/linkedin-contact-sync`.
3. Approve the Edge attach prompt once. The bot reads My Network for new
   connections and updates the workbook; review the new rows (flagged
   `auto-added by contact-sync` in Parse Notes).

**Babysit the first run** — that's where we'll see how LinkedIn's connection list
reads back and tune the skill if the bot grabs the wrong fields.

## If something's off

- `openclaw doctor` — checks config, gateway, and browser wiring.
- `openclaw gateway status --json` / `openclaw gateway restart`.
- Engine not found when the skill runs? Point it at the repo copy instead:
  `$HOME\Characterpose\tools\contact-sync\finlit_sync.py`.
- Test the engine alone, no browser, with a LinkedIn CSV export (see `README.md`):
  `python .\tools\contact-sync\finlit_sync.py --from-csv "$HOME\Downloads\Connections.csv" --dry-run`
