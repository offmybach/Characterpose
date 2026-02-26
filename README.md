# Characterpose

You are right: the **primary goal** is a prompt-based image search app.

This repo now includes a local app that can:
- scan/index images from your folders/drives,
- search by text prompts like "pile of newspaper" or "blue and white shoes",
- show matching results in a local UI,
- and (optionally) run duplicate cleanup with recovery bin.

## Yes — you can download everything at once (no Notepad copy/paste)

Use **one** of these options:

1. **GitHub ZIP (easiest)**
   - Open the repo page on GitHub.
   - Click **Code** → **Download ZIP**.
   - Extract it to a folder like `C:\ImageSearchApp`.

2. **Git clone (if Git is installed)**
   ```bash
   git clone <repo-url>
   ```

3. **GitHub Desktop**
   - File → Clone repository → choose local folder.

All required files come down with the correct file types automatically (`.py`, `.bat`, `.txt`, etc.).
You do **not** need to create files manually in Notepad.


## Do I need `git apply`?

Short answer: **No**, not for normal use.

- `git apply` is a developer command that applies a patch/diff file to source code.
- It is only needed if someone sends you a `.patch`/`.diff` instead of the full project files.
- For you, the easiest path is still: **Code → Download ZIP** and extract it.

So no — copying code into Notepad is **not** your only option, and usually you should avoid that.


## Where is the GitHub page?

If you are asking this, the project may **not be published to GitHub yet**.

How to check quickly:
- If someone gave you a GitHub link, that is the page to use.
- If you have no link, ask the person who shared the files for the repository URL.
- In this copy of the project, there is no configured Git remote URL, so a GitHub page cannot be auto-detected from here.

If you want your own GitHub page for this project:
1. Create a new empty repository on GitHub.
2. Upload this folder (or push with Git/GitHub Desktop).
3. Then use that new repo page's **Code → Download ZIP** button.

So the issue is likely exactly what you suspected: you may be working from a local copy that is not connected to a GitHub repo URL yet.


## What changed in the latest update (plain English)

Latest update focused on reliability/troubleshooting:
- Indexing now prints a `scan_summary` per source folder/drive (exists + candidate image count).
- Drive path handling is safer (`C:` is treated as `C:\\`).
- UI launcher now pins Streamlit to local defaults (`127.0.0.1:8501`) and disables usage stats prompt noise.

If you already have a working folder, these are the only files changed in that update:
- `image_prompt_search.py`
- `run_image_search_windows.bat`
- `README.md`

## Which files do you need to copy/paste?

You should **not** need copy/paste if you can use GitHub **Code -> Download ZIP**.

If ZIP still fails and you must manually copy files, use this minimum set in one folder:
- `setup_windows.bat`
- `run_image_search_windows.bat`
- `diagnose_windows.bat`
- `image_prompt_search.py`
- `streamlit_image_search_app.py`
- `requirements-image-search.txt`

Optional (only for duplicate cleanup):
- `run_dedupe_windows.bat`
- `image_dedupe_manager.py`
- `requirements-image-dedupe.txt`

Also create `python_path.txt` in the same folder with one line:
`C:\PortableTools\python-3.12.10-amd64\python.exe`

## What to keep together

Keep these files in the same extracted folder:
- `setup_windows.bat`
- `diagnose_windows.bat`
- `run_image_search_windows.bat`
- `run_dedupe_windows.bat`
- `image_prompt_search.py`
- `streamlit_image_search_app.py`
- `image_dedupe_manager.py`
- `requirements-image-search.txt`
- `requirements-image-dedupe.txt`

Important: there is no separate “dedupe folder.” Dedupe is handled by files (`run_dedupe_windows.bat` + `image_dedupe_manager.py`) in the same app folder.
If any of those files are missing, download the latest ZIP again and extract to a fresh folder (for example `C:\ImageSearchApp`) before running setup.


## Quick fix (if you are stuck right now)

Do these 6 steps exactly:

1. Put the project in one clean folder, e.g. `C:\ImageSearchApp`.
2. In that folder, create `python_path.txt` with one line:
   `C:\PortableTools\python-3.12.10-amd64\python.exe`
3. In File Explorer, open `C:\ImageSearchApp`, click the address bar, type `cmd`, press Enter.
4. Run: `setup_windows.bat`
5. Wait for `[OK] core modules import successfully`
6. Start app: `run_image_search_windows.bat ui`

If it still shows `K:\...python_embeded`, you are running a different copy of the `.bat` files; search for duplicate `setup_windows.bat` and delete old copies.

## Hard pivot summary (what changed)

This project now uses a **no-venv setup** on Windows:
- `setup_windows.bat` installs dependencies into `./.deps`
- launchers set `PYTHONPATH` to `./.deps`
- this avoids the `No module named venv` failure path entirely

