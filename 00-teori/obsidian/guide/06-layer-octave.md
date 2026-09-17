---
title: Layer — MATLAB / Octave
tags: [guide, guide/layer, octave]
created: 2026-09-17
status: done
lang: en
---

# Layer: MATLAB / Octave (`03-matlab-octave/`)

↑ [[00-START-HERE]] · Plan: session 5 · Türkçe: [[06-katman-octave]]

## What question does it answer?

"Does another language with another coefficient method reach the **same**
numbers?" Python produces coefficients by symbolic differentiation (sympy);
this layer uses **closed forms** (e.g. partial fractions). If both give the
same radius and the same Lagrange ratio, the result cannot be one
implementation's bug.

> [!warning] Never run in MATLAB
> The files are written in a MATLAB-compatible subset (`fprintf`, `~`, `%`
> comments, plain `end`, one main function per file) and were verified
> **only in GNU Octave**: 10.3.0 on Fedora, 11.3.0 on Windows. MATLAB
> compatibility was checked statically only (`RAPOR.md` §2.1).

## File by file

| File | What it does |
|---|---|
| `taylor_katsayilari.m` | `[kats, R, tekillikler] = taylor_katsayilari(ad, a, N)` (coefficients, radius, singularities). Closed forms for seven functions; `a` may be **complex**. For `1/(1+x^2)`: partial fractions $\frac{1}{2i}\left[\frac{1}{z-i}-\frac{1}{z+i}\right]$. |
| `taylor_yaklasim.m` | `[P, fdeg] = taylor_yaklasim(ad, a, N, x)`. $P_N(x)$ by Horner, plus $f(x)$; `x` may be a complex array. Local helper `fonksiyon_degeri`. |
| `kalan_sinir.m` | `rapor = kalan_sinir(ad, a, N, x)`. True error, Lagrange bound, rounding floor, `aday_sayisi`, `yuvarlama_sayisi`, `en_kotu_oran`. The local `turev_ustsiniri` computes $\sup\lvert f^{(m)}\rvert$ **exactly from closed forms** (Python samples a grid). Deliberately raises an error for `1/(1+x^2)`. |
| `yakinsaklik_diski.m` | `[R_okunan, R_teorik, L] = yakinsaklik_diski(ad, a, N, pencere=3, cozunurluk=600)` (read R, theoretical R, map). The $L_N(z)$ map; the shortest distance from the centre to **sign-changing neighbouring pixels**. |
| `demo_calistir.m` | Four-part demo: (1) error inside/outside the disk, (2) Lagrange + float64 candidates, (3) read R vs Python, (4) shifting the centre. |

## How to run

```powershell
$oct = (Get-ChildItem "$env:LOCALAPPDATA\Programs\GNU Octave\*\mingw64\bin\octave-cli.exe" | Select-Object -First 1).FullName
cd 03-matlab-octave
& $oct --no-gui --quiet demo_calistir.m
cd ..
```

```bash
(cd 03-matlab-octave && octave-cli --no-gui --quiet demo_calistir.m)
# or: make octave
```

To try a single function interactively (at the Octave prompt):

```octave
cd 03-matlab-octave
[P, f] = taylor_yaklasim('1/(1+x^2)', 0, 8, 0.5); abs(f - P)
[Ro, Rt] = yakinsaklik_diski('ln(1+x)', 0, 28)
```

## Where is the output?

Console only; no files. Key lines from the Windows 11 / Octave 11.3.0 run:

| Part | Value |
|---|---|
| §1, $N=64$ | inside `0.000e+00`, outside `1.289e+11` |
| §2 | `sin N=5` worst ratio **0.2704** (same as Python's `taylor.py`); total candidates **16** |
| §2 | `cos N=7` **1.0128**, `ln(1+x) N=7` **1.0654** (float64, unconfirmed; see below) |
| §3 | read R: 0.9266 / 0.9165 / 0.9967 / 1.3233 / 1.8564 (Python: 0.9366 / 0.9219 / 0.9953 / 1.3321 / 1.8681) |
| §4 | $a=0,1,2$ → $R=1.0000;\ 1.4142;\ 2.2361$ |

## Prerequisites

- MATLAB/Octave syntax: vectorisation (`.*`, `.^`), `switch`, struct fields
  (`rapor.oran`), local functions.
- Horner's scheme.
- Partial fractions and the geometric expansion of $\frac{1}{z-c}$ around $a$.

## Note: candidates here too, but no confirmation

`kalan_sinir.m` computes the bound **exactly**, so Python's risk of missing
the sup between grid points does not exist here. Yet `cos` and `ln(1+x)` still
give `en_kotu_oran > 1`. The only explanation is catastrophic cancellation
when float64 measures the error. This layer has **no** high-precision step
comparable to mpmath, so these candidates are not confirmed here; the demo
text says so and defers to the Python layer.

## Things to tinker with

1. **Complex centre.** What is the second output ($R$) of
   `taylor_katsayilari('1/(1+x^2)', 0.4+0.3i, 1)`? Compare with
   `hypot(0.4, 0.3-1)`. Then try `yakinsaklik_diski('1/(1+x^2)', 0.4+0.3i, 28)`.
   The theoretical value is the same; how far below is the read value?
2. **Resolution.** Run `yakinsaklik_diski('1/(1-x)', 0, 28, 3, 1200)`. Does
   the read radius move from 0.9165 towards 0.9175 (the root of $r^{29}=1-r$)?
3. **Add the missing function.** Write an upper bound for `'1/(1+x^2)'` in
   `kalan_sinir.m` → `turev_ustsiniri`. Hint: from partial fractions,
   $\lvert f^{(m)}(t)\rvert\le m!\,/\,\lvert t-i\rvert^{m+1}$ and
   $\lvert t-i\rvert\ge1$. Then add
   `'1/(1+x^2)', 0, 6, linspace(-0.9,0.9,401)` to the demo.

## Related

[[03-layer-python]] · [[10-seven-results#3. The disk of convergence came out of the data]]
