---
title: Katman — Lean 4 (biçimsel)
tags: [kilavuz, kilavuz/katman, lean]
created: 2026-09-17
status: tamam
lang: tr
---

# Katman: Lean 4 + Mathlib (`04-lean/`)

↑ [[00-BASLA-BURADAN]] · Plan: Oturum 10 · English: [[07-layer-lean]]

## Hangi soruyu cevaplıyor?

"Ölçtüğümüz şey gerçekten bir **teorem** mi?" 144 096 noktada ihlal
bulunmaması bir kanıt değildir. Lean, ispatı makinede denetler. Kural
baştan belliydi: *Mathlib'de zaten var olanı kullan, yeniden ispatlama.* Bu
katmanın işi, sayısal bulguların hangi biçimsel ifadeye karşılık geldiğini
göstermektir.

## Dosya dosya

| Dosya | İçerik |
|---|---|
| `lean-toolchain` | `leanprover/lean4:v4.34.0`. Kanal adı değil, **açık sürüm**. |
| `lakefile.toml` | Paket `taylorlab`, kütüphane `TaylorLab`. Mathlib'i Reservoir yerine doğrudan **git** ile ister (`rev = "v4.34.0"`). |
| `lake-manifest.json` | Bağımlılıkların sabitlenmiş sürümleri. |
| `TaylorLab.lean` | Üç modülü içe aktarır. |
| `TaylorLab/Kalan.lean` | `ksi_vardir` |
| `TaylorLab/AnalitikDegil.lean` | `purussuz_ama_analitik_degil`, `contDiff_setminus_analytic_nonempty`, `tanik_pozitif` |
| `TaylorLab/Yaricap.lean` | `cauchy_hadamard`, `disk_icinde_mutlak_yakinsar`, `geometrik_yaricap_bir` |

### Yedi teorem ve karşılıkları

| Teorem | Ne der (gayriresmî) | Mathlib'deki dayanağı | Sayısal karşılığı |
|---|---|---|---|
| `ksi_vardir` | $f\in C^\infty$, $x_0\ne x$ ise $\exists\,\xi\in(x_0,x)$: $f(x)-P_n(x)=f^{(n+1)}(\xi)(x-x_0)^{n+1}/(n+1)!$ | `taylor_mean_remainder_lagrange` | `ksi_varligi.md` |
| `purussuz_ama_analitik_degil` | $\exists f:\mathbb R\to\mathbb R$, $C^\infty$ ama 0'da analitik değil | `expNegInvGlue.contDiff`, `expNegInvGlue.not_analyticAt_zero` | `analitik_degil.md` |
| `contDiff_setminus_analytic_nonempty` | Aynısı, küme dilinde | yukarıdaki | — |
| `tanik_pozitif` | Tanık $x>0$'da kesin pozitif | `expNegInvGlue.pos_of_pos` | "seri 0 verir, fonksiyon pozitif" |
| `cauchy_hadamard` | `p.radius = liminf (1/‖pₙ‖^(1/n))` | `FormalMultilinearSeries.radius_eq_liminf` | `cauchy_hadamard.md` |
| `disk_icinde_mutlak_yakinsar` | $\lVert x\rVert<R$ ise $\sum\lVert p_n(x,\dots,x)\rVert$ yakınsar | `summable_norm_apply` | haritanın içi negatif |
| `geometrik_yaricap_bir` | Geometrik serinin yarıçapı 1 | `formalMultilinearSeries_geometric_radius` | `1/(1-x)` satırı: C-H 1,0000 |

![ksi_vardir](ekler/kod-lean-ksi-vardir.png)

## Nasıl çalıştırılır

