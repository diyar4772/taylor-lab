---
title: Yakınsaklık yarıçapı kompleks düzlemde belirlenir
tags: [taylor, kompleks-analiz, yakinsaklik]
konu: Reel eksende hiçbir sebep yokken serinin neden durduğu
kaynak: "[[../taylor-teori.tex|taylor-teori.tex]] §3"
olusturuldu: 2026-09-17
---

# Yakınsaklık yarıçapı kompleks düzlemde belirlenir

Şu fonksiyona reel eksende bakarak bir kusur bulmaya çalış:

$$f(x) = \frac{1}{1+x^2}$$

Her yerde tanımlı. Sınırlı — değerleri $0$ ile $1$ arasında. Sonsuz kez
türevlenebilir. Hiçbir yerde sivri ucu, sıçraması, patlaması yok. Grafiği
sakin bir tepe.

Buna rağmen Maclaurin serisi $1 - x^2 + x^4 - \cdots$ yalnızca $|x| < 1$ için
yakınsar. $x = 1{,}1$'de ıraksar.

**Reel eksende bu sınırı haklı çıkaracak hiçbir şey yoktur.** Baktığın yerde
cevap yok — çünkü sebep bir boyut yukarıda.

## Sebep

$1 + z^2 = (z-i)(z+i)$. Yani fonksiyonun $z = \pm i$ noktalarında kutupları
var ve bu noktalar orijine tam olarak $1$ uzaklıkta. Kuvvet serisi kompleks
düzlemde **daima bir disk üzerinde** yakınsar, ve o disk ilk engele çarptığı
yerde durur. Reel eksen o diskin sadece bir çapıdır; sen çapa bakıp diskin
neden o büyüklükte olduğunu anlayamazsın.

Kural tek cümle: **$R$, merkezin en yakın tekilliğe uzaklığıdır.**

## Bunun en sevdiğim sonucu

Yarıçap fonksiyonun özelliği değil, **(fonksiyon, merkez) çiftinin**
özelliğidir. Aynı $f$ için merkezi kaydırdığında yarıçap değişir, çünkü
tekillikler yerinde durur ama onlara olan uzaklığın değişir:

| merkez $a$ | $R = \lvert a \mp i\rvert$ |
|---|---|
| $0$ | $1$ |
| $1$ | $\sqrt{2} \approx 1{,}414$ |
| $2$ | $\sqrt{5} \approx 2{,}236$ |

"Bu fonksiyonun yakınsaklık yarıçapı kaçtır?" sorusu, merkez söylenmeden
eksik bir sorudur.

## Neden $\limsup$, neden limit değil

Cauchy–Hadamard teoremi $1/R = \limsup |a_n|^{1/n}$ der. Oradaki $\limsup$
titizlik gösterisi değil, zorunluluk. Somut tanığı şu: $f = 1/(1+x^2)$ ve
$a = 1$ alındığında $i$ ile $-i$ merkeze **eşit uzaklıkta ama farklı
yönlerdedir**. Katsayılar bu yüzden salınır ve $|a_n / a_{n+1}|$ oranının
limiti **yoktur**: $N = 52, \dots, 60$ için oran testi sırasıyla
$\sqrt2, 1, 2, 2, \sqrt2, 1, 2, 2, \sqrt2$ verir, yani cevabı nerede
durduğuna bağlıdır. $\limsup$ ile kurulan Cauchy–Hadamard ise aynı aralıkta
yaklaşık %0,6 sapmayla yerinde durur.

> Düzeltme: bu not önceden "oran testi %22,66 sapar, C–H %1,66" diyordu. O
> sayılar katsayıların kayan noktalı merkezle üretilmesinden doğan
> hassasiyet kaybıyla bozulmuştu; `katsayi_dizisi` artık tam aritmetik
> kullanıyor.

İki tekillik merkeze eşit uzaklıkta olur olmaz oran testi çöker; $\limsup$
çökmemek için oradadır.

## Bunu iddia değil gözlem olarak görmek

`02-python/src/kompleks_harita.py` kompleks düzlemde $\frac1N\log_{10}|f-P_N|$
büyüklüğünü çizer. Bu niceliğin *işareti* doğrudan yakınsaklığı söyler, sıfır
düzeyi de tam olarak $|z-a| = R$ çemberidir. Sonuç: **disk kimse çizmeden,
sadece hata verisinden ortaya çıkar.**

Dürüst pay: haritadan okunan yarıçaplar teorik değerin sistematik olarak
%5–8 altında kalır. Bu bir hata değil — yakınsama ancak $N \to \infty$'da tam
olur. Aynı sebeple $\ln(1+z)$'nin sınır eğrisi sonlu $N$'de gözle görülür
biçimde çember *değildir*: katsayıları $1/n$ gibi cebirsel azalır, kutuplu
fonksiyonlardaki geometrik azalmanın aksine, ve sınır daha yavaş sıkışır.

## Bağlantılar

- [[Taylor açılımı bir tanım değil zorunluluktur]]
- [[Pürüzsüz olmak analitik olmak değildir]] — aynı dersin en uç hâli:
  orada kompleks tekillik yarıçapı $1$'e düşürür, burada seriyi tümden
  işe yaramaz kılar.
