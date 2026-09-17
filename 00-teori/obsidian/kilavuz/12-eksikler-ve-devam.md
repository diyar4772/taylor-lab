---
title: Eksikler ve devam
tags: [kilavuz, kilavuz/eksik]
created: 2026-09-17
status: tamam
lang: tr
---

# Eksikler ve devam

↑ [[00-BASLA-BURADAN]] · English: [[12-gaps-and-next-steps]]

Bu not depoda **yapılmamış** ya da **hatalı** olanları toplar. Kaynaklar:
`LEAN-DURUM.md`, `RAPOR.md` §2 ve §6, ve bu kılavuz yazılırken yapılan
kontroller. Kontrollerde depo dosyalarına dokunulmadı. Denemeler geçici
dosyalarda yapıldı ve komutları ilgili notlarda verildi.

## A. Sonuçları etkileyen bulgular

### A1. `1/(1+x²)`, `a=1` katsayıları kayan nokta hassasiyetini kaybediyor

- **Nerede:** `taylor.py` → `katsayi_dizisi(expr, a, N)` →
  `taylor_katsayilari(expr, a, N)`; `a` float (`1.0`) olarak veriliyor.
- **Belirti:** Kapalı biçim $c_n=(-1)^n2^{-(n+1)/2}\sin\frac{(n+1)\pi}4$'e göre
  $n\equiv3\pmod4$ katsayıları tam sıfır olmalı. Float hesapta $n=19$'dan sonra
  bu sıfırlar kayboluyor. Bağıl hata $n=28$'de $1{,}5\times10^{-9}$,
  $n=40$'ta $1{,}1\times10^{-5}$; $n=60$'ta katsayı **işaret dahil** yanlış
  ($+2{,}55\times10^{-9}$, doğrusu $-4{,}66\times10^{-10}$).
