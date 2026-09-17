"""F maddesi: kuantizasyon, serinin KESİLME şartından doğar.

Bir diferansiyel denklemi kuvvet serisiyle çözmek (Frobenius yöntemi)
katsayılar için bir rekürans bağıntısı verir. Rekürans, bir a_0 (ve a_1)
seçildiğinde bütün seriyi belirler. Denklem hiçbir şeyi yasaklamaz: lambda
parametresi NE OLURSA OLSUN bir seri çözüm vardır.

Sorun şudur: o seri çözümün fiziksel olarak kabul edilebilir olması gerekir.

* Legendre denklemi (1-x^2)y'' - 2xy' + lambda*y = 0, [-1,1] aralığında
  kurulur (x = cos(theta)). Rekürans

      a_{n+2} / a_n = [n(n+1) - lambda] / [(n+1)(n+2)]

  Büyük n icin bu oran -> 1'dir; yani katsayılar sonunda 1/n gibi davranır ve
  seri x = +-1'de IRAKSAR. Tek istisna: pay bir yerde sıfırlanırsa seri
  KESİLİR ve polinom olur. Pay n(n+1) - lambda = 0 demek, lambda = l(l+1)
  demektir (l tam sayı).

* Hermite denklemi y'' - 2xy' + 2*lambda*y = 0, tüm eksende kurulur.
  Rekürans a_{n+2}/a_n = 2(n - lambda) / [(n+1)(n+2)]. Kesilmezse seri
  e^(x^2) gibi büyür ve e^(-x^2/2) ile çarpıldığında bile normalize
  edilemez. Kesilme şartı: lambda = n (tam sayı).

Yani tam sayılar denklemden değil, ÇÖZÜMÜN SONLU KALMASI ŞARTINDAN gelir.
Kuantum mekaniğindeki "kuantum sayıları" tam olarak bu kesilme indeksleridir.
Doğa tam sayıları seçmez; seri başka seçenek bırakmaz.

Çalıştırma:  python 02-python/src/frobenius.py
"""

from __future__ import annotations

import numpy as np
import sympy as sp

import ortam

ortam.grafik_temasi()

N_TERIM = 400     # seriyi kaç terime kadar toplayalım


# --------------------------------------------------------------------------
# Rekürans bağıntıları
# --------------------------------------------------------------------------

def legendre_katsayilari(lam: float, a0: float, a1: float, n_terim: int) -> np.ndarray:
    """(1-x²)y'' − 2xy' + λy = 0  için a_0..a_{n_terim} katsayıları.

    Rekürans:  a_{n+2} = [n(n+1) − λ] / [(n+1)(n+2)] · a_n

    Çift ve tek indisler birbirinden bağımsız iki seri oluşturur; a_0 çift
    seriyi, a_1 tek seriyi başlatır.
    """
    a = np.zeros(n_terim + 3)
    a[0], a[1] = a0, a1
    for n in range(n_terim + 1):
        a[n + 2] = (n * (n + 1) - lam) / ((n + 1) * (n + 2)) * a[n]
    return a[:n_terim + 1]


def hermite_katsayilari(lam: float, a0: float, a1: float, n_terim: int) -> np.ndarray:
    """y'' − 2xy' + 2λy = 0  için katsayılar.

    Rekürans:  a_{n+2} = 2(n − λ) / [(n+1)(n+2)] · a_n
    """
    a = np.zeros(n_terim + 3)
    a[0], a[1] = a0, a1
    for n in range(n_terim + 1):
        a[n + 2] = 2.0 * (n - lam) / ((n + 1) * (n + 2)) * a[n]
    return a[:n_terim + 1]


def seri_degeri(katsayilar: np.ndarray, xs: np.ndarray) -> np.ndarray:
    """Seriyi Horner ile değerlendirir (yüksek dereceler için kararlı)."""
    sonuc = np.zeros_like(xs, dtype=float)
    for c in katsayilar[::-1]:
        sonuc = sonuc * xs + c
    return sonuc


