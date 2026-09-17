---
title: Yedi sonuç — derin okuma
tags: [kilavuz, kilavuz/sonuc, taylor]
created: 2026-09-17
status: tamam
lang: tr
---

# Yedi sonuç: derin okuma

↑ [[00-BASLA-BURADAN]] · Kavramlar: [[11-kavram-haritasi]] · English: [[10-seven-results]]

Her sonuç için aynı beş soru:

- **İddia:** ne söyleniyor?
- **Kaynak:** hangi betik üretti?
- **Kritik sütun:** tabloda nereye bakmalı?
- **Neden şaşırtıcı:** beklenmedik olan ne?
- **Yıktığı yanlış:** hangi yaygın yanlış anlamayı düzeltiyor?

---

## 1. Lagrange sınırı hiç ihlal edilmedi

**İddia.** Her $(f,a,N,x)$ için
$$\lvert f(x)-P_N(x)\rvert \le \frac{\sup_{[a,x]}\lvert f^{(N+1)}\rvert}{(N+1)!}\,\lvert x-a\rvert^{N+1}.$$
8 fonksiyon × $N=1..12$ × 1501 nokta = **144 096** denemede teyit edilmiş ihlal **0**.

**Kaynak.** `kalan_dogrulama.py` → `toplu_dogrulama()`, `adaylari_teyit_et()`;
çekirdek `taylor.py` → `kalan_raporu()`.

**Kritik sütunlar** (`out/tablolar/kalan_dogrulama.md`):

- **float64 aday ihlal**: float64'ün "sınır aşıldı" dediği nokta sayısı.
  Toplam 2224 (Fedora); Windows'ta 2232. Platformun `libm`'ine bağlıdır.
- İkinci tablodaki **float64 oran** ve **mpmath oran**: aynı nokta, iki ölçüm.
  Örneğin `1/(1-x), N=2, x≈0` için float64 oranı $1{,}6\times10^{32}$, mpmath
  oranı $1{,}000000$.
- **en kötü oran**: yalnızca "anlamlı rejimde" alınan float64 maksimumudur.
  **8 satırın 6'sında 1'i geçer** (sin 1,0506; cos 1,0178; exp 1,0107;
  ln(1+x) **2,3593**; sqrt 1,0550; exp, a=1: 1,0147; sin, a=π/4: 1,0121).

### Aday ihlal ve teyit edilmiş ihlal

| | Aday ihlal | Teyit edilmiş ihlal |
|---|---|---|
| Kim karar verir? | float64 | mpmath, 60 basamak |
| Ölçtüğü | `abs(f(x) - P(x)) > sınır` (float64) | aynı fark, 60 basamakla |
| Hata kaynağı | yıkıcı sadeleşme: $f(x)\approx P_N(x)$ iken fark ~$\varepsilon\lvert f\rvert\approx10^{-16}$'nın altına inemez | yok (bu mertebede) |
| Sayı | 2224 | **0** |
| Ne anlama gelir? | "buraya bak" | "teorem burada çiğnendi" |

Bir örnekle: `ln(1+x)`, $N=7$, $x\approx0{,}0126$.

- Lagrange sınırı $7{,}94\times10^{-17}$.
- Float64 ile ölçülen hata $1{,}87\times10^{-16}$, oran **2,36**.
- mpmath ile ölçülen hata $7{,}85\times10^{-17}$, oran **0,989**.

Sınır keskindir ama tutar. Float64'ün "anlamlı rejim" filtresi
(`sınır > (N+2)·ε·(Σ|terim| + |f|)`) bu noktayı kaçırmıştır, çünkü sınır
tabanın yalnızca 1,6 katıdır. Bu yüzden depo filtreye de güvenmez: **bütün**
adaylar mpmath'e gider.

**Neden şaşırtıcı?** Binlerce "ihlal" görüp teoremden şüphelenmek çok
doğaldır. Asıl ders, ölçüm aletinin çözünürlüğünün de ölçülmesi gerektiğidir.

**Yıktığı yanlış.** "Bilgisayar hesapladıysa doğrudur" ve "float64 16 hane
verir, yeter". Hata iki yakın sayının **farkı** olduğunda 16 hanenin tamamı
kaybolabilir.

![Lagrange](../../../out/gorseller/kalan_dogrulama.png)

---

## 2. ξ gerçekten var — yarıçapın dışında bile

**İddia.** Lagrange kalanı bir **eşitliktir**:
$f(x)=P_N(x)+\dfrac{f^{(N+1)}(\xi)}{(N+1)!}(x-a)^{N+1}$ ve $\xi$ sayısal
olarak bulunabilir.

