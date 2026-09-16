# Lagrange kalan sınırı doğrulaması

Her satır, o fonksiyon için N=1..12 ve 1501 nokta üzerinde yapılan tüm testlerin özetidir.
`en kötü oran` = max(gerçek hata / Lagrange sınırı); teoremin doğru olması için **1'i asla geçmemeli**.

`yuvarlama rejimi` sütunu, Lagrange sınırının float64'ün ölçebileceğinin altına düştüğü nokta sayısıdır. Oralarda ölçüm anlamsızdır ve ayrıca mpmath ile test edilirler (aşağıdaki ikinci tablo).

| fonksiyon      | a      | aralık      | taranan nokta | float64 aday ihlal | en kötü oran | nerede | yuvarlama rejimi |
|----------------|--------|-------------|---------------|--------------------|--------------|--------|------------------|
| sin(x)         | 0      | [-4, 4]     | 18 012        | 187                | 1.0506       | N=8    | 502              |
| cos(x)         | 0      | [-4, 4]     | 18 012        | 261                | 1.0178       | N=7    | 580              |
| exp(x)         | 0      | [-3, 3]     | 18 012        | 360                | 1.0107       | N=4    | 717              |
| ln(1+x)        | 0      | [-0.85, 2]  | 18 012        | 177                | 2.3593       | N=7    | 272              |
| 1/(1-x)        | 0      | [-0.9, 0.9] | 18 012        | 249                | 0.9988       | N=3    | 474              |
| sqrt(1+x)      | 0      | [-0.7, 2]   | 18 012        | 242                | 1.0550       | N=5    | 484              |
| sin(x), a=pi/4 | 0.7854 | [-3, 3]     | 18 012        | 377                | 1.0121       | N=7    | 715              |
| exp(x), a=1    | 1      | [-2, 4]     | 18 012        | 371                | 1.0147       | N=4    | 717              |

**Toplam: 144 096 nokta tarandı  2224 aday ihlal (4461 nokta yuvarlama rejiminde). mpmath ile TEYİT EDİLEN ihlal: 0.**

Oranın 1'e yaklaştığı yerler, sınırın *keskin* olduğu yerlerdir: orada eşitliği sağlayan ksi, türevin supremumunu aldığı noktaya denk düşer. Oranın küçük kaldığı yerlerde ise sınır gevşektir — ama hiçbir zaman yanlış değildir.

## float64'ün tabanı: sahte ihlaller

Aşağıdaki noktalar float64 ile bakıldığında sınırı katbekat aşıyor görünür. Örneğin `exp`, `a=1`, `N=12`, `x=0.996` için gerçek hata `2.93e-41`, ama çift duyarlıklı aritmetiğin `exp(0.996)≈2.7` civarında ölçebildiği en küçük fark `eps·|f| ≈ 6e-16`. Ölçülen "hata" tamamen yuvarlama gürültüsüdür.

Aynı noktalar mpmath ile 60 basamakta yeniden ölçüldüğünde oran 1'in altına döner — yani aşılan şey teorem değil, **ölçüm aletiydi**.

| fonksiyon | N  | x       | float64 hata | mpmath hata | mpmath sınır | float64 oran | mpmath oran |
|-----------|----|---------|--------------|-------------|--------------|--------------|-------------|
| 1/(1-x)   | 1  | 0.0000  | 2.220e-16    | 1.233e-32   | 1.233e-32    | 1.801e+16    | 1.000000    |
| 1/(1-x)   | 2  | 0.0000  | 2.220e-16    | 1.368e-48   | 1.368e-48    | 1.623e+32    | 1.000000    |
| cos(x)    | 11 | -0.0107 | 1.110e-16    | 4.529e-33   | 4.529e-33    | 2.451e+16    | 0.999999    |
| cos(x)    | 11 | 0.0107  | 1.110e-16    | 4.529e-33   | 4.529e-33    | 2.451e+16    | 0.999999    |
| cos(x)    | 9  | 0.0107  | 1.110e-16    | 5.254e-27   | 5.254e-27    | 2.113e+10    | 0.999999    |
| cos(x)    | 9  | -0.0107 | 1.110e-16    | 5.254e-27   | 5.254e-27    | 2.113e+10    | 0.999999    |
| sin(x)    | 12 | -0.0160 | 3.469e-18    | 7.232e-34   | 7.232e-34    | 4.797e+15    | 0.999999    |
| sin(x)    | 12 | 0.0160  | 3.469e-18    | 7.232e-34   | 7.232e-34    | 4.797e+15    | 0.999999    |
| cos(x)    | 7  | -0.0107 | 1.110e-16    | 4.156e-21   | 4.156e-21    | 2.671e+04    | 0.999999    |
| cos(x)    | 7  | 0.0107  | 1.110e-16    | 4.156e-21   | 4.156e-21    | 2.671e+04    | 0.999999    |

**2224 adayın tamamı teyit edildi; mpmath ile ihlal sayısı: 0.**