def kesilme_derecesi(lam: float, aile: str, parite: int) -> int | None:
    """Seri KESİLİYOR mu? Rekürans payının sıfırlanma şartından belirler.

    Bunu katsayılara sayısal eşik uygulayarak tespit etmek YANLIŞTIR ve bu
    betiğin ilk sürümünde tam da o hata vardı: λ = 2.5 için Hermite serisi
    kesilmez, ama katsayıları `a_n ~ 2^(n/2)/(n/2)!` gibi hızla küçüldüğü
    için n ≈ 28'den sonra 1e-14'ün altına iner ve "kesilmiş" görünür.
    Oysa o katsayılar sıfır değildir; e^(x²)'nin katsayıları da aynı şekilde
    küçülür ve o fonksiyon kesinlikle patlar.

    Doğru ölçüt cebirseldir:

    * Legendre, a_{n+2} ∝ [n(n+1) − λ]:  λ = l(l+1) ve l, başlangıç
      paritesiyle aynı pariteye sahipse l. derecede kesilir.
    * Hermite, a_{n+2} ∝ (n − λ):  λ negatif olmayan bir tam sayı ve
      pariteler uyuşuyorsa λ. derecede kesilir.

    ``parite``: seriyi başlatan katsayının indeksi (a_0 için 0, a_1 için 1).
    """
    if aile == "legendre":
        # l(l+1) = λ  →  l = (-1 + sqrt(1+4λ))/2
        if lam < 0:
            return None
        l = (-1.0 + np.sqrt(1.0 + 4.0 * lam)) / 2.0
        l_yuvarlak = round(l)
        if abs(l - l_yuvarlak) > 1e-12 or l_yuvarlak < 0:
            return None
        return int(l_yuvarlak) if l_yuvarlak % 2 == parite else None

    if aile == "hermite":
        if lam < 0 or abs(lam - round(lam)) > 1e-12:
            return None
        n = int(round(lam))
        return n if n % 2 == parite else None

    raise ValueError(f"bilinmeyen aile: {aile}")


def kesilme_dogrula(katsayilar: np.ndarray, derece: int | None) -> bool:
    """Cebirsel kesilme iddiasını katsayılarla sınar: sonrası TAM sıfır mı?"""
    if derece is None:
        return True
    kuyruk = katsayilar[derece + 1:]
    return bool(np.all(kuyruk == 0.0))


# --------------------------------------------------------------------------
# 1. Legendre: uç noktada ıraksama
# --------------------------------------------------------------------------

