---
title: Gaps and next steps
tags: [guide, guide/gaps]
created: 2026-09-17
status: done
lang: en
---

# Gaps and next steps

↑ [[00-START-HERE]] · Türkçe: [[12-eksikler-ve-devam]]

This note records two things: the bugs **found and fixed** while writing
this guide, and what the repository **still does not do**. Sources:
`LEAN-DURUM.md`, `RAPOR.md` §2 and §6, and the checks made for this guide.

## A. Result bugs found and fixed

### A1. The `1/(1+x²)`, `a=1` coefficients lost floating-point precision

- **Where:** `taylor.py` → `katsayi_dizisi(expr, a, N)` passed the centre to
  `taylor_katsayilari` as a float (`1.0`).
- **Symptom:** by the closed form $c_n=(-1)^n2^{-(n+1)/2}\sin\frac{(n+1)\pi}4$,
  coefficients with $n\equiv3\pmod4$ are exactly zero. In the float
  computation those zeros vanished after $n=19$. The relative error was
  $1.1\times10^{-5}$ at $n=40$; at $n=60$ the coefficient was wrong
  **including its sign** ($+2.55\times10^{-9}$ instead of
  $-4.66\times10^{-10}$).
- **Impact:** the `1/(1+x^2), a=1` row of `cauchy_hadamard.md` showed 22.66 %
  for the ratio test and 1.66 % for C-H. README §4, `taylor-teori.tex` §3 and
  the note [[Yakınsaklık yarıçapı kompleks düzlemde belirlenir]] cited that
  number as evidence that "there is no limit".
- **Fix:** `katsayi_dizisi` now uses `sp.Rational(a)`. The table was
  regenerated: ratio test 1.4142 (0.00 %), C-H 1.4228 (0.61 %).
  `yakinsaklik_orani.py` gained a new table showing the ratio test cycling
  $\sqrt2\to1\to2\to2\to\sqrt2$ for $N=52..60$. The README, the theory text
  and the atomic note now describe that oscillation.
- **Not affected:** `kompleks_harita.py` ($N=28$) was rerun and its table came
  out byte-for-byte identical.

### A2. The "worst ratio" column exceeded 1 without explanation

