# LEAN-DURUM — biçimsel katmanın durumu

**Tarih:** 2026-09-17 · **Lean:** 4.34.0 · **Lake:** 5.0.0 · **Mathlib:** v4.34.0

## Özet

| Soru | Cevap |
|---|---|
| Derleniyor mu? | ✅ `lake build` → **2777 iş, hatasız** |
| Kaç `sorry` var? | **0** |
| Kaç teorem? | 7 |
| Eksen (axiom) kirliliği var mı? | ❌ yok — hepsi yalnız `propext`, `Classical.choice`, `Quot.sound` |

DEVAM.md §6.6 "her `sorry`'yi tek tek listele" diyordu. **Listelenecek `sorry`
yok**; bunun sebebi kahramanlık değil, işin baştan böyle kurgulanmış olmasıdır:
kural "Mathlib'de zaten var olanı kullan, yeniden ispatlama" idi. Buradaki
teoremlerin hepsi Mathlib'in mevcut sonuçlarının ya doğrudan yeniden ifadesi ya
da kullanışlı bir hipotezden türetilmiş hâlidir.

### Doğrulama komutu

```bash
export PATH="$HOME/.elan/bin:$PATH"
cd 04-lean && lake build
grep -rn "sorry" TaylorLab/ TaylorLab.lean     # boş çıkmalı
```

Eksen denetimi için:

```bash
cd 04-lean
printf 'import TaylorLab\nopen TaylorLab\n#print axioms TaylorLab.ksi_vardir\n' > /tmp/eksen.lean
lake env lean /tmp/eksen.lean
```

Beklenen çıktı: `depends on axioms: [propext, Classical.choice, Quot.sound]`.
Bu üçlü Lean'in standart tabanıdır; listede **`sorryAx` görünmemelidir**.

---

## Teorem teorem, hangi sayısal bulguya karşılık geliyor

### `TaylorLab/Kalan.lean`

| Teorem | İçerik | Sayısal karşılığı |
|---|---|---|
| `ksi_vardir` | `ContDiff ℝ ∞ f` için, `x₀ ≠ x` olduğunda `(x₀,x)` arasında öyle bir ξ vardır ki kalan **tam olarak** `f⁽ⁿ⁺¹⁾(ξ)(x−x₀)ⁿ⁺¹/(n+1)!`'dir | `kalan_dogrulama.py` §3: yedi satırın hepsinde ξ bulundu, eşitlik artığı 0 (bir satırda 4,22e−15) |

Mathlib'in `taylor_mean_remainder_lagrange` teoremi `ContDiffOn` ve
`DifferentiableOn` hipotezleriyle ifade edilmiş. `ksi_vardir` bunları
`ContDiff ℝ ∞ f` tek hipotezinden üretir — ispat gövdesi üç satır ve tamamı
Mathlib lemmalarına indirgeniyor (`uniqueDiffOn_uIcc`,
`ContDiffOn.differentiableOn_iteratedDerivWithin`, `uIoo_subset_uIcc_self`).

**Vurgu:** Kalan bir *tahmin* değil, bir **eşitliktir**. Betiğin "eşitlik artığı
0" sütunu tam olarak bunu ölçüyordu; `ksi_vardir` de tam olarak bunu söylüyor.

### `TaylorLab/AnalitikDegil.lean`

| Teorem | İçerik | Sayısal karşılığı |
|---|---|---|
| `purussuz_ama_analitik_degil` | `ContDiff ℝ ∞ f ∧ ¬ AnalyticAt ℝ f 0` olan bir `f` **vardır** | `analitik_degil.py`: ilk 9 türev sembolik limitle 0 çıktı |
| `contDiff_setminus_analytic_nonempty` | aynı ifadenin küme dilindeki hâli | — |
| `tanik_pozitif` | tanık `x > 0` için kesin pozitiftir | seri 0 verirken fonksiyon pozitif |

Tanık Mathlib'de hazır: `expNegInvGlue` (`x>0` için `e^(−1/x)`, değilse `0`) ve
`expNegInvGlue.not_analyticAt_zero`.

> **Dürüstlük notu.** Betiğin incelediği fonksiyon `e^(−1/x²)`, Mathlib'in
> tanığı ise `e^(−1/x)`. Aynı fikrin iki değişkesi; biçimsel katman betikteki
> *tam o fonksiyonu* değil, aynı olguyu (`C^ω ⊊ C^∞`) kanıtlar. `e^(−1/x²)`
> için ayrı bir Mathlib sonucu aranmadı.

Bu ayrım önemli çünkü 9 türevin sıfır çıkması bir **örüntüdür, ispat değildir**
— hele `f(0,1) = e^(−100) ≈ 3,7e−44` float64'ün göremeyeceği kadar küçükken.
Hükmü veren cebir; `purussuz_ama_analitik_degil` o hükmün makinede denetlenmiş
hâli.

