# Frobenius serileri ve kuantizasyonun doğuşu

## Legendre denklemi

```
(1−x²)y'' − 2xy' + λy = 0      a_{n+2} = [n(n+1) − λ] / [(n+1)(n+2)] · a_n
```

Denklem λ üzerinde **hiçbir kısıt koymaz**: her λ için rekürans çalışır ve bir seri çözüm üretir. Kısıt, çözümün `x = ±1`'de (yani kutuplarda, çünkü `x = cos θ`) sonlu kalması gerektiğinden gelir.

| λ                         | seri kesiliyor mu? | y(0.999) | y(1)    | kısmi toplam büyümesi |
|---------------------------|--------------------|----------|---------|-----------------------|
| λ = 0·1 = 0               | evet, derece 0     | 1.0000   | 1.0000  | 0.000e+00             |
| λ = 2·3 = 6               | evet, derece 2     | -1.9940  | -2.0000 | 0.000e+00             |
| λ = 4·5 = 20              | evet, derece 4     | 2.6401   | 2.6667  | 0.000e+00             |
| λ = 5.5  (tam sayı değil) | HAYIR              | -2.3244  | -2.3674 | 2.881e-02             |
| λ = 7.3  (tam sayı değil) | HAYIR              | -0.9980  | -0.9085 | 7.329e-02             |

Büyük n için `a_{n+2}/a_n → 1` olur; yani katsayılar sonunda sabit orana yaklaşır ve `x = 1`'de seri ıraksar.

**Dürüst bir uyarı:** bu ıraksama hızlı değildir. Harmonik seri gibi *logaritmiktir*, bu yüzden 400 terimde bile `y(1)` sonlu bir sayı gibi görünür — tabloda λ=5.5 için −2.37 yazıyor. Iraksamanın kanıtı o sütun değil, **`son çeyrekte artış`** sütunudur: kesilen serilerde tam olarak `0.00e+00`, kesilmeyenlerde sıfırdan farklıdır ve hiç durmaz. Sayısal bir deney ıraksamayı "gösteremez", yalnızca hiç durmadığını gösterebilir; ıraksadığını söyleyen cebirdir.

Ayrıca dikkat: kesilme kararı bu betikte katsayılara eşik uygulanarak **verilmez**. Öyle yapmak yanlış sonuç verir — λ=2.5 için Hermite katsayıları da hızla küçülür (tıpkı `e^(x²)`'nin katsayıları gibi) ve eşik yöntemi seriyi "kesilmiş" sanır. Karar rekürans payının cebirsel olarak sıfırlanmasından okunur, sonra katsayıların gerçekten tam sıfır olduğu ayrıca sınanır.

Iraksamadan kaçmanın **tek** yolu payın sıfırlanmasıdır:

```
n(n+1) − λ = 0   ⟺   λ = l(l+1),  l ∈ ℕ
```

Tam sayı buradan çıkar. Kimse dayatmadı; seri başka seçenek bırakmadı.

## Hermite denklemi

```
y'' − 2xy' + 2λy = 0      a_{n+2} = 2(n − λ) / [(n+1)(n+2)] · a_n
```

Kuantum harmonik osilatörde dalga fonksiyonu `ψ = H(x)·e^(−x²/2)`. H seri olarak kalırsa büyük x'te `e^(x²)` gibi büyür ve `ψ ~ e^(+x²/2)` olur — normalize edilemez, yani parçacığın bulunma olasılığı sonsuza gider. Tablo `x=4`'teki değerleri ve karar ölçütünü verir. Karar tek bir noktaya değil, normalizasyon integraline dayanır: `∫|ψ|² dx` önce `[−4, 4]`, sonra `[−6, 6]` üzerinde hesaplanır. ψ gerçekten sönüyorsa pencereyi büyütmek integrali değiştirmez (oran ≈ 1); ψ ~ e^(+x²/2) ise integral e^(L²) gibi büyür. Eşik: oran < 1.01.

| λ   | seri kesiliyor mu? | H(4)        | ψ(4) = H(4)·e⁻⁸ | ∫ψ² oranı (L=6 / L=4) | durum                |
|-----|--------------------|-------------|-----------------|-----------------------|----------------------|
| 0   | evet, derece 0     | 1.0000e+00  | 3.3546e-04      | 1.000000              | normalize edilebilir |
| 1   | evet, derece 1     | 4.0000e+00  | 1.3419e-03      | 1.000001              | normalize edilebilir |
| 2   | evet, derece 2     | -3.1000e+01 | -1.0399e-02     | 1.000008              | normalize edilebilir |
| 3   | evet, derece 3     | -3.8667e+01 | -1.2971e-02     | 1.000085              | normalize edilebilir |
| 2.5 | HAYIR              | 4.2513e+04  | 1.4261e+01      | 9.522e+06             | PATLIYOR             |
| 3.7 | HAYIR              | 1.0531e+04  | 3.5328e+00      | 1.025e+06             | PATLIYOR             |

Kesilme şartı `λ = n`. Kuantum mekaniği dersinde `E_n = ℏω(n + ½)` diye ezberlenen formüldeki `n`, **bu rekürans hangi indekste sıfırlandıysa odur**. Enerji kuantumlanmış, çünkü seri ancak tam sayılarda kesiliyor.

## Sembolik doğrulama

Rekürans elle türetildiği için sonuçlar sympy ile sınandı: her kesilen seri ilgili diferansiyel denkleme konuldu ve kalıntının **tam olarak sıfır** olduğu doğrulandı.

| denklem  | parametre | bulunan polinom         | denklemdeki kalıntı |
|----------|-----------|-------------------------|---------------------|
| Legendre | l=0, λ=0  | 1                       | 0 ✓                 |
| Legendre | l=1, λ=2  | x                       | 0 ✓                 |
| Legendre | l=2, λ=6  | 1 - 3*x**2              | 0 ✓                 |
| Legendre | l=3, λ=12 | -5*x**3/3 + x           | 0 ✓                 |
| Legendre | l=4, λ=20 | 35*x**4/3 - 10*x**2 + 1 | 0 ✓                 |
| Hermite  | n=0, λ=0  | 1                       | 0 ✓                 |
| Hermite  | n=1, λ=1  | x                       | 0 ✓                 |
| Hermite  | n=2, λ=2  | 1 - 2*x**2              | 0 ✓                 |
| Hermite  | n=3, λ=3  | -2*x**3/3 + x           | 0 ✓                 |
| Hermite  | n=4, λ=4  | 4*x**4/3 - 4*x**2 + 1   | 0 ✓                 |

## Taylor ile bağı

Bu bölüm laboratuvarın geri kalanının tersini yapar. Diğer betiklerde bilinen bir fonksiyonun serisi çıkarılıyordu; burada **seri önce geliyor**, fonksiyon ondan doğuyor. Legendre ve Hermite polinomları "keşfedilmiş" nesneler değil, bir rekürans bağıntısının sonlu kalmaya zorlandığında geriye bıraktığı kalıntılardır.

Ve kritik nokta: **kuantizasyon fizikten değil, yakınsaklıktan gelir.** Fiziğin koyduğu tek şart "çözüm sonlu olsun"dur; gerisini seri halleder.
