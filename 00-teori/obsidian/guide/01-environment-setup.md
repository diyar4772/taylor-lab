---
title: Environment setup (Windows and Linux)
tags: [guide, guide/setup]
created: 2026-09-17
status: done
lang: en
---

# Environment setup

↑ [[00-START-HERE]] · → [[02-study-plan]] · Türkçe: [[01-ortam-kurulumu]]

All commands are run **from the repository root** (`taylor-lab/`). Every tool
has a **Windows (PowerShell)** block followed by a **Linux (bash, Fedora)**
block. What each layer needs:

| Layer | Needs | Required? |
|---|---|---|
| [[03-layer-python]] | Python + `requirements.txt` | Yes; the basis of most sessions |
| [[04-layer-manim]] | manim 0.19 + ffmpeg + LaTeX | No; videos are ready in `out/videolar/` |
| [[05-layer-theory-latex]] | pdflatex | No; the PDF is ready in `out/taylor-teori.pdf` |
| [[06-layer-octave]] | GNU Octave | For session 5 |
| [[07-layer-lean]] | elan + Lean 4.34.0 + Mathlib (~11 GB) | For session 10 |
| [[08-layer-godot]] | Godot 4.7 | For session 8 |
| [[09-layer-web]] | Python (local server) + browser; Node for its test | Sessions 1, 4, 8 |

> [!note] Verification record
> The Windows commands below were run on Windows 11 + Python 3.13.7. The
> Linux commands were run on Fedora 44, according to the repository's own
> records (README "Doğrulama durumu", `RAPOR.md`). Anything not run is
> marked **(not tested)**.

---

## Python

### The two virtual environments: `.venv` and `.venv313`

This only matters on systems whose Python is **3.14** (e.g. Fedora 44).

- `manim==0.19.0` requires `av>=9,<14`. `av` has no prebuilt wheel for
  Python 3.14 (the oldest is 15.1.0), so pip tries to build it from source
  and fails on the ffmpeg headers.
- Solution: a 3.14 `.venv/` for the numerical scripts and a 3.13
  `.venv313/` **for manim only**.
- **On Windows, or on any system with Python 3.13**, one environment is
  enough: `requirements.txt` (including manim) installs cleanly on 3.13.

**Windows (PowerShell):**

The venv steps are **(not tested)**: verification used packages installed
directly into the system Python 3.13. The `taylor.py` line was run.

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\Activate.ps1
# If you get "running scripts is disabled" (once):
#   Set-ExecutionPolicy -Scope CurrentUser RemoteSigned

python 02-python\src\taylor.py      # last line: "Tüm kontroller geçti." (all checks passed)
```

**Linux (bash, Python 3.14):**

```bash
python3 -m venv .venv
grep -v '^manim' requirements.txt > /tmp/req-numeric.txt   # leave manim out (pitfall 1)
.venv/bin/pip install -r /tmp/req-numeric.txt
source .venv/bin/activate

# manim only:
python3.13 -m venv .venv313
.venv313/bin/pip install -r requirements.txt

python 02-python/src/taylor.py
```

> [!warning] About the `grep -v` line
> `requirements.txt` contains `manim==0.19.0`; installing it unchanged into
> 3.14 fails while building `av` (`RAPOR.md` §2.3). That
> is why the README and RAPOR filter manim out. The line is **(not tested)**
> on Fedora.

To open the notebook (`jupyterlab` is in the requirements):

```powershell
jupyter lab 02-python\notebooks\taylor-laboratuvari.ipynb
```

```bash
jupyter lab 02-python/notebooks/taylor-laboratuvari.ipynb
```

---

## Manim (optional)

System dependencies: **ffmpeg** and a **LaTeX** distribution (for `MathTex`).

**Windows:**

```powershell
winget install Gyan.FFmpeg
winget install MiKTeX.MiKTeX

# Quick preview (854x480, 15 fps). Does NOT touch out/videolar:
cd 01-manim
manim -ql --disable_caching scenes\s01_artan_derece.py ArtanDereceSahnesi
# output: 01-manim\media\videos\s01_artan_derece\480p15\ArtanDereceSahnesi.mp4
cd ..
```

**Linux:**

```bash
sudo dnf install -y ffmpeg python3.13 texlive-dvisvgm texlive-doublestroke

