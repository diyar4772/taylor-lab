---
title: Seven results — a deeper reading
tags: [guide, guide/result, taylor]
created: 2026-09-17
status: done
lang: en
---

# Seven results: a deeper reading

↑ [[00-START-HERE]] · Concepts: [[11-concept-map]] · Türkçe: [[10-yedi-sonuc]]

The same five questions for each result:

- **Claim:** what is being said?
- **Source:** which script produced it?
- **Key column:** where to look in the table?
- **Why surprising:** what is unexpected?
- **Misconception broken:** which common misunderstanding does it fix?

Table columns are quoted in Turkish with a translation.

---

## 1. The Lagrange bound was never violated

**Claim.** For every $(f,a,N,x)$,
$$\lvert f(x)-P_N(x)\rvert \le \frac{\sup_{[a,x]}\lvert f^{(N+1)}\rvert}{(N+1)!}\,\lvert x-a\rvert^{N+1}.$$
Across 8 functions × $N=1..12$ × 1501 points = **144,096** trials, there are
**0** confirmed violations.

**Source.** `kalan_dogrulama.py` → `toplu_dogrulama()`,
`adaylari_teyit_et()`; core: `taylor.py` → `kalan_raporu()`.

**Key columns** (`out/tablolar/kalan_dogrulama.md`):

- **float64 aday ihlal** (float64 candidate violations): points where
  float64 says "bound exceeded". Total 2224 on Fedora, 2232 on Windows; the
  count depends on the platform's `libm`.
- **float64 oran** vs **mpmath oran** in the second table: same point,
  two measurements. For `1/(1-x), N=2, x≈0` the float64 ratio is
  $1.6\times10^{32}$ and the mpmath ratio is $1.000000$.
- **en kötü oran** (worst ratio): a float64 maximum taken only in the
  "meaningful regime". **It exceeds 1 in 6 of the 8 rows** (sin 1.0506;
  cos 1.0178; exp 1.0107; ln(1+x) **2.3593**; sqrt 1.0550; exp, a=1: 1.0147;
  sin, a=π/4: 1.0121).

### Candidate violation vs confirmed violation

| | Candidate | Confirmed |
|---|---|---|
| Who decides? | float64 | mpmath, 60 digits |
| What it measures | `abs(f(x) - P(x)) > bound` (float64) | the same difference, at 60 digits |
| Error source | catastrophic cancellation: when $f(x)\approx P_N(x)$ the difference cannot go below ~$\varepsilon\lvert f\rvert\approx10^{-16}$ | none (at this scale) |
| Count | 2224 | **0** |
| Meaning | "look here" | "the theorem failed here" |

A worked example: `ln(1+x)`, $N=7$, $x\approx0.0126$.

- The Lagrange bound is $7.94\times10^{-17}$.
- float64 measures the error as $1.87\times10^{-16}$, ratio **2.36**.
- mpmath measures it as $7.85\times10^{-17}$, ratio **0.989**.

The bound is sharp, and it holds. float64's "meaningful regime" filter
(`bound > (N+2)·ε·(Σ|term| + |f|)`) let this point through because the bound
is only 1.6 times the floor. That is exactly why the repository does not
trust the filter either: **every** candidate goes to mpmath.

**Why surprising?** Seeing thousands of "violations" and doubting the
theorem is natural. The real lesson is that the resolution of the measuring
instrument must be measured too.

**Misconception broken.** "If the computer computed it, it is right" and
"float64 has 16 digits, that is enough". When the error is the **difference**
of two close numbers, all 16 digits can be lost.

![Lagrange](../../../out/gorseller/kalan_dogrulama.png)

---

## 2. ξ really exists — even outside the radius

**Claim.** The Lagrange remainder is an **equality**,
$f(x)=P_N(x)+\dfrac{f^{(N+1)}(\xi)}{(N+1)!}(x-a)^{N+1}$, and $\xi$ can be
found numerically.

