# Taylor Laboratory

*[Türkçe sürüm için: **[README.md](README.md)**]*

> **Note on language.** This repository is written in Turkish: documentation,
> code comments, file names and identifiers. This file is the English entry
> point. A [glossary](#glossary) at the bottom maps the Turkish identifiers
> you will meet in the source, so the code stays navigable without Turkish.

A Taylor series is not a computational trick. It is a **complete accounting**
of how a function behaves near a point: every term carries information, and
every term you discard sends a bill that is paid somewhere else. This
repository shows where those bills are paid.

The thesis in one sentence:

> A discarded term does not vanish. It comes back — in the error, in the
> radius of convergence, in a pendulum's period depending on amplitude, or
> in an energy level turning out to be an integer.

Seven layers arrive at the **same** numbers by different routes: numerical
scripts, symbolic algebra, formal proof, animation, a browser and a game
engine.

## The rule of this repository

**Nothing is called "working" unless it was actually run.**

If this README says something was verified, the [verification
status](#verification-status) table below contains the command that produced
it on this machine. What could *not* be verified is stated just as plainly —
for example MATLAB is installed and licensed here but **will not start**, so
the `.m` files are never claimed to "work in MATLAB".

---

## Layout

| Folder | Contents |
|---|---|
| `00-teori/` | LaTeX theory text (8 pages) and four atomic Obsidian notes. *teori = theory* |
| `01-manim/` | Six Manim scenes — the animated layer. |
| `02-python/` | Core numerical lab: seven scripts and a notebook; everything under `out/` is produced here. |
| `03-matlab-octave/` | An independent second implementation in a MATLAB-compatible subset, run under Octave. |
| `04-lean/` | Lean 4 + Mathlib formal layer: seven theorems, zero `sorry`. |
| `05-godot/` | Two interactive Godot 4 scenes. |
| `06-web/` | Single-file interactive version (three panels), no dependencies. |
| `out/` | Generated artifacts: 7 tables, 10 figures, 6 videos, the theory PDF. |

---

## Headline results

### 1. The Lagrange bound was scanned at 144,096 points and never once violated

`out/tablolar/kalan_dogrulama.md`

Eight functions × 12 degrees × 1,501 points. In float64, **2,224 points
appeared to exceed the bound**. Every one of those candidates was re-measured
with `mpmath` at 60 digits, and the number of **confirmed** violations was
**0**.

This distinction is the heart of the project. When the true error falls far
below the bound, float64 hits its own measurement floor (`eps·|f| ≈ 1e-16`)
and the error *looks* larger than the bound. What is exceeded is not the
theorem but **the instrument** — so the verdict was never left to float64.

![Lagrange bound vs actual error](out/gorseller/kalan_dogrulama.png)

### 2. The ξ of the Lagrange remainder was searched for and found — even outside the radius

`out/tablolar/ksi_varligi.md`

The Lagrange remainder is an **equality**, not an inequality, and ξ is not an
abstract existence claim: each value was located numerically, with the
residual of the two sides in the last column (0.00e+00 in six of seven rows,
4.22e-15 in the last).

The last row matters most: for `ln(1+x)` the point `x = 1.8` lies **outside**
the radius of convergence (R = 1). The series diverges there — yet for finite
N the equality still holds and ξ still exists. **A Taylor polynomial and a
Taylor series are not the same object.**

### 3. The disc of convergence was not drawn — it emerged from the data

`out/tablolar/kompleks_yaricap.md`

| case | a | singularities | theoretical R | R read off the map |
|---|---|---|---|---|
| 1/(1+z²) | 0 | ±i | 1.0000 | 0.9366 |
| 1/(1−z) | 0 | 1 | 1.0000 | 0.9219 |
| ln(1+z) | 0 | −1 | 1.0000 | 0.9953 |
| eᶻ | 0 | none | ∞ | — |
| 1/(1+z²) | 1 | ±i | 1.4142 | 1.3321 |
| 1/(1−z) | −1 | 1 | 2.0000 | 1.8681 |

The right-hand column was obtained without ever looking at the theoretical
value: `(1/N)·log10|f(z) − P₂₈(z)|` was mapped over the complex plane and its
**own zero level** was measured. Nothing drew the disc; it arose from the
behaviour of the error.

The last two rows are the point: same function, different centre, different
radius — **the radius belongs not to the function but to the (function,
centre) pair.** The 5–8% shortfall against the theoretical R is not an error
but the honest price of finite N.

![Error map in the complex plane](out/gorseller/kompleks_hata_haritasi.png)

On the real axis the same function gives nothing away:

![No hint on the real axis](out/gorseller/reel_eksende_ipucu_yok.png)

### 4. The same radius, found a second time from the coefficients alone

`out/tablolar/cauchy_hadamard.md`

Cauchy–Hadamard estimates R from the coefficient sequence only — without
looking at the function or its singularities. Two independent routes meeting
at the same number *is* the content of the theorem. The script also exposes
three honest limits:

1. **R = ∞ cannot be seen numerically.** For `exp`, `|aₙ|^(1/n) ≈ e/n`; at
   n = 60 this still gives R ≈ 22. You can read "growing", never "infinite".
2. **Algebraic coefficients are slow.** `ln(1+x)` and `√(1+x)` still deviate
   by 7–13% at n = 60. That is the nature of `limsup`.
3. **The ratio test is not always available.** For `1/(1+x²)` centred at
   a = 1, Cauchy–Hadamard lands within 1.66% while the ratio test is off by
   22.66% — because `i` and `−i` are *equidistant from the centre but in
   different directions*, so the coefficients oscillate and `|aₙ/aₙ₊₁|` has no
   limit. That is precisely why the theorem is stated with `limsup`.

### 5. The bill for the small-angle approximation: at 150° the prediction is 76% wrong

`out/tablolar/sarkac.md` — `g = 9.80665 m/s²`, `L = 1.0 m`, `T₀ = 2.006409 s`

| θ₀ | harmonic T₀ | measured T | deviation |
|---|---|---|---|
| 10° | 2.006409 | 2.010236 | 0.19% |
| 45° | 2.006409 | 2.086612 | 4.00% |
| 90° | 2.006409 | 2.368246 | 18.03% |
| 150° | 2.006409 | 3.535702 | 76.22% |

`sin θ ≈ θ` discards `−θ³/6`. In a harmonic oscillator the period is
independent of amplitude (isochronism) — the `harmonic T₀` column is
constant. A real pendulum is not: at 150° the true period is 3.54 s while the
harmonic prediction is still 2.01 s. The discarded term returned as
anharmonicity.

The largest discrepancy between the ODE solver and the closed elliptic form
is `1.3e-11%`, so every difference in the table comes from the Taylor
truncation, not from numerical error.

The order of the truncation error is not a guess but a **measurable
prediction**: read off the log–log slope, the residual error goes as
`θ₀^2.00` with no correction, `θ₀^4.00` with the `θ₀²/16` term, and
`θ₀^6.01` with the next one. Each correction raises the order by exactly 2,
because the `θ₀ → −θ₀` symmetry forbids odd powers.

![Pendulum period](out/gorseller/sarkac_periyot.png)

### 6. Quantization arises from convergence, not from physics

`out/tablolar/frobenius.md` — Hermite equation, `ψ = H(x)·e^(−x²/2)`

| λ | series truncates? | ψ(4) | outcome |
|---|---|---|---|
| 0 | yes, degree 0 | 3.3546e-04 | normalizable |
| 2 | yes, degree 2 | −1.0399e-02 | normalizable |
| 3 | yes, degree 3 | −1.2971e-02 | normalizable |
| 2.5 | **no** | 1.4261e+01 | **blows up** |
| 3.7 | **no** | 3.5328e+00 | **blows up** |

This section inverts the rest of the lab: elsewhere a known function yields a
series, here **the series comes first** and the function is born from it. The
recurrence `aₙ₊₂ = 2(n−λ)/[(n+1)(n+2)]·aₙ` places no constraint on λ. The
constraint comes from the requirement that the solution stay finite, which
happens only when the numerator vanishes — that is, when `λ = n` is an
integer.

The `n` in `Eₙ = ℏω(n + ½)` is simply **the index at which that recurrence
vanished.** Nobody imposed it; the series left no alternative.

Two honest warnings are recorded in the theory text: the divergence of the
non-truncating Legendre series at `x = 1` is logarithmic and therefore
unobservable numerically (400 terms still look finite — algebra, not
experiment, settles it), and the truncation decision cannot be made by
thresholding coefficients, since the λ = 2.5 coefficients also shrink fast.

![Hermite](out/gorseller/frobenius_hermite.png)

### 7. Smooth but not analytic

`out/tablolar/analitik_degil.md` — `f(x) = e^(−1/x²)`

All derivatives vanish at `x = 0` (computed by **symbolic** limits, not
numerically — `f(0.1) = e^(−100) ≈ 3.7e-44` is already below what float64 can
see, so "it printed zero" would prove nothing). The Maclaurin series is
therefore identically 0 and **converges for every x** — with infinite radius.
What it converges to is the zero function, while `f(x) > 0` for every
`x ≠ 0`.

> A Taylor series converging does not mean it converges to the function that
> produced it.

The reason is again in the complex plane: along `z = iy` we get
`e^(+1/y²) → ∞`, so `z = 0` is an **essential singularity**. Concretely, at
`|z| = 0.05` the real direction gives `1.9e-174` and the imaginary direction
`5.2e+173`. This is the concrete witness of `C^ω ⊊ C^∞`.

![Not analytic](out/gorseller/analitik_degil.png)

---

## The formal layer (Lean 4 + Mathlib)

Seven theorems, `lake build` green over 2,777 jobs, **zero `sorry`**, and
`#print axioms` on each theorem reports only `propext`, `Classical.choice`
and `Quot.sound` — no `sorryAx`.

The rule was: **use what Mathlib already has, do not re-prove it.** The work
was to state which formal proposition each numerical finding corresponds to.

| Theorem | Content | Numerical counterpart |
|---|---|---|
| `ksi_vardir` | ξ exists and the remainder is an *equality* | the ξ table above |
| `purussuz_ama_analitik_degil` | ∃ f ∈ C^∞ that is not analytic at 0 | `e^(−1/x²)` |
| `cauchy_hadamard` | radius from the coefficient sequence | the C–H table |
| `disk_icinde_mutlak_yakinsar` | absolute convergence inside the disc | the complex map |
| `geometrik_yaricap_bir` | the geometric series has radius exactly 1 | C–H error 0.00% |

Four topics were deliberately left out of scope; they are listed at the end
of [`LEAN-DURUM.md`](LEAN-DURUM.md) (that file is in Turkish, but the theorem
names and Mathlib lemma names in it are language-neutral).

---

## Running it

### There are two virtual environments — do not mix them

| Environment | Python | Purpose | Why separate |
|---|---|---|---|
| `.venv/` | 3.14.7 | numpy / scipy / sympy / matplotlib / mpmath — **all numerical scripts** | the system Python |
| `.venv313/` | 3.13.15 | **manim only** | `manim 0.19.0` requires `av<14`; `av` has no Python 3.14 wheel and building it from source fails on the `libavformat` headers |

```bash
cd taylor-lab
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
source .venv/bin/activate
export PATH="$HOME/.elan/bin:$PATH"   # lean / lake
```

Run manim in **its own** environment:

```bash
PATH="$PWD/.venv313/bin:$PATH" bash 01-manim/render.sh
```

### Verify everything with one command

```bash
make dogrula          # every layer in turn; exits 1 if any layer fails
make dogrula-hizli    # same, skipping Lean (lake build can be slow)
```

*(`dogrula` = verify)*

Last run on this machine: **8/8 passed, 0 failed, 0 skipped, 18 s.**

### Layer by layer

```bash
.venv/bin/python 02-python/src/kalan_dogrulama.py   # numerical lab
make teori                                          # theory PDF (3 passes)
cd 03-matlab-octave && octave-cli --no-gui --quiet demo_calistir.m
cd 04-lean && lake build                            # first run downloads Mathlib
godot --path 05-godot                               # interactive scenes
node 06-web/test_matematik.mjs                      # web math tests
```

The web page will not open from `file://` in Chrome; serve it:

```bash
python3 -m http.server 8765
# then: http://localhost:8765/06-web/index.html
```

---

## Verification status

Every row below was actually executed on this machine (Fedora Linux 44,
x86_64, glibc 2.43). Rows that could not be verified say so.

| Layer | Command | Result |
|---|---|---|
| Python core | `python 02-python/src/taylor.py` | Passed — all checks, exit 0 |
| Lagrange scan | `python 02-python/src/kalan_dogrulama.py` | Passed — exit 0, 11.7 s |
| LaTeX | `make teori` (3 passes) | Passed — 0 errors / 0 warnings, 8 pages |
| Manim | `bash 01-manim/render.sh` | Passed — **all six** scenes re-rendered, 1920×1080 @ 60 fps |
| Octave | `octave-cli --no-gui --quiet demo_calistir.m` | Passed — exit 0; radii independently matched the Python layer |
| MATLAB | `matlab -batch "disp(version)"` | **Failed** — R2026a installed and licensed, but crashes before the interpreter starts |
| Lean | `lake build` | Passed — 2,777 jobs |
| Lean axioms | `#print axioms` × 7 | Passed — no `sorryAx`; `grep -rn sorry` empty |
| Web math | `node 06-web/test_matematik.mjs` | Passed — **34/34** |
| Web UI | Chrome | Passed — three panels, no console errors |
| Godot math | `godot --headless --script res://test_dogrulama.gd` | Passed — **30/30** |
| Godot scenes | `godot --headless --quit-after 90` × 2 | Passed — both ran clean |
| Godot visuals | `godot --path 05-godot` | Passed — curves render; both pendulums swing and the phase bar turns red at 150° |

### About MATLAB, on the record

MATLAB R2026a is **installed and licensed** on this machine, but
`matlab -batch` crashes before the interpreter starts, inside the builtin
registry (`LXE Object runtime information ... missing 'mxClassName'`). It is
not a licensing problem: the crash precedes the licence check, and a
different `*_builtinimpl.so` fails on each run. `-nojvm -nodisplay` and
`MW_DISABLE_LXE=1` behave identically. The likely cause is that Fedora 44's
base (glibc 2.43, GCC 16) is far ahead of MathWorks' supported distributions.

So the repository says this about `03-matlab-octave/` and nothing more:

> The files are written in a MATLAB-compatible subset (`fprintf`, `~`, `%`,
> plain `end`, one main function per file) and were **run and verified under
> GNU Octave 10.3.0**. That they run under MATLAB could not be demonstrated
> on this machine.

### Cross-platform numerical difference

`kalan_dogrulama.py` found 2,232 candidate violations on Windows 11 /
Python 3.13.7 and 2,224 on Fedora 44 / Python 3.14.7. The candidate count
depends on the platform's `libm` (last-bit rounding of `sin`, `exp`, `log`),
so it moves by a few units. The claim that matters — **0 violations confirmed
by mpmath** — came out identical on both.

---

## Glossary

The source is Turkish. These are the identifiers you will actually meet:

| Turkish | English |
|---|---|
| `taylor_yaklasim` | Taylor approximation |
| `taylor_katsayilari` | Taylor coefficients |
| `kalan_sinir`, `kalan_dogrulama` | remainder bound, remainder verification |
| `yakinsaklik_diski`, `yakinsaklik_orani` | disc of convergence, convergence ratio |
| `kompleks_harita` | complex map |
| `analitik_degil` | not analytic |
| `sarkac` | pendulum |
| `denge` | equilibrium |
| `ksi_vardir` | "ξ exists" |
| `purussuz_ama_analitik_degil` | "smooth but not analytic" |
| `disk_icinde_mutlak_yakinsar` | "converges absolutely inside the disc" |
| `aday` / `teyit edilen` | candidate / confirmed |
| `yuvarlama tabanı` | rounding floor |
| `hata`, `sınır`, `oran` | error, bound, ratio |
| `görsel`, `tablo`, `videolar` | figure, table, videos |
| `dogrula` | verify |
| `teori`, `gecis` | theory, pass (as in compiler pass) |

Documents: [`RAPOR.md`](RAPOR.md) is the honesty report (what worked, what did
not, the eight real bugs found and fixed); [`LEAN-DURUM.md`](LEAN-DURUM.md)
covers the formal layer; [`ENVANTER.md`](ENVANTER.md) is the tool inventory of
both machines; [`DEVAM.md`](DEVAM.md) is the working-state note.

---

## License

MIT — Copyright (c) 2026 Samed Yolcu. Full text: [`LICENSE`](LICENSE).
