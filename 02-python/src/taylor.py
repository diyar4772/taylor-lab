"""Taylor açılımı çekirdeği: sembolik (sympy) ve sayısal (numpy) motor.

Bu modül laboratuvarın geri kalanının üzerine kurulduğu tek kaynaktır.
Diğer betikler buradaki fonksiyonları import eder; formül tekrarı yoktur.

Tasarımın merkezindeki fikir:

    P_N(x) = sum_{n=0}^{N} f^(n)(a) / n! * (x - a)^n

Buradaki n! bir süsleme değildir. (x-a)^n terimini n kez türevlediğinde
önüne n! çarpanı düşer; katsayıyı n!'e bölmek tam olarak bu çarpanı
sıfırlar. Yani a_n = f^(n)(a)/n! seçimi, "P_N'in a noktasındaki n. türevi
f'in a noktasındaki n. türevine eşit olsun" koşulunun ZORUNLU sonucudur,
bir tercih değil.  (Bkz. "00-teori/obsidian/Taylor açılımı bir tanım değil zorunluluktur.md")
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from functools import lru_cache
from typing import Callable, Sequence

import numpy as np
import sympy as sp

import ortam  # UTF-8 çıktı ve ortak yollar (yan etkisi için import edilir)

_ = ortam.PALET  # linter'ın import'u "kullanılmıyor" diye atmasını engeller

# --------------------------------------------------------------------------
# Ortak sembol ve fonksiyon kataloğu
# --------------------------------------------------------------------------

x = sp.Symbol("x", real=True)

#: Laboratuvar boyunca kullanılan standart fonksiyonlar.
#: Her giriş: (sympy ifadesi, varsayılan açılım merkezi a, teorik yakınsaklık
#: yarıçapı R -- a merkezli, matematiksel olarak bilinen değer).
KATALOG: dict[str, tuple[sp.Expr, float, float]] = {
    "sin":        (sp.sin(x),            0.0, math.inf),
    "cos":        (sp.cos(x),            0.0, math.inf),
    "exp":        (sp.exp(x),            0.0, math.inf),
    "ln(1+x)":    (sp.log(1 + x),        0.0, 1.0),
    "1/(1-x)":    (1 / (1 - x),          0.0, 1.0),
    "1/(1+x^2)":  (1 / (1 + x**2),       0.0, 1.0),
    "arctan":     (sp.atan(x),           0.0, 1.0),
    "sqrt(1+x)":  (sp.sqrt(1 + x),       0.0, 1.0),
}


# --------------------------------------------------------------------------
# Sembolik katman
# --------------------------------------------------------------------------

def taylor_katsayilari(expr: sp.Expr, a: float, N: int) -> list[sp.Expr]:
    """a_0..a_N katsayılarını f^(n)(a)/n! tanımından, TÜREV ALARAK üretir.

    Kasıtlı olarak ``sp.series`` kullanılmaz: amaç katsayının nereden
    geldiğini kodda da görünür kılmak. n. türev alınır, x=a konur, n!'e
    bölünür -- tanımın birebir çevirisi.
    """
    katsayilar = []
    turev = expr
    for n in range(N + 1):
        if n > 0:
            turev = sp.diff(turev, x)
        katsayilar.append(sp.simplify(turev.subs(x, a) / sp.factorial(n)))
    return katsayilar


def taylor_polinomu(expr: sp.Expr, a: float, N: int) -> sp.Expr:
    """N. dereceden Taylor polinomunu sympy ifadesi olarak döndürür."""
    katsayilar = taylor_katsayilari(expr, a, N)
    return sum((c * (x - a) ** n for n, c in enumerate(katsayilar)), sp.Integer(0))


def taylor_polinomu_latex(expr: sp.Expr, a: float, N: int) -> str:
    """Manim ve LaTeX metni için hazır dize."""
    return sp.latex(sp.expand(taylor_polinomu(expr, a, N)))


# --------------------------------------------------------------------------
# Sayısal katman
# --------------------------------------------------------------------------

def polinom_fonksiyonu(expr: sp.Expr, a: float, N: int) -> Callable[[np.ndarray], np.ndarray]:
    """Taylor polinomunu vektörize edilmiş bir numpy fonksiyonuna çevirir.

    Horner düzeni yerine doğrudan katsayı toplamı kullanılır; N bu
    laboratuvarda küçük (<= ~40) olduğu için sayısal fark önemsiz, okunurluk
    kazancı ise büyüktür.
    """
    katsayilar = np.array([float(c) for c in taylor_katsayilari(expr, a, N)])

    def P(t: np.ndarray) -> np.ndarray:
        t = np.asarray(t, dtype=float)
        u = t - a
        sonuc = np.zeros_like(u, dtype=float)
        guc = np.ones_like(u, dtype=float)
        for c in katsayilar:
            sonuc = sonuc + c * guc
            guc = guc * u
        return sonuc

    return P


def sayisal_fonksiyon(expr: sp.Expr) -> Callable[[np.ndarray], np.ndarray]:
    """sympy ifadesini numpy üzerinde çalışan bir fonksiyona çevirir."""
    return sp.lambdify(x, expr, "numpy")


def katsayi_dizisi(expr: sp.Expr, a: float, N: int) -> np.ndarray:
    """a_0..a_N katsayılarını float dizisi olarak verir (Cauchy-Hadamard için).

    Merkez, float64'ün TAM ikili değerine karşılık gelen rasyonele
    (``sp.Rational(a)``) çevrilir; türevler sembolik tutulur ve yalnızca en
    sonda float'a indirgenir. Float bir ``a`` ile sympy yüksek mertebeli
    türevleri 15 basamakta değerlendirir ve yıkıcı sadeleşme katsayıları
    bozar: 1/(1+x^2), a=1.0 için n=40'ta bağıl hata ~1e-5, n=60'ta
    katsayının işareti bile yanlış çıkıyordu (kapalı biçim:
    c_n = (-1)^n 2^(-(n+1)/2) sin((n+1)π/4)).
    """
    return np.array([float(c) for c in taylor_katsayilari(expr, sp.Rational(a), N)])


# --------------------------------------------------------------------------
# Lagrange kalanı
# --------------------------------------------------------------------------

@dataclass
class KalanRaporu:
    """Bir (f, a, N, x) dörtlüsü için hata ve sınır karşılaştırması.

    ``aday_noktalar`` ile ``yuvarlama_sayisi`` ayrımı bu laboratuvarın en
    önemli sayısal ayrıntısıdır; ayrıntı için aşağıdaki ``kalan_raporu``
    açıklamasına bakın. Özetle: float64 ihlal SANABİLİR, karar veremez.
    """

    gercek_hata: np.ndarray       # float64 ile ölçülen |f(x) - P_N(x)|
    lagrange_sinir: np.ndarray    # sup|f^(N+1)| / (N+1)! * |x-a|^(N+1)
    yuvarlama_tabani: np.ndarray  # float64'ün bu noktada ölçebileceği en küçük hata
    aday_sayisi: int              # float64'e göre sınırın aşıldığı nokta sayısı
    yuvarlama_sayisi: int         # sınır yuvarlama tabanının altında kalan nokta sayısı
    en_kotu_oran: float           # yalnızca anlamlı bölgede max(hata/sınır)
    aday_noktalar: np.ndarray     # sınırın aşıldığı x'ler (mpmath ile teyit edilmeli)


def polinom_yuvarlama_tabani(
    expr: sp.Expr, a: float, N: int
) -> Callable[[np.ndarray], np.ndarray]:
    """P_N(x)'i float64 ile toplamanın kaçınılmaz yuvarlama hatasını kestirir.

    n terimli bir kayan nokta toplamının klasik hata sınırı

        |hesaplanan - gerçek| <= n * eps * sum |terim_i|

    mertebesindedir. Buna f(x)'in kendi değerlendirme hatası (~eps*|f(x)|)
    eklenir. Sonuç, "bu noktada float64 ile ölçülebilecek en küçük hata"dır;
    gerçek matematiksel hata bunun altındaysa ölçüm aleti yetersizdir,
    teorem değil.
    """
    katsayilar = np.array([float(c) for c in taylor_katsayilari(expr, a, N)])
    f = sayisal_fonksiyon(expr)
    eps = float(np.finfo(float).eps)

    def taban(t: np.ndarray) -> np.ndarray:
        t = np.asarray(t, dtype=float)
        u = t - a
        mutlak_toplam = np.zeros_like(u, dtype=float)
        guc = np.ones_like(u, dtype=float)
        for c in katsayilar:
            mutlak_toplam = mutlak_toplam + abs(c) * np.abs(guc)
            guc = guc * u
        with np.errstate(over="ignore", invalid="ignore", divide="ignore"):
            f_degeri = np.abs(np.asarray(f(t), dtype=float))
        f_degeri = np.where(np.isfinite(f_degeri), f_degeri, 0.0)
        return (N + 2) * eps * (mutlak_toplam + f_degeri)

    return taban


def lagrange_sinir(
    expr: sp.Expr,
    a: float,
    N: int,
    noktalar: np.ndarray,
    ornek_sayisi: int = 20001,
) -> np.ndarray:
    """Lagrange kalan sınırını hesaplar (vektörize, kümülatif maksimum ile).

        |R_N(x)| <= max_{ksi in [a,x]} |f^(N+1)(ksi)| / (N+1)! * |x-a|^(N+1)

    Naif yöntem her x için [a,x] aralığını ayrı ayrı tarar: P nokta için
    O(P*M) iş. Oysa sup_{[a,x]} |f^(N+1)| , x a'dan uzaklaştıkça yalnızca
    BÜYÜYEBİLİR -- yani a'dan dışarı doğru taranan bir kümülatif maksimumdur.
    Tek bir ızgara üzerinde ``np.maximum.accumulate`` ile O(M+P)'ye düşer.
    Sol (x<a) ve sağ (x>a) kollar ayrı ayrı, her biri a'dan dışarı doğru
    birikerek hesaplanır.

    Doğruluk kontrolü: ``lagrange_sinir_yavas`` aynı değerleri üretir ve
    kalan_dogrulama.py ikisini bir örneklem üzerinde karşılaştırır.
    """
    turev_f = sp.lambdify(x, sp.diff(expr, x, N + 1), "numpy")
    fakt = float(sp.factorial(N + 1))

    noktalar = np.atleast_1d(np.asarray(noktalar, dtype=float))
    sinirlar = np.zeros_like(noktalar)

    def _kol(hedefler: np.ndarray, uc: float) -> np.ndarray:
        """a ile uc arasında kümülatif sup; hedefler a'dan uzaklığa göre artan."""
        izgara = np.linspace(a, uc, ornek_sayisi)
        with np.errstate(over="ignore", invalid="ignore", divide="ignore"):
            degerler = np.abs(np.asarray(turev_f(izgara), dtype=float))
        # Tanımsız/sonsuz noktalar (örn. ln(1+x) için x=-1) sup'u sonsuz yapar.
        degerler = np.where(np.isfinite(degerler), degerler, np.inf)
        birikimli = np.maximum.accumulate(degerler)
        # |hedef - a| ızgarada hangi indekse denk geliyor?
        uzaklik = np.abs(izgara - a)
        idx = np.searchsorted(uzaklik, np.abs(hedefler - a), side="left")
        idx = np.clip(idx, 0, ornek_sayisi - 1)
        return birikimli[idx]

    sag = noktalar > a
    sol = noktalar < a
    if np.any(sag):
        sinirlar[sag] = _kol(noktalar[sag], float(noktalar[sag].max()))
    if np.any(sol):
        sinirlar[sol] = _kol(noktalar[sol], float(noktalar[sol].min()))

    sinirlar = sinirlar / fakt * np.abs(noktalar - a) ** (N + 1)
    sinirlar[noktalar == a] = 0.0
    return sinirlar