**Source.** `kalan_dogrulama.py` → `ksi_bul()`, `ksi_tablosu()`. Formal
counterpart: `TaylorLab.ksi_vardir`.

**Key columns** (`ksi_varligi.md`): **bulunan ksi** (ξ found), **(a,x)
içinde mi?** (inside (a,x)?), **eşitlik artığı** (equality residual). Last
row: `ln(1+x)`, $N=6$, $x=1.8$, $\xi\approx0.14357$, residual
$4.22\times10^{-15}$.

**How is it found?** The equality fixes the required derivative value on its
own: $f^{(N+1)}(\xi)=\dfrac{(f(x)-P_N(x))\,(N+1)!}{(x-a)^{N+1}}$. The right-hand
side is a number. $(a,x)$ is scanned at 4001 points and `brentq` finds the
root at the first sign change. Hand check (`sin`, $N=3$, $x=1.2$):
$\sin\xi = (0.932039-0.912)\cdot24/2.0736 \approx 0.2319 \Rightarrow \xi\approx0.2341$. ✓

### ξ exists outside the radius too

The series of $\ln(1+x)$ about 0 has radius 1; at $x=1.8$ the series
**diverges** ($P_N(1.8)$ goes nowhere as $N\to\infty$). Nevertheless:

- Lagrange's theorem only needs $f$ to be $N+1$ times differentiable on
  $[0, 1.8]$, and $\ln(1+x)$ is smooth there (its singularity is at $x=-1$).
- The theorem is about **one fixed $N$**; it says nothing about the limit
  $N\to\infty$.
- The divergence shows up as the remainder at $x=1.8$ growing rather than
  shrinking with $N$. For every fixed $N$, though, some $\xi$ gives the
  remainder exactly.

**Why surprising?** One learns that "outside the radius Taylor means
nothing". The **series** means nothing there; the **polynomial** and its
remainder are meaningful everywhere.

**Misconception broken.** "The Taylor polynomial is just a truncated Taylor
series, so where the series diverges the polynomial has nothing to say." And
also: "$\xi$ is unique". The theorem only asserts existence; `ksi_bul`
returns the first root.

---

## 3. The disk of convergence came out of the data

**Claim.** $R$ is the distance from the centre to the nearest complex
singularity, and it can be read off the sign of the error without ever
using the theoretical value.

**Source.** `kompleks_harita.py` → `hata_haritasi()`,
`yaricapi_haritadan_kestir()`. Independent second implementation:
`03-matlab-octave/yakinsaklik_diski.m`. Third: web panel 2.

**Key columns** (`kompleks_yaricap.md`): **teorik R** (theoretical) and
**haritadan okunan R** (read from the map). Read the last two rows together:
`1/(1+z²)` $a=0\to R=1$, $a=1\to R=\sqrt2$; `1/(1-z)` $a=0\to1$, $a=-1\to2$.

**Mechanism.** $\lvert f-P_N\rvert\sim C\,(\lvert z-a\rvert/R)^{N+1}$ ⇒
$L_N=\frac1N\log_{10}\lvert f-P_N\rvert\to\log_{10}(\lvert z-a\rvert/R)$.
Its sign tells convergence; its zero level is the circle $\lvert z-a\rvert=R$.

**Why always 5–8 % low?** The read radius is the **shortest** distance from
the centre to the zero level, and that shortest distance lies towards the
singularity, where the factor $C$ blows up. For `1/(1-z)`,
$f-P_N=z^{N+1}/(1-z)$; along $z=r$ the zero level is the root of
$r^{29}=1-r$, i.e. $r\approx0.9175$, and on the grid this reads as 0.9219. As
$N\to\infty$, $C^{1/N}\to1$ and the deviation disappears.

![Complex map](../../../out/gorseller/kompleks_hata_haritasi.png)

**Why surprising?** `1/(1+x²)` is flawless on the real line, yet its series
stops at $\lvert x\rvert=1$. The reason lives one dimension up.

![No clue on the real axis](../../../out/gorseller/reel_eksende_ipucu_yok.png)

