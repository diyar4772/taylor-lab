/-
  Cauchy–Hadamard ve yakınsaklık yarıçapı —
  `02-python/src/yakinsaklik_orani.py` ve `kompleks_harita.py`'ın biçimsel
  karşılığı.

  Betikler R'yi iki bağımsız yoldan buluyordu: (a) yalnızca katsayılara
  bakarak (Cauchy–Hadamard), (b) kompleks düzlemde hatanın davranışından.
  İkisinin aynı sayıda buluşması bu bölümün içeriğidir.
-/
import Mathlib.Analysis.Analytic.RadiusLiminf
import Mathlib.Analysis.Analytic.Constructions

open Filter Topology
open scoped NNReal ENNReal

namespace TaylorLab

variable {𝕜 : Type*} [NontriviallyNormedField 𝕜]
variable {E F : Type*} [NormedAddCommGroup E] [NormedSpace 𝕜 E]
  [NormedAddCommGroup F] [NormedSpace 𝕜 F]

/-- **Cauchy–Hadamard.**

Yakınsaklık yarıçapı yalnızca katsayı dizisine bakılarak belirlenir —
fonksiyona, tekilliklerine, hatta fonksiyonun var olup olmadığına hiç
bakılmadan. `yakinsaklik_orani.py`'ın yaptığı tam olarak buydu.

Mathlib bunu `limsup |a_n|^(1/n)` yerine denk olan `liminf 1/|a_n|^(1/n)`
biçiminde ifade eder. -/
theorem cauchy_hadamard (p : FormalMultilinearSeries 𝕜 E F) :
    p.radius = liminf (fun n => (1 / (‖p n‖₊ ^ (1 / (n : ℝ)) : ℝ≥0) : ℝ≥0∞)) atTop :=
  p.radius_eq_liminf

/-- **Diskin içi gerçekten yakınsaklık bölgesidir.**

`kompleks_harita.py` bunu ölçtü: `(1/N)·log|f - P_N|` büyüklüğünün işareti
diskin içinde negatif, dışında pozitifti. Buradaki biçimsel içerik, yarıçaptan
küçük her `x` için serinin **mutlak** yakınsadığıdır. -/
theorem disk_icinde_mutlak_yakinsar (p : FormalMultilinearSeries 𝕜 E F) {x : E}
    (hx : x ∈ Metric.eball (0 : E) p.radius) :
    Summable fun n => ‖p n fun _ => x‖ :=
  p.summable_norm_apply hx

/-- **En basit somut örnek: geometrik seri, R = 1.**

`1/(1-x)` betiklerde de baş roldeydi: katsayıları hep `1` olduğu için
`|a_n|^(1/n) = 1`, yani `R = 1`. Sayısal tabloda C–H kestirimi bu satırda
tam olarak `1.0000` çıkmıştı (hata %0,00) — geometrik azalma
`limsup`'ın en kolay okuduğu durumdur. -/
theorem geometrik_yaricap_bir :
    (formalMultilinearSeries_geometric 𝕜 𝕜).radius = 1 :=
  formalMultilinearSeries_geometric_radius 𝕜 𝕜

end TaylorLab