def lagrange_sinir_yavas(
    expr: sp.Expr,
    a: float,
    N: int,
    noktalar: np.ndarray,
    ornek_sayisi: int = 2001,
) -> np.ndarray:
    """Lagrange sınırının naif (nokta başına tarama) sürümü — referans.

    Hızlı sürümle aynı sonucu vermeli; tek işi onu doğrulamak. Supremum her
    x için ayrı bir ızgarada örneklenir, bu yüzden O(P*M) maliyetlidir ve
    yalnızca küçük örneklemlerde kullanılır.

    Not: supremum örnekleme ile kestirildiği için ALT kestirim riski vardır
    (gerçek tepe ızgara noktaları arasına düşerse sınır olduğundan küçük
    çıkar). Bu yüzden ızgara yoğun tutulur ve ihlaller ayrıca sayılır.
    """
    turev = sp.diff(expr, x, N + 1)
    turev_f = sp.lambdify(x, turev, "numpy")
    fakt = float(sp.factorial(N + 1))

    noktalar = np.atleast_1d(np.asarray(noktalar, dtype=float))
    sinirlar = np.empty_like(noktalar)

    for i, xi in enumerate(noktalar):
        if xi == a:
            sinirlar[i] = 0.0
            continue
        ksi = np.linspace(min(a, xi), max(a, xi), ornek_sayisi)
        with np.errstate(over="ignore", invalid="ignore", divide="ignore"):
            degerler = np.abs(np.asarray(turev_f(ksi), dtype=float))
        # Hızlı sürümle aynı sözleşme: tanımsız nokta varsa sup sonsuzdur.
        degerler = np.where(np.isfinite(degerler), degerler, np.inf)
        sinirlar[i] = degerler.max() / fakt * abs(xi - a) ** (N + 1)

    return sinirlar


