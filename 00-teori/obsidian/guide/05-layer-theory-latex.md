---
title: Layer — Theory (LaTeX)
tags: [guide, guide/layer, theory]
created: 2026-09-17
status: done
lang: en
---

# Layer: Theory (`00-teori/`)

↑ [[00-START-HERE]] · Plan: sessions 1, 4, 7, 9 · Türkçe: [[05-katman-teori-latex]]

## What question does it answer?

"Which theorem explains **why** the numbers come out this way, and what is
the skeleton of its proof?" The other layers measure; this one justifies.
The text is in Turkish.

## Files

| File | Contents |
|---|---|
| `taylor-teori.tex` | Source of the 8-page text |
| `obsidian/*.md` | Four atomic notes (below) |
| `obsidian/kilavuz/`, `obsidian/guide/` | This guide (TR / EN) |
| `../out/taylor-teori.pdf` | Compiled PDF |

### `taylor-teori.tex`, section by section

| § | Title (translated) | Main result | Measured by |
|---|---|---|---|
| 1 | Coefficients: $n!$ is not decoration | Proposition: $P^{(n)}(a)=n!\,c_n$ ⇒ $c_n=f^{(n)}(a)/n!$; polynomial vs series | `taylor.py` self-test |
| 2 | Taylor's theorem and the Lagrange remainder | Theorem (proved by applying Rolle $N+1$ times); error bound corollary | `kalan_dogrulama.py` |
| 3 | The radius of convergence is complex-plane geometry | Cauchy–Hadamard; $R=\operatorname{dist}(a,\Sigma)$; centre-shift table; the $L_N(z)$ map | `kompleks_harita.py`, `yakinsaklik_orani.py` |
| 4 | Smooth but not analytic | $e^{-1/x^2}$ theorem, induction $f^{(n)}(x)=p_n(1/x)e^{-1/x^2}$ | `analitik_degil.py` |
| 5 | Application: every stable equilibrium is a harmonic oscillator | expansion of $V(x_0+u)$; pendulum and $T=T_0(1+\theta_0^2/16+11\theta_0^4/3072+\cdots)$ | `sarkac.py` |
| 6 | Bonus: Frobenius series | Legendre and Hermite recurrences, truncation condition | `frobenius.py` |
| 7 | Summary | six-point summary | — |
| — | Bibliography | Rudin, Ahlfors, Stein–Shakarchi, Whittaker–Watson, Arfken, Landau–Lifshitz, Griffiths | — |

### The four atomic notes (Turkish)

- [[Taylor açılımı bir tanım değil zorunluluktur]]: §1
- [[Yakınsaklık yarıçapı kompleks düzlemde belirlenir]]: §3
- [[Pürüzsüz olmak analitik olmak değildir]]: §4
- [[Her kararlı denge harmonik osilatördür]]: §5, §6

## How to compile

Details and pitfalls: [[01-environment-setup#LaTeX]]. **Three passes** are needed.

```powershell
cd 00-teori
1..3 | ForEach-Object { pdflatex -interaction=nonstopmode -enable-installer taylor-teori.tex | Out-Null }
cd ..
```

```bash
make teori
```

## Where is the output?

`00-teori/taylor-teori.pdf` (git-ignored), and via `make teori`
`out/taylor-teori.pdf`. Intermediate files (`.aux`, `.log`, `.out`, `.toc`)
are in `.gitignore`.

## Prerequisites

- Calculus: Rolle's theorem, mean value theorem, derivatives.
- Power series, $\limsup$.
- Complex analysis: holomorphic function, pole, essential singularity.
- Physics: potential energy, small oscillations; what the quantum harmonic
  oscillator is.

## Corrections made to the text

- §2 used to give only **2232** float64 candidates (the Windows count); the
  README and the table give Fedora's **2224**. The text now says "about 2200
  (2224–2232 depending on the platform)"
  ([[10-seven-results#1. The Lagrange bound was never violated]]).
- The comment on line 2 said to compile "twice"; it now says three times.
- §3's sentence "the ratio test is off by 22.66 %" was replaced by a
  description of the ratio test oscillating with $N$
  ([[12-gaps-and-next-steps]], A1).
- On Windows/MiKTeX the build gives 0 errors and 1 warning (a babel
  configuration warning).

## Things to tinker with

1. **Extend the table.** Add rows $a=-1$ and $a=0.5$ to the "Merkezi
   kaydırmak" table in §3 ($R=\sqrt2$, $R=\sqrt{1.25}\approx1.118$). Compare
   with the `yaricap()` formula used by `test_dogrulama.gd`.
2. **Write the proof yourself.** Cover the Rolle proof in §2 and rebuild it
   on paper for $N=1$ ($f(x)=f(a)+f'(a)(x-a)+\tfrac12 f''(\xi)(x-a)^2$). Then
   check the `sin, N=3, x=1.2` row of `ksi_varligi.md` by hand:
   $\sin\xi=(\sin1.2-P_3(1.2))\cdot 4!/1.2^4$ ⇒ $\xi\approx0.2341$.
3. **New section.** Add the "pendulum series has radius $\pi$" observation
   from [[12-gaps-and-next-steps]] to §5 as a note box (`notkutusu`
   environment) and compile with three passes.

## Related

[[03-layer-python]] · [[07-layer-lean]] · [[11-concept-map]]