Kurulum (DNS engeli dahil): [[01-ortam-kurulumu#Lean]].

```powershell
cd 04-lean
lake exe cache get
lake build          # "Build completed successfully (2777 jobs)."
Select-String -Path TaylorLab\*.lean, TaylorLab.lean -Pattern sorry    # boş çıkmalı
cd ..
```

```bash
cd 04-lean && lake exe cache get && lake build
grep -rn sorry TaylorLab/ TaylorLab.lean
```

Aksiyom denetimi için [[02-calisma-plani#Oturum 10 — Biçimsel katman]]'daki
`eksen.lean` bloğunu kullan. Yedi teoremin hepsi
`[propext, Classical.choice, Quot.sound]` verir; bu, Windows'ta Lean 4.34.0
ile de doğrulandı.

## Çıktı nerede?

`04-lean/.lake/` (~8 GB; `.gitignore`'da). Derleme sonucu yalnızca
konsoldadır.

## Ön bilgi

- Lean 4 temel sözdizimi: `theorem`, `∃`, `:=`, `by`, `refine`, `exact`,
  `have`, anonim kurucu `⟨…⟩`.
- Mathlib kavramları: `ContDiff 𝕜 n f`, `AnalyticAt`, `FormalMultilinearSeries`,
  `uIcc` / `uIoo` (uçların sırasından bağımsız aralıklar),
  `iteratedDerivWithin`, `taylorWithinEval`, `ℝ≥0∞`.
- "Ölçüm ≠ ispat" fikri: [[10-yedi-sonuc]].

## Sınırlar (LEAN-DURUM.md'den)

Dört konu bilerek dışarıda bırakıldı:

1. "$R$ = en yakın tekilliğe uzaklık"ın biçimsel ifadesi.
2. Sarkaç / harmonik osilatör (`taylor_isLittleO` ile yapılabilir, yapılmadı).
3. Frobenius / kuantizasyon.
4. $e^{-1/x^2}$'nin kendisi için ayrı tanık (Mathlib'in tanığı $e^{-1/x}$).

Ayrıntı: [[12-eksikler-ve-devam#Lean'de kapsam dışı kalan dört konu]].

## Kurcalama önerileri

1. **`sorry` tuzağı.** Geçici bir dosyada `theorem deneme : (1:Nat) = 2 := by sorry`
   yaz, `#print axioms deneme` ile `sorryAx`'ı gör. Sonra `ksi_vardir`'in
   ispatındaki `exact` satırını `sorry` yap, `lake build` yine **geçer**
   (yalnızca uyarı verir), ama `#print axioms TaylorLab.ksi_vardir`'e
   `sorryAx` eklenir. İşin bitince `git restore 04-lean/`.
2. **Genel teoremi somut bir örneğe uygula.** Aşağıdaki blok ($e^x$, $a=0$,
   $x=1$, $N=2$) Lean 4.34.0'da derlendi:

   ```lean
   import TaylorLab
   open scoped Nat
   example : ∃ ξ ∈ Set.uIoo (0:ℝ) 1,
       Real.exp 1 - taylorWithinEval Real.exp 2 (Set.uIcc 0 1) 0 1 =
         iteratedDerivWithin 3 Real.exp (Set.uIcc 0 1) ξ * (1 - 0) ^ 3 / 3! :=
     TaylorLab.ksi_vardir (f := Real.exp) (x := 1) (x₀ := 0) 2 (by norm_num) Real.contDiff_exp
   ```

   Adlı argümanları (`(f := …)`) silip dene. Denemede buna benzer bir
   `unsolved goals ⊢ ¬?m.90 = ?m.89` hatası alındı: `by norm_num`
   çalıştığında Lean `x₀` ile `x`'in ne olduğunu henüz bilmiyordu.
   Hata mesajı okumak bu katmanın asıl dersidir.
3. **Kapsam dışı 2. maddeye başla.** `#check @taylor_isLittleO` şunu verir:
   `Convex ℝ s → x₀ ∈ s → ContDiffOn ℝ n f s → (fun x => f x - taylorWithinEval f n s x₀ x) =o[nhdsWithin x₀ s] fun x => (x - x₀) ^ n`.
   Bunu $n=2$ ve $V'(x_0)=0$ ile kullanarak
   $V(x)-V(x_0)-\tfrac12V''(x_0)(x-x_0)^2=o((x-x_0)^2)$ ifadesini kurmaya çalış.

## İlgili

[[05-katman-teori-latex]] · [[03-katman-python]] · `LEAN-DURUM.md`
