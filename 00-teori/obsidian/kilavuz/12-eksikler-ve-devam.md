---
title: Eksikler ve devam
tags: [kilavuz, kilavuz/eksik]
created: 2026-09-17
status: tamam
lang: tr
---

# Eksikler ve devam

↑ [[00-BASLA-BURADAN]] · English: [[12-gaps-and-next-steps]]

Bu not iki şeyi kaydeder: kılavuz yazılırken **bulunan ve düzeltilen**
hataları, ve depoda hâlâ **yapılmamış** olanları. Kaynaklar: `LEAN-DURUM.md`,
`RAPOR.md` §2 ve §6, ve bu kılavuz için yapılan kontroller.

## A. Bulunan ve düzeltilen sonuç hataları

### A1. `1/(1+x²)`, `a=1` katsayıları kayan nokta hassasiyetini kaybediyordu

- **Nerede:** `taylor.py` → `katsayi_dizisi(expr, a, N)`, merkezi float
  (`1.0`) olarak `taylor_katsayilari`'na veriyordu.
- **Belirti:** Kapalı biçim $c_n=(-1)^n2^{-(n+1)/2}\sin\frac{(n+1)\pi}4$'e göre
  $n\equiv3\pmod4$ katsayıları tam sıfır olmalı. Float hesapta bu sıfırlar
  $n=19$'dan sonra kayboluyordu. Bağıl hata $n=40$'ta $1{,}1\times10^{-5}$ idi;
  $n=60$'ta katsayı **işaret dahil** yanlıştı ($+2{,}55\times10^{-9}$, doğrusu
  $-4{,}66\times10^{-10}$).
- **Etkisi:** `cauchy_hadamard.md`'nin `1/(1+x^2), a=1` satırı oran testi için
  %22,66, C-H için %1,66 gösteriyordu. README §4, `taylor-teori.tex` §3 ve
  [[Yakınsaklık yarıçapı kompleks düzlemde belirlenir]] notu bu sayıyı
  "limit yok" dersinin kanıtı olarak kullanıyordu.
- **Düzeltme:** `katsayi_dizisi` artık `sp.Rational(a)` kullanıyor. Tablo
  yeniden üretildi: oran testi 1,4142 (%0,00), C-H 1,4228 (%0,61).
  `yakinsaklik_orani.py`'a $N=52..60$ için oran testinin
  $\sqrt2\to1\to2\to2\to\sqrt2$ salınımını gösteren yeni bir tablo eklendi.
  README, teori metni ve atomik not bu salınımı anlatacak biçimde güncellendi.
- **Etkilenmeyen:** `kompleks_harita.py` ($N=28$) yeniden çalıştırıldı;
  tablo bayt bayt aynı çıktı.

### A2. "En kötü oran" sütunu 1'i geçiyordu ve bu açıklanmıyordu

