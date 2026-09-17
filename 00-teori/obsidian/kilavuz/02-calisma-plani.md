---
title: Çalışma planı — 10 oturum
tags: [kilavuz, kilavuz/plan]
created: 2026-09-17
status: tamam
lang: tr
---

# Çalışma planı: 10 oturum

↑ [[00-BASLA-BURADAN]] · ← [[01-ortam-kurulumu]] · English: [[02-study-plan]]

**Sıra:** görsel sezgi (1) → sayısal kanıt (2–3) → kompleks düzlem (4–7) →
fizik (8–9) → biçimsel ispat (10). Toplam ~11 saat.

**Kural:** Her oturumun sorularını **önce kendin cevapla**. Cevaplar notun
en sonunda, [[#Cevaplar]] başlığı altında.

**Kolaylık için:** komutlar depo kökünden verilir. Windows'ta `/` yerine `\`
kullanabilirsin; PowerShell ikisini de kabul eder. Her oturumun sonuna bir
[[_sablonlar/oturum-kaydi|oturum kaydı]] açabilirsin.

> [!warning] Çıktılar yeniden yazılır
> Python betikleri `out/tablolar/` ve `out/gorseller/` dosyalarını yeniden
> üretir. İşin bitince `git status`'a bak; değişiklikleri istemiyorsan
> `git restore out/` ile geri al.

| # | Oturum | Süre | Katman |
|---|---|---|---|
| 1 | [[#Oturum 1 — Polinom fonksiyonu nerede bırakır?]] | 40 dk | web, manim |
| 2 | [[#Oturum 2 — Taylor çekirdeği]] | 60 dk | python, teori |
| 3 | [[#Oturum 3 — Lagrange kalanı bir eşitliktir]] | 90 dk | manim, python |
| 4 | [[#Oturum 4 — Bir boyut yukarı]] | 45 dk | manim, web |
| 5 | [[#Oturum 5 — Diski veriden okumak]] | 75 dk | python, octave |
| 6 | [[#Oturum 6 — Yarıçapı katsayılardan okumak]] | 60 dk | python |
| 7 | [[#Oturum 7 — Yakınsamak eşit olmak değildir]] | 45 dk | manim, python |
| 8 | [[#Oturum 8 — Atılan terim periyotta geri döner]] | 90 dk | python, web, godot, manim |
| 9 | [[#Oturum 9 — Kuantizasyon kesilmeden doğar]] | 60 dk | python |
| 10 | [[#Oturum 10 — Biçimsel katman]] | 90 dk | lean |

---

## Oturum 1 — Polinom fonksiyonu nerede bırakır?

**Süre:** 40 dk

**Amaç:** $N$'i artırmanın iyi bölgeyi büyüttüğünü, ama bir sınırın
ötesinde işe yaramadığını ve katsayıdaki $n!$'in nereden geldiğini görmek.

**Çalıştır:**

```powershell
python -m http.server 8765
# tarayıcı: http://localhost:8765/06-web/index.html
```

**Bak:**

1. Web → **1 · Yaklaşım ve hata** sekmesi. `1/(1+x²)` seç, "Yakınsaklık
   aralığını göster"i aç, $N$'i 2'den 30'a kaydır. Alt kartlardan **hata,
   diskin içinde** değerinin küçüldüğünü, **hata, diskin dışında** değerinin
   ise büyüdüğünü izle.

   ![Web paneli 1](ekler/web-panel1-yaklasim.png)

2. Aynı şeyi `sin x` ile yap: artık duvar yok, ama her $N$'de eğri yine bir
   yerden sonra kaçıyor.
3. Video 1 (25 sn): sağ üstteki "geçerli bölge" sayısı $N=1$'de $|x|<0{,}6$,
   $N=15$'te $|x|<6{,}1$.

   [![Video 1 — Artan derece](ekler/video1-artan-derece.png)](../../../out/videolar/1-ArtanDereceSahnesi.mp4)
   ![[1-ArtanDereceSahnesi.mp4]]

4. Video 2 (40 sn): $x=a$ koyunca hangi terimlerin öldüğüne dikkat et.

   [![Video 2 — Türetme](ekler/video2-turetme.png)](../../../out/videolar/2-TuretmeSahnesi.mp4)
   ![[2-TuretmeSahnesi.mp4]]

**Oku:**

- `01-manim/scenes/s01_artan_derece.py` → `iyi_bolge()` ("geçerli bölge"nin
  tanımı) ve `sin_taylor()`.
- `out/taylor-teori.pdf` §1: $P^{(n)}(a)=n!\,c_n$ önermesi ve ispatı.
- Atomik not: [[Taylor açılımı bir tanım değil zorunluluktur]].

**Kendine sor:**

1. $\sin$ için $R=\infty$ iken neden her sonlu $N$'de polinom bir yerden sonra kaçar?
2. `1/(1+x²)` reel eksende her yerde düzgün. Duvarın $|x|=1$'de olmasını
   reel eksendeki bir şeyle açıklayabilir misin?
3. $c_n=f^{(n)}(a)/n!$ içindeki $n!$ nereden geliyor? Tek cümle.
4. Videodaki "geçerli bölge" bir metafor mu, ölçülen bir sayı mı?

---

## Oturum 2 — Taylor çekirdeği

**Süre:** 60 dk

**Amaç:** Bütün sayısal katmanın dayandığı `taylor.py`'ı satır satır tanımak.

**Çalıştır:**

```powershell
python 02-python\src\taylor.py
```

**Bak:** Çıktı dört blok basar: `sin` katsayıları, `exp` türev testi,
`sin, a=0, N=5: aday ihlal=0, en kötü oran=0.2704` ve üç fonksiyon için
C-H/oran kestirimi. Son satır `Tüm kontroller geçti.` olmalı. Şu satıra
dikkat et: `exp: C-H R≈7.9289  oran R≈30.0000  teorik R=inf`.

**Oku** (`02-python/src/taylor.py`):

- `taylor_katsayilari()`: katsayıyı **türev alarak** üretir.
- `polinom_fonksiyonu()`: sympy'den numpy'ye geçiş.
- `KalanRaporu`: `aday_sayisi`, `yuvarlama_sayisi`, `en_kotu_oran` alanları.
- `lagrange_sinir()`: `np.maximum.accumulate` ile $O(M+P)$ sınır.
- `cauchy_hadamard_R()` ve `oran_testi_R()`.
- En alttaki `if __name__ == "__main__":` bloğu (testler).
- Ayrıntı: [[03-katman-python]].

**Kendine sor:**

1. `taylor_katsayilari` neden `sp.series` kullanmıyor?
2. `lagrange_sinir` neden kümülatif maksimum kullanabiliyor? Hangi gözleme dayanıyor?
3. `exp` için C-H $\approx 7{,}93$, oran testi $=30$ çıkıyor, teorik $R=\infty$. Bu bir hata mı?
4. `aday_sayisi` ile `yuvarlama_sayisi` ne ölçer?

---

## Oturum 3 — Lagrange kalanı bir eşitliktir

**Süre:** 90 dk

**Amaç:** Float64'ün "ihlal" dediği noktaların neden teorem ihlali
olmadığını ve $\xi$'nin gerçekten bulunabildiğini görmek.

**Çalıştır:**

```powershell
python 02-python\src\kalan_dogrulama.py      # ~12 sn, out\ altını yeniden yazar
```

Sonra tablodaki en şüpheli satırı kendin incele. `02-python/src` klasöründe
`python` yaz ve şunu yapıştır:

```python
import numpy as np, sympy as sp, taylor as T
e = sp.log(1 + T.x); x = np.linspace(-0.85, 2.0, 1501)
r = T.kalan_raporu(e, 0.0, 7, x)
anlamli = np.isfinite(r.gercek_hata) & (r.lagrange_sinir > r.yuvarlama_tabani)
oran = np.where(anlamli, r.gercek_hata / np.where(r.lagrange_sinir > 0, r.lagrange_sinir, 1), 0)
i = int(np.argmax(oran)); print(x[i], oran[i], r.gercek_hata[i], r.lagrange_sinir[i])
m = T.yuksek_hassasiyet_sadece_hata(e, 0.0, 7, float(x[i])); print("mpmath oranı:", m / r.lagrange_sinir[i])
```

Beklenen: `x ≈ 0.0126`, float64 oranı `2.359…`, mpmath oranı `0.9889…`.

**Bak:**

- `out/tablolar/kalan_dogrulama.md`: **float64 aday ihlal**, **en kötü
  oran** ve **yuvarlama rejimi** sütunları; alttaki ikinci tabloda
  **float64 oran** ile **mpmath oran**.
- `out/tablolar/ksi_varligi.md`: son satır (`ln(1+x)`, `x=1.8`).
- `out/gorseller/kalan_dogrulama.png`: gri bant = float64 ölçüm tabanı.

  ![Lagrange kalanı](../../../out/gorseller/kalan_dogrulama.png)

- Video 3: $N=10$, $x=2$'de oran $0{,}9748$. Sınır keskin.

  [![Video 3 — Lagrange kalanı](ekler/video3-kalan.png)](../../../out/videolar/3-KalanTerimiSahnesi.mp4)
  ![[3-KalanTerimiSahnesi.mp4]]

**Oku:**

- `taylor.py` → `kalan_raporu()` (docstring'deki `exp, a=1, N=12, x=0.996` örneği).

  ![kalan_raporu](ekler/kod-taylor-kalan-raporu.png)

- `taylor.py` → `_mpmath_katsayilari()` (neden `sp.Rational(a)`?) ve
  `yuksek_hassasiyet_sadece_hata()`.
- `kalan_dogrulama.py` → `adaylari_teyit_et()`, `ksi_bul()`.

  ![mpmath teyidi](ekler/kod-mpmath-teyit.png)

- Derinlemesine: [[10-yedi-sonuc#1. Lagrange sınırı hiç ihlal edilmedi]] ve
  [[10-yedi-sonuc#2. ξ gerçekten var — yarıçapın dışında bile]].

**Kendine sor:**

1. Tabloda `ln(1+x)` için "en kötü oran" 2,3593. Teorem çiğnendi mi?
2. Sınır float64'te hesaplanıyor da hata neden mpmath istiyor?
3. `x=1.8`, $R=1$'in dışında. $\xi$ orada neden hâlâ var?
4. `ksi_bul` tek bir $\xi$ döndürüyor. $\xi$ tek midir?

---

## Oturum 4 — Bir boyut yukarı

**Süre:** 45 dk

**Amaç:** Yakınsaklık yarıçapının merkezden en yakın **kompleks**
tekilliğe uzaklık olduğunu gözle görmek.

**Çalıştır:** Oturum 1'deki sunucu. Web → **2 · Kompleks disk**.

**Bak:**

1. `1/(1+x²)`, $N=28$. `Merkez Re(a)`'yı 0 → 1 → 2 kaydır, **teorik R** ile
   **haritadan okunan R** kartlarını karşılaştır. $a=1$'de ekran:

   ![Web paneli 2](ekler/web-panel2-kompleks.png)

2. `Merkez Im(a)`'yı $+0{,}5$'e çek: disk ne yapıyor?
3. `ln(1+x)` seç, $N$'i 4'ten 48'e çıkar: beyaz sınır sola doğru basık.
4. `eˣ` seç: sınır yok.
5. Video 4 (58 sn), en önemli video.

   [![Video 4 — disk beliriyor](ekler/video4-disk-beliriyor.png)](../../../out/videolar/4-KompleksYaricapSahnesi.mp4)
   ![[4-KompleksYaricapSahnesi.mp4]]

   ![Video 4 — merkezi kaydır](ekler/video4-merkez-kaydir.png)

**Oku:**

- `out/taylor-teori.pdf` §3: "Yarıçap = en yakın tekilliğe uzaklık" teoremi
  ve "Merkezi kaydırmak" tablosu.
- Atomik not: [[Yakınsaklık yarıçapı kompleks düzlemde belirlenir]].

**Kendine sor:**

1. `Im(a)` sıfırdan farklıyken $R$ nasıl değişir?
2. `1/(1+x²)` için $a=0$'da neden $R=1$?
3. "Sonlu N sapması" neden hep negatif?
4. `eˣ` için neden sınır çizgisi çıkmıyor?

---

## Oturum 5 — Diski veriden okumak

**Süre:** 75 dk

**Amaç:** Diskin çizilmediğini, hatanın kendi işaretinden çıktığını iki
bağımsız uygulamada (Python ve Octave) doğrulamak.

**Çalıştır:**

```powershell
python 02-python\src\kompleks_harita.py
cd 03-matlab-octave; & $oct --no-gui --quiet demo_calistir.m; cd ..
```

(`$oct` için bkz. [[01-ortam-kurulumu#Octave]]; Linux'ta `octave-cli`.)

**Bak:**

- `out/gorseller/kompleks_hata_haritasi.png`: siyah kontur = haritanın
  kendi sıfır düzeyi, yeşil kesikli = teorik çember.

  ![Kompleks hata haritası](../../../out/gorseller/kompleks_hata_haritasi.png)

- `out/gorseller/reel_eksende_ipucu_yok.png` ve `yaricap_gecisi.png`.
- `out/tablolar/kompleks_yaricap.md`: **teorik R** ve **haritadan okunan R**.
- Octave çıktısı §1: $x=0{,}5$'te hata $N$ ile düşer, $x=1{,}5$'te büyür.
- Octave çıktısı §3: **okunan R**, **sapma** ve **python** sütunları yan yana.

**Oku:**

- `kompleks_harita.py` → `hata_haritasi()` docstring'i (neden $N$'e bölünüyor).
- `kompleks_harita.py` → `yaricapi_haritadan_kestir()`.

  ![yaricapi_haritadan_kestir](ekler/kod-yaricapi-haritadan-kestir.png)

- `03-matlab-octave/yakinsaklik_diski.m` (işaret değiştiren pikseller) ve
  `taylor_katsayilari.m` → `case '1/(1+x^2)'` (kısmi kesirle kapalı biçim).

**Kendine sor:**

1. $\frac1N\log_{10}|f-P_N|$ neden $\log_{10}(|z-a|/R)$'ye gider?
2. `1/(1-z)` için okunan $R=0{,}9219$. Neden 1 değil ve neden en kısa uzaklık
   özellikle $z=1$ yönünde?
3. Octave 0,9165, Python 0,9219 buluyor. Hangisi "doğru"?
4. Octave §1'de $x=1{,}5$'te $N$'i 4'ten 64'e çıkarmak ne işe yarıyor?

---

## Oturum 6 — Yarıçapı katsayılardan okumak

**Süre:** 60 dk

**Amaç:** Cauchy–Hadamard'ın neden limit değil **limsup** ile kurulduğunu
ve sonlu veriyle neyin görülüp neyin görülemeyeceğini anlamak.

**Çalıştır:**

```powershell
python 02-python\src\yakinsaklik_orani.py
```

Ardından `02-python/src` içinde `python` aç ve oran testinin $N$'e göre
nasıl davrandığını **tam (rasyonel) katsayılarla** gör:

```python
import numpy as np, sympy as sp, taylor as T
e = 1/(1 + T.x**2)
tam = np.array([float(c) for c in T.taylor_katsayilari(e, sp.Integer(1), 60)])
kayan = T.katsayi_dizisi(e, 1.0, 60)            # tablonun kullandığı
for N in range(52, 61):
    print(N, round(T.oran_testi_R(tam[:N+1]), 4), round(T.cauchy_hadamard_R(tam[:N+1]), 4))
print("c_60  tam:", tam[60], " kayan:", kayan[60])
```

Beklenen: oran testi `1.4142, 1.0, 2.0, 2.0, 1.4142, …` diye dönüp durur;
C-H ≈ `1.423`'te sabit kalır; `c_60` tam değeri `-4.66e-10`, kayan noktalı
değeri `+2.55e-09`.

**Bak:**

- `out/tablolar/cauchy_hadamard.md`: **C-H kestirimi**, **C-H hatası**,
  **oran testi**, **oran hatası**.
- `out/gorseller/cauchy_hadamard.png`: sağ panelde $e/n$ (Stirling).

  ![Cauchy–Hadamard](../../../out/gorseller/cauchy_hadamard.png)

**Oku:**

- `yakinsaklik_orani.py` → `kismi_kestirimler()`, `seyreklik_tuzagi()`.
- `taylor.py` → `cauchy_hadamard_R()` (`son_k=12`, sıfırları atlama) ve
  `oran_testi_R()` (`d` derece farkı).
- `04-lean/TaylorLab/Yaricap.lean` → `cauchy_hadamard`.
- Derinlemesine: [[10-yedi-sonuc#4. Aynı yarıçap, yalnızca katsayılardan]].

**Kendine sor:**

1. `exp` için C-H 19,11 çıkıyor. $R=\infty$ ile çelişiyor mu?
2. `1/(1+x²)`, $a=1$ için oran testinin limiti neden yok?
3. Tablodaki %22,66'nın hepsi "limit yok" gerçeğinden mi geliyor?
4. Mathlib neden $\limsup |a_n|^{1/n}$ yerine $\liminf 1/|a_n|^{1/n}$ yazıyor?

---

## Oturum 7 — Yakınsamak eşit olmak değildir

**Süre:** 45 dk

**Amaç:** $C^\infty$ ile $C^\omega$ arasındaki farkı $e^{-1/x^2}$ üzerinden kavramak.

**Çalıştır:**

```powershell
python 02-python\src\analitik_degil.py
```

**Bak:**

- `out/tablolar/analitik_degil.md`: iki tablo. Türevler ($n=0..8$, limit ve
  $x=0{,}1$ değeri) ve "reel eksen / hayali eksen".
- `out/gorseller/analitik_degil.png`.

  ![Analitik değil](../../../out/gorseller/analitik_degil.png)

- Video 5 (47 sn):

  [![Video 5 — seri sıfır](ekler/video5-seri-sifir.png)](../../../out/videolar/5-AnalitikDegilSahnesi.mp4)
  ![[5-AnalitikDegilSahnesi.mp4]]

  ![Video 5 — esas tekillik](ekler/video5-esas-tekillik.png)

**Oku:**

- `analitik_degil.py` → `turevler_sifirda()` (`sp.limit`), `kompleks_tekillik()`.
- `out/taylor-teori.pdf` §4 (ispatın çatısı: $f^{(n)}(x)=p_n(1/x)e^{-1/x^2}$).
- `04-lean/TaylorLab/AnalitikDegil.lean`.
- Atomik not: [[Pürüzsüz olmak analitik olmak değildir]].

**Kendine sor:**

1. Türevler neden sayısal fark yerine `sympy.limit` ile hesaplanıyor?
2. Serinin yarıçapı $\infty$ ama $z=0$ esas tekillik. "R = en yakın
   tekilliğe uzaklık" ile çelişki var mı?
3. Lean'deki tanık $e^{-1/x}$, betikteki $e^{-1/x^2}$. Bu önemli mi?

---

## Oturum 8 — Atılan terim periyotta geri döner

**Süre:** 90 dk

**Amaç:** Her kararlı dengenin neden harmonik olduğunu ve atılan
$-\theta^3/6$'nın periyodun genliğe bağımlılığı olarak nasıl ölçüldüğünü
görmek.

**Çalıştır:**

```powershell
python 02-python\src\sarkac.py
godot --path 05-godot res://denge_oyunu.tscn
godot --headless --path 05-godot --script res://test_dogrulama.gd
```

**Bak:**

1. Video 6 (55 sn): önce parabolün gerçek potansiyele oturması...

   [![Video 6 — parabol](ekler/video6-parabol.png)](../../../out/videolar/6-DengeSahnesi.mp4)
   ![[6-DengeSahnesi.mp4]]

   ...sonra genlik 1,3'te iki eğrinin ayrışması. **Bu kareye eleştirel bak**
   (Soru 3):

   ![Video 6 — genlik 1.3](ekler/video6-bariyer.png)

2. `out/tablolar/sarkac.md`: **ölçülen T**, **eliptik T**, **ölçüm-kapalı
   fark**, **Taylor-2 hatası**, **Taylor-4 hatası**.
3. `out/gorseller/sarkac_periyot.png`: sağ panel başlığındaki log–log eğimler.

   ![Sarkaç periyodu](../../../out/gorseller/sarkac_periyot.png)

4. Web → **3 · Sarkaç**, genlik 150°:

   ![Web paneli 3](ekler/web-panel3-sarkac.png)

5. Godot denge oyunu: genliği 10°, 45°, 90°, 150° yap ve **Dayanma süresi**'ni
   not et.

   ![Godot denge oyunu](ekler/godot-denge-oyunu.png)

**Oku:**

- `sarkac.py` → `periyodu_olc()`, `tam_periyot_eliptik()`, `taylor_periyot()`.
- `05-godot/denge_oyunu.gd` → `ellipK()` (AGM), `_rk4()`, `ESIK_DERECE`.
- `01-manim/scenes/s06_denge.py` → `V()`, `denge_bul()`, `genlikler`.
- Atomik not: [[Her kararlı denge harmonik osilatördür]].

**Kendine sor:**

1. "150°'de tahmin %76 yanlış." %76 neye göre?
2. Log–log eğimleri neden 2, 4, 6 diye ikişer artıyor?
3. Video 6'da genlik 1,3'teki ayrışma gerçekten "anharmonisite" mi?
4. `periyodu_olc` neden $T = 4\,t_{\text{ilk geçiş}}$ alıyor?

---

## Oturum 9 — Kuantizasyon kesilmeden doğar

**Süre:** 60 dk

**Amaç:** Tam sayıların denklemden değil, serinin sonlu kalma şartından
çıktığını görmek.

**Çalıştır:**

```powershell
python 02-python\src\frobenius.py
```

**Bak:**

- `out/tablolar/frobenius.md`: Legendre tablosu (**kısmi toplam büyümesi**
  sütunu), Hermite tablosu (**H(4)**, **ψ(4)**, **durum**), sembolik
  doğrulama (**denklemdeki kalıntı**).
- `out/gorseller/frobenius_hermite.png` ve `frobenius_legendre.png`.

  ![Hermite](../../../out/gorseller/frobenius_hermite.png)

**Oku:**

- `frobenius.py` → `legendre_katsayilari()`, `hermite_katsayilari()`,
  `kesilme_derecesi()`, `kesilme_dogrula()`,
  `sembolik_dogrulama.kesin_katsayilar()`.

  ![kesilme_derecesi](ekler/kod-frobenius-kesilme.png)

- `out/taylor-teori.pdf` §6.

**Kendine sor:**

1. $\lambda=2$ iken **tek** seri ($a_0=0,\ a_1=1$) kesilir mi?
2. Kesilme kararı neden "katsayı $10^{-14}$'ün altına indi mi" diye verilemez?
3. Tablodaki "normalize edilebilir / PATLIYOR" kararı neye göre veriliyor?
4. $E_n=\hbar\omega(n+\tfrac12)$'deki $n$ bu betikte nerede?

---

## Oturum 10 — Biçimsel katman

**Süre:** 90 dk (ilk kurulum hariç; Mathlib indirmesi daha uzun sürebilir)

**Amaç:** Üç sayısal bulgunun Lean/Mathlib'deki biçimsel karşılığını
okumak ve bir ispatın "sorry'siz" olduğunu nasıl denetleyeceğini öğrenmek.

**Çalıştır (Windows):**

```powershell
cd 04-lean
lake build
$p = Join-Path $env:TEMP 'eksen.lean'
[IO.File]::WriteAllText($p, @'
import TaylorLab
#print axioms TaylorLab.ksi_vardir
#print axioms TaylorLab.purussuz_ama_analitik_degil
#print axioms TaylorLab.cauchy_hadamard
theorem deneme : (1 : Nat) = 2 := by sorry
#print axioms deneme
'@)
lake env lean $p
cd ..
```

**Linux:** aynı içeriği `/tmp/eksen.lean`'e yaz, sonra
`cd 04-lean && lake env lean /tmp/eksen.lean`.

**Bak:** Gerçek teoremler için
`depends on axioms: [propext, Classical.choice, Quot.sound]`; `deneme` için
`warning: declaration uses 'sorry'` ve `depends on axioms: [sorryAx]`.

**Oku:**

- `04-lean/TaylorLab/Kalan.lean` → `ksi_vardir`.

  ![ksi_vardir](ekler/kod-lean-ksi-vardir.png)

- `04-lean/TaylorLab/AnalitikDegil.lean` → `purussuz_ama_analitik_degil`,
  `contDiff_setminus_analytic_nonempty`, `tanik_pozitif`.
- `04-lean/TaylorLab/Yaricap.lean` → `cauchy_hadamard`,
  `disk_icinde_mutlak_yakinsar`, `geometrik_yaricap_bir`.
- `LEAN-DURUM.md` (tamamı) ve [[07-katman-lean]].

**Kendine sor:**

1. `ksi_vardir` neden `Ioo` değil de `uIoo x₀ x` kullanıyor?
2. `#print axioms` neden `lake build`'in başarılı olmasından daha güçlü bir kanıt?
3. Yedi sonuçtan hangileri Lean'de **hiç** yok?
4. `geometrik_yaricap_bir`, `cauchy_hadamard.md`'deki hangi satırın karşılığı?

---

## Cevaplar

> [!warning] Önce kendin cevapla.

### Oturum 1

1. $\sin$'in serisi her $x$ için yakınsar, ama bu **limitte** olur.
   Sabit $N$'de $P_N$ bir polinomdur ve $|x|\to\infty$'da $\pm\infty$'a gider;
   $\sin$ ise sınırlıdır. Hata $|x|^{N+1}/(N+1)!$ mertebesindedir, yani iyi bölge
   yaklaşık $|x| \lesssim ((N+1)!\cdot\text{tol})^{1/(N+1)}$ kadardır ve $N$ ile büyür.
2. Hayır. Reel eksende fonksiyon sınırlı ve sonsuz türevlenebilir. Sebep
   $z=\pm i$'deki kutuplardır (Oturum 4).
3. $(x-a)^n$'i $n$ kez türevleyince önüne $n!$ düşer; $P^{(n)}(a)=f^{(n)}(a)$
   istenirse $n!$'e bölmek bu çarpanı geri almanın tek yoludur.
4. Ölçülen bir sayı: `iyi_bolge()`, $|\sin x - P_N(x)|$'in **0,05**'i ilk
   aştığı $x$'i (0'dan sağa, 4000 noktalık ızgarada) döndürür.

### Oturum 2

1. Amaç katsayının nereden geldiğini kodda görünür kılmak: $n$. türev alınır,
   $x=a$ konur, $n!$'e bölünür. Tanımın birebir çevirisidir.
2. $[a,x]$ aralığı $x$, $a$'dan uzaklaştıkça yalnızca **genişler**, dolayısıyla
   $\sup_{[a,x]}|f^{(N+1)}|$ azalamaz. Tek ızgarada $a$'dan dışarı doğru kümülatif
   maksimum yeterli. Sol ve sağ kol ayrı hesaplanır. Doğruluğu
   `lagrange_sinir_yavas` ile karşılaştırılır (kalan_dogrulama.py §2).
3. Hata değil, **yöntemin sınırı.** Sonsuzu sonlu veriden okuyamazsın.
   $(1/n!)^{1/n}\approx e/n$ olduğundan kestirim $N$ ile büyür: $N=30$'da 7,93,
   $N=60$'ta 19,11, $N=120$'de 41,3. Oran testi ise tam $N$'yi verir
   ($|a_n/a_{n+1}|=n+1$). "Büyüyor" demek, $R=\infty$'u görmenin tek dürüst yoludur.
4. `aday_sayisi`: float64'e göre `gerçek hata > sınır` olan nokta sayısı
   (teyit edilmemiş). `yuvarlama_sayisi`: sınırın float64'ün ölçebileceği en
   küçük farkın (`(N+2)·eps·(Σ|terim|+|f|)`) **altında** kaldığı nokta sayısı.

### Oturum 3

1. Hayır. O oran float64 ile ölçüldü. Nokta $x\approx0{,}0126$, sınır
   $\approx7{,}9\times10^{-17}$, yani makine epsilonu mertebesinde. "Anlamlı rejim"
   sınıflandırması `(N+2)·eps` sabitine dayanan bir kestirim olduğu için bu nokta
   sınırın hemen üstünde kalıp "anlamlı" sayıldı. mpmath oranı **0,989**. Tablodaki
   8 satırın 6'sında "en kötü oran" 1'i geçer; hepsi aynı türden ölçüm
   artığıdır ve 2224 adayın **tamamı** mpmath'le 1'in altına döner.
   Bkz. [[10-yedi-sonuc#1. Lagrange sınırı hiç ihlal edilmedi]].
2. Sınır, $\sup|f^{(N+1)}|\cdot|x-a|^{N+1}/(N+1)!$ biçiminde bir **çarpım**dır;
   yıkıcı sadeleşme yoktur. Hata ise birbirine çok yakın iki sayının **farkıdır**
   ($f(x)-P_N(x)$); float64 16 haneden sonrasını göremez.
3. Lagrange teoremi yalnızca $f$'in $[a,x]$ üzerinde yeterince türevlenebilir
   olmasını ister. $\ln(1+x)$, $[0,\,1{,}8]$'de pürüzsüzdür. Yakınsaklık
   yarıçapı ise $N\to\infty$ limitiyle ilgili bir kavramdır; sonlu $N$ eşitliğini
   etkilemez. Polinom ≠ seri.
4. Hayır, tek olmak zorunda değil. Teorem yalnızca **varlık** söyler.
   `ksi_bul`, $(a,x)$'i 4001 noktada tarar ve **ilk** işaret değişimindeki kökü
   `brentq` ile döndürür; başka kökler olabilir.

### Oturum 4

1. $R=\min(|a-i|,|a+i|)$ olur. $\operatorname{Im}(a)>0$ iken merkez $+i$'ye yaklaşır
   ve $R$ küçülür. Disk hep daha yakın olan tekilliğe değer.
2. $1+z^2=(z-i)(z+i)$; kutuplar $\pm i$, ikisi de 0'a 1 uzaklıkta.
3. Sonlu $N$'de $|f-P_N|\approx C\,(r/R)^{N+1}$ ifadesindeki $C$ çarpanı
   tekilliğe yaklaştıkça büyür ve sıfır düzeyini içeri çeker. Okunan $R$ bu
   düzeyin merkeze **en kısa** uzaklığı olduğu için hep tekilliğe doğru olan
   yönde ölçülür ve daima biraz küçük çıkar (Oturum 5, Soru 2).
4. $e^z$'nin tekilliği yoktur ($R=\infty$). Pencerenin her yerinde hata
   $N$ ile sıfıra gider, yani işaret değişimi olmaz.

### Oturum 5

1. Kuyruk $|f-P_N|\sim C(|z-a|/R)^{N+1}$ gibi davranır. Logaritma alıp $N$'e
   bölünce $\frac{N+1}{N}\log_{10}(|z-a|/R)+\frac{\log_{10}C}{N}\to\log_{10}(|z-a|/R)$.
   İşareti yakınsaklığı söyler, sıfır düzeyi $|z-a|=R$ çemberidir.
2. $f-P_N = z^{N+1}/(1-z)$. $z=r$ (tekilliğe doğru) yönünde sıfır düzeyi
   $r^{29}=1-r$ denkleminin kökü olur: $r\approx0{,}9175$. Izgara adımı
   ($4{,}4/600\approx0{,}007$) ile ilk pozitif piksel 0,9219'da. Ters yönde
   $|1-z|=1+r$ olduğu için sıfır düzeyi 1'in **dışına** düşer; en kısa uzaklık
   o yüzden tekillik yönündedir.
3. İkisi de doğru ama aynı şeyi ölçmüyor. Python pencere 2,2 / 600 piksel /
   `L>0` olan en yakın piksel kullanıyor; Octave pencere 3 / 600 piksel /
   **işaret değiştiren komşu çiftler** kullanıyor. Fark ızgaradan geliyor.
   İkisi de teorik değerin altında (Soru 2).
4. Hiçbir işe yaramıyor, tersine zarar veriyor. Hata $3{,}5$'ten
   $1{,}3\times10^{11}$'e çıkıyor, çünkü $|x|>R$'de terimler $(1{,}5)^n$ gibi büyür.

### Oturum 6

1. Çelişmiyor. Sonlu $N$'den $R=\infty$ okunamaz; kestirim $N$ ile büyür
   (Oturum 2, Soru 3). Tabloda bu satırın hata sütunu bilerek "—".
2. $a=1$'den $i$ ve $-i$ **eşit uzaklıkta** ($\sqrt2$) ama farklı yönde. Katsayılar
   $c_n=(-1)^n\,2^{-(n+1)/2}\sin\frac{(n+1)\pi}{4}$ biçimindedir. $\sin$ çarpanı
   periyodiktir ve $n\equiv3 \pmod 4$ için sıfırdır. Bu yüzden ardışık oranlar
   $\{1,\ 2,\ 2,\ \sqrt2\}$ arasında döner; oranın **limiti yoktur**.
   $\limsup|c_n|^{1/n}=1/\sqrt2$ ise vardır.
3. **Hayır.** `katsayi_dizisi(expr, 1.0, 60)`, $a$'yı kayan noktalı sayı olarak
   verir ve yüksek mertebeli türevlerde hassasiyet kaybolur. $n=40$'ta bağıl hata
   $\sim10^{-5}$, $n=60$'ta katsayının **işareti bile yanlış**. Tam katsayılarla
   $N=60$'ta oran testi tam $\sqrt2$, C-H 1,4228 (%0,61) çıkar. Tablodaki %22,66
   ve %1,66 bu hassasiyet kaybıyla kirlenmiş sayılardır. "Limit yok" dersi yine
   doğrudur, ama onu gösteren şey tek bir $N$ değil, oranın $N$ ile **salınmasıdır**.
   Bkz. [[12-eksikler-ve-devam]].
4. İkisi denktir: $\limsup x_n = 1/\liminf(1/x_n)$ (pozitif diziler ve
   $[0,\infty]$ değerleri için). Mathlib yarıçapı doğrudan $\mathbb{R}_{\ge0}^\infty$'da
   ifade etmek için bu biçimi seçer (`p.radius_eq_liminf`).

### Oturum 7

1. $f(0{,}1)=e^{-100}\approx3{,}7\times10^{-44}$. Float64 fark bölümü bunu sıfırdan
   ayırt edemez; "sıfır çıktı" demek hiçbir şey kanıtlamaz. `sympy.limit`
   cebirsel limit alır.
2. Çelişki yok. O teorem $f$'in merkez etrafında bir diskte **holomorf** olmasını
   ister. $e^{-1/z^2}$, $z=0$'da holomorf değildir, dolayısıyla teorem
   uygulanmaz. Buradaki "seri" holomorf bir fonksiyonun serisi değil,
   yalnızca reel türevlerden kurulmuş biçimsel bir seridir ve özdeş olarak 0'dır.
3. Kavramsal olarak hayır: ikisi de $C^\omega\subsetneq C^\infty$'nin tanığıdır.
   Ama biçimsel olarak Lean, betikteki **tam o fonksiyonu** kanıtlamıyor.
   `LEAN-DURUM.md` bunu açıkça yazar.

### Oturum 8

1. **Harmonik tahmine** göre: $(3{,}535702-2{,}006409)/2{,}006409=\%76{,}2$.
   Gerçek periyoda göre bağıl hata $(3{,}535702-2{,}006409)/3{,}535702=\%43{,}3$.
   Tablodaki "Taylor-2 hatası" sütunu ise **eliptik** değere göredir
   (150°'de %18,94).
2. $T(\theta_0)$ çift fonksiyondur ($\theta_0\to-\theta_0$ simetrisi), dolayısıyla
   seride yalnızca çift kuvvetler vardır. $\theta_0^2$ terimini eklemek hatayı
   $\theta_0^2$'den $\theta_0^4$'e, bir sonrakini eklemek $\theta_0^6$'ya indirir.
   Ölçülen: 4,00 ve 6,01.
3. **Hayır.** Sahnedeki potansiyelde $x_0\approx2{,}1918$, diğer kritik noktalar
   $-1{,}248$ (yerel minimum) ve $0{,}249$ (tepe, $V\approx3{,}077$). Genlik 1,3'te
   enerji $V(x_0+1{,}3)\approx9{,}49$, tepeden yüksek. Parçacık kuyudan çıkar,
   $u$ yaklaşık $-4{,}75$'e kadar gider. Grafik $\pm1{,}6$'da kırpıldığı için
   düz platolar görünür. Bu küçük bir anharmonik düzeltme değil, **bariyer
   aşımıdır**. Genlik 0,7'de ($E\approx2{,}46<3{,}08$) parçacık kuyuda kalır.
   Bkz. [[04-katman-manim]].
4. Sarkaç $\theta_0$'dan sıfır hızla bırakılır; ilk kez $\theta=0$'a vardığı an
   çeyrek periyottur. Olay (`events`) mekanizması bu anı adım içinde kök bularak
   bulur, ızgaradan daha hassastır.

### Oturum 9

1. Hayır. Hermite kesilmesi hem $\lambda$'nın tam sayı olmasını **hem** paritenin
   uyuşmasını ister ($\lambda=2$ çift). Tek seri
   $a_{n+2}\propto(n-2)a_n$ ile $n=1,3,5,\dots$ üzerinden ilerler ve $n-2$ hiç
   sıfır olmaz. `kesilme_derecesi(2, "hermite", 1)` → `None`.
2. Kesilmeyen seriler de hızla küçülen katsayılara sahip olabilir. $\lambda=2{,}5$
   için katsayılar $e^{x^2}$'ninkiler gibi azalır ve $n\approx28$'den sonra
   $10^{-14}$'ün altına iner, ama sıfır değildir; fonksiyon patlar. Karar
   rekürans **payının** cebirsel olarak sıfırlanmasından okunur.
3. Tek noktalı bir ölçüt: $|\psi(4)|<1$ ise "normalize edilebilir". Bu bir
   normalizasyon integrali değildir, bir göstergedir.
   Bkz. [[12-eksikler-ve-devam]].
4. `kesilme_derecesi` Hermite için $n=\lambda$ döndürür: rekürans payının
   $2(n-\lambda)$ sıfırlandığı indeks. $y''-2xy'+2\lambda y=0$ denklemi kuantum
   harmonik osilatörde $E=\hbar\omega(\lambda+\tfrac12)$'ye karşılık gelir.

### Oturum 10

1. $x$, $x_0$'dan küçük de olabilir. `uIoo x₀ x`, iki ucun sırasından bağımsız
   açık aralıktır. Betikteki `exp(x), x=-1.5` satırı tam bu durum.
2. `lake build` yalnızca "tip denetimi geçti" der; `sorry` ile kapatılmış bir
   ispat da derlenir (yalnızca uyarı verir). `#print axioms` ispatın dayandığı
   aksiyomları listeler. `sorryAx` görünmüyorsa açıkta ispat yoktur.
3. Sarkaç / harmonik osilatör (sonuç 5), Frobenius / kuantizasyon (sonuç 6) ve
   "R = en yakın tekilliğe uzaklık"ın kendisi (sonuç 3'ün geometrik yarısı).
   Ayrıca sonuç 7 için tanık $e^{-1/x^2}$ değil $e^{-1/x}$.
4. `1/(1-x)`, $a=0$ satırı: C-H 1,0000, hata %0,00.
