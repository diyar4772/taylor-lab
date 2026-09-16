# Pürüzsüz ama analitik değil: e^(−1/x²)

## Türevler

`f^(n)(0)` değerleri **sembolik limit** ile hesaplandı (`sympy.limit`). Sayısal türev burada kanıt olarak kabul edilemez: `f(0.1) = e^(-100) ≈ 3.7e-44` zaten float64'ün fark edemeyeceği kadar küçüktür, "sıfır çıktı" demek hiçbir şey göstermez.

| n | f⁽ⁿ⁾(0)  (limit) | aynı türevin x=0.1'deki değeri |
|---|------------------|--------------------------------|
| 0 | 0                | 3.720e-44                      |
| 1 | 0                | 7.440e-41                      |
| 2 | 0                | 1.466e-37                      |
| 3 | 0                | 2.843e-34                      |
| 4 | 0                | 5.428e-31                      |
| 5 | 0                | 1.019e-27                      |
| 6 | 0                | 1.883e-24                      |
| 7 | 0                | 3.417e-21                      |
| 8 | 0                | 6.092e-18                      |

Sağ sütun işin püf noktasını gösterir: türevler x=0.1'de devasa sayılara ulaşır (n büyüdükçe `1/x^(3n)` mertebesinde çarpanlar doğar), ama `e^(-1/x²)` çarpanı bunların hepsini ezer. Üstel sıfıra gidiş, her polinom patlamasından güçlüdür.

## Sonuç

Bütün türevler sıfır olduğu için Maclaurin serisi

```
0 + 0·x + 0·x² + 0·x³ + … = 0
```

olur. Bu seri **her x için yakınsar** — yakınsaklık yarıçapı sonsuzdur. Yakınsadığı şey sıfır fonksiyonudur. Oysa `f(x) ≠ 0` her `x ≠ 0` için. Yani:

> Bir Taylor serisinin yakınsaması, onu üreten fonksiyona yakınsaması anlamına gelmez.

Bu, `C^ω ⊊ C^∞` içermesinin somut tanığıdır: f sonsuz kez türevlenebilir (C^∞) ama hiçbir 0 komşuluğunda kendi Taylor serisiyle temsil edilemez (C^ω değil).

## Sebep kompleks düzlemdedir

Reel eksende f uslu uslu sıfıra gider; hiçbir şey olmuyor gibidir. Ama `z = iy` alırsak `-1/z² = +1/y²` olur ve `e^(1/y²) → ∞`. Aynı `z=0` noktasına iki yönden yaklaşıp biri 0, diğeri sonsuz veriyorsa orada limit yoktur — `z=0` bir **esas tekilliktir**.

| |z|  | reel eksen boyunca: e^(−1/x²) | hayali eksen boyunca: e^(+1/y²) |
|------|-------------------------------|---------------------------------|
| 0.5  | 1.832e-02                     | 5.460e+01                       |
| 0.3  | 1.495e-05                     | 6.691e+04                       |
| 0.2  | 1.389e-11                     | 7.200e+10                       |
| 0.1  | 3.720e-44                     | 2.688e+43                       |
| 0.05 | 1.915e-174                    | 5.221e+173                      |

Bu, `kompleks_yaricap.md` dosyasındaki dersin en uç hâlidir: reel eksende hiçbir kusuru olmayan bir fonksiyonun Taylor davranışını belirleyen şey, kompleks düzlemde olup bitenlerdir. `1/(1+x²)`'de bu bir kutuptu ve yarıçapı 1'e düşürüyordu; burada esas tekilliktir ve seriyi tamamen işe yaramaz kılar.
