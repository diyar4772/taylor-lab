"""D maddesi: C^oo (pürüzsüz) ile C^omega (analitik) aynı şey değildir.

    f(x) = e^(-1/x^2)   (x != 0),      f(0) = 0

Bu fonksiyon her mertebeden türevlenebilir ve TÜM türevleri sıfırda sıfırdır.
Dolayısıyla Maclaurin serisi

    0 + 0*x + 0*x^2 + ... = 0

yani özdeş olarak sıfır fonksiyonudur. Seri her x için yakınsar (R = sonsuz);
yakınsadığı şey sıfırdır. Oysa f, x != 0 için asla sıfır değildir.

Sonuç: Taylor serisinin yakınsaması, fonksiyona yakınsaması demek DEĞİLDİR.
Pürüzsüzlük (C^oo) analitiklikten (C^omega) kesinlikle zayıftır:

    C^omega  (gerçek) alt küme  C^oo

Neden böyle? Çünkü x=0'da f'in tüm türevleri, e^(-1/x^2)'nin sıfıra giderken
her polinomu ezmesinden ötürü sıfırlanır. Kompleks tarafta ise z -> 0 için
e^(-1/z^2), hayali eksen boyunca PATLAR: z = iy alındığında -1/z^2 = +1/y^2
olur ve e^(1/y^2) -> sonsuz. Yani z=0 gerçek bir esas tekilliktir; reel
eksende bunun hiçbir izi yoktur. C maddesindeki dersin en uç biçimi budur.

Bu betik üç şeyi sayısal olarak gösterir:
1. f'in 0'daki ilk türevlerinin (sembolik limit ile) tam olarak sıfır olduğu,
2. Maclaurin serisinin f'e değil, sıfıra yakınsadığı,
3. Kompleks düzlemde z=0'a hayali eksen boyunca yaklaşınca fonksiyonun
   patladığı -- yani reel eksende görünmeyen tekilliğin oradaki varlığı.

Çalıştırma:  python 02-python/src/analitik_degil.py
"""

from __future__ import annotations

import numpy as np
import sympy as sp

import ortam
import taylor as T

ortam.grafik_temasi()

TUREV_SAYISI = 8     # sembolik olarak sınanacak türev mertebesi
X = T.x


def f_sayisal(t: np.ndarray) -> np.ndarray:
    """f(x) = e^(-1/x^2), f(0) = 0 -- taşmaya karşı güvenli sayısal sürüm."""
    t = np.asarray(t, dtype=float)
    sonuc = np.zeros_like(t, dtype=float)
    sifirsiz = t != 0.0
    with np.errstate(over="ignore", divide="ignore", under="ignore"):
        sonuc[sifirsiz] = np.exp(-1.0 / t[sifirsiz] ** 2)
    return sonuc


def turevler_sifirda() -> list[list[str]]:
    """f^(n)(0) değerlerini SEMBOLİK limit ile hesaplar.

    Neden sayısal fark değil de limit? Çünkü sayısal türev burada tamamen
    yanıltıcıdır: f(h) ~ e^(-1/h^2) zaten h=0.1'de 1e-44 mertebesindedir,
    float64 onu sıfırdan ayırt edemez. "Sıfır çıktı" demek hiçbir şey
    kanıtlamaz. Oysa sympy limit'i, x->0 için ifadenin gerçek limitini
    cebirsel olarak bulur.
    """
    f_sembolik = sp.exp(-1 / X**2)
    satirlar = []
    turev = f_sembolik
    for n in range(TUREV_SAYISI + 1):
        if n > 0:
            turev = sp.diff(turev, X)
        limit = sp.limit(turev, X, 0)
        # Karşılaştırma: aynı türevin x=0.1'deki sayısal değeri
        sayisal = float(sp.N(turev.subs(X, sp.Rational(1, 10))))
        satirlar.append([str(n), sp.sstr(sp.simplify(limit)),
                         f"{sayisal:.3e}"])
        print(f"  f^({n})(0) = {limit}     (x=0.1'de: {sayisal:.3e})")
        assert limit == 0, f"{n}. türev sıfır çıkmadı: {limit}"
    return satirlar


