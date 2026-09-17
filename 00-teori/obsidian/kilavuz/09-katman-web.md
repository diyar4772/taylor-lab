---
title: Katman — Web (tarayıcı)
tags: [kilavuz, kilavuz/katman, web]
created: 2026-09-17
status: tamam
lang: tr
---

# Katman: Web (`06-web/`)

↑ [[00-BASLA-BURADAN]] · Plan: Oturum 1, 4, 8 · English: [[09-layer-web]]

## Hangi soruyu cevaplıyor?

"Kurulum yapmadan, tarayıcıda görebilir ve kurcalayabilir miyim?" Ayrıca
dördüncü bağımsız uygulamadır: JavaScript'te kendi kompleks aritmetiği
(`C` nesnesi), kapalı biçim katsayıları, RK4 ve AGM.

## Dosya dosya

| Dosya | Ne yapar |
|---|---|
| `index.html` | Tek dosya (~860 satır), dış kaynak yok. Üç sekme, dört `<canvas>`. Betik bölümleri: kompleks aritmetik `C`, `KATALOG` (7 fonksiyon, kapalı biçim `kats(a, N)` ve `R(a)`), `polinom()` (Horner), sekme anahtarı, panel 1 (`yCiz`), panel 2 (`kCiz`), panel 3 (`rk4`, `periyotOlc`, `ellipK`, `sCiz`, `sGrafikCiz`, `sAdim`). |
| `test_matematik.mjs` | `index.html`'in **kendisini** okur, DOM'a dokunmayan matematik çekirdeğini keser ve 34 kontrol çalıştırır: fonksiyon değerleri, katsayılar, $N=40$'ta yakınsama, merkez kaydırma, **kompleks merkez** ($a=0{,}4+0{,}3i$, $N=45$), sarkaç periyotları. |

### Üç panel

| Sekme | Ayarlar | Kartlar |
|---|---|---|
| **1 · Yaklaşım ve hata** | fonksiyon, $N\in[0,30]$, $a\in[-2,2]$, hata eğrisi, yakınsaklık aralığı | yakınsaklık yarıçapı R, hata (diskin içinde / dışında), terim sayısı |
| **2 · Kompleks disk** | fonksiyon, $N\in[4,48]$, $\operatorname{Re}a\in[-2,2]$, $\operatorname{Im}a\in[-1{,}5;1{,}5]$, teorik çember, tekillikler | teorik R, haritadan okunan R, sonlu N sapması, derece N |
| **3 · Sarkaç** | genlik $\theta_0\in[5°,170°]$, animasyon | $T_0$, ölçülen T, $T_0(1+\theta_0^2/16)$, harmoniğe göre sapma, ölçüm ↔ eliptik |

![Panel 1](ekler/web-panel1-yaklasim.png)

![Panel 2 — 1/(1+x²), a=1, N=28: okunan R = 1,3263 (−6,2 %)](ekler/web-panel2-kompleks.png)

![Panel 3 — 150°](ekler/web-panel3-sarkac.png)

## Nasıl çalıştırılır

```powershell
python -m http.server 8765
# http://localhost:8765/06-web/index.html
node 06-web\test_matematik.mjs       # SONUC: 0 hata / 34 kontrol
```

## Çıktı nerede?

Tarayıcıda. Dosya üretmez.

## Ön bilgi

- Canvas 2D API, `ImageData` / `Float32Array`.
- Kompleks sayıları `[re, im]` çifti olarak tutmak; kompleks `log` ve `sqrt`'ün
  dal kesimleri (`ln(1+z)` ve `√(1+z)` için $z\le-1$ ışını).
- ES modülleri: `test_matematik.mjs` çekirdeği `data:` URL'si olarak içe aktarır.

## Katmanlar arası karşılaştırma

| Ölçüm | Python | Octave | Web | Godot |
|---|---|---|---|---|
| $R$ okunan, `1/(1+z²)`, $a=0$ | 0,9366 | 0,9266 | 0,9333 (Chrome) | — |
| $R$ okunan, `1/(1+z²)`, $a=1$ | 1,3321 | 1,3233 | 1,3263 | — |
| $T(150°)$ | 3,535702 | — | 3,535701938 | 3,5357019383 |

## Gözlemler

- Yalnızca Chrome'da denendi (masaüstü ve headless). Firefox ve Safari
  denenmedi.
- Panel 3'te büyük genliklerde (≈150°) sarkaç topu tuvalin üst kenarına
  taşar; yukarıdaki ekran görüntüsünde görülüyor.
- Sayfanın alt metni "150°'de harmonik tahmin **%76 yanlıştır**" der; bu
  harmonik değere göre bağıl farktır. Bkz.
  [[10-yedi-sonuc#5. Küçük açı yaklaşımının faturası]].

## Kurcalama önerileri

1. **Kompleks merkez.** Panel 2'de `Im(a)=0,5`, `Re(a)=0` yap. Teorik R
   $\lvert 0{,}5i - i\rvert=0{,}5$ olmalı. Disk artık hangi tekilliğe değiyor?
2. **Dal kesimi.** Panel 2'de `√(1+x)` seç ve $N$'i 48'e çıkar. Beyaz sınır
   $z=-1$'e doğru nasıl davranıyor? `ln(1+x)` ile karşılaştır.
3. **Test yaz.** `test_matematik.mjs`'e
   `esit("cos a_2 = -1/2", M.KATALOG["cos(x)"].kats([0, 0], 2)[2][0], -0.5, 1e-15);`
   satırını ekle ve `node 06-web/test_matematik.mjs` çalıştır. Kontrol sayısı
   35'e çıkmalı.

## İlgili

[[08-katman-godot]] · [[04-katman-manim]] · [[03-katman-python]]
