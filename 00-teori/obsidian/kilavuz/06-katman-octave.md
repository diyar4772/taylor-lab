---
title: Katman — MATLAB / Octave
tags: [kilavuz, kilavuz/katman, octave]
created: 2026-09-17
status: tamam
lang: tr
---

# Katman: MATLAB / Octave (`03-matlab-octave/`)

↑ [[00-BASLA-BURADAN]] · Plan: Oturum 5 · English: [[06-layer-octave]]

## Hangi soruyu cevaplıyor?

"Başka bir dil, başka bir katsayı yöntemiyle **aynı** sayılara varılıyor mu?"
Python katsayıları sympy ile türev alarak üretir; bu katman ise **kapalı
biçimden** (ör. kısmi kesirler) üretir. İki yol aynı yarıçapı ve aynı
Lagrange oranını veriyorsa, sonuç tek bir uygulamanın hatası olamaz.

> [!warning] MATLAB'da hiç çalıştırılmadı
> Dosyalar MATLAB uyumlu alt kümede yazıldı (`fprintf`, `~`, `%` yorum, düz
> `end`, dosya başına bir ana fonksiyon) ve **yalnızca GNU Octave'da**
> doğrulandı: Fedora'da 10.3.0, Windows'ta 11.3.0. MATLAB uyumluluğu yalnızca
> statik olarak denetlendi (`RAPOR.md` §2.1).

## Dosya dosya

| Dosya | Ne yapar |
|---|---|
| `taylor_katsayilari.m` | `[kats, R, tekillikler] = taylor_katsayilari(ad, a, N)`. Yedi fonksiyon için kapalı biçim. `a` **kompleks** olabilir. `1/(1+x^2)` için kısmi kesir $\frac{1}{2i}\left[\frac{1}{z-i}-\frac{1}{z+i}\right]$. |
| `taylor_yaklasim.m` | `[P, fdeg] = taylor_yaklasim(ad, a, N, x)`. Horner ile $P_N(x)$ ve $f(x)$; `x` kompleks dizi olabilir. Yerel yardımcı: `fonksiyon_degeri`. |
| `kalan_sinir.m` | `rapor = kalan_sinir(ad, a, N, x)`. Gerçek hata, Lagrange sınırı, yuvarlama tabanı, `aday_sayisi`, `yuvarlama_sayisi`, `en_kotu_oran`. Yerel `turev_ustsiniri` $\sup\lvert f^{(m)}\rvert$'yi **kapalı biçimden, tam olarak** hesaplar (Python ızgarada örnekler). `1/(1+x^2)` için bilerek hata verir. |
| `yakinsaklik_diski.m` | `[R_okunan, R_teorik, L] = yakinsaklik_diski(ad, a, N, pencere=3, cozunurluk=600)`. $L_N(z)$ haritası; **işaret değiştiren komşu pikseller**in merkeze en kısa uzaklığı. |
| `demo_calistir.m` | Dört bölümlük demo: (1) disk içi/dışı hata, (2) Lagrange + float64 adayları, (3) okunan R ile Python karşılaştırması, (4) merkez kaydırma. |

## Nasıl çalıştırılır

```powershell
$oct = (Get-ChildItem "$env:LOCALAPPDATA\Programs\GNU Octave\*\mingw64\bin\octave-cli.exe" | Select-Object -First 1).FullName
cd 03-matlab-octave
& $oct --no-gui --quiet demo_calistir.m
cd ..
```

```bash
(cd 03-matlab-octave && octave-cli --no-gui --quiet demo_calistir.m)
# ya da: make octave
```

Tek bir fonksiyonu etkileşimli denemek için (Octave istemi içinde):

```octave
cd 03-matlab-octave
[P, f] = taylor_yaklasim('1/(1+x^2)', 0, 8, 0.5); abs(f - P)
[Ro, Rt] = yakinsaklik_diski('ln(1+x)', 0, 28)
```

## Çıktı nerede?

Yalnızca konsola yazar; dosya üretmez. Windows 11 / Octave 11.3.0'daki
çıktıdan önemli satırlar:

| Bölüm | Değer |
|---|---|
| §1, $N=64$ | içeride `0.000e+00`, dışarıda `1.289e+11` |
| §2 | `sin N=5` en kötü oran **0.2704** (Python `taylor.py` ile aynı); toplam aday **16** |
| §2 | `cos N=7` **1.0128**, `ln(1+x) N=7` **1.0654** (float64, teyitsiz; aşağı bak) |
| §3 | okunan R: 0.9266 / 0.9165 / 0.9967 / 1.3233 / 1.8564 (Python: 0.9366 / 0.9219 / 0.9953 / 1.3321 / 1.8681) |
| §4 | $a=0,1,2$ → $R=1{,}0000;\ 1{,}4142;\ 2{,}2361$ |

## Ön bilgi

- MATLAB/Octave sözdizimi: vektörleştirme (`.*`, `.^`), `switch`, yapı
  alanları (`rapor.oran`), yerel fonksiyonlar.
- Horner şeması.
- Kısmi kesirler ve $\frac{1}{z-c}$'nin $a$ etrafındaki geometrik açılımı.

## Dikkat: bu katmanda da "aday" var ama teyit yok

`kalan_sinir.m` sınırı **tam** hesaplar, dolayısıyla Python'daki "ızgarada
sup'u kaçırma" riski burada yoktur. Buna rağmen `cos` ve `ln(1+x)` için
`en_kotu_oran > 1` çıkar. Bunun tek açıklaması float64'ün hatayı ölçerkenki
yıkıcı sadeleşmesidir. Octave katmanında mpmath karşılığı bir yüksek
hassasiyet adımı **yok**, dolayısıyla bu adaylar bu katmanda teyit edilmez.
Demo metni bunu açıkça söyler ve hükmü Python katmanına bırakır.

## Kurcalama önerileri

1. **Kompleks merkez.** `taylor_katsayilari('1/(1+x^2)', 0.4+0.3i, 1)`'in
   ikinci çıktısı ($R$) nedir? `hypot(0.4, 0.3-1)` ile karşılaştır.
   Ardından `yakinsaklik_diski('1/(1+x^2)', 0.4+0.3i, 28)`'i dene. Teorik
   değer aynı; okunan değer yüzde kaç aşağıda?
2. **Çözünürlük.** `yakinsaklik_diski('1/(1-x)', 0, 28, 3, 1200)` çalıştır.
   Okunan $R$ 0,9165'ten 0,9175'e ($r^{29}=1-r$'nin kökü) yaklaşıyor mu?
3. **Eksik fonksiyonu ekle.** `kalan_sinir.m` → `turev_ustsiniri` içinde
   `'1/(1+x^2)'` için bir üst sınır yaz. İpucu: kısmi kesirden
   $\lvert f^{(m)}(t)\rvert\le m!\,/\,\lvert t-i\rvert^{m+1}$ ve
   $\lvert t-i\rvert\ge1$. Sonra demoya `'1/(1+x^2)', 0, 6, linspace(-0.9,0.9,401)` ekle.

## İlgili

[[03-katman-python]] · [[10-yedi-sonuc#3. Yakınsaklık diski veriden çıktı]]