def seri_ile_karsilastirma() -> None:
    """Maclaurin serisi (= 0) ile f'in kendisini yan yana çizer."""
    import matplotlib.pyplot as plt

    xs = np.linspace(-2.0, 2.0, 2000)
    ys = f_sayisal(xs)

    fig, eksenler = plt.subplots(1, 2, figsize=(14, 5.5))

    ax = eksenler[0]
    ax.plot(xs, ys, color=ortam.PALET["fonksiyon"], lw=2.4,
            label=r"$f(x)=e^{-1/x^2}$")
    ax.plot(xs, np.zeros_like(xs), color=ortam.PALET["hata"], lw=2.0, ls="--",
            label="Maclaurin serisi $\\equiv 0$")
    ax.plot([0], [0], "o", color=ortam.PALET["vurgu"], ms=7)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_title("Seri her yerde yakınsıyor — ama f'e değil, sıfıra")
    ax.legend()

    # Sağ: x->0 yakınlaştırması, log ölçekte. f sıfıra DÜZ gitmiyor;
    # her polinomdan hızlı gidiyor.
    ax = eksenler[1]
    xz = np.linspace(1e-3, 0.8, 4000)
    ax.semilogy(xz, np.maximum(f_sayisal(xz), 1e-320),
                color=ortam.PALET["fonksiyon"], lw=2.2, label=r"$e^{-1/x^2}$")
    for k, renk in zip((2, 6, 12), ortam.SERI_RENKLERI):
        ax.semilogy(xz, xz**k, ls=":", lw=1.5, color=renk, label=f"$x^{{{k}}}$")
    ax.set_ylim(1e-40, 5)
    ax.set_xlabel("x")
    ax.set_ylabel("y  (log ölçek)")
    ax.set_title("Sıfıra gidiş her $x^k$'dan hızlı\n"
                 "bu yüzden her mertebeden türev 0'da sıfırlanır")
    ax.legend(fontsize=9)

    fig.suptitle(r"$C^\infty \supsetneq C^\omega$ : pürüzsüz ama analitik değil",
                 fontsize=14, color=ortam.PALET["fonksiyon"])
    fig.tight_layout()
    yol = ortam.gorsel_yolu("analitik_degil.png")
    fig.savefig(yol)
    plt.close(fig)
    print(f"  yazıldı: {yol.relative_to(ortam.PROJE_KOK)}")


def kompleks_tekillik() -> list[list[str]]:
    """z=0'a farklı yönlerden yaklaşınca e^(-1/z^2) ne yapıyor?

    Reel eksen boyunca (z = x):     -1/x^2 < 0  =>  e^(negatif) -> 0
    Hayali eksen boyunca (z = iy):  -1/(iy)^2 = +1/y^2  =>  e^(pozitif) -> oo

    Aynı noktaya iki yönden yaklaşıp biri 0 diğeri sonsuz veriyorsa, orada
    limit yoktur: z=0 bir ESAS TEKİLLİKTİR. Reel eksende bunun hiçbir izi
    görünmez -- fonksiyon orada uslu uslu sıfıra gider.
    """
    satirlar = []
    for y in (0.5, 0.3, 0.2, 0.1, 0.05):
        reel = float(np.exp(-1.0 / y**2))
        # z = iy  =>  -1/z^2 = 1/y^2
        us = 1.0 / y**2
        hayali = float(np.exp(us)) if us < 700 else float("inf")
        satirlar.append([f"{y:g}", f"{reel:.3e}",
                         "taşma (>1e308)" if not np.isfinite(hayali) else f"{hayali:.3e}"])
        print(f"  |z|={y:<5g}  reel eksende: {reel:.3e}     "
              f"hayali eksende: {'taşma' if not np.isfinite(hayali) else f'{hayali:.3e}'}")
    return satirlar


