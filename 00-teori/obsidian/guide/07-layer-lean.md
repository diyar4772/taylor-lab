---
title: Layer — Lean 4 (formal)
tags: [guide, guide/layer, lean]
created: 2026-09-17
status: done
lang: en
---

# Layer: Lean 4 + Mathlib (`04-lean/`)

↑ [[00-START-HERE]] · Plan: session 10 · Türkçe: [[07-katman-lean]]

## What question does it answer?

"Is what we measured actually a **theorem**?" Finding no violation at
144,096 points is not a proof; Lean checks the proof by machine. The rule was
set from the start: *use what already exists in Mathlib, don't re-prove it.*
The job of this layer is to show which formal statement each numerical
finding corresponds to. (Theorem names are Turkish.)

## File by file

| File | Contents |
|---|---|
| `lean-toolchain` | `leanprover/lean4:v4.34.0`: an **explicit version**, not a channel name. |
| `lakefile.toml` | Package `taylorlab`, library `TaylorLab`. Requests Mathlib directly via **git** (`rev = "v4.34.0"`) instead of Reservoir. |
| `lake-manifest.json` | Pinned dependency versions. |
| `TaylorLab.lean` | Imports the three modules. |
| `TaylorLab/Kalan.lean` (remainder) | `ksi_vardir` |
| `TaylorLab/AnalitikDegil.lean` (not analytic) | `purussuz_ama_analitik_degil`, `contDiff_setminus_analytic_nonempty`, `tanik_pozitif` |
| `TaylorLab/Yaricap.lean` (radius) | `cauchy_hadamard`, `disk_icinde_mutlak_yakinsar`, `geometrik_yaricap_bir` |

### The seven theorems and their counterparts

| Theorem | Informal meaning | Mathlib basis | Numerical counterpart |
|---|---|---|---|
| `ksi_vardir` ("ξ exists") | $f\in C^\infty$, $x_0\ne x$ ⇒ $\exists\,\xi\in(x_0,x)$: $f(x)-P_n(x)=f^{(n+1)}(\xi)(x-x_0)^{n+1}/(n+1)!$ | `taylor_mean_remainder_lagrange` | `ksi_varligi.md` |
| `purussuz_ama_analitik_degil` ("smooth but not analytic") | $\exists f:\mathbb R\to\mathbb R$, $C^\infty$ but not analytic at 0 | `expNegInvGlue.contDiff`, `expNegInvGlue.not_analyticAt_zero` | `analitik_degil.md` |
| `contDiff_setminus_analytic_nonempty` | same, in set language | as above | — |
| `tanik_pozitif` ("the witness is positive") | the witness is strictly positive for $x>0$ | `expNegInvGlue.pos_of_pos` | "the series gives 0, the function is positive" |
| `cauchy_hadamard` | `p.radius = liminf (1/‖pₙ‖^(1/n))` | `FormalMultilinearSeries.radius_eq_liminf` | `cauchy_hadamard.md` |
| `disk_icinde_mutlak_yakinsar` ("converges absolutely inside the disk") | $\lVert x\rVert<R$ ⇒ $\sum\lVert p_n(x,\dots,x)\rVert$ converges | `summable_norm_apply` | the map is negative inside |
| `geometrik_yaricap_bir` ("geometric radius is one") | the geometric series has radius 1 | `formalMultilinearSeries_geometric_radius` | the `1/(1-x)` row: C-H 1.0000 |

![ksi_vardir](../kilavuz/ekler/kod-lean-ksi-vardir.png)

## How to run

Setup (including the DNS workaround): [[01-environment-setup#Lean]].

```powershell
cd 04-lean
lake exe cache get
lake build          # "Build completed successfully (2777 jobs)."
Select-String -Path TaylorLab\*.lean, TaylorLab.lean -Pattern sorry    # must be empty
cd ..
```

```bash
cd 04-lean && lake exe cache get && lake build
grep -rn sorry TaylorLab/ TaylorLab.lean
```

For the axiom check use the `axioms.lean` block in
[[02-study-plan#Session 10 — The formal layer]]. All seven theorems give
`[propext, Classical.choice, Quot.sound]`; this was also verified on Windows
with Lean 4.34.0.

## Where is the output?

`04-lean/.lake/` (~8 GB; in `.gitignore`). Build results are console-only.

## Prerequisites

- Lean 4 basics: `theorem`, `∃`, `:=`, `by`, `refine`, `exact`, `have`,
  anonymous constructor `⟨…⟩`.
- Mathlib notions: `ContDiff 𝕜 n f`, `AnalyticAt`, `FormalMultilinearSeries`,
  `uIcc` / `uIoo` (intervals independent of endpoint order),
  `iteratedDerivWithin`, `taylorWithinEval`, `ℝ≥0∞`.
- The idea "measurement ≠ proof": [[10-seven-results]].

## Limits (from LEAN-DURUM.md)

Four topics were deliberately left out:

1. A formal statement of "$R$ = distance to the nearest singularity".
2. Pendulum / harmonic oscillator (possible via `taylor_isLittleO`, not done).
3. Frobenius / quantization.
4. A separate witness for $e^{-1/x^2}$ itself (Mathlib's witness is $e^{-1/x}$).

Details: [[12-gaps-and-next-steps#Four topics left out of Lean]].

## Things to tinker with

1. **The `sorry` trap.** In a scratch file write
   `theorem test : (1:Nat) = 2 := by sorry` and see `sorryAx` with
   `#print axioms test`. Then replace the `exact` line in the proof of
   `ksi_vardir` with `sorry`: `lake build` still **passes** (with a warning
   only), but `#print axioms TaylorLab.ksi_vardir` now includes `sorryAx`.
   Afterwards run `git restore 04-lean/`.
2. **Apply the general theorem to a concrete case.** The following block
   ($e^x$, $a=0$, $x=1$, $N=2$) compiled with Lean 4.34.0:

   ```lean
   import TaylorLab
   open scoped Nat
   example : ∃ ξ ∈ Set.uIoo (0:ℝ) 1,
       Real.exp 1 - taylorWithinEval Real.exp 2 (Set.uIcc 0 1) 0 1 =
         iteratedDerivWithin 3 Real.exp (Set.uIcc 0 1) ξ * (1 - 0) ^ 3 / 3! :=
     TaylorLab.ksi_vardir (f := Real.exp) (x := 1) (x₀ := 0) 2 (by norm_num) Real.contDiff_exp
   ```

   Try deleting the named arguments (`(f := …)`). A similar attempt produced
   `unsolved goals ⊢ ¬?m.90 = ?m.89`: when `by norm_num` ran, Lean did not
   yet know what `x₀` and `x` were. Reading error messages is the real lesson
   of this layer.
3. **Start on out-of-scope item 2.** `#check @taylor_isLittleO` gives
   `Convex ℝ s → x₀ ∈ s → ContDiffOn ℝ n f s → (fun x => f x - taylorWithinEval f n s x₀ x) =o[nhdsWithin x₀ s] fun x => (x - x₀) ^ n`.
   Use it with $n=2$ and $V'(x_0)=0$ to state
   $V(x)-V(x_0)-\tfrac12V''(x_0)(x-x_0)^2=o((x-x_0)^2)$.

## Related

[[05-layer-theory-latex]] · [[03-layer-python]] · `LEAN-DURUM.md`
