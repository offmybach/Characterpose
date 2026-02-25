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

## What to keep together

Keep these files in the same extracted folder:
- `image_prompt_search.py`
- `streamlit_image_search_app.py`
- `run_image_search_windows.bat`
- `setup_windows.bat`
- `requirements-image-search.txt`

(Existing dedupe files can remain too.)

## 1) One-time setup (Windows)

1. Install Python 3.11+ from [python.org](https://www.python.org/downloads/).
2. Open your extracted folder.
3. Double-click `setup_windows.bat`.

## 2) Build your image index (first run)

Open **Command Prompt** in this folder and run:

```bat
run_image_search_windows.bat index "D:\Photos" "E:\Archive"
```

This scans images and creates `./.image_search_index`.

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