def main() -> int:
    ortam.baslik_yaz("1. Sıfırdaki türevler (sembolik limit)")
    print("  Sayısal türev burada kanıt değildir: f(0.1) zaten 1e-44'tür,\n"
          "  float64 onu sıfırdan ayıramaz. Bu yüzden sympy.limit kullanılıyor.\n")
    turev_satirlari = turevler_sifirda()
    print(f"\n  {TUREV_SAYISI + 1} türevin tamamı sıfır ⇒ Maclaurin serisi ≡ 0")

    ortam.baslik_yaz("2. Seri ile fonksiyonun karşılaştırılması")
    seri_ile_karsilastirma()

    ortam.baslik_yaz("3. Reel eksende görünmeyen tekillik")
    print("  Aynı |z| için iki yön:\n")
    kompleks_satirlari = kompleks_tekillik()

    icerik = (
        "## Türevler\n\n"
        "`f^(n)(0)` değerleri **sembolik limit** ile hesaplandı "
        "(`sympy.limit`). Sayısal türev burada kanıt olarak kabul edilemez: "
        "`f(0.1) = e^(-100) ≈ 3.7e-44` zaten float64'ün fark edemeyeceği "
        "kadar küçüktür, \"sıfır çıktı\" demek hiçbir şey göstermez.\n\n"
        + ortam.markdown_tablo(
            ["n", "f⁽ⁿ⁾(0)  (limit)", "aynı türevin x=0.1'deki değeri"],
            turev_satirlari)
        + "\n\nSağ sütun işin püf noktasını gösterir: türevler x=0.1'de "
          "devasa sayılara ulaşır (n büyüdükçe `1/x^(3n)` mertebesinde "
          "çarpanlar doğar), ama `e^(-1/x²)` çarpanı bunların hepsini ezer. "
          "Üstel sıfıra gidiş, her polinom patlamasından güçlüdür.\n\n"
        "## Sonuç\n\n"
        "Bütün türevler sıfır olduğu için Maclaurin serisi\n\n"
        "```\n0 + 0·x + 0·x² + 0·x³ + … = 0\n```\n\n"
        "olur. Bu seri **her x için yakınsar** — yakınsaklık yarıçapı "
        "sonsuzdur. Yakınsadığı şey sıfır fonksiyonudur. Oysa `f(x) ≠ 0` "
        "her `x ≠ 0` için. Yani:\n\n"
        "> Bir Taylor serisinin yakınsaması, onu üreten fonksiyona "
        "yakınsaması anlamına gelmez.\n\n"
        "Bu, `C^ω ⊊ C^∞` içermesinin somut tanığıdır: f sonsuz kez "
        "türevlenebilir (C^∞) ama hiçbir 0 komşuluğunda kendi Taylor "
        "serisiyle temsil edilemez (C^ω değil).\n\n"
        "## Sebep kompleks düzlemdedir\n\n"
        "Reel eksende f uslu uslu sıfıra gider; hiçbir şey olmuyor gibidir. "
        "Ama `z = iy` alırsak `-1/z² = +1/y²` olur ve `e^(1/y²) → ∞`. "
        "Aynı `z=0` noktasına iki yönden yaklaşıp biri 0, diğeri sonsuz "
        "veriyorsa orada limit yoktur — `z=0` bir **esas tekilliktir**.\n\n"
        + ortam.markdown_tablo(
            ["|z|", "reel eksen boyunca: e^(−1/x²)", "hayali eksen boyunca: e^(+1/y²)"],
            kompleks_satirlari)
        + "\n\nBu, `kompleks_yaricap.md` dosyasındaki dersin en uç hâlidir: "
          "reel eksende hiçbir kusuru olmayan bir fonksiyonun Taylor "
          "davranışını belirleyen şey, kompleks düzlemde olup bitenlerdir. "
          "`1/(1+x²)`'de bu bir kutuptu ve yarıçapı 1'e düşürüyordu; burada "
          "esas tekilliktir ve seriyi tamamen işe yaramaz kılar."
    )
    ortam.tablo_yaz("analitik_degil.md",
                    "Pürüzsüz ama analitik değil: e^(−1/x²)", icerik)
    print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
