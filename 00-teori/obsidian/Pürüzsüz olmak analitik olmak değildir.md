---
title: Pürüzsüz olmak analitik olmak değildir
tags: [taylor, analiz, karsi-ornek]
konu: Serinin yakınsaması, fonksiyona yakınsaması demek değil
kaynak: "[[../taylor-teori.tex|taylor-teori.tex]] §4"
olusturuldu: 2026-09-17
---

# Pürüzsüz olmak analitik olmak değildir

[[Yakınsaklık yarıçapı kompleks düzlemde belirlenir]] notundaki başarısızlık
biçimi anlaşılırdı: seri ıraksıyordu, yani bir cevap üretmiyordu. Buradaki
başarısızlık çok daha rahatsız edici, çünkü seri **ıraksamıyor**.

Tanık:

$$f(x) = \begin{cases} e^{-1/x^2}, & x \neq 0 \\ 0, & x = 0 \end{cases}$$

Bu fonksiyon $\mathbb{R}$ üzerinde $C^\infty$'dur — sonsuz kez
türevlenebilir, hiçbir noktada kırık yok. Ama **sıfırdaki bütün türevleri
sıfırdır.** Her biri. Sonsuz tanesi.

Sonuç: Maclaurin serisi özdeş olarak $0$'dır. Bu seri **her $x$ için
yakınsar** — yakınsaklık yarıçapı sonsuzdur. Sadece yanlış şeye yakınsar:
$x \neq 0$ için $f(x) > 0$ iken seri $0$ verir.

> Seri yakınsadı. Fonksiyona yakınsamadı.

Bu, $C^\omega \subsetneq C^\infty$ içermesinin gerçek olduğunun kanıtıdır:
analitiklik, pürüzsüzlükten **kesinlikle** daha güçlü bir şarttır.

## Neden bütün türevler ölüyor

Gerekçe tek bir yarıştır. $x \neq 0$ için türevler

$$f^{(n)}(x) = p_n\!\left(\tfrac1x\right) e^{-1/x^2}$$

biçimindedir — $p_n$ bir polinom. $x \to 0$ giderken $1/x$ patlar, yani
$p_n(1/x)$ da patlar. Ama $e^{-1/x^2}$ **daha hızlı** sıfırlanır. Üstel her
polinomu yener, her mertebede yener, hep yener. Bu yüzden her türev $0$'da
sıfırlanır.

Fonksiyon $0$ civarında o kadar düz yatıyor ki, türevler onun sıfırdan farklı
olduğunu **hiçbir mertebede fark edemiyor**. Taylor serisi ise fonksiyon
hakkında yalnızca türevleri bilir. Bilgi zaten kaynağında yok; seri elinden
geleni yapmış.

## Sayısal deney burada kanıt değildir

Önemli bir dürüstlük notu: `02-python/src/analitik_degil.py` ilk dokuz türevi
**sembolik limit** ile hesaplar, sayısal türevle değil. Sebep basit —
$f(0{,}1) = e^{-100} \approx 3{,}7 \times 10^{-44}$ zaten float64'ün
göremeyeceği kadar küçüktür. Sayısal olarak "sıfır çıktı" demek burada
hiçbir şey göstermez: ölçüm aletinin sıfır göstermesiyle miktarın sıfır
olması aynı şey değil. Hükmü cebir verir.

## Sebep yine kompleks düzlemdedir

Reel eksende $f$ uslu uslu sıfıra gidiyor. Hayali eksende bak:

$$z = iy \;\Longrightarrow\; -\frac{1}{z^2} = +\frac{1}{y^2}
\;\Longrightarrow\; e^{-1/z^2} = e^{1/y^2} \xrightarrow[y\to 0]{} \infty$$

Aynı $z = 0$ noktasına reel yönden yaklaşınca $0$, hayali yönden yaklaşınca
$\infty$ geliyor. Limit yok: $z = 0$ bir **esas tekilliktir**. Somut ölçü —
$|z| = 0{,}05$ için reel yönde $1{,}9\times10^{-174}$, hayali yönde
$5{,}2\times10^{+173}$.

Yani bu not bağımsız bir tuhaflık değil, önceki notun devamı. Orada kompleks
tekillik yarıçapı $1$'e düşürüyordu; burada tekillik merkezin *üstünde*
olduğu için yarıçap sıfıra iner ve seri hiçbir komşulukta işe yaramaz.

## Bağlantılar

- [[Yakınsaklık yarıçapı kompleks düzlemde belirlenir]]
- [[Taylor açılımı bir tanım değil zorunluluktur]] — polinom/seri ayrımı
  tam olarak bu yüzden önemliydi.
