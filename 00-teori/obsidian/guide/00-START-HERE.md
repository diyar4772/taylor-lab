---
title: Start Here — Taylor Lab Study Guide
tags: [guide, guide/moc, taylor]
created: 2026-09-17
status: done
aliases: [Guide MOC, Taylor Lab guide]
lang: en
---

# Start Here

> [!info] What this guide is not
> It is not a summary of the README. It is a lesson plan for learning the
> repository **in order, by running things yourself**. Turkish version:
> [[00-BASLA-BURADAN]].
>
> The repository itself (code comments, tables, videos, the LaTeX text) is in
> **Turkish**. This guide translates the key terms as it goes. Column
> names are quoted in Turkish with an English gloss, e.g.
> **aday ihlal** (candidate violation).

## What does the repository claim? (one paragraph)

A Taylor series is not a computational trick. It is a **complete ledger** of
a function's behaviour near a point: once you write
$P_N(x)=\sum_{n\le N} \frac{f^{(n)}(a)}{n!}(x-a)^n$, every term you drop gets
billed somewhere. The repository shows, **by measurement**, four places where
the bill arrives: in the error (Lagrange remainder), in the radius of
convergence (complex singularities), in the amplitude dependence of a
pendulum's period (anharmonicity), and in an energy level being an integer
(quantization). Its rule: **nothing is called "working" unless it was
actually run.**

## Seven layers, and why they are separate

All layers reach **the same numbers by different routes**. A number
produced by one program cannot be told apart from that program's bug. If two
independent implementations agree, a bug would have to be made identically
in both, which is far less likely.

| Layer | Folder | Question | Why separate? |
|---|---|---|---|
| Theory | `00-teori/` | What do the theorems say, what is the proof skeleton? | Produces **reasons**, not numbers. |
| Animation | `01-manim/` | How do I see it? | Intuition; numbers computed live, never typed in. |
| Numerical core | `02-python/` | Do the theorems hold numerically? | **All** tables and plots in `out/` come from here. |
| MATLAB/Octave | `03-matlab-octave/` | Does another language and method give the same number? | Coefficients from **closed forms**, not symbolic differentiation. |
| Formal | `04-lean/` | Is the theorem actually true? | Measurement is not proof; Lean + Mathlib checks it by machine. |
| Game engine | `05-godot/` | What happens when I tweak it by hand? | Third independent implementation (GDScript) + interaction. |
| Web | `06-web/` | Can I see it in a browser, no install? | Fourth independent implementation (JavaScript), no dependencies. |

Concrete example: the period of a pendulum at 150° amplitude is
**3.535702 s** in Python (`solve_ivp`), **3.535701938 s** in JavaScript
(RK4 + AGM), **3.5357019383 s** in GDScript (AGM). Details in
[[10-seven-results#5. The bill for the small-angle approximation]].

## Suggested reading order

1. [[00-START-HERE]] ← you are here
2. [[01-environment-setup]]: tools first
3. [[02-study-plan]]: **the actual lesson plan** (10 sessions)
4. Layer notes, used as references during sessions:
   - [[05-layer-theory-latex]]
   - [[04-layer-manim]]
   - [[09-layer-web]]
   - [[03-layer-python]]
   - [[06-layer-octave]]
   - [[08-layer-godot]]
   - [[07-layer-lean]]
5. [[10-seven-results]]: a deeper reading of the seven main results
6. [[11-concept-map]]: how the concepts connect
7. [[12-gaps-and-next-steps]]: what is **not** in the repo, and bugs found

The repository's own atomic notes (Turkish, written before this guide):

- [[Taylor açılımı bir tanım değil zorunluluktur]] (*A Taylor expansion is a necessity, not a definition*)
- [[Yakınsaklık yarıçapı kompleks düzlemde belirlenir]] (*The radius of convergence is decided in the complex plane*)
- [[Pürüzsüz olmak analitik olmak değildir]] (*Smooth is not analytic*)
- [[Her kararlı denge harmonik osilatördür]] (*Every stable equilibrium is a harmonic oscillator*)

Visual overview: [[guide-map.canvas|Guide map (Canvas)]]

## Three routes

> [!tip] I only have 30 minutes
> 1. Open the web page ([[01-environment-setup#Web]]) and, in the
>    **2 · Kompleks disk** (complex disk) tab, move the centre. (10 min)
> 2. Watch `4-KompleksYaricapSahnesi.mp4`. (1 min)
> 3. Read results **3** and **7** in [[10-seven-results]]. (15 min)
>
> Take-away: "the radius is decided in the complex plane" and "converging
> is not the same as being equal".

> [!tip] I have one evening (~3 hours)
> **Sessions 1, 3, 4, 7 and 8** of [[02-study-plan]]. Only the Python
> environment is needed ([[01-environment-setup#Python]]).

> [!tip] I have a week
> One or two sessions a day: all of [[02-study-plan]] (10 sessions, ~11 h),
> then one of the "try it yourself" projects in [[12-gaps-and-next-steps]].

## Opening this guide in Obsidian

- For images, videos and links to source files to work, **open the
  repository root (`taylor-lab/`) as the vault** (Obsidian → *Open folder as
  vault*). The guide uses relative paths (`../../../out/...`).
- The guide imposes no Obsidian settings; the repo has no `.obsidian/` folder.
- Optional graph-view suggestions and note templates:
  [[_templates/templates-readme|About the templates]].
- Maths is written with `$...$`; diagrams are Mermaid blocks. Both render in
  Obsidian without plugins.
- Screenshots and video stills are shared with the Turkish version and live
  in `../kilavuz/ekler/`.
