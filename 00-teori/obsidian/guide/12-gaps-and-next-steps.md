---
title: Gaps and next steps
tags: [guide, guide/gaps]
created: 2026-09-17
status: done
lang: en
---

# Gaps and next steps

↑ [[00-START-HERE]] · Türkçe: [[12-eksikler-ve-devam]]

This note collects what the repository **does not do** or **gets wrong**.
Sources: `LEAN-DURUM.md`, `RAPOR.md` §2 and §6, and checks made while writing
this guide. The checks did not modify any repository file; experiments ran
in scratch files, and their commands are given in the relevant notes.

## A. Findings that affect results

### A1. The `1/(1+x²)`, `a=1` coefficients lose floating-point precision

- **Where:** `taylor.py` → `katsayi_dizisi(expr, a, N)` →
  `taylor_katsayilari(expr, a, N)`, with `a` passed as a float (`1.0`).
- **Symptom:** by the closed form $c_n=(-1)^n2^{-(n+1)/2}\sin\frac{(n+1)\pi}4$,
  coefficients with $n\equiv3\pmod4$ are exactly zero. In the float
  computation those zeros vanish after $n=19$. Relative error is
  $1.5\times10^{-9}$ at $n=28$ and $1.1\times10^{-5}$ at $n=40$; at $n=60$
  the coefficient is wrong **including its sign** ($+2.55\times10^{-9}$
  instead of $-4.66\times10^{-10}$).