`kalan_dogrulama.md` "1'i asla geçmemeli" diyordu; oysa 8 satırın 6'sında
geçiyor (en büyüğü `ln(1+x)` 2,3593). Sütun float64'tür ve "anlamlı rejim"
filtresi yaklaşıktır; aynı noktanın mpmath oranı 0,989'dur.
**Düzeltme:** betiğin ve tablonun açıklama metni ile README §1 bunu
açıkça anlatıyor. Ayrıntı:
[[10-yedi-sonuc#1. Lagrange sınırı hiç ihlal edilmedi]]. Octave demosundaki
benzer değerler (`cos` 1,0128, `ln(1+x)` 1,0654) orada hâlâ yüksek
hassasiyetle teyit edilmiyor (bkz. D3).

### A3. Video 6 bariyer aşımını "anharmonisite" diye gösteriyordu

Genlik 1,3'te enerji ($\approx9{,}49$) tepeyi ($\approx3{,}08$) aşıyor,
parçacık kuyudan çıkıyordu. Eşik genlik $\approx0{,}784$.
**Düzeltme:** `genlikler = [0.25, 0.5, 0.7]`; video 1080p60 olarak yeniden
üretildi. Ayrıntı: [[04-katman-manim]].

### A4. Frobenius'ta "normalize edilebilir" kararı tek noktalıydı

Eski ölçüt yalnızca $x=4$'te `abs(psi) < 1.0` idi.
**Düzeltme:** `hermite_incelemesi()` artık $\int\psi^2dx$'i $[-4,4]$ ve
$[-6,6]$ üzerinde hesaplıyor; oran $<1{,}01$ ise normalize edilebilir.
Tabloya **∫ψ² oranı (L=6 / L=4)** sütunu eklendi: tam sayı $\lambda$'da
$1{,}000000$–$1{,}000085$, $\lambda=2{,}5$ ve $3{,}7$'de $9{,}5\times10^6$ ve
$1{,}0\times10^6$.

### A5. Markdown tablolarında `|` işareti

`analitik_degil.md`'deki `|z|` başlığı ve yeni Frobenius başlığındaki
`|ψ|` tablo sütunlarını bölüyordu. **Düzeltme:** başlıklar `mutlak z` ve
`∫ψ²` oldu.

### A6. Açık kalan: Python'daki Lagrange sınırı ızgarada örnekleniyor

`lagrange_sinir()` sup'u 20 001 noktalık ızgarada alır;
`lagrange_sinir_yavas` docstring'i "alt kestirim riski"ni kabul eder. Risk
tetiklenmedi (teyitli ihlal 0), ama sınır tam değil. Octave katmanı sup'u
kapalı biçimden **tam** alır. **Düzeltilmedi.**

## B. Düzeltilen eski ya da yanlış atıflar

| Dosya | Sorun | Şimdi |
|---|---|---|
| `02-python/src/taylor.py` | var olmayan `01-taylor-kavramsal-temel.md`'ye atıf | [[Taylor açılımı bir tanım değil zorunluluktur]] |
| `05-godot/project.godot` | `testler/test_kendini.gd`; sabitler "`s06_denge.py` ile birebir aynı" | `test_dogrulama.gd`, `sarkac.py` |
| `05-godot/taylor_explorer.gd` | düzeltme öncesi `-Im(...)` yorumu | `(-1)^n * Im(...)` |
| `05-godot/denge_oyunu.gd` | "5°'de dakikalar sürer" ($\lvert\Delta\theta\rvert\le2\theta_0=10°$ olduğu için eşik 5°'de hiç aşılmaz) | düzeltildi |
| `Makefile` | var olmayan `./yap.ps1` | Windows notu kılavuza yönlendiriyor |
| `00-teori/taylor-teori.tex` | "(iki kez)"; §2'de yalnız 2232 | "(üç kez)"; "2224–2232" |
| `README.md`, `RAPOR.md` | `requirements.txt`'i (manim dahil) Python 3.14 ortamına kuruyordu | manim ayıklanıyor, `.venv313` ayrı |
| `dogrula.sh` | Windows'ta `.venv\Scripts\python.exe`'yi ve Octave'ı bulamıyordu | ikisini de arıyor |

## C. Platform eksikleri (açık)

- **MATLAB hiç çalıştırılmadı.** Fedora 44'te açılışta çöktü (LXE builtin
  registry hatası), Windows'ta kurulu değildi. `.m` dosyaları yalnızca
  Octave'da (10.3.0 ve 11.3.0) doğrulandı.
- **Windows'ta LaTeX adımı `dogrula.sh`'ta atlanıyor** (`make` yok) ve
  MiKTeX'te derleme 1 babel uyarısı verdiği için `teori_dogrula`'nın
  "0 uyarı" şartını zaten geçemez. LaTeX'i Windows'ta elle doğrula
  ([[01-ortam-kurulumu#LaTeX]]).
- **Web yalnızca Chrome'da** denendi.
- **Sürekli entegrasyon (CI) yok.**

## Lean'de kapsam dışı kalan dört konu

`LEAN-DURUM.md` → "Kapsanmayanlar (bilerek)":

1. **"R = en yakın tekilliğe uzaklık"** biçimsel olarak ifade edilmedi.
   `1/(1+z²)` için $R=1$ gibi somut bir örnek bile, kutupların analitik devam
   teorisini gerektiriyor.
2. **Sarkaç / harmonik osilatör** yok. `taylor_isLittleO` Mathlib'de var
   (imzası [[07-katman-lean]]'de), kullanılmadı.
3. **Frobenius / kuantizasyon** yok.
4. **$e^{-1/x^2}$'nin kendisi** için tanık kurulmadı. Mathlib'in tanığı
   `expNegInvGlue` yani $e^{-1/x}$ ($x>0$).

Sonuç olarak yedi sonucun ikisi (5, 6) Lean'de hiç yok; biri (3) yalnızca
"disk içinde mutlak yakınsar" yarısıyla var.

## D. Genişletilebilecek yönler (kendin dene)

1. **Oran testi salınımının grafiği.** `yakinsaklik_orani.py`'daki salınım
   tablosunu $N=20..60$ için bir grafiğe çevir.
2. **Sarkaç serisinin yarıçapı.** $T(\theta_0)/T_0=\frac2\pi K(\sin^2\frac{\theta_0}2)$.
   $K(m)$, $m\in[1,\infty)$ dışında analitik; $\sin^2(\theta_0/2)\ge1$ olan en
   yakın kompleks $\theta_0$ ise $\pm\pi$. Beklenti: $\theta_0$ cinsinden
   serinin yarıçapı $\pi$ (tepede duran sarkaç, $T\to\infty$). **Depoda
   ölçülmedi.** Kılavuz yazılırken yapılan mpmath ön denemesinde 60 terimde
   oran testi 3,195 çıktı ve azalıyordu; bu $\pi$ ile tutarlı ama kanıt değil.
   Sonuç 3 ile 5'i birbirine bağlar.
3. **Octave'a yüksek hassasiyetli teyit.** Octave `symbolic` paketi ile
   (`vpa`) float64 adaylarını yeniden ölç.
4. **Lean madde 2.** $V'(x_0)=0$ ⇒ $V(x)-V(x_0)-\frac12V''(x_0)(x-x_0)^2=o((x-x_0)^2)$.
5. **Ayrı bir `dogrula.ps1`**, LaTeX'i de Windows'ta çalıştıran.
6. **Padé yaklaşımı.** Taylor'un yarıçap duvarını aşmanın klasik yolu.
   `ln(1+x)` ya da `arctan(x)` için $x>1$'de Padé ile Taylor'u karşılaştır
   (`1/(1+x²)` rasyonel olduğu için [2/2] Padé onu tam verir).
7. **A6'yı kapat.** Python'daki sup'u da kapalı biçimden al.
8. **Firefox testi** ve **GitHub Actions** (`taylor.py`, `node` testi ve Godot
   headless testi dakikalar içinde koşar; Lean için Mathlib önbelleği gerekir).

## E. Bu kılavuzun kendi sınırları

- Linux komutlarının bir kısmı (ör. `grep -v '^manim'` ile kurulum)
  Fedora'da **denenmedi**; yanlarında belirtildi.
- Düzeltmeler Windows'ta yapıldı ve orada doğrulandı: `taylor.py`,
  yeniden üretilen üç tablo, Godot testi, Octave demosu, `pdflatex` ×3,
  video 6'nın 1080p60 render'ı. `kalan_dogrulama.py` yeniden
  **çalıştırılmadı** (Windows'ta aday sayısı 2232 çıkar); tablosunda yalnızca
  açıklama metni değişti.
- Ekran görüntüleri ve video kareleri bir Windows makinesinde üretildi.
- Oturum sürelerindeki dakikalar tahmindir.