# Quick preview, leaves out/videolar alone:
(cd 01-manim && PATH="$PWD/../.venv313/bin:$PATH" manim -ql --disable_caching scenes/s01_artan_derece.py ArtanDereceSahnesi)

# All six scenes at 1080p60, OVERWRITES out/videolar (pitfall 3):
PATH="$PWD/.venv313/bin:$PATH" bash 01-manim/render.sh
```

---

## LaTeX

The theory text needs **three passes** (after two, "Label(s) may have
changed" is still reported).

**Windows (MiKTeX):**

```powershell
cd 00-teori
1..3 | ForEach-Object { pdflatex -interaction=nonstopmode -enable-installer taylor-teori.tex | Out-Null }
cd ..
# output: 00-teori\taylor-teori.pdf (8 pages)
```

**Linux (TeX Live):**

```bash
sudo dnf install -y texlive-enumitem texlive-babel-turkish texlive-hyphen-turkish
make teori          # 3 passes + copies to out/taylor-teori.pdf
```

---

## Octave

**Windows:** winget does **not** put Octave on the PATH; use the full path.

```powershell
winget install --id GNU.Octave --exact
$oct = (Get-ChildItem "$env:LOCALAPPDATA\Programs\GNU Octave\*\mingw64\bin\octave-cli.exe" | Select-Object -First 1).FullName
cd 03-matlab-octave
& $oct --no-gui --quiet demo_calistir.m
cd ..
```

**Linux:**

```bash
sudo dnf install -y octave
(cd 03-matlab-octave && octave-cli --no-gui --quiet demo_calistir.m)
```

---

## Lean

The project pins an **explicit version** (`04-lean/lean-toolchain` →
`leanprover/lean4:v4.34.0`). Total download is ~11 GB (toolchain + Mathlib).

**Windows:**

```powershell
winget install --id Lean.Elan --exact
cd 04-lean
elan toolchain install leanprover/lean4:v4.34.0
lake exe cache get      # Mathlib's prebuilt .olean files (~8900 files)
lake build              # expected last line: "Build completed successfully (2777 jobs)."
cd ..
```

If `elan toolchain install` fails with the error below, your network cannot
resolve `release.lean-lang.org` (pitfall 5):

```text
error: error during download
info: caused by: [6] Could not resolve hostname (Could not resolve host: release.lean-lang.org)
```

Install the toolchain straight from GitHub. The following block was run
and verified in **Git Bash**:

```bash
curl -L -o /tmp/lean.zip https://github.com/leanprover/lean4/releases/download/v4.34.0/lean-4.34.0-windows.zip   # ~850 MB
mkdir -p ~/.elan/toolchains/_tmp && unzip -q /tmp/lean.zip -d ~/.elan/toolchains/_tmp
mv ~/.elan/toolchains/_tmp/lean-4.34.0-windows ~/.elan/toolchains/leanprover--lean4---v4.34.0
rmdir ~/.elan/toolchains/_tmp
elan toolchain list      # -> leanprover/lean4:v4.34.0
```

**Linux:**

```bash
curl https://elan.lean-lang.org/elan-init.sh -sSf | sh     # if elan is missing
export PATH="$HOME/.elan/bin:$PATH"
cd 04-lean && lake exe cache get && lake build
```

If the same DNS problem appears on Linux, follow the manual steps in
`LEAN-DURUM.md` → "Windows'taki engel nasıl aşıldı" (how the block was worked around).

---

## Godot

**Windows:**

```powershell
winget install --id GodotEngine.GodotEngine --exact
godot --path 05-godot                            # scene 1: Taylor explorer
godot --path 05-godot res://denge_oyunu.tscn     # scene 2: equilibrium game
godot --headless --path 05-godot --script res://test_dogrulama.gd   # "SONUC: 0 hata" (0 errors)
```

**Linux:**

```bash
sudo dnf install -y godot
godot --path 05-godot
godot --path 05-godot res://denge_oyunu.tscn
godot --headless --path 05-godot --script res://test_dogrulama.gd
```

---

## Web

`06-web/index.html` is a single file with no external dependencies. The
repository notes that Chrome will not open it via `file://`; use a local server.