**Misconception broken.** "The radius of convergence is a property of the
function" (it belongs to the (function, centre) pair) and "a real function's
behaviour is decided on the real line".

---

## 4. The same radius, from coefficients alone

**Claim.** $1/R=\limsup\lvert a_n\rvert^{1/n}$ (Cauchy–Hadamard). Without
looking at any singularity, the radii of result 3 are recovered from the
coefficient sequence alone.

**Source.** `yakinsaklik_orani.py`; `taylor.py` → `cauchy_hadamard_R()`
(maximum over the last 12 non-zero terms), `oran_testi_R()`
($\lvert a_n/a_{n+d}\rvert^{1/d}$). Formal: `TaylorLab.cauchy_hadamard`.

**Key columns** (`cauchy_hadamard.md`): **C-H kestirimi** (estimate), **C-H
hatası** (error), **oran testi** (ratio test), **oran hatası** (ratio error).

### Why limsup and not a limit?

A $\lim$ exists only if the sequence settles to a single value. A $\limsup$
always exists: it is the largest value the tail keeps coming back to.

The `1/(1+x²)`, $a=1$ example: $i$ and $-i$ are **equally far** from the
centre ($\sqrt2$) but in different directions. Partial fractions give
$$c_n=(-1)^n\,2^{-(n+1)/2}\,\sin\frac{(n+1)\pi}{4}.$$
The factor $\lvert\sin\rvert$ is periodic in $n$ with period 4, taking the
values $\{0.707,\,1,\,0.707,\,0\}$ (the coefficient is exactly **zero** for
$n\equiv3 \pmod 4$). Hence:

- $\lvert c_n\rvert^{1/n}\to 2^{-1/2}$ **along a subsequence** ⇒ $\limsup=1/\sqrt2$ ⇒ $R=\sqrt2$. ✓
- $\lvert c_n/c_{n+1}\rvert$, however, keeps cycling. With exact coefficients,
  the ratio test for $N=52..60$ gives
  `1.4142, 1.0, 2.0, 2.0, 1.4142, 1.0, 2.0, 2.0, 1.4142`.
  **There is no limit**; the ratio test's answer depends on where you stop.

> [!note] Correction: the old 22.66 %
> The first version of the repository reported that in this row the ratio
> test was off by 22.66 % and C-H by 1.66 %. A check made while writing this
> guide showed the numbers were **contaminated by floating-point precision
> loss**: `katsayi_dizisi` passed the centre as a float; at $n=40$ the
> relative error was ~$10^{-5}$, and $c_{60}$ even had the wrong sign
> ($+2.55\times10^{-9}$ instead of $-4.66\times10^{-10}$). After the fix
> (`sp.Rational(a)`), the table at $N=60$ gives exactly $\sqrt2$ (0.00 %) for
> the ratio test and 1.4228 (0.61 %) for C-H, and it now includes the
> oscillation table above. Details: [[12-gaps-and-next-steps]].

**The other rows.**

- `exp`, `sin`: $R=\infty$ cannot be seen. C-H grows with $N$ (N=30: 7.93;
  N=60: 19.11; N=120: 41.3), and the ratio test returns exactly $N$.
- `ln(1+x)`, `sqrt(1+x)`: the coefficients carry an algebraic factor like
  $1/n$, and $(1/n)^{1/n}\to1$ very slowly; 7–13 % remains at $N=60$.
- `1/(1-x), a=-1`: C-H is 1.16 % high because
  $\lvert c_n\rvert^{1/n}=2^{-(n+1)/n}$ and $(n+1)/n>1$ at finite $n$. The
  ratio test gives exactly 2.

![Cauchy–Hadamard](../../../out/gorseller/cauchy_hadamard.png)

**Why surprising?** Geometry (the singularities) and arithmetic (the growth
rate of the coefficients) give the same number.

**Misconception broken.** "The ratio test and the root test are the same"
and "limsup is just pedantry".

---

## 5. The bill for the small-angle approximation

