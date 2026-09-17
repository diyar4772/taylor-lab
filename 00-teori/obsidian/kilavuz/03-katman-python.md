---
title: Katman — Python (sayısal çekirdek)
tags: [kilavuz, kilavuz/katman, python]
created: 2026-09-17
status: tamam
lang: tr
---

# Katman: Python (`02-python/`)

↑ [[00-BASLA-BURADAN]] · Plan: [[02-calisma-plani]] (Oturum 2, 3, 5–9) · English: [[03-layer-python]]

## Hangi soruyu cevaplıyor?

"Teorem sayılarla tutuyor mu, ve tutmuyor **gibi** göründüğü yerde kusur
kimde, teoremde mi ölçüm aletinde mi?" `out/` altındaki 7 tablonun ve 10
grafiğin **tamamı** bu katmandan çıkar.

## Dosya dosya

| Dosya | Ne yapar | Ürettiği |
|---|---|---|
| `src/ortam.py` | stdout'u UTF-8'e çevirir, `out/` yollarını tanımlar, koyu grafik teması (`PALET`), `markdown_tablo()` ve `tablo_yaz()` | — |
| `src/taylor.py` | **Çekirdek.** `KATALOG`, `taylor_katsayilari()` (türev alarak), `polinom_fonksiyonu()`, `KalanRaporu`, `lagrange_sinir()` (+ yavaş referans sürüm), `kalan_raporu()`, mpmath yardımcıları, `cauchy_hadamard_R()`, `oran_testi_R()`. Kendi kendini test eder. | — |
| `src/kalan_dogrulama.py` | 8 fonksiyon × $N=1..12$ × 1501 nokta = **144 096** noktada Lagrange sınırı; float64 adaylarını mpmath (60 basamak) ile teyit; `ksi_bul()` ile $\xi$'yi bulur. Teyit edilen ihlal varsa çıkış kodu 1. | `kalan_dogrulama.md`, `ksi_varligi.md`, `kalan_dogrulama.png` |
| `src/kompleks_harita.py` | 6 durum için $\frac1N\log_{10}\lvert f-P_N\rvert$ haritası ($N=28$, 600×600), sıfır düzeyinden $R$ okur. | `kompleks_yaricap.md`, `kompleks_hata_haritasi.png`, `reel_eksende_ipucu_yok.png`, `yaricap_gecisi.png` |
| `src/yakinsaklik_orani.py` | 9 durum, $n\le60$ katsayıdan Cauchy–Hadamard ve oran testi; seyreklik tuzağı. | `cauchy_hadamard.md`, `cauchy_hadamard.png` |
| `src/analitik_degil.py` | $e^{-1/x^2}$: $f^{(n)}(0)$, $n=0..8$ (`sympy.limit`); reel/hayali eksen karşılaştırması. | `analitik_degil.md`, `analitik_degil.png` |
| `src/sarkac.py` | Tam sarkaç (`solve_ivp`, olay tabanlı periyot), eliptik kapalı biçim, $T_0(1+\theta_0^2/16)$ ve bir sonraki terim; log–log eğim. | `sarkac.md`, `sarkac_periyot.png`, `sarkac_yorungeler.png` |
| `src/frobenius.py` | Legendre ve Hermite reküransları (400 terim), cebirsel kesilme ölçütü, sympy ile kalıntı = 0. | `frobenius.md`, `frobenius_legendre.png`, `frobenius_hermite.png` |
| `notebooks/taylor-laboratuvari.ipynb` | 6 bölümlük özet defter; betiklerin fonksiyonlarını içe aktarır. | — (yalnızca defter içi) |

## Nasıl çalıştırılır

```powershell
python 02-python\src\taylor.py              # test, dosya yazmaz
python 02-python\src\kalan_dogrulama.py     # ~12 sn
python 02-python\src\kompleks_harita.py
python 02-python\src\yakinsaklik_orani.py
python 02-python\src\analitik_degil.py
python 02-python\src\sarkac.py
python 02-python\src\frobenius.py
```

Linux'ta `make python` son altısını sırayla çalıştırır. Ortam:
[[01-ortam-kurulumu#Python]].

## Çıktı nerede?

`out/tablolar/*.md` ve `out/gorseller/*.png`. Yollar `ortam.py`'de tek yerde
tanımlıdır; betik hangi klasörden çağrılırsa çağrılsın aynı yere yazar.

## Ön bilgi

- numpy dizileri ve vektörleştirme; sympy'de `diff`, `subs`, `lambdify`.
- Kayan nokta: makine epsilonu ($\approx2{,}2\times10^{-16}$), **yıkıcı
  sadeleşme** (birbirine yakın iki sayının farkı).
- `scipy.integrate.solve_ivp` (olay fonksiyonları), `scipy.optimize.brentq`.
- Matematik: [[05-katman-teori-latex]] §1–§3.

## Dikkat edilecek tasarım kararları

1. **Hüküm float64'e bırakılmaz.** Float64 yalnızca *aday* işaretler;
   karar mpmath'indir. Bkz. [[10-yedi-sonuc#1. Lagrange sınırı hiç ihlal edilmedi]].
2. **Tekrar yok:** bütün betikler `taylor.py`'ı içe aktarır.
3. **mpmath katsayıları için `sp.Rational(a)`:** `_mpmath_katsayilari`
   docstring'i, kayan noktalı `a`'nın hassasiyeti yediğini açıkça söyler.
   Ancak aynı koruma `katsayi_dizisi()`'de **yok**. Sonucu için
   [[12-eksikler-ve-devam]] (a=1 katsayıları).

## Kurcalama önerileri

1. **Tabanı değiştir.** `taylor.py` → `polinom_yuvarlama_tabani()` içindeki
   `(N + 2) * eps` çarpanını `10 * (N + 2) * eps` yap ve
   `kalan_dogrulama.py`'ı çalıştır. "En kötü oran" sütunundaki 1'den büyük
   değerler ne oluyor? "yuvarlama rejimi" sayıları nasıl değişiyor? Teyit
   edilen ihlal sayısı değişmemeli. Neden?
2. **Yeni fonksiyon ekle.** `kompleks_harita.py` → `DURUMLAR` listesine
   `(r"$1/(1+z^2)$, $a=0.5$", 1/(1+T.x**2), 0.5, [1j,-1j], np.sqrt(1.25), 2.4)`
   ekle. Okunan $R$ teorik $\approx1{,}118$'in yüzde kaç altında kalıyor?
   Dikkat: `ciz()` eksenleri `zip()` ile gezer ve 2×3 ızgarada 6 eksen var.
   7. durum **sessizce atlanır**. `plt.subplots(2, 3, …)`'ü `(3, 3, …)` yap.
3. **Katsayı hassasiyeti.** `yakinsaklik_orani.py` → `tablo()` içinde
   `T.katsayi_dizisi(expr, a, N_MAKS)` yerine
   `np.array([float(c) for c in T.taylor_katsayilari(expr, sp.Rational(a), N_MAKS)])`
   kullan. `1/(1+x^2), a=1` satırının oran testi hatası %22,66'dan kaça iniyor?
   (Beklenen: %0,00. [[02-calisma-plani#Oturum 6 — Yarıçapı katsayılardan okumak]])

## İlgili

- Aynı sayıların başka uygulamaları: [[06-katman-octave]], [[08-katman-godot]], [[09-katman-web]]
- Biçimsel karşılıkları: [[07-katman-lean]]