def legendre_incelemesi() -> list[list[str]]:
    """λ tam sayı l(l+1) iken polinom, değilken x=±1'de ıraksama."""
    satirlar = []
    # Çift seriyi (a0=1, a1=0) izleyeceğiz; l çift iken kesilmeli.
    for l_veya_lam, etiket in [(0, "λ = 0·1 = 0"), (2, "λ = 2·3 = 6"),
                               (4, "λ = 4·5 = 20"), (None, "λ = 5.5  (tam sayı değil)"),
                               (None, "λ = 7.3  (tam sayı değil)")]:
        if l_veya_lam is not None:
            lam = float(l_veya_lam * (l_veya_lam + 1))
        else:
            lam = 5.5 if "5.5" in etiket else 7.3

        a = legendre_katsayilari(lam, 1.0, 0.0, N_TERIM)
        kes = kesilme_derecesi(lam, "legendre", parite=0)
        assert kesilme_dogrula(a, kes), f"λ={lam}: kesilme iddiası katsayılarla tutmuyor"

        # x = 1'de seri = katsayıların toplamı. Kesilmiyorsa bu toplam
        # ıraksar; ıraksamayı N_TERIM'de kesilmiş kısmi toplamın hâlâ
        # BÜYÜYOR olmasından anlarız.
        kismi = np.cumsum(a)
        y_1 = float(kismi[-1])
        y_999 = float(seri_degeri(a, np.array([0.999]))[0])
        # Son çeyrekte kısmi toplam ne kadar arttı? Kesilen seride 0, ıraksayanda değil.
        artis = float(abs(kismi[-1] - kismi[3 * len(kismi) // 4]))

        satirlar.append([
            etiket,
            f"evet, derece {kes}" if kes is not None else "HAYIR",
            f"{y_999:.4f}",
            f"{y_1:.4f}",
            f"{artis:.3e}",
        ])
        print(f"  {etiket:<28} kesiliyor mu: "
              f"{(f'evet (derece {kes})') if kes is not None else 'HAYIR':<18} "
              f"y(0.999)={y_999:>10.4f}   y(1)={y_1:>10.4f}   "
              f"son çeyrekte artış={artis:.2e}")
    return satirlar


def legendre_grafigi() -> None:
    import matplotlib.pyplot as plt

    xs = np.linspace(-1.0, 1.0, 2000)
    fig, eksenler = plt.subplots(1, 2, figsize=(14, 5.5))

    ax = eksenler[0]
    for i, l in enumerate((0, 2, 4, 6)):
        lam = float(l * (l + 1))
        a = legendre_katsayilari(lam, 1.0, 0.0, N_TERIM)
        ax.plot(xs, seri_degeri(a, xs), lw=2.0,
                color=ortam.SERI_RENKLERI[i % len(ortam.SERI_RENKLERI)],
                label=f"λ = {l}·{l+1} = {lam:.0f}   (derece {l})")
    ax.set_ylim(-1.5, 1.5)
    ax.set_xlabel("x")
    ax.set_ylabel("y(x)")
    ax.set_title("λ = l(l+1):  seri KESİLİYOR → Legendre polinomu\n"
                 "x=±1'de sonlu")
    ax.legend(fontsize=8)

    ax = eksenler[1]
    for i, lam in enumerate((1.0, 3.7, 5.5, 7.3)):
        a = legendre_katsayilari(lam, 1.0, 0.0, N_TERIM)
        ax.plot(xs, seri_degeri(a, xs), lw=2.0,
                color=ortam.SERI_RENKLERI[i % len(ortam.SERI_RENKLERI)],
                label=f"λ = {lam}")
    for kenar in (-1.0, 1.0):
        ax.axvline(kenar, color=ortam.PALET["tekillik"], ls="--", lw=1.4)
    ax.set_ylim(-8, 8)
    ax.set_xlabel("x")
    ax.set_ylabel("y(x)")
    ax.set_title("λ ≠ l(l+1):  seri kesilmiyor → x=±1'de IRAKSIYOR\n"
                 "denklem çözülüyor ama çözüm fiziksel değil")
    ax.legend(fontsize=8)

    fig.suptitle("Legendre: kuantizasyon, kesilme şartından doğuyor",
                 fontsize=14, color=ortam.PALET["fonksiyon"])
    fig.tight_layout()
    yol = ortam.gorsel_yolu("frobenius_legendre.png")
    fig.savefig(yol)
    plt.close(fig)
    print(f"  yazıldı: {yol.relative_to(ortam.PROJE_KOK)}")


# --------------------------------------------------------------------------
# 2. Hermite: sonsuzda patlama
# --------------------------------------------------------------------------

def hermite_incelemesi() -> list[list[str]]:
    """λ tam sayı iken polinom; değilken çözüm e^(x²) gibi büyür.

    Kuantum harmonik osilatörde dalga fonksiyonu psi = H(x)·e^(-x²/2)'dir.
    H seri olarak kalırsa e^(x²) gibi büyür ve psi ~ e^(+x²/2) olur -- yani
    normalize EDİLEMEZ. Kesilme şartı burada doğrudan "parçacık uzayda
    kaybolmasın" demektir.
    """
    satirlar = []
    xs_test = np.array([4.0])

    def norm_integrali(a: np.ndarray, L: float) -> float:
        """∫_{-L}^{L} |ψ|² dx, ψ = H(x)·e^(-x²/2) (yamuk kuralı, 8001 nokta)."""
        xs = np.linspace(-L, L, 8001)
        psi = seri_degeri(a, xs) * np.exp(-xs**2 / 2)
        return float(np.trapezoid(psi**2, xs))

    for lam in (0.0, 1.0, 2.0, 3.0, 2.5, 3.7):
        # Pariteyi λ'ya uydur: tam sayı λ için kesilme ancak eşleşen parite
        # zincirinde olur. Tam sayı olmayan λ'da parite fark etmez, a_0 ile
        # başlatılır.
        parite = int(round(lam)) % 2 if abs(lam - round(lam)) < 1e-12 else 0
        a0, a1 = (1.0, 0.0) if parite == 0 else (0.0, 1.0)
        a = hermite_katsayilari(lam, a0, a1, N_TERIM)
        kes = kesilme_derecesi(lam, "hermite", parite)
        assert kesilme_dogrula(a, kes), f"λ={lam}: kesilme iddiası tutmuyor"
        H = float(seri_degeri(a, xs_test)[0])
        psi = H * float(np.exp(-xs_test[0] ** 2 / 2))
        # Normalizasyon ölçütü tek noktaya değil integrale bakar: ψ gerçekten
        # sönüyorsa ∫|ψ|² pencere büyüdükçe sabitlenir (oran ≈ 1); ψ ~ e^(+x²/2)
        # ise ∫|ψ|² ~ e^(L²) gibi büyür ve oran patlar.
        n4, n6 = norm_integrali(a, 4.0), norm_integrali(a, 6.0)
        oran = n6 / n4
        normalize = oran < 1.01
        satirlar.append([
            f"{lam:g}",
            f"evet, derece {kes}" if kes is not None else "HAYIR",
            f"{H:.4e}",
            f"{psi:.4e}",
            f"{oran:.6f}" if oran < 1e3 else f"{oran:.3e}",
            "normalize edilebilir" if normalize else "PATLIYOR",
        ])
        print(f"  λ={lam:<5g} kesiliyor mu: "
              f"{(f'evet (derece {kes})') if kes is not None else 'HAYIR':<18} "
              f"H(4)={H:>12.4e}   ψ(4)={psi:>12.4e}   "
              f"∫|ψ|²(L=6)/∫|ψ|²(L=4)={oran:>12.6e}   "
              f"{'OK' if normalize else 'PATLIYOR'}")
    return satirlar


def hermite_grafigi() -> None:
    import matplotlib.pyplot as plt

    xs = np.linspace(-4.0, 4.0, 2000)
    zarf = np.exp(-xs**2 / 2)

    fig, eksenler = plt.subplots(1, 2, figsize=(14, 5.5))

    ax = eksenler[0]
    for i, n in enumerate((0, 1, 2, 3)):
        a0, a1 = (1.0, 0.0) if n % 2 == 0 else (0.0, 1.0)
        a = hermite_katsayilari(float(n), a0, a1, N_TERIM)
        psi = seri_degeri(a, xs) * zarf
        psi = psi / np.max(np.abs(psi))
        ax.plot(xs, psi + i * 2.2, lw=2.0,
                color=ortam.SERI_RENKLERI[i % len(ortam.SERI_RENKLERI)],
                label=f"λ = n = {n}")
        ax.axhline(i * 2.2, color=ortam.PALET["soluk"], lw=0.6, ls=":")
    ax.set_xlabel("x")
    ax.set_ylabel(r"$\psi = H(x)\,e^{-x^2/2}$  (kaydırılmış)")
    ax.set_title("λ tam sayı: H kesiliyor, ψ sonsuzda sönüyor\n"
                 "kuantum harmonik osilatörün özdurumları")
    ax.legend(fontsize=8)

    ax = eksenler[1]
    for i, lam in enumerate((2.0, 2.3, 2.5, 2.8)):
        a = hermite_katsayilari(lam, 1.0, 0.0, N_TERIM)
        psi = seri_degeri(a, xs) * zarf
        ax.semilogy(xs, np.maximum(np.abs(psi), 1e-8), lw=2.0,
                    color=ortam.SERI_RENKLERI[i % len(ortam.SERI_RENKLERI)],
                    label=f"λ = {lam}" + ("  (tam sayı)" if lam == round(lam) else ""))
    ax.set_xlabel("x")
    ax.set_ylabel(r"$|\psi|$  (log ölçek)")
    ax.set_title("λ tam sayı değilse: H ~ e^(x²) ve ψ ~ e^(+x²/2)\n"
                 "normalize edilemez → fiziksel değil")
    ax.legend(fontsize=8)

    fig.suptitle("Hermite: 'kuantum sayısı' bir kesilme indeksidir",
                 fontsize=14, color=ortam.PALET["fonksiyon"])
    fig.tight_layout()
    yol = ortam.gorsel_yolu("frobenius_hermite.png")
    fig.savefig(yol)
    plt.close(fig)
    print(f"  yazıldı: {yol.relative_to(ortam.PROJE_KOK)}")


# --------------------------------------------------------------------------
# 3. Sembolik doğrulama: bulduğumuz polinomlar gerçekten denklemi sağlıyor mu?
# --------------------------------------------------------------------------

def sembolik_dogrulama() -> list[list[str]]:
    """Kesilen serilerin denklemi SAĞLADIĞINI sympy ile doğrular.

    Rekürans doğru türetilmediyse ortaya çıkan polinom denklemi sağlamaz.
    Bu yüzden kalıntıyı (denklemin sol tarafını) sembolik olarak sıfıra
    indirgemek, bütün sayısal işin üzerine konan bir güvencedir.
    """
    x = sp.Symbol("x")
    satirlar = []

    def kesin_katsayilar(lam: int, aile: str, parite: int, derece: int) -> list[sp.Rational]:
        """Rekürransı TAM kesirli aritmetikle yürütür.

        float ile hesaplayıp sonra rasyonelleştirmek burada işe yaramaz:
        Legendre l=3 için a_3 = -5/3'tür ve bu bir ikilik kesir değildir.
        float64'ten üretilen en yakın rasyonel, denklemde `-x/536870912`
        mertebesinde bir kalıntı bırakır -- yani "sıfır çıktı" diyemeyiz.
        Doğrulamanın anlamlı olması için katsayılar baştan kesin olmalı.
        """
        a = [sp.Integer(0)] * (derece + 3)
        a[parite] = sp.Integer(1)
        for n in range(derece + 1):
            if aile == "legendre":
                pay = sp.Integer(n * (n + 1) - lam)
            else:
                pay = sp.Integer(2 * (n - lam))
            a[n + 2] = pay / sp.Integer((n + 1) * (n + 2)) * a[n]
        return a[:derece + 1]

    for l in range(5):
        lam = l * (l + 1)
        a = kesin_katsayilar(lam, "legendre", parite=l % 2, derece=l)
        y = sum(c * x**n for n, c in enumerate(a))
        kalinti = sp.simplify(
            (1 - x**2) * sp.diff(y, x, 2) - 2 * x * sp.diff(y, x) + lam * y)
        tamam = kalinti == 0
        satirlar.append(["Legendre", f"l={l}, λ={lam}", sp.sstr(sp.expand(y)),
                         "0 ✓" if tamam else sp.sstr(kalinti)])
        print(f"  Legendre l={l} (λ={lam:>2}): y = {sp.expand(y)}"
              f"      kalıntı: {kalinti}")
        assert tamam, f"Legendre l={l} denklemi sağlamıyor: {kalinti}"

    for n in range(5):
        a = kesin_katsayilar(n, "hermite", parite=n % 2, derece=n)
        y = sum(c * x**k for k, c in enumerate(a))
        kalinti = sp.simplify(sp.diff(y, x, 2) - 2 * x * sp.diff(y, x) + 2 * n * y)
        tamam = kalinti == 0
        satirlar.append(["Hermite", f"n={n}, λ={n}", sp.sstr(sp.expand(y)),
                         "0 ✓" if tamam else sp.sstr(kalinti)])
        print(f"  Hermite  n={n}: y = {sp.expand(y)}"
              f"      kalıntı: {kalinti}")
        assert tamam, f"Hermite n={n} denklemi sağlamıyor: {kalinti}"

    return satirlar


# --------------------------------------------------------------------------

def main() -> int:
    ortam.baslik_yaz("1. Legendre: λ ne olursa olsun seri çözüm VAR")
    print("  (1−x²)y'' − 2xy' + λy = 0,   a_{n+2} = [n(n+1)−λ]/[(n+1)(n+2)]·a_n\n")
    legendre_satirlari = legendre_incelemesi()
    legendre_grafigi()

    ortam.baslik_yaz("2. Hermite: kesilmezse dalga fonksiyonu patlar")
    print("  y'' − 2xy' + 2λy = 0,   a_{n+2} = 2(n−λ)/[(n+1)(n+2)]·a_n")
    print("  ψ = H(x)·e^(−x²/2);  x=4'te test ediliyor\n")
    hermite_satirlari = hermite_incelemesi()
    hermite_grafigi()

    ortam.baslik_yaz("3. Sembolik doğrulama: polinomlar denklemi sağlıyor mu?")
    dogrulama_satirlari = sembolik_dogrulama()
    print("\n  Tüm kalıntılar tam olarak 0 — rekürans doğru türetilmiş.")

    icerik = (
        "## Legendre denklemi\n\n"
        "```\n(1−x²)y'' − 2xy' + λy = 0      a_{n+2} = [n(n+1) − λ] / [(n+1)(n+2)] · a_n\n```\n\n"
        "Denklem λ üzerinde **hiçbir kısıt koymaz**: her λ için rekürans "
        "çalışır ve bir seri çözüm üretir. Kısıt, çözümün `x = ±1`'de "
        "(yani kutuplarda, çünkü `x = cos θ`) sonlu kalması gerektiğinden "
        "gelir.\n\n"
        + ortam.markdown_tablo(
            ["λ", "seri kesiliyor mu?", "y(0.999)", "y(1)", "kısmi toplam büyümesi"],
            legendre_satirlari)
        + "\n\nBüyük n için `a_{n+2}/a_n → 1` olur; yani katsayılar sonunda "
          "sabit orana yaklaşır ve `x = 1`'de seri ıraksar.\n\n"
          "**Dürüst bir uyarı:** bu ıraksama hızlı değildir. Harmonik seri "
          "gibi *logaritmiktir*, bu yüzden 400 terimde bile `y(1)` sonlu bir "
          "sayı gibi görünür — tabloda λ=5.5 için −2.37 yazıyor. Iraksamanın "
          "kanıtı o sütun değil, **`son çeyrekte artış`** sütunudur: kesilen "
          "serilerde tam olarak `0.00e+00`, kesilmeyenlerde sıfırdan "
          "farklıdır ve hiç durmaz. Sayısal bir deney ıraksamayı \"gösteremez\", "
          "yalnızca hiç durmadığını gösterebilir; ıraksadığını söyleyen "
          "cebirdir.\n\n"
          "Ayrıca dikkat: kesilme kararı bu betikte katsayılara eşik "
          "uygulanarak **verilmez**. Öyle yapmak yanlış sonuç verir — λ=2.5 "
          "için Hermite katsayıları da hızla küçülür (tıpkı `e^(x²)`'nin "
          "katsayıları gibi) ve eşik yöntemi seriyi \"kesilmiş\" sanır. "
          "Karar rekürans payının cebirsel olarak sıfırlanmasından okunur, "
          "sonra katsayıların gerçekten tam sıfır olduğu ayrıca sınanır.\n\n"
          "Iraksamadan kaçmanın **tek** yolu payın sıfırlanmasıdır:\n\n"
          "```\nn(n+1) − λ = 0   ⟺   λ = l(l+1),  l ∈ ℕ\n```\n\n"
          "Tam sayı buradan çıkar. Kimse dayatmadı; seri başka seçenek "
          "bırakmadı.\n\n"
        "## Hermite denklemi\n\n"
        "```\ny'' − 2xy' + 2λy = 0      a_{n+2} = 2(n − λ) / [(n+1)(n+2)] · a_n\n```\n\n"
        "Kuantum harmonik osilatörde dalga fonksiyonu `ψ = H(x)·e^(−x²/2)`. "
        "H seri olarak kalırsa büyük x'te `e^(x²)` gibi büyür ve "
        "`ψ ~ e^(+x²/2)` olur — normalize edilemez, yani parçacığın bulunma "
        "olasılığı sonsuza gider. Tablo `x=4`'teki değerleri ve karar ölçütünü "
        "verir. Karar tek bir noktaya değil, normalizasyon integraline "
        "dayanır: `∫|ψ|² dx` önce `[−4, 4]`, sonra `[−6, 6]` üzerinde "
        "hesaplanır. ψ gerçekten sönüyorsa pencereyi büyütmek integrali "
        "değiştirmez (oran ≈ 1); ψ ~ e^(+x²/2) ise integral e^(L²) gibi "
        "büyür. Eşik: oran < 1.01.\n\n"
        + ortam.markdown_tablo(
            ["λ", "seri kesiliyor mu?", "H(4)", "ψ(4) = H(4)·e⁻⁸",
             "∫ψ² oranı (L=6 / L=4)", "durum"],
            hermite_satirlari)
        + "\n\nKesilme şartı `λ = n`. Kuantum mekaniği dersinde "
          "`E_n = ℏω(n + ½)` diye ezberlenen formüldeki `n`, **bu rekürans "
          "hangi indekste sıfırlandıysa odur**. Enerji kuantumlanmış, çünkü "
          "seri ancak tam sayılarda kesiliyor.\n\n"
        "## Sembolik doğrulama\n\n"
        "Rekürans elle türetildiği için sonuçlar sympy ile sınandı: her "
        "kesilen seri ilgili diferansiyel denkleme konuldu ve kalıntının "
        "**tam olarak sıfır** olduğu doğrulandı.\n\n"
        + ortam.markdown_tablo(
            ["denklem", "parametre", "bulunan polinom", "denklemdeki kalıntı"],
            dogrulama_satirlari)
        + "\n\n## Taylor ile bağı\n\n"
          "Bu bölüm laboratuvarın geri kalanının tersini yapar. Diğer "
          "betiklerde bilinen bir fonksiyonun serisi çıkarılıyordu; burada "
          "**seri önce geliyor**, fonksiyon ondan doğuyor. Legendre ve "
          "Hermite polinomları \"keşfedilmiş\" nesneler değil, bir rekürans "
          "bağıntısının sonlu kalmaya zorlandığında geriye bıraktığı "
          "kalıntılardır.\n\n"
          "Ve kritik nokta: **kuantizasyon fizikten değil, yakınsaklıktan "
          "gelir.** Fiziğin koyduğu tek şart \"çözüm sonlu olsun\"dur; "
          "gerisini seri halleder."
    )
    ortam.tablo_yaz("frobenius.md",
                    "Frobenius serileri ve kuantizasyonun doğuşu", icerik)
    print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