**Claim.** The approximation $\sin\theta\approx\theta$ drops the
$-\theta^3/6$ term, which returns as **the amplitude dependence of the
period**:
$T=T_0\left(1+\frac{\theta_0^2}{16}+\frac{11\theta_0^4}{3072}+\cdots\right)$.

**Source.** `sarkac.py` → `periyodu_olc()` (solve_ivp + events),
`tam_periyot_eliptik()`, `taylor_periyot()`. Independently: web (RK4 + AGM),
Godot (AGM).

**Key columns** (`sarkac.md`):

- **harmonik T₀** is constant (2.006409 s): isochronism.
- **ölçüm-kapalı fark** (measured vs closed form) is at most
  $1.3\times10^{-11}$ %: the solver can be trusted, so every remaining
  difference comes from the Taylor truncation.
- **Taylor-2 hatası** / **Taylor-4 hatası** (errors), relative to the elliptic value.
- Log–log slopes: 4.00 and 6.01.

### "76 %" relative to what?

| Comparison | At 150° |
|---|---|
| $(T-T_0)/T_0$: deviation from harmonic (README, web, Godot) | **76.22 %** |
| $(T-T_0)/T$: error of the harmonic prediction relative to the truth | 43.25 % |
| $\lvert T_0(1+\theta_0^2/16)-T\rvert/T$: Taylor-2 error | 18.94 % |
| Taylor-4 error | 9.40 % |

**Why surprising?** The order is not a guess but something you can
**measure**: each correction raises the error exponent by exactly 2, because
$T(\theta_0)$ is even.

**Misconception broken.** "A pendulum's period does not depend on its
amplitude" (true only in the harmonic approximation) and "the price of an
approximation is just a small numerical error". The price is
**qualitative**: isochronism is lost.

![Pendulum](../../../out/gorseller/sarkac_periyot.png)

---

## 6. Quantization comes from convergence, not from physics

**Claim.** The Hermite equation $y''-2xy'+2\lambda y=0$ has a series solution
for every $\lambda$. The integers come from the requirement that the
solution stays finite.

**Source.** `frobenius.py` → `hermite_katsayilari()`, `kesilme_derecesi()`,
`kesilme_dogrula()`, `sembolik_dogrulama()`.

**Key columns** (`frobenius.md`): **seri kesiliyor mu?** (does the series
terminate?), **H(4)**, **ψ(4)**, **∫ψ² oranı (L=6 / L=4)** (ratio of
integrals); for Legendre, **kısmi toplam büyümesi**
(partial-sum growth); in the check, **denklemdeki kalıntı** (residual), all `0 ✓`.

### How quantization is born from the recurrence terminating

1. Substituting $y=\sum a_nx^n$ gives
   $a_{n+2}=\dfrac{2(n-\lambda)}{(n+1)(n+2)}\,a_n$. The equation places **no
   restriction** on $\lambda$.
2. If the series does not terminate, then for large $n$,
   $a_{n+2}/a_n\approx 2/n$. That is the coefficient ratio of $e^{x^2}$, so
   $H\sim e^{x^2}$ and $\psi=He^{-x^2/2}\sim e^{+x^2/2}$: **not normalizable**.
3. The only escape is for the numerator to vanish: $n-\lambda=0$ ⇒
   $\lambda\in\mathbb N$ (and the parity of the starting coefficient must
   match). The series becomes a polynomial.
4. Physics only says "$\psi$ must stay finite". Since
   $E=\hbar\omega(\lambda+\tfrac12)$, the $n$ in $E_n=\hbar\omega(n+\tfrac12)$
   **is the truncation index**.

For Legendre the same logic gives $\lambda=\ell(\ell+1)$. There the
divergence is at $x=\pm1$ and **logarithmic**, so $y(1)$ still looks finite
after 400 terms; the evidence is the **partial-sum growth** column (exactly
0 for the terminating ones).

**Two honesty notes.**

- Termination cannot be decided by a **threshold**: for $\lambda=2.5$ the
  coefficients drop below $10^{-14}$ after $n\approx28$ but are not zero.