### `TaylorLab/Yaricap.lean`

| Teorem | İçerik | Sayısal karşılığı |
|---|---|---|
| `cauchy_hadamard` | `p.radius = liminf (1 / ‖pₙ‖^(1/n))` | `yakinsaklik_orani.py`: R yalnızca katsayılardan kestirildi |
| `disk_icinde_mutlak_yakinsar` | `x ∈ eball 0 p.radius` ise seri **mutlak** yakınsar | `kompleks_harita.py`: `(1/N)log|f−P_N|`'in işareti diskin içinde negatif |
| `geometrik_yaricap_bir` | geometrik serinin yarıçapı tam olarak `1` | `cauchy_hadamard.md`: `1/(1-x)` satırında C–H kestirimi 1.0000, hata %0,00 |

Mathlib `limsup |aₙ|^(1/n)` yerine denk olan `liminf 1/|aₙ|^(1/n)` biçimini
kullanır; `cauchy_hadamard` bunun yeniden ifadesidir.

---

## Kapsanmayanlar (bilerek)

Bunlar **eksik değil, kapsam dışı**. Yarın devam edilirse buradan seçilebilir:

1. **"R = en yakın tekilliğe uzaklık"** biçimsel olarak ifade edilmedi.
   `1/(1+z²)` için `R = 1` gibi somut bir örneği Lean'de kurmak, kutupların
   analitik devam teorisini gerektirir; Mathlib'de altyapı var ama iş bir
   oturumluk değil.
2. **Sarkaç / harmonik osilatör** hiç ele alınmadı. `V'(x₀)=0, V''(x₀)>0`
   durumunda ikinci mertebe terimin hayatta kaldığını ifade etmek mümkün
   (Mathlib'de `taylor_isLittleO` var) ama yapılmadı.
3. **Frobenius / kuantizasyon** hiç ele alınmadı.
4. `e^(−1/x²)`'nin kendisi için ayrı bir tanık kurulmadı (yukarıdaki dürüstlük
   notuna bak).

---

## Windows'taki engel nasıl aşıldı

Windows oturumunda `elan default stable` şu hatayla düşmüştü:

```
error: error during download
info: caused by: [6] Could not resolve host: release.lean-lang.org
```

**Bu makinede de aynen tekrarlandı** (`getent hosts release.lean-lang.org` →
çözülemedi). Ama teşhis bir adım ileri götürülünce engelin dar olduğu görüldü:

| Host | Ne için | Yerel ISS çözümleyicisi |
|---|---|---|
| `release.lean-lang.org` | toolchain **index**'i (Cloudflare Pages) | ❌ çözemiyor |
| `releases.lean-lang.org` | toolchain **dosyaları** | ✅ çözüyor |
| `github.com` | Mathlib deposu | ✅ çözüyor |
| `cache.mathlib.org` | Mathlib `.olean` önbelleği | ✅ çözüyor |

Yani kırık olan tek şey **index adının çözümlenmesiydi**. Çözüm:

1. Index'i DNS'i atlayarak çek:
   `curl --resolve release.lean-lang.org:443:172.66.46.239 https://release.lean-lang.org/`
   → stable = **v4.34.0**, linux varlığı `releases.lean-lang.org` üzerinde.
2. Tarball'ı doğrudan indir (553 MB) ve elan'ın beklediği dizin adıyla aç:
   `~/.elan/toolchains/leanprover--lean4---v4.34.0`
3. `elan default leanprover/lean4:v4.34.0` — elan onu kurulu görüyor,
   index'e bir daha ihtiyaç duymuyor.
4. `lakefile.toml`'da Mathlib **Reservoir yerine doğrudan git ile** isteniyor
   (`git = "https://github.com/leanprover-community/mathlib4.git"`), çünkü
   github.com çözülüyor.

**Sudo gerekmedi, DNS'e dokunulmadı.** DEVAM.md §5'teki `nmcli` ile DNS
değiştirme adımı artık **gerekli değil** (yine de zararsız).

> Kalıcı bir uyarı: `elan default stable` gibi *index'e giden* komutlar bu ağda
> hâlâ düşer. Toolchain yükseltmek gerekirse ya yukarıdaki elle kurma yolunu
> tekrarla ya da DNS'i 1.1.1.1'e çevir.

## Disk maliyeti

```
04-lean/.lake   8,0 GB     (mathlib git geçmişi 7,3 GB + .olean'lar)
```

`.gitignore` bunu zaten dışlıyor (`04-lean/.lake/`). Depoya giren Lean
dosyaları toplam ~10 KB.