If you can run normal Python + pip, this app can run without creating a virtual environment.

## 1) One-time setup (Windows)

1. Install Python 3.11+ from [python.org](https://www.python.org/downloads/).
2. Open your extracted folder.
3. Double-click `setup_windows.bat`.

You can run the scripts in **either** of these ways:
- **Double-click way (easiest):** double-click the `.bat` file in File Explorer. If no command is provided, launchers now open an interactive menu instead of closing immediately.
- **Terminal way (recommended for seeing errors):** open Command Prompt in that folder, then type the `.bat` command.

### What “same folder” means (important)

“Same folder” means the directory that contains these files together:
- `setup_windows.bat`
- `run_image_search_windows.bat`
- `diagnose_windows.bat`
- `python_path.txt` (if you use the C: override)

Example of a correct folder:
- `C:\ImageSearchApp\`

In that case, `python_path.txt` should be:
- `C:\ImageSearchApp\python_path.txt`

### How to open a terminal in that exact folder

1. Open File Explorer.
2. Browse to your project folder (example: `C:\ImageSearchApp`).
3. Click the address bar, type `cmd`, press Enter.
4. A Command Prompt opens already in the right folder.
5. Run commands there, for example:

```bat
setup_windows.bat
run_image_search_windows.bat ui
```

## 2) Build your image index (first run)

Open **Command Prompt** in this folder and run:

```bat
run_image_search_windows.bat index "D:\Photos" "E:\Archive"
```

This scans images and creates `./.image_search_index`.

Tips for drive-level indexing on Windows:
- Prefer root drives without a trailing slash in quotes: `"C:" "D:" "E:"`
- Or target known media folders first (`Pictures`, camera dumps, archives) to validate quickly.
- If indexing fails, the script now prints a `scan_summary` showing each source path, whether it exists, and how many candidate image files were found.

## 3) Launch the search app UI

```bat
run_image_search_windows.bat ui
```

Then use the local browser page to type prompts and view matching images.

## 4) Quick CLI search (optional)

```bat
run_image_search_windows.bat search blue and white shoes
```

## Optional: duplicate cleanup tool

If you also want duplicate cleanup with app recycle bin, use:

```bat
run_dedupe_windows.bat scan "D:\Photos"
run_dedupe_windows.bat scan-visual "D:\Photos"
run_dedupe_windows.bat restore
```

## Notes

- Prompt search quality depends on the model and image quality.
- Re-run `index` when you add many new images.
- Everything runs locally on your machine (no cloud required by this tool itself).


## If you hit an error after setup

I could not open your shared ChatGPT link from this environment (network/proxy blocked), so I added a one-click local diagnostics script.

Run this in your tool folder:

```bat
diagnose_windows.bat
```

It checks:
- Python installed and selected correctly
- `.deps` exists (local dependency folder)
- required modules installed (`Pillow`, `numpy`, `sentence-transformers`, `streamlit`, `imagehash`)
- app Python files compile

Then follow the suggested next command it prints.

If it still fails, copy the exact error text from that window and share it.


## Force the app to use your C: Python (avoid ComfyUI K: embedded Python)

If diagnostics show paths like `K:\...\python_embeded\python.exe`, create a file named:

`python_path.txt`

in this project folder, with exactly one line, for example:

`C:\PortableTools\python-3.12.10-amd64\python.exe`

Then run:

```bat
setup_windows.bat
```

All launchers in this repo (`setup_windows.bat`, `run_image_search_windows.bat`, `run_dedupe_windows.bat`, `diagnose_windows.bat`) prefer `python_path.txt` first.

Important: keep `python_path.txt` in the same folder as the `.bat` files.
The scripts switch to their own folder first, so this works even if you launch from another directory.

This pivot removes virtualenv dependency entirely: setup installs packages into a local `.deps` folder and launchers set `PYTHONPATH` to use it.


## If you STILL see `K:\...\python_embeded\python.exe`

You are almost certainly running an older copy of `setup_windows.bat` from a different folder.

Do this exactly:
1. In the folder where your `.bat` files are, run `diagnose_windows.bat`.
2. Confirm it prints `Script folder: ...` at the top and check that path is the one you expect.
3. In that **same folder**, create `python_path.txt` with one line only:
   `C:\PortableTools\python-3.12.10-amd64\python.exe`
4. Run `setup_windows.bat` from that same folder.

If you still get K:, you are launching a different script copy. Search your PC for duplicate `setup_windows.bat` files and remove old copies.


## What your latest diagnostic output means

Your output is actually good progress:
- It shows your C: Python is selected correctly.
- If `.deps` is missing, setup has not completed yet.
- Missing-module errors mean dependencies were not installed to `.deps` yet.

Run this next in the same folder:

```bat
setup_windows.bat
```