**Windows:**

```powershell
python -m http.server 8765
# browser: http://localhost:8765/06-web/index.html
node 06-web\test_matematik.mjs      # "SONUC: 0 hata / 34 kontrol" (0 errors / 34 checks)
```

**Linux:**

```bash
python3 -m http.server 8765
node 06-web/test_matematik.mjs
```

Without Node: Windows `winget install OpenJS.NodeJS.LTS` **(not tested)**,
Linux `sudo dnf install -y nodejs`.

---

## Verifying everything with one command

**Linux:**

```bash
make dogrula          # everything
make dogrula-hizli    # everything except Lean
```

**Windows:** there is no `make`, but `bash dogrula.sh --hizli` runs in Git
Bash. It looks for Python at `.venv/bin/python` or `.venv/Scripts/python.exe`,
and for Octave on the PATH or under `%LOCALAPPDATA%\Programs\GNU Octave\`.
Without `make` it marks the LaTeX step **ATLANDI** (skipped). On a Windows
machine with no `.venv`, the result was `GEÇTİ 4 · KALDI 0 · ATLANDI 4`
(passed 4, failed 0, skipped 4: Python and LaTeX, plus Lean because of
`--hizli`). Verify the skipped ones one by one:

```powershell
python 02-python\src\taylor.py
python 02-python\src\kalan_dogrulama.py      # note: rewrites out\ (pitfall 4)
node 06-web\test_matematik.mjs
godot --headless --path 05-godot --script res://test_dogrulama.gd
cd 03-matlab-octave; & $oct --no-gui --quiet demo_calistir.m; cd ..
cd 04-lean; lake build; cd ..
```

---

## Pitfalls

Sources: `RAPOR.md` §2, `LEAN-DURUM.md`, and the tests run
while writing this guide.

1. **manim does not install on Python 3.14.** `av<14` has no cp314 wheel.
   Run manim from a 3.13 environment; do not install `requirements.txt`
   unchanged into 3.14.
2. **Do not mix the two environments.** If `.venv313` is active, do not run
   the numerical scripts there. Call manim with the
   `PATH="$PWD/.venv313/bin:$PATH"` prefix.
3. **`render.sh` overwrites `out/videolar/`.** For low-quality experiments
   call `manim -ql` directly (output goes to `01-manim/media/`, git-ignored),
   not `render.sh`.
4. **The Python scripts rewrite `out/`.** Scripts such as
   `kalan_dogrulama.py` regenerate the tables and PNGs. Because of platform
   differences (candidate count 2232 on Windows, 2224 on Fedora) you may see
   changes in `git status`. To undo: `git restore out/`.
5. **Lean: `release.lean-lang.org` does not resolve on some networks.**
   Commands that need a channel name (`elan default stable`,
   `elan toolchain install stable`) fail. **Do not run** `elan default stable`:
   even if it succeeded it would move the default away from v4.34.0 and
   Mathlib's `.olean` files would no longer match. Install the explicit
   version from GitHub (above).
6. **`04-lean/.lake` is ~8 GB.** It is in `.gitignore`; never commit it. If
   deleted, `lake exe cache get` downloads it again.
7. **TeX Live does not fetch missing `.sty` files** (MiKTeX does). On a
   "File ... not found" error, install the matching `texlive-*` package with `dnf`.
8. **MiKTeX can hang silently.** `-interaction=nonstopmode` alone was not
   enough: `pdflatex` waited without output while asking to install a
   package. `-enable-installer` fixed it. On Windows the last pass leaves 1
   warning (`Package babel Warning: Configuration files are deprecated`);
   this is MiKTeX-specific, and Fedora reports 0 warnings.
9. **The web page does not open via `file://`** (Chrome). Use
   `python -m http.server`.
10. **Octave is not on the PATH on Windows.** Use the `$oct` variable.
11. **MATLAB was never run in this repository.** The `.m` files were only
    verified in Octave; MATLAB crashed at start-up on Fedora 44 (`RAPOR.md` §2.1).
12. **The Windows console may garble Turkish characters.** The scripts
    switch their own output to UTF-8 via `ortam.py`. One-liner
    `python -c` commands need `$env:PYTHONIOENCODING="utf-8"`.
