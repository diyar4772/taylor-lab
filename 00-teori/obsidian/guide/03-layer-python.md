---
title: Layer — Python (numerical core)
tags: [guide, guide/layer, python]
created: 2026-09-17
status: done
lang: en
---

# Layer: Python (`02-python/`)

↑ [[00-START-HERE]] · Plan: [[02-study-plan]] (sessions 2, 3, 5–9) · Türkçe: [[03-katman-python]]

## What question does it answer?

"Do the theorems hold numerically, and where they **seem** not to, is the
fault in the theorem or in the measuring instrument?" **All** 7 tables and
10 plots in `out/` come from this layer.

## File by file

| File | What it does | Produces |
|---|---|---|
| `src/ortam.py` | switches stdout to UTF-8, defines the `out/` paths, dark plot theme (`PALET`), `markdown_tablo()` and `tablo_yaz()` (table writers) | — |
| `src/taylor.py` | **Core.** `KATALOG` (function catalogue), `taylor_katsayilari()` (coefficients by differentiation), `polinom_fonksiyonu()`, `KalanRaporu` (remainder report), `lagrange_sinir()` (+ slow reference version), `kalan_raporu()`, mpmath helpers, `cauchy_hadamard_R()`, `oran_testi_R()`. Self-testing. | — |
| `src/kalan_dogrulama.py` | Lagrange bound at 8 functions × $N=1..12$ × 1501 points = **144,096** points; confirms float64 candidates with mpmath (60 digits); finds $\xi$ with `ksi_bul()`. Exit code 1 if any violation is confirmed. | `kalan_dogrulama.md`, `ksi_varligi.md`, `kalan_dogrulama.png` |
| `src/kompleks_harita.py` | $\frac1N\log_{10}\lvert f-P_N\rvert$ map for 6 cases ($N=28$, 600×600); reads $R$ off the zero level. | `kompleks_yaricap.md`, `kompleks_hata_haritasi.png`, `reel_eksende_ipucu_yok.png`, `yaricap_gecisi.png` |
| `src/yakinsaklik_orani.py` | 9 cases, Cauchy–Hadamard and ratio test from $n\le60$ coefficients; sparsity trap. | `cauchy_hadamard.md`, `cauchy_hadamard.png` |
| `src/analitik_degil.py` | $e^{-1/x^2}$: $f^{(n)}(0)$ for $n=0..8$ (`sympy.limit`); real vs imaginary axis. | `analitik_degil.md`, `analitik_degil.png` |
| `src/sarkac.py` | Full pendulum (`solve_ivp`, event-based period), elliptic closed form, $T_0(1+\theta_0^2/16)$ and the next term; log–log slopes. | `sarkac.md`, `sarkac_periyot.png`, `sarkac_yorungeler.png` |
| `src/frobenius.py` | Legendre and Hermite recurrences (400 terms), algebraic truncation criterion, sympy residual = 0. | `frobenius.md`, `frobenius_legendre.png`, `frobenius_hermite.png` |
| `notebooks/taylor-laboratuvari.ipynb` | 6-section summary notebook; imports the scripts' functions. | — (notebook only) |

## How to run

```powershell
python 02-python\src\taylor.py              # test, writes no files
python 02-python\src\kalan_dogrulama.py     # ~12 s
python 02-python\src\kompleks_harita.py
python 02-python\src\yakinsaklik_orani.py
python 02-python\src\analitik_degil.py
python 02-python\src\sarkac.py
python 02-python\src\frobenius.py
```

On Linux, `make python` runs the last six in order. Environment:
[[01-environment-setup#Python]].

## Where is the output?

`out/tablolar/*.md` and `out/gorseller/*.png`. Paths are defined once in
`ortam.py`, so a script writes to the same place whatever directory it is
called from.

## Prerequisites

- numpy arrays and vectorisation; sympy's `diff`, `subs`, `lambdify`.
- Floating point: machine epsilon ($\approx2.2\times10^{-16}$), **catastrophic
  cancellation** (difference of two nearly equal numbers).
- `scipy.integrate.solve_ivp` (event functions), `scipy.optimize.brentq`.
- Maths: [[05-layer-theory-latex]] §1–§3.

## Design decisions worth noticing

1. **float64 never delivers the verdict.** It only flags *candidates*; mpmath
   decides. See [[10-seven-results#1. The Lagrange bound was never violated]].
2. **No duplication:** every script imports `taylor.py`.
3. **`sp.Rational(a)` for coefficients:** a float `a` eats precision in the
   high-order derivatives. `_mpmath_katsayilari` always used this
   protection; `katsayi_dizisi()` was fixed later (see
   [[12-gaps-and-next-steps]], A1). `polinom_fonksiyonu()` and
   `polinom_yuvarlama_tabani()` still use a float `a`; at the degrees used
   there ($N\le12$) this has no effect.

## Things to tinker with

1. **Move the floor.** In `taylor.py` → `polinom_yuvarlama_tabani()`, change
   the `(N + 2) * eps` factor to `10 * (N + 2) * eps` and rerun
   `kalan_dogrulama.py`. What happens to the "en kötü oran" (worst ratio)
   values above 1, and to the "yuvarlama rejimi" (rounding regime) counts?
   The number of confirmed violations should not change. Why?
2. **Add a case.** Append
   `(r"$1/(1+z^2)$, $a=0.5$", 1/(1+T.x**2), 0.5, [1j,-1j], np.sqrt(1.25), 2.4)`
   to `DURUMLAR` in `kompleks_harita.py`. How far below the theoretical
   $\approx1.118$ is the read radius? Careful: `ciz()` iterates the axes with
   `zip()` and a 2×3 grid has 6 axes, so the 7th case is **silently dropped**.
   Change `plt.subplots(2, 3, …)` to `(3, 3, …)`.
3. **Bring the bug back.** In `taylor.py` → `katsayi_dizisi()`, change
   `sp.Rational(a)` to `a` and run `yakinsaklik_orani.py`. How far does the
   ratio-test error of the `1/(1+x^2), a=1` row rise from 0.00 %? What happens
   to the oscillation table? (Expected: 22.66 %. Afterwards run
   `git restore 02-python/src/taylor.py out/`;
   [[02-study-plan#Session 6 — Reading the radius from coefficients]].)

## Related

- Other implementations of the same numbers: [[06-layer-octave]], [[08-layer-godot]], [[09-layer-web]]
- Formal counterparts: [[07-layer-lean]]
