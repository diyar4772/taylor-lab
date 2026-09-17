---
title: Layer — Manim (animation)
tags: [guide, guide/layer, manim]
created: 2026-09-17
status: done
lang: en
---

# Layer: Manim (`01-manim/`)

↑ [[00-START-HERE]] · Plan: sessions 1, 3, 4, 7, 8 · Türkçe: [[04-katman-manim]]

## What question does it answer?

"How do I **see** this claim?" Numbers in the scenes are not typed in; they
are computed live from the same formulas (e.g. the ratio in video 3, the
equilibrium point in video 6). The colour palette lives in `tema.py` and is
identical to `02-python/src/ortam.py`. On-screen text is in Turkish.

## Files and videos

Videos are in `out/videolar/`: 1920×1080, 60 fps. The embedded players below
only work in Obsidian when the repository root is the vault; on GitHub,
click the thumbnail to open the video.

| Scene file | Class | Length | What it shows | Key parameter |
|---|---|---|---|---|
| `scenes/s01_artan_derece.py` | `ArtanDereceSahnesi` (increasing degree) | 25.3 s | $P_N$ settling on $\sin$; the "valid region" band grows | `DERECELER = [1,3,…,15]`, `iyi_bolge(tolerans=0.05)` |
| `scenes/s02_turetme.py` | `TuretmeSahnesi` (derivation) | 40.3 s | set $x=a$ / differentiate → $c_n=f^{(n)}(a)/n!$ | — |
| `scenes/s03_kalan_terimi.py` | `KalanTerimiSahnesi` (remainder) | 33.7 s | true error and bound on a log axis, $N=1..10$ | for $\sin$, $\sup\lvert f^{(N+1)}\rvert=1$; test point $x=2$, $N=10$ |
| `scenes/s04_kompleks_yaricap.py` | `KompleksYaricapSahnesi` (complex radius) | 57.9 s | real axis → poles $\pm i$ → heat map ($N=2,4,8,16,30$) → centres $a=0.7;\,1.4;\,2.0$ | `PENCERE = 2.6`, `IZGARA = 420` |
| `scenes/s05_analitik_degil.py` | `AnalitikDegilSahnesi` (not analytic) | 47.1 s | $f^{(n)}(0)=0$, series $\equiv0$, $f(1)=0.3679$, $z\to0$ from two directions | `f_guvenli()` |
| `scenes/s06_denge.py` | `DengeSahnesi` (equilibrium) | 54.9 s | arbitrary $V(x)$, $x_0\approx2.1918$, $k=V''(x_0)\approx5.880$; amplitudes 0.25 / 0.5 / 0.7 | `V()`, `genlikler` |
| `scenes/tema.py` | — | — | colours, font sizes, `baslik()`, `eksen()`, `etiket_kutusu()` | — |
| `render.sh` | — | — | renders scenes and copies them to `out/videolar/<n>-<Class>.mp4` | `KALITE` (default `-qh`) |

[![1](../kilavuz/ekler/video1-artan-derece.png)](../../../out/videolar/1-ArtanDereceSahnesi.mp4)
![[1-ArtanDereceSahnesi.mp4]]

[![2](../kilavuz/ekler/video2-turetme.png)](../../../out/videolar/2-TuretmeSahnesi.mp4)
![[2-TuretmeSahnesi.mp4]]

[![3](../kilavuz/ekler/video3-kalan.png)](../../../out/videolar/3-KalanTerimiSahnesi.mp4)
![[3-KalanTerimiSahnesi.mp4]]

[![4](../kilavuz/ekler/video4-merkez-kaydir.png)](../../../out/videolar/4-KompleksYaricapSahnesi.mp4)
![[4-KompleksYaricapSahnesi.mp4]]

[![5](../kilavuz/ekler/video5-esas-tekillik.png)](../../../out/videolar/5-AnalitikDegilSahnesi.mp4)
![[5-AnalitikDegilSahnesi.mp4]]

[![6](../kilavuz/ekler/video6-parabol.png)](../../../out/videolar/6-DengeSahnesi.mp4)
![[6-DengeSahnesi.mp4]]

## How to run

```powershell
cd 01-manim
manim -ql --disable_caching scenes\s04_kompleks_yaricap.py KompleksYaricapSahnesi   # preview
cd ..
```

```bash
(cd 01-manim && PATH="$PWD/../.venv313/bin:$PATH" manim -ql --disable_caching scenes/s04_kompleks_yaricap.py KompleksYaricapSahnesi)
PATH="$PWD/.venv313/bin:$PATH" bash 01-manim/render.sh 4     # 1080p60, overwrites out/videolar
```

## Where is the output?

- Calling `manim` directly: `01-manim/media/videos/<file>/<resolution>/<Class>.mp4`
  (`-ql` → `480p15`). This folder is git-ignored.
- Via `render.sh`: `out/videolar/`, **overwriting** the verified videos.

## Prerequisites

- Manim Community **0.19** API: `Scene.construct`, `self.play`, `Axes.plot`,
  `Transform` / `ReplacementTransform`, `MathTex`, `Text`.
- A LaTeX installation (`MathTex` → dvisvgm).
- For scene 4: grid computations with numpy, `ImageMobject`.

## Correction note: the last part of video 6

![Amplitude 0.7](../kilavuz/ekler/video6-anharmonik.png)

The first version of the scene used amplitudes 0.25 / 0.7 / **1.3**, and its
closing text said (in Turkish) that as the amplitude grows the dropped
$\tfrac16V'''(x_0)u^3$ term comes back, "and that is anharmonicity". For
1.3 that was not true:

- The potential's critical points are $-1.248$ (left minimum), $0.249$
  (barrier top, $V\approx3.077$) and $2.192$ (right minimum).
- At amplitude 1.3 the energy is $V(x_0+1.3)\approx9.49 > 3.077$. The
  particle crossed the barrier and $u$ went down to about $-4.75$. The plot
  clips with `np.clip(u, -1.6, 1.6)`, so the escape showed up as **flat
  plateaus**.
- The threshold amplitude, from $V(x_0+A)=V_{\text{top}}$, is $A\approx0.784$.

Fix: `genlikler = [0.25, 0.5, 0.7]`, and the video was re-rendered at 1080p60
(length unchanged: 54.9 s). The last amplitude now shows
"genlik = 0.7, ayrışma: 1.685" (amplitude, separation). The true curve stays
in the well but is clearly asymmetric with a longer period, so the closing
text now describes what is on screen. The parentheses in the
`genlik = (1.3)` label were also removed.

## Things to tinker with

1. **Reproduce the bug.** Set `genlikler` in `s06_denge.py` to
   `[0.25, 0.7, 1.3]` and render with `-ql` to see the flat plateaus. Then try
   `[0.25, 0.7, 0.78]`, just below the threshold: how much longer does the
   period get? Afterwards run `git restore 01-manim/`.
2. **Play with the tolerance.** In `s01_artan_derece.py` use `tolerans=0.005`
   instead of `iyi_bolge(N, tolerans=0.05)`. How far does the region at
   $N=15$ shrink from $6.1$?
3. **Another centre.** Add `-1.0` to the `for a_yeni in (0.7, 1.4, 2.0)` loop
   in `s04_kompleks_yaricap.py`. The displayed $R=|a-i|$ should be $\sqrt2$.
   Which way does the disk move?

## Related

- Interactive versions of the same scenes: [[09-layer-web]], [[08-layer-godot]]
- The numbers behind the scenes: [[03-layer-python]]