def kalan_raporu(expr: sp.Expr, a: float, N: int, noktalar: np.ndarray) -> KalanRaporu:
    """Gerçek hatayı Lagrange sınırıyla karşılaştırır.

    Beklenti: gerçek hata HER noktada sınırın altında kalmalı. Bu bir
    yaklaşımın "genelde iyi çalışması" değil, teoremin iddiasıdır.

    Ancak float64 ile ölçüm yaparken kaçınılmaz bir tuzak var. Örnek:
    f=exp, a=1, N=12, x=0.996 için

        gerçek matematiksel hata  ~ 2.9e-41
        float64 ile ÖLÇÜLEN hata  ~ 4.4e-16   (= eps * |f(x)|)

    Ölçülen hata sınırdan 10^25 kat büyük görünür. Bu bir teorem ihlali
    değildir; hesap makinesinin çözünürlüğüdür. 2.9e-41'i çift duyarlıkla
    ölçmek, cetvelle atom çapı ölçmeye benzer.

    Bu yüzden noktalar iki rejime ayrılır:

    * **anlamlı rejim** (sınır > yuvarlama tabanı): float64 ölçümü kabaca
      güvenilir.
    * **yuvarlama rejimi** (sınır < yuvarlama tabanı): float64 yeterli değil.

    Ancak bu sınıflandırma, içindeki (N+2)·eps sabiti yüzünden kesin değildir:
    tabanın hemen üstünde kalan noktalarda da float64 sahte ihlal üretebilir.
    Bu yüzden ``aday_noktalar`` sınırı aşan TÜM noktaları taşır ve nihai hüküm
    float64'e bırakılmaz -- kalan_dogrulama.py her adayı mpmath ile yeniden
    ölçer. Yuvarlama tabanı yalnızca raporlama/tanı amaçlıdır.
    """
    f = sayisal_fonksiyon(expr)
    P = polinom_fonksiyonu(expr, a, N)
    taban_f = polinom_yuvarlama_tabani(expr, a, N)

    with np.errstate(over="ignore", invalid="ignore", divide="ignore"):
        gercek = np.abs(np.asarray(f(noktalar), dtype=float) - P(noktalar))
    sinir = lagrange_sinir(expr, a, N, noktalar)
    taban = taban_f(noktalar)

    gecerli = np.isfinite(gercek) & np.isfinite(sinir)
    anlamli = gecerli & (sinir > taban)
    yuvarlama = gecerli & ~anlamli

    adaylar = np.asarray(noktalar)[gecerli & (gercek > sinir)]

    oranlar = np.where(anlamli, gercek / np.where(sinir > 0, sinir, 1.0), 0.0)
    en_kotu = float(np.max(oranlar)) if oranlar.size else 0.0

    return KalanRaporu(gercek, sinir, taban, int(adaylar.size),
                       int(np.sum(yuvarlama)), en_kotu, adaylar)


