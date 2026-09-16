/-
  C^ω ⊊ C^∞ — `02-python/src/analitik_degil.py`'ın biçimsel karşılığı.

  Betik e^(-1/x²)'nin ilk dokuz türevinin 0'da sıfır olduğunu SEMBOLİK limitle
  doğruladı (sayısal türev burada kanıt sayılamaz: e^(-100) zaten float64'ün
  göremeyeceği kadar küçüktür). Dokuz türev bir örüntüdür, ispat değildir.
  İspat Mathlib'de duruyor.
-/
import Mathlib.Analysis.SpecialFunctions.SmoothTransition

open scoped ContDiff

namespace TaylorLab

/-- **Pürüzsüz olmak analitik olmak değildir.**

`C^ω ⊆ C^∞` içermesi apaçıktır; asıl iddia bu içermenin *gerçek* olduğu, yani
eşitlik olmadığıdır. Tanık Mathlib'de `expNegInvGlue` adıyla hazır:
`x > 0` için `e^(-1/x)`, `x ≤ 0` için `0`.

Bu, betiğin incelediği `e^(-1/x²)` ile aynı fikrin bir değişkesidir: üstel her
polinomdan hızlı sıfırlandığı için bütün türevler `0`'da ölür, dolayısıyla
Taylor serisi özdeş olarak sıfırdır — ve seri **yakınsar**, sadece fonksiyona
yakınsamaz. -/
theorem purussuz_ama_analitik_degil :
    ∃ f : ℝ → ℝ, ContDiff ℝ ∞ f ∧ ¬ AnalyticAt ℝ f 0 :=
  ⟨expNegInvGlue, expNegInvGlue.contDiff, expNegInvGlue.not_analyticAt_zero⟩

/-- Aynı ifadenin küme dilindeki hâli: sonsuz türevlenebilir olup `0`'da
analitik **olmayan** fonksiyonların kümesi boş değildir. -/
theorem contDiff_setminus_analytic_nonempty :
    {f : ℝ → ℝ | ContDiff ℝ ∞ f ∧ ¬ AnalyticAt ℝ f 0}.Nonempty :=
  purussuz_ama_analitik_degil

/-- Tanığın kendisi her yerde `0`'dan büyük-eşittir ve `x > 0` için kesin
pozitiftir. Bu, "seri yakınsıyor ama yanlış yere yakınsıyor" cümlesinin
somut ayağıdır: seri `0` verirken fonksiyon pozitiftir. -/
theorem tanik_pozitif {x : ℝ} (hx : 0 < x) : 0 < expNegInvGlue x :=
  expNegInvGlue.pos_of_pos hx

end TaylorLab