- The "normalize edilebilir / PATLIYOR" (normalizable / blows up) verdict
  rests on the normalization integral: the ratio of $\int\psi^2$ over
  $[-6,6]$ to that over $[-4,4]$. For integer $\lambda$ the ratio is at most
  $1.000085$; for $\lambda=2.5$ it is $9.5\times10^6$. (The first version only
  checked $\lvert\psi(4)\rvert<1$.)

![Hermite](../../../out/gorseller/frobenius_hermite.png)

**Why surprising?** Integers are taught like a "quantum postulate". Here they
come out of a series being required to stay finite.

**Misconception broken.** "The equation itself can only be solved for
integers." No: it is solvable for every $\lambda$; only for integers is the
solution **physical**.

---

## 7. Smooth but not analytic

**Claim.** For $f(x)=e^{-1/x^2}$ (with $f(0)=0$), $f\in C^\infty$ and
$f^{(n)}(0)=0$ for every $n$. Its Maclaurin series is $\equiv0$ and
converges everywhere, but $f(x)>0$ for $x\neq0$. Hence $C^\omega\subsetneq C^\infty$.

**Source.** `analitik_degil.py` → `turevler_sifirda()` (`sympy.limit`,
$n=0..8$), `kompleks_tekillik()`. Formal: `purussuz_ama_analitik_degil`
(witness `expNegInvGlue`, i.e. $e^{-1/x}$).

**Key columns** (`analitik_degil.md`): **f⁽ⁿ⁾(0) (limit)** is always 0.
**Aynı türevin x=0.1'deki değeri** (the same derivative at $x=0.1$) rises
from $3.7\times10^{-44}$ to $6.1\times10^{-18}$. Second table: at
$\lvert z\rvert=0.05$, $1.9\times10^{-174}$ along the real axis and
$5.2\times10^{173}$ along the imaginary axis.

**Mechanism.** $f^{(n)}(x)=p_n(1/x)\,e^{-1/x^2}$; $e^{-u^2}$ decays faster than
any polynomial grows. On the complex side, for $z=iy$, $-1/z^2=+1/y^2$ ⇒
$e^{1/y^2}\to\infty$: $z=0$ is an **essential singularity**.

**Relation to result 3.** The theorem "R = distance to the nearest
singularity" requires $f$ to be holomorphic at the centre, which it is not
here. So the series having $R=\infty$ does not contradict it: the series is
not $f$'s but the zero function's.

![Not analytic](../../../out/gorseller/analitik_degil.png)

**Why surprising?** The series **converges**, everywhere, just to the wrong thing.

**Misconception broken.** "An infinitely differentiable function equals its
Taylor series" and "if the series converges, it converges to the function".
Also: "the numerical derivative came out zero, so it is zero", when $f(0.1)$
is already too small for float64 to see.

---

## Summary table

| # | Result | Script | Table | Video | Lean |
|---|---|---|---|---|---|
| 1 | Lagrange bound holds | `kalan_dogrulama.py` | `kalan_dogrulama.md` | 3 | (indirectly) `ksi_vardir` |
| 2 | ξ exists | `kalan_dogrulama.py` | `ksi_varligi.md` | 3 | `ksi_vardir` |
| 3 | R lives in the complex plane | `kompleks_harita.py` | `kompleks_yaricap.md` | 4 | `disk_icinde_mutlak_yakinsar` (partly) |
| 4 | R from coefficients | `yakinsaklik_orani.py` | `cauchy_hadamard.md` | — | `cauchy_hadamard`, `geometrik_yaricap_bir` |
| 5 | Pendulum | `sarkac.py` | `sarkac.md` | 6 | none |
| 6 | Quantization | `frobenius.py` | `frobenius.md` | — | none |
| 7 | $C^\omega\subsetneq C^\infty$ | `analitik_degil.py` | `analitik_degil.md` | 5 | `purussuz_ama_analitik_degil` |