@lru_cache(maxsize=256)
def _mpmath_katsayilari(expr: sp.Expr, a_str: str, N: int, basamak: int):
    """mpmath katsayılarını (f^(n)(a)/n!) `basamak` hanede üretir — önbellekli.

    ÖNEMLİ: katsayılar float bir ``a`` ile hesaplanamaz. a=1.0 verilirse sympy
    exp(1.0)'ı hemen 15 basamaklı bir Float'a çevirir ve katsayı daha doğmadan
    hassasiyetini kaybeder. Bu yüzden a, float64'ün TAM ikili değerine karşılık
    gelen rasyonele (``sp.Rational(a)``) çevrilir ve türevler sembolik tutulur;
    indirgeme yalnızca en sonda yapılır.

    Önbellek (expr, a, N) başına simgesel türev işini bir kez yapar; binlerce
    aday noktayı teyit ederken fark 100 kat mertebesindedir.
    """
    import mpmath as mp

    a_kesin = sp.Rational(float(a_str))
    katsayilar = []
    turev = expr
    onceki = mp.mp.dps
    mp.mp.dps = basamak + 15
    try:
        for n in range(N + 1):
            if n > 0:
                turev = sp.diff(turev, x)
            c = turev.subs(x, a_kesin) / sp.factorial(n)
            katsayilar.append(mp.mpf(str(sp.N(c, basamak + 15))))
    finally:
        mp.mp.dps = onceki
    return tuple(katsayilar)


