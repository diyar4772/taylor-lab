---
title: Her kararlı denge harmonik osilatördür
tags: [taylor, fizik, harmonik-osilator, kuantizasyon]
konu: Fiziğin harmonik osilatörü seçmediği, Taylor'ın başka seçenek bırakmadığı
kaynak: "[[../taylor-teori.tex|taylor-teori.tex]] §5, §6"
olusturuldu: 2026-09-17
---

# Her kararlı denge harmonik osilatördür

Fizikte harmonik osilatörün her yerden çıkması öğrenciye bir tesadüf ya da
hocaların kolaycılığı gibi görünür: yay, sarkaç, LC devresi, kristal örgüsü,
moleküler titreşim, kuantum alanları. Hepsi neden aynı denkleme indirgeniyor?

Cevap fizikte değil, Taylor açılımının katsayı muhasebesinde:
[[Taylor açılımı bir tanım değil zorunluluktur]].

## Argüman üç satır

$V$ bir potansiyel, $x_0$ da bir **kararlı denge** noktası olsun — yani
$V'(x_0) = 0$ ve $V''(x_0) > 0$. $u = x - x_0$ yazıp $V$'yi $x_0$ etrafında aç:

$$V(x_0+u) = \underbrace{V(x_0)}_{\text{sabit}}
+ \underbrace{V'(x_0)\,u}_{=\,0}
+ \tfrac12 V''(x_0)\,u^2 + \tfrac16 V'''(x_0)\,u^3 + \cdots$$

Terimleri tek tek ele:

1. **Sabit terim** harekete katkı yapmaz, çünkü kuvvet $-V'$'dür ve sabitin
   türevi sıfırdır. Potansiyelin sıfır noktası zaten keyfîdir.
2. **Birinci mertebe terim sıfırdır** — ama bir tesadüf olduğu için değil,
   $x_0$'ın denge noktası *olmasının tanımı* bu olduğu için.
3. Geriye **ilk hayatta kalan terim** olarak $\tfrac12 V''(x_0) u^2$ kalır.
   Bu, $k = V''(x_0)$ yay sabitiyle yay potansiyelinin ta kendisidir.

Yani küçük salınımlar için, potansiyelin biçimi *ne olursa olsun*, hareket
$m\ddot u = -V''(x_0)\,u$ denklemine indirgenir.

**Doğa harmonik osilatörü seçmiyor. Taylor serisi başka seçenek bırakmıyor.**
İlk iki terim zorunlu olarak öldüğü için, sırada kalan ilk şey kareseldir; ve
karesel potansiyel demek harmonik osilatör demektir.

## Atılan terimin faturası: sarkaç

"Küçük açı yaklaşımı" $\sin\theta \approx \theta$ masum bir sadeleştirme gibi
sunulur. Değil — bu, $\sin\theta = \theta - \theta^3/6 + \cdots$ serisini ilk
terimde kesmektir ve atılan $-\theta^3/6$ **yok olmaz, periyotta geri döner**.

Harmonik osilatörde periyot genlikten bağımsızdır (izokronizm). Gerçek
sarkaçta değildir. `02-python/src/sarkac.py` tam denklemi `solve_ivp` ile
çözüp periyodu olay tabanlı sıfır geçişinden ölçer
($L = 1$ m, $g = 9{,}80665$ m/s², $T_0 = 2{,}006409$ s):

| $\theta_0$ | ölçülen $T$ (s) | harmoniğe göre sapma |
|---|---|---|
| $10°$ | 2,010236 | %0,19 |
| $45°$ | 2,086612 | %4,00 |
| $90°$ | 2,368246 | %18,03 |
| $150°$ | 3,535702 | %76,22 |

$150°$'de harmonik tahmin **%76 yanlıştır**. "Yaklaşım" dediğimiz şeyin
faturası budur.

## Mertebe bir tahmin değil, ölçülebilir bir öngörüdür

Bu notun en sevdiğim kısmı. Taylor kesmesinin hata mertebesini log–log
eğiminden *ölçebilirsin*:

| düzeltme | ölçülen mertebe | beklenen |
|---|---|---|
| düzeltmesiz | $\theta_0^{2{,}00}$ | 2 |
| $+\,\theta_0^2/16$ | $\theta_0^{4{,}00}$ | 4 |
| $+$ bir sonraki terim | $\theta_0^{6{,}01}$ | 6 |

Her düzeltme mertebeyi tam olarak **2** artırıyor — 1 değil. Sebep:
$\theta_0 \to -\theta_0$ simetrisi tek kuvvetleri yasaklar, bu yüzden seri
ikişer ikişer ilerler. Teori sayıyı önceden söylüyor, ölçüm onu virgülden
sonra ikinci haneye kadar doğruluyor.

Not: sayısal ölçüm ile eliptik kapalı biçim arasındaki fark en fazla
$1{,}3\times10^{-11}$ %'dir. Yani tablodaki sapmalar çözücü hatası değil,
**tamamı Taylor kesmesinden** geliyor.

## Aynı fikrin bir üst basamağı: kuantizasyon

Denge argümanı "hangi terim hayatta kalır" sorusuydu. Frobenius serilerinde
soru "seri ne zaman **durmak zorunda**" olur ve cevap şaşırtıcı bir yere
çıkar.

Kuantum harmonik osilatörde dalga fonksiyonu $\psi = H(x)e^{-x^2/2}$'dir.
$H$ sonsuz seri olarak kalırsa büyük $x$'te $e^{x^2}$ gibi büyür, dolayısıyla
$\psi \sim e^{+x^2/2}$ olur — **normalize edilemez.** Fiziğin koyduğu tek
şart budur: çözüm sonlu kalsın. Gerisini rekürans halleder; seri ancak
$\lambda$ tam sayı olduğunda kesilir.

`02-python/src/frobenius.py` bunu $x=4$'te ölçüyor: $\lambda = 3$ için
$\psi(4) \approx -1{,}3\times10^{-2}$ (sönüyor), $\lambda = 2{,}5$ için
$\psi(4) \approx 1{,}4\times10^{1}$ (patlıyor).

Yani $E_n = \hbar\omega(n + \tfrac12)$ formülündeki $n$, rekürans bağıntısının
hangi indekste sıfırlandığıdır. **Kuantizasyon fizikten değil,
yakınsaklıktan doğar.**

> Dürüst uyarı: kesilme kararı katsayılara sayısal eşik uygulanarak
> verilemez. $\lambda = 2{,}5$ için katsayılar da hızla küçülür (tıpkı
> $e^{x^2}$'nin katsayıları gibi) ve eşik yöntemi seriyi yanlışlıkla
> "kesilmiş" sayar. Karar, rekürans payının cebirsel sıfırlanmasından
> okunmalıdır.

## Ortak çekirdek

Dört notun da aynı kapıya çıktığı yer burası: **Taylor serisi bir hesap aracı
değil, yerel davranışın tam bir muhasebesidir.** Attığın her terimin faturası
bir yerde kesilir — sarkacın periyodunda, yakınsaklık diskinin kenarında
([[Yakınsaklık yarıçapı kompleks düzlemde belirlenir]]), ya da bir kuantum
sayısında.

## Bağlantılar

- [[Taylor açılımı bir tanım değil zorunluluktur]]
- [[Yakınsaklık yarıçapı kompleks düzlemde belirlenir]]
- [[Pürüzsüz olmak analitik olmak değildir]]
