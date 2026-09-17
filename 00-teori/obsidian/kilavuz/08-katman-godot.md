---
title: Katman — Godot (etkileşim)
tags: [kilavuz, kilavuz/katman, godot]
created: 2026-09-17
status: tamam
lang: tr
---

# Katman: Godot 4 (`05-godot/`)

↑ [[00-BASLA-BURADAN]] · Plan: Oturum 8 · English: [[08-layer-godot]]

## Hangi soruyu cevaplıyor?

"Parametreyi **elimle** değiştirince ne olur?" Ayrıca üçüncü bağımsız
uygulamadır: katsayılar GDScript'te kapalı biçimden, sarkaç periyodu AGM ile
hesaplanır ve Python'un sayılarıyla karşılaştırılır.

## Dosya dosya

| Dosya | Ne yapar |
|---|---|
| `project.godot` | Godot 4.7, GL Compatibility, 1600×900, ana sahne `taylor_explorer.tscn` |
| `taylor_explorer.tscn` + `.gd` | **Sahne 1, Taylor keşfi.** Fonksiyon seçimi (`1/(1+x^2)`, `1/(1-x)`, `ln(1+x)`, `sin`, `exp`), derece $N\in[0,30]$, merkez $a\in[-2,2]$. Sağ panel $N$, $a$, $R$ ve yakınsaklık aralığını yazar; aralık mavi bantla çizilir. Fonksiyonlar: `f()`, `katsayilar()`, `yaricap()`, `polinom()` (Horner). |
| `denge_oyunu.tscn` + `.gd` | **Sahne 2, denge oyunu.** Solda tam denklem, sağda harmonik; ikisi RK4 ile ($h=0{,}002$) aynı genlikten başlar. **Dayanma süresi** = $\lvert\Delta\theta\rvert$'nın ilk kez `ESIK_DERECE = 10°`'yi aştığı an. Alttaki çubuk eşik aşılınca kırmızıya döner. `ellipK()` (AGM, 60 adım), `tam_periyot()`. |
| `test_dogrulama.gd` | Pencere açmadan **30 kontrol**: 16 katsayı, 5 yakınsama ($a=0{,}3$, $N=40$), 4 yarıçap, 5 sarkaç periyodu. |
| `icon.svg`, `.gitignore` | Simge; `.godot/` önbelleği git-dışı |

![Taylor keşfi — 1/(1+x²), N=16, a=0.5](ekler/godot-taylor-kesif.png)

![Denge oyunu — 150°](ekler/godot-denge-oyunu.png)

## Nasıl çalıştırılır

```powershell
godot --path 05-godot                            # Taylor keşfi
godot --path 05-godot res://denge_oyunu.tscn     # denge oyunu
godot --headless --path 05-godot --script res://test_dogrulama.gd
```

(Linux'ta aynı komutlar.) İki sahne de Windows'ta pencerede açıldı ve
test "SONUC: 0 hata" verdi.

## Çıktı nerede?

Dosya üretmez. Godot ilk açılışta `05-godot/.godot/` önbelleğini oluşturur
(git-dışı).

## Ön bilgi

- GDScript: `extends Node2D`, `_ready`, `_process`, `_draw`, `queue_redraw`,
  sinyaller (`value_changed.connect`), `match`.
- RK4 integrasyonu; birinci tür tam eliptik integral $K(m)$ ve
  aritmetik-geometrik ortalama: $K(m)=\dfrac{\pi}{2\,\mathrm{AGM}(1,\sqrt{1-m})}$.
- Sarkaç: $T=4\sqrt{L/g}\,K(\sin^2(\theta_0/2))$.

## Gözlemler

- Keşif sahnesinde eksen **sayı etiketi yoktur**; ızgara çizgileri tam
  sayılardadır ($x,y\in[-3,3]$).
- Katalogda `cos` ve `sqrt(1+x)` yoktur (web ve Octave'da vardır).
- Denge oyununda 150°'de dayanma süresi yaklaşık **0,13 s**: sarkaçlar neredeyse
  hemen ayrışır.
- Düzeltilen yorumlar ([[12-eksikler-ve-devam]], B):
  - `project.godot`'taki yorum var olmayan `testler/test_kendini.gd`'ye atıf
    yapıyor ve sabitleri `s06_denge.py` ile "birebir aynı" sayıyordu. Artık
    `test_dogrulama.gd`'yi ve `sarkac.py`'ı anıyor.
  - `taylor_explorer.gd`'deki eski `-Im(...)` yorumu `(-1)^n * Im(...)` oldu
    (`RAPOR.md` §3.5).
  - `denge_oyunu.gd`'deki "5°'de dakikalar sürer" cümlesi düzeltildi.

## Kurcalama önerileri

1. **Dayanma tablosu.** Genliği 10°, 15°, 20°, 30°, 45° yap ve dayanma
   sürelerini not et. $\log(\text{süre})$'yi $\log\theta_0$'a karşı çiz.
   Kaba beklenti: $\lvert\Delta\theta\rvert\approx\theta_0\,\Delta\omega\,t$ ve
   $\Delta\omega/\omega\approx\theta_0^2/16$, yani süre $\propto\theta_0^{-3}$
   (eğim $\approx-3$). Ölçüm bunu tutuyor mu? Bir de 5°'yi dene: iki açının
   farkı en fazla $2\theta_0=10°$ olabilir, eşik ise "10°'den **büyük**".
   Dayanma süresi yazısı çıkıyor mu?
2. **Eşiği değiştir.** `denge_oyunu.gd` → `const ESIK_DERECE := 10.0`'ı `1.0`
   yap. 5°'de süre ne kadar kısalıyor?
3. **Eksik fonksiyonu ekle.** `taylor_explorer.gd` → `KATALOG`'a `"cos"` ekle;
   `f()`, `katsayilar()` (döngü: `[cos(a), -sin(a), -cos(a), sin(a)]`) ve
   `test_dogrulama.gd`'ye `cos c_2 = -0.5` kontrolünü ekle. Testi çalıştır.

## İlgili

[[09-katman-web]] (aynı iki fikir tarayıcıda) · [[03-katman-python]] (referans sayılar)