- **Impact:** the `1/(1+x^2), a=1` row of `cauchy_hadamard.md`. With exact
  coefficients the ratio test gives 1.4142 (0.00 %) and C-H 1.4228
  (0.61 %); the table has 1.0938 (22.66 %) and 1.3907 (1.66 %). README §4,
  `taylor-teori.tex` §3 and the note
  [[Yakınsaklık yarıçapı kompleks düzlemde belirlenir]] cite 22.66 % as
  evidence that "there is no limit". The lesson is right; the number is
  contaminated. Correct evidence: the ratio test oscillating
  $1.41\to1\to2\to2\to1.41$ with $N$
  ([[10-seven-results#4. The same radius, from coefficients alone]]).
- **Not affected:** `kompleks_harita.py` uses $N=28$, where the relative error
  is ~$10^{-9}$, which does not change the map. The $a=0$ and $a=-1$ rows are
  also clean.
- **Suggested fix:** use `taylor_katsayilari(expr, sp.Rational(a), N)` inside
  `katsayi_dizisi` (as `_mpmath_katsayilari` already does), then regenerate
  the table and update the texts.

### A2. The "worst ratio" column exceeds 1 and this is not explained

The `kalan_dogrulama.md` table says the value "must never exceed 1 for the
theorem to hold", yet it does in 6 of 8 rows (largest: `ln(1+x)` 2.3593).
The column is float64, and the "meaningful regime" filter is approximate.
There is no violation (mpmath ratio 0.989), but the README shows the table
without explanation. Details:
[[10-seven-results#1. The Lagrange bound was never violated]]. The same
happens in the Octave demo (`cos` 1.0128, `ln(1+x)` 1.0654), and there is
**no** high-precision confirmation there.

### A3. The end of video 6 presents barrier crossing as "anharmonicity"

At amplitude 1.3 the energy ($\approx9.49$) exceeds the barrier top
($\approx3.08$) and the particle leaves the well; the plot is clipped at
$\pm1.6$, so this shows up as flat plateaus. The threshold amplitude is
$\approx0.784$. Details: [[04-layer-manim]].

### A4. Frobenius's "normalizable" verdict is a single point

`hermite_incelemesi()` applies `abs(psi) < 1.0` at $x=4$. That is not a
normalization integral. The verdict points the right way, but the criterion
is only an indicator. Improvement: look at how
$\int_{-L}^{L}\lvert\psi\rvert^2dx$ behaves as $L$ grows.

### A5. The Python Lagrange bound is sampled on a grid

`lagrange_sinir()` takes the sup on a 20,001-point grid; the docstring of
`lagrange_sinir_yavas` acknowledges the "under-estimation risk". It was not
triggered in kalan_dogrulama (0 confirmed violations), but the bound is not
exact. The Octave layer takes the sup **exactly** from closed forms.

## B. Stale or wrong references

| File | Problem |
|---|---|
| `02-python/src/taylor.py` (module docstring) | Refers to `00-teori/obsidian/01-taylor-kavramsal-temel.md`, which does not exist; its counterpart is [[Taylor açılımı bir tanım değil zorunluluktur]]. |
| `05-godot/project.godot` (comment) | Says `testler/test_kendini.gd`; the file is `test_dogrulama.gd`. Says the constants are "identical" to `s06_denge.py`; the equilibrium game uses the pendulum, not `s06`'s polynomial potential. |
| `05-godot/taylor_explorer.gd` | The first comment of the `1/(1+x^2)` block still quotes the pre-fix `-Im(...)` formula. |
| `05-godot/denge_oyunu.gd` (docstring) | Says "at 5° it takes minutes"; but $\lvert\Delta\theta\rvert\le2\theta_0=10°$, so the 10° threshold can **never** be exceeded at 5°. |
| `Makefile` (comment) | Mentions a PowerShell counterpart `./yap.ps1`; the file does not exist. |
| `00-teori/taylor-teori.tex` | Line 2 says "(twice)", but three passes are needed. §2 says 2232 candidates (the Windows count); the README says 2224 (Fedora). |
| `README.md` (setup) | `.venv/bin/pip install -r requirements.txt` will most likely fail on Python 3.14 because of `manim` → `av` ([[01-environment-setup#Pitfalls]]). |

## C. Platform gaps

- **MATLAB was never run.** It crashed at start-up on Fedora 44 (LXE builtin
  registry error) and was not installed on Windows. The `.m` files were
  verified only in Octave (10.3.0 and 11.3.0); MATLAB compatibility is a
  static check only.
- **No one-command verification on Windows.** There is no `make`.
  `dogrula.sh` runs in Git Bash but looks for `.venv/bin/python` and
  `octave-cli` on the PATH, so it skips 5 layers. A `dogrula.ps1` is missing.
- **The web page was tested only in Chrome.**
- **No continuous integration (CI).** Verification is run by hand.
- **LaTeX gives 1 warning on Windows** (MiKTeX babel "Configuration files
  are deprecated"); 0 on Fedora.

## Four topics left out of Lean

From `LEAN-DURUM.md` → "Kapsanmayanlar (bilerek)" (deliberately not covered):

1. **"R = distance to the nearest singularity"** is not stated formally.
   Even a concrete case such as $R=1$ for `1/(1+z²)` needs the theory of
   analytic continuation around poles.
2. **Pendulum / harmonic oscillator** is absent. `taylor_isLittleO` exists in
   Mathlib (signature in [[07-layer-lean]]) but was not used.
3. **Frobenius / quantization** is absent.
4. **No witness for $e^{-1/x^2}$ itself.** Mathlib's witness is
   `expNegInvGlue`, i.e. $e^{-1/x}$ for $x>0$.

So two of the seven results (5, 6) are entirely absent from Lean, and one (3)
is present only through its "converges absolutely inside the disk" half.

## D. Directions to extend (try it yourself)

1. **Fix A1.** A one-line change, rerun `yakinsaklik_orani.py`, update the
   README/tex/note text, and add a small plot of the ratio test oscillating with $N$.
2. **Radius of the pendulum series.** $T(\theta_0)/T_0=\frac2\pi K(\sin^2\frac{\theta_0}2)$.
   $K(m)$ is analytic off $m\in[1,\infty)$, and the nearest complex
   $\theta_0$ with $\sin^2(\theta_0/2)\ge1$ is $\pm\pi$. Expectation: the
   series in $\theta_0$ has radius $\pi$ (the pendulum balanced upright,
   $T\to\infty$). **Not measured in the repository.** A quick mpmath trial
   while writing this guide gave a ratio test of 3.195 at 60 terms, still
   decreasing: consistent with $\pi$, but not a proof. It could be added as a
   row to `yakinsaklik_orani.py`, linking results 3 and 5.
3. **High-precision confirmation in Octave.** Re-measure the float64
   candidates with the Octave `symbolic` package (`vpa`).
4. **Lean item 2.** $V'(x_0)=0$ ⇒ $V(x)-V(x_0)-\frac12V''(x_0)(x-x_0)^2=o((x-x_0)^2)$.
5. **`dogrula.ps1`.** A PowerShell counterpart of `dogrula.sh`: `.venv\Scripts\python.exe`,
   the full Octave path, `pdflatex -enable-installer`.
6. **Padé approximants.** The classic way past Taylor's radius wall. Adding a
   [2/2] Padé curve for `1/(1+x²)` to web panel 1 would show that "the wall
   belongs to the polynomial, not the function". Since that function is
   rational, [2/2] Padé reproduces it **exactly**; a more instructive
   experiment is comparing Padé and Taylor for `ln(1+x)` or `arctan(x)` at $x>1$.
7. **Normalization integral** (A4) and a **Firefox test** (C).
8. **GitHub Actions.** `taylor.py`, the `node` test and the Godot headless
   test run in minutes; Lean needs the Mathlib cache.

## E. Limits of this guide

- Some Linux commands (e.g. installing with `grep -v '^manim'`) were **not
  tested** on Fedora; they are marked as such.
- Screenshots and video stills were produced on a Windows machine; fonts may
  differ on other systems.
- Session durations are estimates.
