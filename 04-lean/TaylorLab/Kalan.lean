/-
  Lagrange kalanı — `02-python/src/kalan_dogrulama.py`'ın biçimsel karşılığı.

  Betik 144 096 noktada |f - P_N| ≤ sınır olduğunu ölçtü ve teyit edilen ihlal
  sayısını 0 buldu. Ölçüm bir kanıt değildir; kanıt Mathlib'de zaten var.
-/
import Mathlib.Analysis.Calculus.Taylor

open Set
open scoped ContDiff Nat

namespace TaylorLab

/-- **ξ gerçekten vardır.**

Betiğin "ksi varlığı" tablosu her satırda bir ξ sayısı buldu ve eşitlik
artığının 0 olduğunu gösterdi. Bunun biçimsel içeriği Mathlib'in
`taylor_mean_remainder_lagrange` teoremidir: kalan bir *tahmin* değil, tek bir
ara noktada **eşitliktir**.

Burada tek yaptığımız, teoremi `ContDiff ℝ ∞` gibi kullanışlı bir hipotezden
türetmek — ispat Mathlib'e ait. -/
theorem ksi_vardir {f : ℝ → ℝ} {x x₀ : ℝ} (n : ℕ) (hx : x₀ ≠ x)
    (hf : ContDiff ℝ ∞ f) :
    ∃ ξ ∈ uIoo x₀ x,
      f x - taylorWithinEval f n (uIcc x₀ x) x₀ x =
        iteratedDerivWithin (n + 1) f (uIcc x₀ x) ξ * (x - x₀) ^ (n + 1) / (n + 1)! := by
  have huniq : UniqueDiffOn ℝ (uIcc x₀ x) := uniqueDiffOn_uIcc hx
  refine taylor_mean_remainder_lagrange hx (hf.of_le (by exact_mod_cast le_top)).contDiffOn ?_
  exact (hf.contDiffOn.differentiableOn_iteratedDerivWithin
    (by exact_mod_cast WithTop.coe_lt_top n) huniq).mono uIoo_subset_uIcc_self

end TaylorLab