`kalan_dogrulama.md` said the value "must never exceed 1", yet it does in 6
of 8 rows (largest: `ln(1+x)` 2.3593). The column is float64 and the
"meaningful regime" filter is approximate; the mpmath ratio at the same point
is 0.989.
**Fix:** the explanatory text of the script and table, and README §1, now say
so explicitly. Details:
[[10-seven-results#1. The Lagrange bound was never violated]]. The similar
values in the Octave demo (`cos` 1.0128, `ln(1+x)` 1.0654) are still not
confirmed at high precision there (see D3).

### A3. Video 6 presented barrier crossing as "anharmonicity"

At amplitude 1.3 the energy ($\approx9.49$) exceeded the barrier top
($\approx3.08$) and the particle left the well. The threshold amplitude is
$\approx0.784$.
**Fix:** `genlikler = [0.25, 0.5, 0.7]`; the video was re-rendered at
1080p60. Details: [[04-layer-manim]].

### A4. Frobenius's "normalizable" verdict used a single point

The old criterion was just `abs(psi) < 1.0` at $x=4$.
**Fix:** `hermite_incelemesi()` now computes $\int\psi^2dx$ over $[-4,4]$ and
$[-6,6]$; a ratio $<1.01$ means normalizable. The table gained a
**∫ψ² oranı (L=6 / L=4)** column: $1.000000$–$1.000085$ for integer
$\lambda$, and $9.5\times10^6$ and $1.0\times10^6$ for $\lambda=2.5$ and $3.7$.

### A5. `|` characters in Markdown tables

The `|z|` header in `analitik_degil.md` and the new Frobenius header's `|ψ|`
split the table columns. **Fix:** the headers are now `mutlak z` (absolute z)
and `∫ψ²`.

### A6. Still open: the Python Lagrange bound is sampled on a grid

`lagrange_sinir()` takes the sup on a 20,001-point grid; the docstring of
`lagrange_sinir_yavas` acknowledges the "under-estimation risk". It was not
triggered (0 confirmed violations), but the bound is not exact. The Octave
layer takes the sup **exactly** from closed forms. **Not fixed.**

## B. Stale or wrong references that were fixed

| File | Problem | Now |
|---|---|---|
| `02-python/src/taylor.py` | referred to a non-existent `01-taylor-kavramsal-temel.md` | [[Taylor açılımı bir tanım değil zorunluluktur]] |
| `05-godot/project.godot` | `testler/test_kendini.gd`; constants "identical to `s06_denge.py`" | `test_dogrulama.gd`, `sarkac.py` |
| `05-godot/taylor_explorer.gd` | pre-fix `-Im(...)` comment | `(-1)^n * Im(...)` |
| `05-godot/denge_oyunu.gd` | "takes minutes at 5°" (since $\lvert\Delta\theta\rvert\le2\theta_0=10°$, the threshold is never crossed at 5°) | corrected |
| `Makefile` | non-existent `./yap.ps1` | Windows note points to the guide |
| `00-teori/taylor-teori.tex` | "(twice)"; only 2232 in §2 | "(three times)"; "2224–2232" |
| `README.md`, `RAPOR.md` | installed `requirements.txt` (with manim) into the Python 3.14 environment | manim filtered out, `.venv313` separate |
| `dogrula.sh` | could not find `.venv\Scripts\python.exe` or Octave on Windows | looks for both |

## C. Platform gaps (open)

- **MATLAB was never run.** It crashed at start-up on Fedora 44 (LXE builtin
  registry error) and was not installed on Windows. The `.m` files were
  verified only in Octave (10.3.0 and 11.3.0).
- **The LaTeX step is skipped by `dogrula.sh` on Windows** (no `make`), and
  since MiKTeX leaves 1 babel warning, it could not pass `teori_dogrula`'s
  "0 warnings" requirement anyway. Verify LaTeX by hand on Windows
  ([[01-environment-setup#LaTeX]]).
- **The web page was tested only in Chrome.**
- **No continuous integration (CI).**

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

1. **Plot the ratio-test oscillation.** Turn the oscillation table in
   `yakinsaklik_orani.py` into a plot for $N=20..60$.
2. **Radius of the pendulum series.** $T(\theta_0)/T_0=\frac2\pi K(\sin^2\frac{\theta_0}2)$.
   $K(m)$ is analytic off $m\in[1,\infty)$, and the nearest complex
   $\theta_0$ with $\sin^2(\theta_0/2)\ge1$ is $\pm\pi$. Expectation: the
   series in $\theta_0$ has radius $\pi$ (the pendulum balanced upright,
   $T\to\infty$). **Not measured in the repository.** A quick mpmath trial
   while writing this guide gave a ratio test of 3.195 at 60 terms, still
   decreasing: consistent with $\pi$, but not a proof. It links results 3 and 5.
3. **High-precision confirmation in Octave.** Re-measure the float64
   candidates with the Octave `symbolic` package (`vpa`).
4. **Lean item 2.** $V'(x_0)=0$ ⇒ $V(x)-V(x_0)-\frac12V''(x_0)(x-x_0)^2=o((x-x_0)^2)$.
5. **A separate `dogrula.ps1`** that also runs LaTeX on Windows.
6. **Padé approximants.** The classic way past Taylor's radius wall. Compare
   Padé and Taylor for `ln(1+x)` or `arctan(x)` at $x>1$ (`1/(1+x²)` is
   rational, so [2/2] Padé reproduces it exactly).
7. **Close A6.** Take the Python sup from closed forms too.
8. **A Firefox test** and **GitHub Actions** (`taylor.py`, the `node` test and
   the Godot headless test run in minutes; Lean needs the Mathlib cache).

## E. Limits of this guide

- Some Linux commands (e.g. installing with `grep -v '^manim'`) were **not
  tested** on Fedora; they are marked as such.
- The fixes were made and verified on Windows: `taylor.py`, the three
  regenerated tables, the Godot test, the Octave demo, `pdflatex` ×3, and the
  1080p60 render of video 6. `kalan_dogrulama.py` was **not** rerun (on
  Windows it reports 2232 candidates); only the explanatory text of its table
  changed.
- Screenshots and video stills were produced on a Windows machine.
- Session durations are estimates.