def yuksek_hassasiyet_sadece_hata(
    expr: sp.Expr, a: float, N: int, xd: float, basamak: int = 60
) -> float:
    """|f(x) - P_N(x)|'i ``basamak`` ondalıkla hesaplar (sınırı hesaplamaz).

    Aday ihlalleri teyit etmek için bu yeter: Lagrange sınırı sup|f^(N+1)|
    üzerinden kurulur ve O(1) mertebesinde bir sayıdır -- float64 onu zaten
    doğru hesaplar. Hassasiyeti yiyen tek şey f(x) - P_N(x) farkındaki
    yıkıcı sadeleşmedir (catastrophic cancellation). Dolayısıyla pahalı olan
    sup taraması tekrarlanmaz.
    """
    import mpmath as mp

    onceki = mp.mp.dps
    mp.mp.dps = basamak
    try:
        katsayilar = _mpmath_katsayilari(expr, repr(float(a)), N, basamak)
        f_mp = sp.lambdify(x, expr, "mpmath")
        xm, am = mp.mpf(xd), mp.mpf(a)
        P = mp.mpf(0)
        u = xm - am
        guc = mp.mpf(1)
        for c in katsayilar:
            P += c * guc
            guc *= u
        return float(abs(f_mp(xm) - P))
    finally:
        mp.mp.dps = onceki


def yuksek_hassasiyet_hatasi(
    expr: sp.Expr, a: float, N: int, xd: float, basamak: int = 60
) -> tuple[float, float]:
    """|f(x) - P_N(x)| ve Lagrange sınırını ``basamak`` ondalıkla hesaplar.

    float64'ün yetmediği noktalarda başvurulur. mpmath keyfi hassasiyette
    çalıştığı için 1e-41 mertebesindeki bir hata da doğru ölçülür.
    """
    import mpmath as mp

    onceki = mp.mp.dps
    mp.mp.dps = basamak
    try:
        f_mp = sp.lambdify(x, expr, "mpmath")
        turev_mp = sp.lambdify(x, sp.diff(expr, x, N + 1), "mpmath")

        katsayilar = _mpmath_katsayilari(expr, repr(float(a)), N, basamak)
        xm, am = mp.mpf(xd), mp.mpf(a)
        P = mp.mpf(0)
        for n, c in enumerate(katsayilar):
            P += c * (xm - am) ** n
        hata = abs(f_mp(xm) - P)

        # sup|f^(N+1)| kestirimi: aralıkta yoğun örnekleme
        ornek = 401
        alt, ust = (am, xm) if am < xm else (xm, am)
        adim = (ust - alt) / (ornek - 1)
        sup = max(abs(turev_mp(alt + i * adim)) for i in range(ornek))
        sinir = sup / mp.factorial(N + 1) * abs(xm - am) ** (N + 1)
        return float(hata), float(sinir)
    finally:
        mp.mp.dps = onceki