**Kaynak.** `kalan_dogrulama.py` → `ksi_bul()`, `ksi_tablosu()`. Biçimsel
karşılığı `TaylorLab.ksi_vardir`.

**Kritik sütunlar** (`ksi_varligi.md`): **bulunan ksi**, **(a,x) içinde mi?**,
**eşitlik artığı**. Son satır: `ln(1+x)`, $N=6$, $x=1{,}8$, $\xi\approx0{,}14357$,
artık $4{,}22\times10^{-15}$.

**Nasıl bulunuyor?** Eşitlikten gereken türev değeri tek başına çıkar:
$f^{(N+1)}(\xi)=\dfrac{(f(x)-P_N(x))\,(N+1)!}{(x-a)^{N+1}}$. Sağ taraf bir
sayıdır. $(a,x)$ 4001 noktada taranır, ilk işaret değişiminde `brentq` kökü
bulur. Elle kontrol (`sin`, $N=3$, $x=1{,}2$):
$\sin\xi = (0{,}932039-0{,}912)\cdot24/2{,}0736 \approx 0{,}2319 \Rightarrow \xi\approx0{,}2341$. ✓

### ξ'nin yarıçap dışında da var olması

$\ln(1+x)$'in 0 merkezli serisinin yarıçapı 1'dir; $x=1{,}8$'de seri
**ıraksar** ($P_N(1{,}8)$, $N\to\infty$'da hiçbir yere gitmez). Buna rağmen:

- Lagrange teoremi yalnızca $f$'in $[0;1{,}8]$ üzerinde $N+1$ kez
  türevlenebilir olmasını ister. $\ln(1+x)$ orada pürüzsüzdür (tekillik
  $x=-1$'de).
- Teorem **tek bir sabit $N$** hakkındadır; $N\to\infty$ limiti hakkında
  hiçbir şey söylemez.
- Iraksama şurada görünür: $x=1{,}8$'de kalan $N$ ile küçülmez, büyür. Ama her
  sabit $N$ için kalanı tam veren bir $\xi$ vardır.

**Neden şaşırtıcı?** "Yarıçapın dışında Taylor anlamsızdır" diye öğrenilir.
Anlamsız olan **seri**dir; **polinom** ve onun kalanı her yerde anlamlıdır.

**Yıktığı yanlış.** "Taylor polinomu = Taylor serisinin kısaltması, dolayısıyla
seri ıraksayan yerde polinomun da söyleyecek bir şeyi yoktur." Bir de: "$\xi$
tektir". Teorem yalnızca varlık söyler; `ksi_bul` ilk kökü döndürür.

---

## 3. Yakınsaklık diski veriden çıktı

**İddia.** $R$, merkezin en yakın kompleks tekilliğe uzaklığıdır ve bu,
teorik değer hiç kullanılmadan hatanın kendi işaretinden okunabilir.

**Kaynak.** `kompleks_harita.py` → `hata_haritasi()`,
`yaricapi_haritadan_kestir()`. Bağımsız ikinci uygulama:
`03-matlab-octave/yakinsaklik_diski.m`. Üçüncüsü: web panel 2.

**Kritik sütunlar** (`kompleks_yaricap.md`): **teorik R** ve **haritadan
okunan R**. Son iki satırı birlikte oku: `1/(1+z²)` $a=0\to R=1$, $a=1\to R=\sqrt2$;
`1/(1-z)` $a=0\to1$, $a=-1\to2$.

**Mekanizma.** $\lvert f-P_N\rvert\sim C\,(\lvert z-a\rvert/R)^{N+1}$ ⇒
$L_N=\frac1N\log_{10}\lvert f-P_N\rvert\to\log_{10}(\lvert z-a\rvert/R)$.
İşareti yakınsaklığı söyler; sıfır düzeyi $\lvert z-a\rvert=R$ çemberidir.

**Neden hep %5–8 aşağıda?** Okunan $R$, sıfır düzeyinin merkeze **en kısa**
uzaklığıdır ve bu en kısa uzaklık tekilliğe doğru olan yöndedir, çünkü
oradaki $C$ çarpanı büyür. `1/(1-z)` için $f-P_N=z^{N+1}/(1-z)$; $z=r$ yönünde
sıfır düzeyi $r^{29}=1-r$'nin kökü, yani $r\approx0{,}9175$. Izgarada okunan
0,9219 buna karşılık gelir. $N\to\infty$'da $C^{1/N}\to1$ olur ve sapma kaybolur.

![Kompleks harita](../../../out/gorseller/kompleks_hata_haritasi.png)

**Neden şaşırtıcı?** `1/(1+x²)` reel eksende kusursuzdur, ama seri
$\lvert x\rvert=1$'de durur. Sebep bir boyut yukarıdadır.

![Reel eksende ipucu yok](../../../out/gorseller/reel_eksende_ipucu_yok.png)

**Yıktığı yanlış.** "Yakınsaklık yarıçapı fonksiyonun bir özelliğidir" (oysa
(fonksiyon, merkez) çiftinindir) ve "reel fonksiyonun davranışını reel eksen
belirler".

---

## 4. Aynı yarıçap, yalnızca katsayılardan

**İddia.** $1/R=\limsup\lvert a_n\rvert^{1/n}$ (Cauchy–Hadamard). Tekilliklere
hiç bakmadan, yalnızca katsayı dizisinden 3. sonuçtaki yarıçaplar yeniden
bulunur.

**Kaynak.** `yakinsaklik_orani.py`; `taylor.py` → `cauchy_hadamard_R()`
(son 12 sıfırsız terimin maksimumu), `oran_testi_R()`
($\lvert a_n/a_{n+d}\rvert^{1/d}$). Biçimsel: `TaylorLab.cauchy_hadamard`.

**Kritik sütunlar** (`cauchy_hadamard.md`): **C-H kestirimi**, **C-H
hatası**, **oran testi**, **oran hatası**.

### limsup neden limit değil?

$\lim$ ancak dizi tek bir değere yerleşirse vardır. $\limsup$ ise her zaman
vardır: dizinin kuyrukta **tekrar tekrar** yaklaştığı en büyük değerdir.

`1/(1+x²)`, $a=1$ örneği: $i$ ve $-i$ merkezden **eşit uzaklıkta**
($\sqrt2$) ama farklı yönlerde. Kısmi kesirden
$$c_n=(-1)^n\,2^{-(n+1)/2}\,\sin\frac{(n+1)\pi}{4}.$$
$\lvert\sin\rvert$ çarpanı $n$'e göre 4 periyotla $\{0{,}707;\,1;\,0{,}707;\,0\}$
değerlerini alır ($n\equiv3 \pmod 4$ için katsayı tam **sıfır**). Sonuçta:

- $\lvert c_n\rvert^{1/n}\to 2^{-1/2}$ **alt dizi boyunca** ⇒ $\limsup=1/\sqrt2$ ⇒ $R=\sqrt2$. ✓
- $\lvert c_n/c_{n+1}\rvert$ ise dönüp durur. Tam katsayılarla $N=52..60$ için
  oran testi: `1.4142, 1.0, 2.0, 2.0, 1.4142, 1.0, 2.0, 2.0, 1.4142`.
  **Limit yoktur**; oran testinin sonucu hangi $N$'de durduğuna bağlıdır.

> [!note] Düzeltme: eski %22,66
> Deponun ilk sürümü bu satırda oran testinin %22,66, C-H'nin %1,66 saptığını
> yazıyordu. Bu kılavuz yazılırken yapılan kontrol, sayıların **kayan nokta
> hassasiyet kaybıyla kirlendiğini** gösterdi: `katsayi_dizisi` merkezi float
> olarak veriyordu; $n=40$'ta bağıl hata ~$10^{-5}$, $c_{60}$'ın ise işareti
> yanlıştı ($+2{,}55\times10^{-9}$, doğrusu $-4{,}66\times10^{-10}$).
> Düzeltmeden sonra (`sp.Rational(a)`) tablo $N=60$'ta oran testi için tam
> $\sqrt2$ (%0,00), C-H için 1,4228 (%0,61) veriyor ve yukarıdaki salınım
> tablosunu da içeriyor. Ayrıntı: [[12-eksikler-ve-devam]].

**Diğer satırlar.**

- `exp`, `sin`: $R=\infty$ görülemez. C-H $N$ ile büyür (N=30: 7,93;
  N=60: 19,11; N=120: 41,3), oran testi tam $N$ verir.
- `ln(1+x)`, `sqrt(1+x)`: katsayılarda $1/n$ gibi cebirsel çarpan var ve
  $(1/n)^{1/n}\to1$ çok yavaş; $N=60$'ta %7–13 sapma kalır.
- `1/(1-x), a=-1`: C-H %1,16 fazla, çünkü $\lvert c_n\rvert^{1/n}=2^{-(n+1)/n}$
  ve sonlu $n$'de $(n+1)/n>1$. Oran testi tam 2.

![Cauchy–Hadamard](../../../out/gorseller/cauchy_hadamard.png)

**Neden şaşırtıcı?** Geometri (tekillikler) ile aritmetik (katsayıların
büyüme hızı) aynı sayıyı veriyor.

**Yıktığı yanlış.** "Oran testi ile kök testi aynı şeydir" ve "limsup sadece
titizlik süsüdür".

---

## 5. Küçük açı yaklaşımının faturası

**İddia.** $\sin\theta\approx\theta$ yaklaşımı $-\theta^3/6$ terimini atar;
bu terim **periyodun genliğe bağımlılığı** olarak geri döner:
$T=T_0\left(1+\frac{\theta_0^2}{16}+\frac{11\theta_0^4}{3072}+\cdots\right)$.

**Kaynak.** `sarkac.py` → `periyodu_olc()` (solve_ivp + olay),
`tam_periyot_eliptik()`, `taylor_periyot()`. Bağımsız: web (RK4 + AGM),
Godot (AGM).

**Kritik sütunlar** (`sarkac.md`):

- **harmonik T₀** sabit (2,006409 s): izokronizm.
- **ölçüm-kapalı fark** en fazla $1{,}3\times10^{-11}$ %: çözücü güvenilir,
  kalan her fark Taylor kesmesinden gelir.
- **Taylor-2 hatası** / **Taylor-4 hatası**: eliptik değere göre.
- Log–log eğimler: 4,00 ve 6,01.

### "%76" neye göre?

| Karşılaştırma | 150°'de |
|---|---|
| $(T-T_0)/T_0$: harmoniğe göre sapma (README, web, Godot) | **%76,22** |
| $(T-T_0)/T$: harmonik tahminin gerçeğe göre hatası | %43,25 |
| $\lvert T_0(1+\theta_0^2/16)-T\rvert/T$: Taylor-2 hatası | %18,94 |
| Taylor-4 hatası | %9,40 |

**Neden şaşırtıcı?** Mertebe bir tahmin değil, **ölçülebilir**: her düzeltme
hata üstelini tam 2 artırır, çünkü $T(\theta_0)$ çifttir.

**Yıktığı yanlış.** "Sarkacın periyodu genlikten bağımsızdır" (yalnızca
harmonik yaklaşımda doğru) ve "yaklaşımın bedeli yalnızca küçük bir sayısal
hatadır". Bedel **niteliksel**: izokronizm kaybolur.

![Sarkaç](../../../out/gorseller/sarkac_periyot.png)

---

## 6. Kuantizasyon fizikten değil, yakınsaklıktan

**İddia.** Hermite denklemi $y''-2xy'+2\lambda y=0$ her $\lambda$ için seri
çözüme sahiptir. Tam sayılar, çözümün sonlu kalması şartından gelir.

**Kaynak.** `frobenius.py` → `hermite_katsayilari()`, `kesilme_derecesi()`,
`kesilme_dogrula()`, `sembolik_dogrulama()`.

**Kritik sütunlar** (`frobenius.md`): **seri kesiliyor mu?**, **H(4)**,
**ψ(4)**, **∫ψ² oranı (L=6 / L=4)**; Legendre için **kısmi toplam büyümesi**; doğrulamada
**denklemdeki kalıntı** (hepsi `0 ✓`).

### Kuantizasyon rekürans kesilmesinden nasıl doğar?

1. $y=\sum a_nx^n$ konunca $a_{n+2}=\dfrac{2(n-\lambda)}{(n+1)(n+2)}\,a_n$ çıkar.
   Denklem $\lambda$'yı **kısıtlamaz**.
2. Kesilmezse büyük $n$'de $a_{n+2}/a_n\approx 2/n$ olur. Bu $e^{x^2}$'nin
   katsayı oranıdır, dolayısıyla $H\sim e^{x^2}$ ve
   $\psi=He^{-x^2/2}\sim e^{+x^2/2}$: **normalize edilemez**.
3. Tek kaçış payın sıfırlanmasıdır: $n-\lambda=0$ ⇒ $\lambda\in\mathbb N$
   (ve başlatan katsayının paritesi uymalı). Seri polinoma döner.
4. Fizik yalnızca "$\psi$ sonlu olsun" der. $E=\hbar\omega(\lambda+\tfrac12)$
   olduğundan $E_n=\hbar\omega(n+\tfrac12)$'deki $n$ **kesilme indeksidir**.

Legendre'de aynı mantık $\lambda=\ell(\ell+1)$ verir. Oradaki ıraksama
$x=\pm1$'de ve **logaritmik** olduğu için 400 terimde bile $y(1)$ sonlu görünür.
Kanıt **kısmi toplam büyümesi** sütunudur (kesilenlerde tam 0).

**İki dürüstlük notu.**

- Kesilme **eşikle** belirlenemez: $\lambda=2{,}5$ için katsayılar
  $n\approx28$'den sonra $10^{-14}$'ün altına iner ama sıfır değildir.
- "normalize edilebilir / PATLIYOR" kararı normalizasyon integraline
  dayanır: $\int\psi^2$'nin $[-6,6]$ ile $[-4,4]$ üzerindeki oranı. Tam sayı
  $\lambda$'da oran en fazla $1{,}000085$, $\lambda=2{,}5$'te
  $9{,}5\times10^6$. (İlk sürüm yalnızca $\lvert\psi(4)\rvert<1$'e bakıyordu.)

![Hermite](../../../out/gorseller/frobenius_hermite.png)

**Neden şaşırtıcı?** Tam sayılar "kuantum postülası" gibi öğretilir.
Burada bir serinin sonlu kalma koşulundan çıkıyorlar.

**Yıktığı yanlış.** "Denklemin kendisi yalnızca tam sayılarda çözülür." Hayır,
her $\lambda$'da çözülür; yalnızca tam sayılarda çözüm **fiziksel** olur.

---

## 7. Pürüzsüz ama analitik değil

**İddia.** $f(x)=e^{-1/x^2}$ ($f(0)=0$) için $f\in C^\infty$ ve her $n$ için
$f^{(n)}(0)=0$. Maclaurin serisi $\equiv0$, her $x$'te yakınsar, ama $x\neq0$
için $f(x)>0$. Dolayısıyla $C^\omega\subsetneq C^\infty$.

**Kaynak.** `analitik_degil.py` → `turevler_sifirda()` (`sympy.limit`,
$n=0..8$), `kompleks_tekillik()`. Biçimsel: `purussuz_ama_analitik_degil`
(tanık `expNegInvGlue`, yani $e^{-1/x}$).

**Kritik sütunlar** (`analitik_degil.md`): **f⁽ⁿ⁾(0) (limit)** hep 0. **Aynı
türevin x=0.1'deki değeri** $3{,}7\times10^{-44}$'ten $6{,}1\times10^{-18}$'e
çıkar. İkinci tablo: $\lvert z\rvert=0{,}05$'te reel yönde
$1{,}9\times10^{-174}$, hayali yönde $5{,}2\times10^{173}$.

**Mekanizma.** $f^{(n)}(x)=p_n(1/x)\,e^{-1/x^2}$; $e^{-u^2}$ her polinomdan
hızlı söner. Kompleks tarafta $z=iy$ için $-1/z^2=+1/y^2$ ⇒ $e^{1/y^2}\to\infty$:
$z=0$ **esas tekilliktir**.

**3. sonuçla ilişkisi.** "R = en yakın tekilliğe uzaklık" teoremi $f$'in
merkezde holomorf olmasını ister; burada değildir. Serinin $R=\infty$ çıkması
bu yüzden teoremle çelişmez: seri $f$'in değil, sıfır fonksiyonunun serisidir.

![Analitik değil](../../../out/gorseller/analitik_degil.png)

**Neden şaşırtıcı?** Seri **yakınsıyor**, hem de her yerde, ama yanlış şeye.

**Yıktığı yanlış.** "Sonsuz kez türevlenebilen fonksiyon Taylor serisine
eşittir" ve "seri yakınsıyorsa fonksiyona yakınsıyordur". Bir de: "Sayısal
türev sıfır çıktı, demek ki sıfır". $f(0{,}1)$ zaten float64'ün
göremeyeceği kadar küçük.

---

## Özet tablo

| # | Sonuç | Betik | Tablo | Video | Lean |
|---|---|---|---|---|---|
| 1 | Lagrange sınırı tutar | `kalan_dogrulama.py` | `kalan_dogrulama.md` | 3 | (dolaylı) `ksi_vardir` |
| 2 | ξ vardır | `kalan_dogrulama.py` | `ksi_varligi.md` | 3 | `ksi_vardir` |
| 3 | R kompleks düzlemde | `kompleks_harita.py` | `kompleks_yaricap.md` | 4 | `disk_icinde_mutlak_yakinsar` (kısmen) |
| 4 | R katsayılardan | `yakinsaklik_orani.py` | `cauchy_hadamard.md` | — | `cauchy_hadamard`, `geometrik_yaricap_bir` |
| 5 | Sarkaç | `sarkac.py` | `sarkac.md` | 6 | yok |
| 6 | Kuantizasyon | `frobenius.py` | `frobenius.md` | — | yok |
| 7 | $C^\omega\subsetneq C^\infty$ | `analitik_degil.py` | `analitik_degil.md` | 5 | `purussuz_ama_analitik_degil` |
