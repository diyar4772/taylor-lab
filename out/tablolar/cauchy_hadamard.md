# Yakınsaklık yarıçapının katsayılardan kestirimi

Katsayılar `n ≤ 60` için üretildi. `C-H` sütunu `1/R = limsup |a_n|^(1/n)` formülünün son 12 sıfırdan farklı terim üzerinden kestirimidir; `oran` sütunu `R ≈ |a_n/a_(n+d)|^(1/d)` testidir.

| fonksiyon      | a  | teorik R | C-H kestirimi | C-H hatası | oran testi | oran hatası |
|----------------|----|----------|---------------|------------|------------|-------------|
| exp(x)         | 0  | ∞        | 19.1121       | —          | 60.0000    | —           |
| sin(x)         | 0  | ∞        | 14.6525       | —          | 58.4979    | —           |
| ln(1+x)        | 0  | 1.0000   | 1.0706        | 7.06%      | 1.0169     | 1.69%       |
| 1/(1-x)        | 0  | 1.0000   | 1.0000        | 0.00%      | 1.0000     | 0.00%       |
| 1/(1+x^2)      | 0  | 1.0000   | 1.0000        | 0.00%      | 1.0000     | 0.00%       |
| arctan(x)      | 0  | 1.0000   | 1.0716        | 7.16%      | 1.0174     | 1.74%       |
| sqrt(1+x)      | 0  | 1.0000   | 1.1313        | 13.13%     | 1.0256     | 2.56%       |
| 1/(1+x^2), a=1 | 1  | 1.4142   | 1.3907        | 1.66%      | 1.0938     | 22.66%      |
| 1/(1-x), a=-1  | -1 | 2.0000   | 2.0232        | 1.16%      | 2.0000     | 0.00%       |

## Okunacaklar

**1. Sonlu R'de iki yöntem de iyi çalışır.** `1/(1-x)`, `1/(1+x²)` gibi kutuplu fonksiyonlarda katsayılar geometrik azaldığı için `|a_n|^(1/n)` hemen 1/R'ye oturur.

**2. `ln(1+x)` ve `sqrt(1+x)` yavaştır.** Katsayılar `1/n` gibi cebirsel bir çarpan taşır; `(1/n)^(1/n) → 1` yakınsaması logaritmik yavaşlıktadır. N=60'ta bile birkaç yüzdelik sapma kalır. Bu yöntemin kusuru değil, limsup'ın doğasıdır.

**3. `exp` ve `sin` için R = ∞ ve bunu sayısal olarak 'görmek' mümkün değildir.** `(1/n!)^(1/n) ≈ e/n` Stirling'den gelir; n=60'ta bu hâlâ ≈ 0.045, yani R ≈ 22. Sonsuzu sonlu veriden okuyamazsınız — yalnızca 'büyüyor' diyebilirsiniz. Tablodaki C-H sütununun `exp` satırında sonsuz yerine sonlu bir sayı çıkması **yöntemin dürüst sınırıdır**, hata değil.

**4. Seyreklik.**

1/(1+x²) serisinde tek dereceli katsayıların tamamı sıfırdır (1, 0, −1, 0, 1, …). Son 12 terimin 6 tanesi sıfır. Sıfırlar `|a_n|^(1/n)` dizisine katılırsa 0 değerleri maksimuma hiç katkı vermez ama diziyi delik deşik eder; **limsup yine de doğru çıkar** çünkü limsup zaten maksimuma bakar: bu örnekte her iki yol da R ≈ 1.0000 verir. Asıl bozulan ORAN TESTİdir: ardışık iki katsayıdan biri sıfır olduğunda |a_n/a_(n+1)| ya 0 ya tanımsızdır. Bu yüzden oran testi `taylor.py` içinde ardışık **sıfırdan farklı** terimler arasındaki derece farkı d ile |a_n/a_(n+d)|^(1/d) biçiminde uygulanır.

**5. Oran testi her zaman çalışmaz — `1/(1+x²)`, `a=1` satırına bakın.** Orada C-H %1.66 hatayla doğru cevabı verirken oran testi %22.66 sapar. Sebep şu: bu merkez için en yakın iki tekillik `i` ve `−i`, `a=1`'e **eşit uzaklıkta ama farklı yönlerdedir**. Katsayılar bu yüzden salınır ve `|a_n/a_(n+1)|` oranının bir LİMİTİ YOKTUR. Oran testi ancak limit varsa geçerlidir; Cauchy-Hadamard ise limsup kullandığı için limit olmasa da çalışır. Teoremin neden limit değil limsup ile kurulduğu tam olarak budur.

**6. İki bağımsız yol, aynı sayı.** Bu tablodaki R değerleri yalnızca katsayı dizisine bakılarak elde edildi — fonksiyonun kompleks düzlemdeki tekilliklerine hiç bakılmadan. `out/tablolar/kompleks_yaricap.md` ise aynı sayılara tekilliklerin geometrisinden ulaşır. Cauchy-Hadamard teoremi tam olarak bu iki yolun her zaman buluştuğunu söyler.