# --------------------------------------------------------------------------
# Cauchy-Hadamard
# --------------------------------------------------------------------------

def cauchy_hadamard_R(katsayilar: Sequence[float], son_k: int = 12) -> float:
    """1/R = limsup |a_n|^(1/n) formülünden R'yi sayısal olarak kestirir.

    limsup sonlu veriden okunamayacağı için son ``son_k`` sıfırdan farklı
    terimin |a_n|^(1/n) değerlerinin maksimumu alınır. Terimleri seyrek olan
    seriler (örn. 1/(1+x^2): tek dereceli katsayılar sıfır) bu yüzden
    sıfırlar atlanarak işlenir -- aksi halde 0^(1/n)=0 limsup'ı yanlış
    biçimde aşağı çeker.
    """
    dizi = []
    for n, c in enumerate(katsayilar):
        if n == 0 or c == 0:
            continue
        dizi.append(abs(c) ** (1.0 / n))
    if not dizi:
        return math.inf
    kuyruk = dizi[-son_k:]
    ust = max(kuyruk)
    return math.inf if ust == 0 else 1.0 / ust


def oran_testi_R(katsayilar: Sequence[float]) -> float:
    """Oran testiyle R kestirimi: R ~ |a_n / a_{n+1}| (son sıfırdan farklı çift).

    Cauchy-Hadamard her zaman geçerlidir; oran testi ise limit varsa daha
    hızlı yakınsar. İkisini birlikte raporlamak, seyrek serilerde oran
    testinin neden yanıltıcı olabileceğini de gösterir.
    """
    sifirsiz = [(n, c) for n, c in enumerate(katsayilar) if c != 0]
    if len(sifirsiz) < 2:
        return math.nan
    (n1, c1), (n2, c2) = sifirsiz[-2], sifirsiz[-1]
    if c2 == 0:
        return math.inf
    # Seyrek seride ardışık sıfırsız terimler arasındaki derece farkı d>1
    # olabilir; |a_n/a_{n+d}|^(1/d) doğru ölçekleme budur.
    d = n2 - n1
    return abs(c1 / c2) ** (1.0 / d)


# --------------------------------------------------------------------------
# Kendi kendine test
# --------------------------------------------------------------------------

if __name__ == "__main__":
    print("Taylor çekirdeği — hızlı doğrulama\n" + "=" * 46)

    # 1) Katsayılar tanımdan doğru mu?
    kats = taylor_katsayilari(sp.sin(x), 0.0, 7)
    print("sin katsayıları (a_0..a_7):", [str(c) for c in kats])
    assert kats[1] == 1 and kats[3] == sp.Rational(-1, 6), "sin katsayıları hatalı"

    # 2) exp için P_N'in türevleri f'in türevleriyle x=a'da çakışıyor mu?
    #    Bu, n! bölmesinin neden zorunlu olduğunun doğrudan testidir.
    P = taylor_polinomu(sp.exp(x), 0.0, 6)
    for n in range(7):
        assert sp.diff(P, x, n).subs(x, 0) == 1, f"exp: {n}. türev uyuşmadı"
    print("exp: P_6'nın 0..6. türevleri f ile birebir uyuşuyor ✓")

    # 3) Lagrange sınırı ihlal ediliyor mu?
    nokta = np.linspace(-2.0, 2.0, 401)
    r = kalan_raporu(sp.sin(x), 0.0, 5, nokta)
    print(f"sin, a=0, N=5: aday ihlal={r.aday_sayisi}, "
          f"en kötü oran={r.en_kotu_oran:.4f}")
    assert r.aday_sayisi == 0

    # 4) Yakınsaklık yarıçapı kestirimi
    for ad in ("exp", "ln(1+x)", "1/(1+x^2)"):
        expr, a, R = KATALOG[ad]
        c = katsayi_dizisi(expr, a, 30)
        print(f"{ad:>10}: C-H R≈{cauchy_hadamard_R(c):.4f}  oran R≈{oran_testi_R(c):.4f}  teorik R={R}")

    print("\nTüm kontroller geçti.")