- **Etkisi:** `cauchy_hadamard.md`'deki `1/(1+x^2), a=1` satırı. Tam
  katsayılarla oran testi 1,4142 (%0,00), C-H 1,4228 (%0,61); tabloda
  1,0938 (%22,66) ve 1,3907 (%1,66). README §4, `taylor-teori.tex` §3 ve
  [[Yakınsaklık yarıçapı kompleks düzlemde belirlenir]] notu %22,66'yı
  "limit yok" dersinin kanıtı olarak kullanıyor. Ders doğru, sayı kirli.
  Doğru kanıt: oran testinin $N$ ile $1{,}41\to1\to2\to2\to1{,}41$ diye
  salınması ([[10-yedi-sonuc#4. Aynı yarıçap, yalnızca katsayılardan]]).
- **Etkilemediği:** `kompleks_harita.py` $N=28$ kullanıyor; oradaki bağıl hata
  ~$10^{-9}$, harita sonucunu değiştirmez. $a=0$ ve $a=-1$ satırları da temiz.
- **Önerilen düzeltme:** `katsayi_dizisi` içinde
  `taylor_katsayilari(expr, sp.Rational(a), N)` kullanmak (`_mpmath_katsayilari`
  zaten böyle yapıyor), ardından tabloyu ve metinleri yeniden üretmek.

### A2. "En kötü oran" sütunu 1'i geçiyor ve bu açıklanmıyor

`kalan_dogrulama.md` tablosu "teoremin doğru olması için 1'i asla
geçmemeli" der; oysa 8 satırın 6'sında geçer (en büyüğü `ln(1+x)` 2,3593).
Sütun float64'tür ve "anlamlı rejim" filtresi yaklaşık bir filtredir. İhlal
yoktur (mpmath oranı 0,989), ama README bu tabloyu açıklamasız veriyor.
Ayrıntı: [[10-yedi-sonuc#1. Lagrange sınırı hiç ihlal edilmedi]]. Aynı durum
Octave demosunda da var (`cos` 1,0128, `ln(1+x)` 1,0654) ve orada yüksek
hassasiyetli teyit **yok**.

### A3. Video 6'nın son bölümü bariyer aşımını "anharmonisite" diye sunuyor

Genlik 1,3'te enerji ($\approx9{,}49$) tepeyi ($\approx3{,}08$) aşıyor, parçacık
kuyudan çıkıyor; grafik $\pm1{,}6$'da kırpıldığı için bu düz platolar olarak
görünüyor. Eşik genlik $\approx0{,}784$. Ayrıntı: [[04-katman-manim]].

### A4. Frobenius'ta "normalize edilebilir" kararı tek noktalı

`hermite_incelemesi()` `abs(psi) < 1.0` ölçütünü $x=4$'te uygular. Bu bir
normalizasyon integrali değildir. Sonuç doğru yöndedir, ama ölçüt bir
göstergedir. İyileştirme: $\int_{-L}^{L}\lvert\psi\rvert^2dx$'in $L$ ile
davranışı.

### A5. Python'daki Lagrange sınırı ızgarada örnekleniyor

`lagrange_sinir()` sup'u 20 001 noktalık ızgarada alır; `lagrange_sinir_yavas`
docstring'i "alt kestirim riski"ni kabul eder. Bu risk kalan_dogrulama'da
tetiklenmedi (teyitli ihlal 0), ama sınır tam değil. Octave katmanı sup'u
kapalı biçimden **tam** alır.

## B. Eski ya da yanlış atıflar

| Dosya | Sorun |
|---|---|
| `02-python/src/taylor.py` (modül docstring'i) | `00-teori/obsidian/01-taylor-kavramsal-temel.md`'ye atıf yapıyor; böyle bir dosya yok. Karşılığı [[Taylor açılımı bir tanım değil zorunluluktur]]. |
| `05-godot/project.godot` (yorum) | `testler/test_kendini.gd` diyor; dosya `test_dogrulama.gd`. "sabitler `s06_denge.py` ile birebir aynı" diyor; denge oyunu sarkaç kullanıyor, `s06`'nın polinom potansiyelini değil. |
| `05-godot/taylor_explorer.gd` | `1/(1+x^2)` bloğunun ilk yorumu düzeltilmeden önceki `-Im(...)` formülünü anıyor. |
| `05-godot/denge_oyunu.gd` (docstring) | "5°'de dakikalar sürer" diyor; oysa $\lvert\Delta\theta\rvert\le2\theta_0=10°$ olduğu için 10°'lik eşik 5°'de **hiç** aşılamaz. |
| `Makefile` (yorum) | `./yap.ps1` diye bir PowerShell muadilinden söz ediyor; dosya yok. |
| `00-teori/taylor-teori.tex` | 2. satırda "(iki kez)" yazıyor, doğrusu üç geçiş. §2'de 2232 aday (Windows sayısı), README'de 2224 (Fedora). |
| `README.md` (kurulum) | `.venv/bin/pip install -r requirements.txt` Python 3.14'te büyük olasılıkla `manim` → `av` yüzünden düşer ([[01-ortam-kurulumu#Tuzaklar]]). |

## C. Platform eksikleri

- **MATLAB hiç çalıştırılmadı.** Fedora 44'te açılışta çöktü (LXE builtin
  registry hatası), Windows'ta kurulu değildi. `.m` dosyaları yalnızca
  Octave'da (10.3.0 ve 11.3.0) doğrulandı; MATLAB uyumluluğu yalnızca
  statik denetim.
- **Windows'ta tek komutluk doğrulama yok.** `make` yok. `dogrula.sh` Git
  Bash'te çalışır ama `.venv/bin/python` ve PATH'teki `octave-cli`'yi
  aradığı için 5 katmanı atlar. Bir `dogrula.ps1` eksik.
- **Web yalnızca Chrome'da** denendi.
- **Sürekli entegrasyon (CI) yok.** Doğrulamalar elle çalıştırılıyor.
- **Windows'ta LaTeX 1 uyarı** veriyor (MiKTeX babel "Configuration files
  are deprecated"); Fedora'da 0.

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

1. **A1'i düzelt.** Tek satırlık değişiklik + `yakinsaklik_orani.py`'ı yeniden
   çalıştır + README/tex/not metnini güncelle. Oran testinin $N$'e göre
   salınımını gösteren küçük bir grafik ekle.
2. **Sarkaç serisinin yarıçapı.** $T(\theta_0)/T_0=\frac2\pi K(\sin^2\frac{\theta_0}2)$.
   $K(m)$, $m\in[1,\infty)$ dışında analitik; $\sin^2(\theta_0/2)\ge1$ olan en
   yakın kompleks $\theta_0$ ise $\pm\pi$. Beklenti: $\theta_0$ cinsinden
   serinin yarıçapı $\pi$ (tepede duran sarkaç, $T\to\infty$). **Depoda
   ölçülmedi.** Kılavuz yazılırken yapılan mpmath ön denemesinde 60 terimde
   oran testi 3,195 çıktı ve azalıyordu; bu $\pi$ ile tutarlı ama kanıt değil.
   `yakinsaklik_orani.py`'a bir satır olarak eklenebilir. Bu, sonuç 3 ile 5'i
   birbirine bağlar.
3. **Octave'a yüksek hassasiyetli teyit.** Octave `symbolic` paketi ile
   (`vpa`) float64 adaylarını yeniden ölç.
4. **Lean madde 2.** $V'(x_0)=0$ ⇒ $V(x)-V(x_0)-\frac12V''(x_0)(x-x_0)^2=o((x-x_0)^2)$.
5. **`dogrula.ps1`.** `dogrula.sh`'ın PowerShell karşılığı: `.venv\Scripts\python.exe`,
   Octave tam yolu, `pdflatex -enable-installer`.
6. **Padé yaklaşımı.** Taylor'un yarıçap duvarını aşmanın klasik yolu. Web
   panel 1'e `1/(1+x²)` için [2/2] Padé eğrisi eklemek, "duvar polinomun,
   fonksiyonun değil" fikrini gösterir. Rasyonel bir fonksiyon olduğu için
   [2/2] Padé onu **tam** verir; daha öğretici bir deney `ln(1+x)` ya da
   `arctan(x)` için $x>1$'de Padé ile Taylor'u karşılaştırmaktır.
7. **Normalizasyon integrali** (A4) ve **Firefox testi** (C).
8. **GitHub Actions.** `taylor.py`, `node` testi ve Godot headless testi
   dakikalar içinde koşar; Lean için Mathlib önbelleği gerekir.

## E. Bu kılavuzun kendi sınırları

- Linux komutlarının bir kısmı (ör. `grep -v '^manim'` ile kurulum)
  Fedora'da **denenmedi**; yanlarında belirtildi.
- Ekran görüntüleri ve video kareleri bir Windows makinesinde üretildi;
  yazı tipleri farklı sistemlerde değişebilir.
- Oturum sürelerindeki dakikalar tahmindir.
