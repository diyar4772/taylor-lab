"""C maddesi: yakınsaklık yarıçapı reel eksende değil, KOMPLEKS DÜZLEMDE yaşar.

Reel eksende bakıldığında 1/(1+x²) kusursuzdur: her yerde tanımlı, her yerde
sonsuz kez türevlenebilir, hiçbir yerde patlamaz. Buna rağmen 0 merkezli
Maclaurin serisi yalnızca |x| < 1 için yakınsar. Reel eksende bu sonucun
sebebini gösteren HİÇBİR ŞEY yoktur.

Sebep bir boyut yukarıdadır: fonksiyonun z = ±i noktalarında kutupları vardır
ve bu noktalar orijine tam olarak 1 uzaklıktadır. Kuvvet serisi, merkez
etrafındaki en büyük "temiz" diskten daha ileri gidemez — çünkü bir kuvvet
serisinin yakınsadığı bölge her zaman bir DİSKTİR, ve o disk ilk tekilliğe
çarptığı anda durmak zorundadır.

    R = |a - (a'ya en yakın tekillik)|

Bu betik bunu iddia etmez, GÖSTERİR: kompleks düzlemde (1/N)·log|f(z)-P_N(z)|
haritası çizilir. Bu büyüklük log(|z-a|/R)'ye yakınsadığı için haritanın
işareti doğrudan yakınsaklığı söyler ve sıfır düzeyi kendiliğinden bir
ÇEMBER olur -- kimse çizmeden.

Çalıştırma:  python 02-python/src/kompleks_harita.py
"""

from __future__ import annotations

import numpy as np
import sympy as sp

import ortam
import taylor as T

ortam.grafik_temasi()

# --------------------------------------------------------------------------
# Haritalanacak durumlar
#
# Son iki satır kritik: AYNI fonksiyon, FARKLI merkez. Yarıçap değişiyor,
# çünkü merkezin tekilliklere uzaklığı değişiyor. Yarıçap fonksiyonun değil,
# (fonksiyon, merkez) çiftinin özelliğidir.
# --------------------------------------------------------------------------

DURUMLAR = [
    # (başlık, sympy ifadesi, merkez a, tekillikler, teorik R, pencere yarıçapı)
    (r"$1/(1+z^2)$,  $a=0$",   1 / (1 + T.x**2),  0.0,  [1j, -1j],      1.0,          2.2),
    (r"$1/(1-z)$,  $a=0$",     1 / (1 - T.x),     0.0,  [1 + 0j],       1.0,          2.2),
    (r"$\ln(1+z)$,  $a=0$",    sp.log(1 + T.x),   0.0,  [-1 + 0j],      1.0,          2.2),
    (r"$e^z$,  $a=0$  (tekillik yok)", sp.exp(T.x), 0.0, [],            np.inf,       2.2),
    (r"$1/(1+z^2)$,  $a=1$",   1 / (1 + T.x**2),  1.0,  [1j, -1j],      np.sqrt(2.0), 2.6),
    (r"$1/(1-z)$,  $a=-1$",    1 / (1 - T.x),     -1.0, [1 + 0j],       2.0,          3.0),
]

N_DERECE = 28        # büyük N: içeride/dışarıda kontrast uçurum olur
IZGARA = 600         # piksel


# --------------------------------------------------------------------------

def hata_haritasi(expr: sp.Expr, a: float, N: int, yaricap: float, izgara: int):
    """Kompleks düzlemde (1/N)·log10|f(z) - P_N(z)| haritasını üretir.

    Merkez a etrafında [a-yaricap, a+yaricap] × [-yaricap, yaricap] penceresi
    taranır. P_N burada reel katsayılarla ama KOMPLEKS argümanla değerlendirilir
    -- katsayılar f'in a'daki reel türevlerinden gelir, değişen tek şey nereye
    baktığımızdır.

    Neden ham log|hata| değil de N'e BÖLÜNMÜŞ hali? Çünkü kuyruk

        |f(z) - P_N(z)| ~ C · (|z-a| / R)^(N+1)

    gibi davranır. Logaritmasını alıp N'e bölersek

        (1/N)·log10|hata|  ->  log10(|z-a| / R)

    kalır. Bu büyüklüğün üç güzel özelliği var:

    * İşareti doğrudan yakınsaklığı söyler: |z-a| < R iken NEGATİF,
      |z-a| > R iken POZİTİF. Sıfır düzeyi tam olarak |z-a| = R çemberidir.
    * N'den (neredeyse) bağımsızdır; N'i artırmak sınırı keskinleştirir,
      yerini değiştirmez.
    * Ham log|hata| haritasında geçiş yumuşak bir gradyandır ve diski göz
      kararı yerleştirmek gerekir; burada sınır kendiliğinden çizgi olur.
    """
    re = np.linspace(a - yaricap, a + yaricap, izgara)
    im = np.linspace(-yaricap, yaricap, izgara)
    RE, IM = np.meshgrid(re, im)
    Z = RE + 1j * IM

    f = sp.lambdify(T.x, expr, "numpy")
    katsayilar = T.katsayi_dizisi(expr, a, N)

    with np.errstate(over="ignore", invalid="ignore", divide="ignore"):
        F = np.asarray(f(Z), dtype=complex)
        P = np.zeros_like(Z, dtype=complex)
        guc = np.ones_like(Z, dtype=complex)
        for c in katsayilar:
            P = P + c * guc
            guc = guc * (Z - a)
        hata = np.abs(F - P)

    # Tam sıfır (kusursuz sadeleşme) log'da -inf verir. Bunu "çok büyük"e
    # eşlemek haritayı bozar; float64'ün taban gürültüsüne sabitlemek doğru
    # olandır. Taşan/NaN değerler ise gerçekten ıraksamadır: +sonsuz.
    hata = np.where(np.isnan(hata), np.inf, hata)
    hata = np.maximum(hata, 1e-18)
    with np.errstate(divide="ignore", invalid="ignore"):
        L = np.log10(hata) / N
    L = np.where(np.isfinite(L), L, 30.0 / N)
    return re, im, L


def yaricapi_haritadan_kestir(re, im, L, a: float) -> float:
    """Haritadan R'yi geri okur: L = 0 düzeyinin merkeze en kısa uzaklığı.

    L = (1/N)·log10|hata| büyüklüğünün işareti yakınsaklığı söyler; L = 0
    çizgisi tam olarak |z-a| = R çemberidir. Burada teorik R hiç
    kullanılmaz -- bu, haritanın gerçekten yakınsaklık diskini çizdiğini
    sınayan BAĞIMSIZ bir kestirimdir.
    """
    RE, IM = np.meshgrid(re, im)
    uzaklik = np.abs((RE + 1j * IM) - a)
    disarida = L > 0.0
    if not np.any(disarida):
        return np.inf     # pencerede ıraksama yok: R pencereden büyük
    return float(uzaklik[disarida].min())


def ciz() -> list[list[str]]:
    import matplotlib.pyplot as plt
    from matplotlib.colors import Normalize

    fig, eksenler = plt.subplots(2, 3, figsize=(16.5, 10.5))
    satirlar = []

    for ax, (baslik, expr, a, tekillikler, R_teorik, pencere) in zip(
            eksenler.ravel(), DURUMLAR):
        re, im, L = hata_haritasi(expr, a, N_DERECE, pencere, IZGARA)
        R_olculen = yaricapi_haritadan_kestir(re, im, L, a)

        # Iraksayan bölge (L>0) ile yakınsayan bölge (L<0) ayrı renklere
        # düşsün diye sıfır merkezli, ayrışık (diverging) bir palet.
        gor = ax.imshow(
            L,
            extent=(re[0], re[-1], im[0], im[-1]),
            origin="lower", aspect="equal", cmap="RdBu_r",
            norm=Normalize(vmin=-0.75, vmax=0.75),
        )

        # Haritanın KENDİ sıfır düzeyi: veriden çıkan sınır.
        ax.contour(re, im, L, levels=[0.0], colors=["#0E1117"], linewidths=2.2)

        # Teorik yakınsaklık çemberi (haritanın üstüne çizilir, haritayı
        # oluşturmakta KULLANILMAZ -- örtüşmeyi görmek için).
        if np.isfinite(R_teorik):
            aci = np.linspace(0, 2 * np.pi, 400)
            ax.plot(a + R_teorik * np.cos(aci), R_teorik * np.sin(aci),
                    color="#7CF5C2", lw=1.6, ls="--", alpha=0.95,
                    label=f"teorik R = {R_teorik:.4f}")

        # Tekillikler
        for s in tekillikler:
            ax.plot(s.real, s.imag, "x", color="#7CF5C2", ms=11, mew=2.4)

        # Merkez
        ax.plot(a, 0.0, "o", color="#FFFFFF", ms=6, mew=0)
        ax.axhline(0, color="#FFFFFF", lw=0.7, alpha=0.35)

        olculen_metin = ("—" if not np.isfinite(R_olculen) else f"{R_olculen:.4f}")
        ax.set_title(f"{baslik}\nharitadan okunan R = {olculen_metin}", fontsize=11)
        ax.set_xlabel("Re z")
        ax.set_ylabel("Im z")
        ax.grid(False)
        if np.isfinite(R_teorik):
            ax.legend(fontsize=8, loc="upper right")

        satirlar.append([
            baslik.replace("$", "").replace("\\", ""),
            f"{a:g}",
            ", ".join(f"{s:.0f}" for s in tekillikler) if tekillikler else "yok",
            "∞" if not np.isfinite(R_teorik) else f"{R_teorik:.4f}",
            olculen_metin,
        ])

    cb = fig.colorbar(gor, ax=eksenler, shrink=0.72, pad=0.02)
    cb.set_label("(1/N)*log10|f(z)-P_N(z)|  ~  log10(|z-a|/R)   —   negatif: yakinsiyor, pozitif: iraksiyor")

    fig.suptitle(
        "Yakınsaklık diski kimse çizmeden ortaya çıkıyor\n"
        f"N={N_DERECE}  ·  mavi: yakınsıyor, kırmızı: ıraksıyor  ·  "
        "siyah: haritanın kendi sınırı  ·  yeşil kesikli: teorik R",
        fontsize=14, color=ortam.PALET["fonksiyon"])
    yol = ortam.gorsel_yolu("kompleks_hata_haritasi.png")
    fig.savefig(yol)
    plt.close(fig)
    print(f"  yazıldı: {yol.relative_to(ortam.PROJE_KOK)}")
    return satirlar


def reel_eksen_karsilastirmasi() -> None:
    """Reel eksende bakınca neden hiçbir ipucu olmadığını gösterir.

    Üstte f(x) = 1/(1+x²): pürüzsüz, sakin, hiçbir yerde tuhaf değil.
    Altta aynı fonksiyonun Taylor polinomları: x=±1'de yırtılıyorlar.
    Reel eksende bu sınırın sebebi görünmez; sebep yukarıdaki haritadadır.
    """
    import matplotlib.pyplot as plt

    expr, a = 1 / (1 + T.x**2), 0.0
    xs = np.linspace(-2.2, 2.2, 1400)
    f = T.sayisal_fonksiyon(expr)

    fig, eksenler = plt.subplots(2, 1, figsize=(10, 8), sharex=True,
                                 height_ratios=[1, 1.25])

    ax = eksenler[0]
    ax.plot(xs, f(xs), color=ortam.PALET["fonksiyon"], lw=2.4, label=r"$1/(1+x^2)$")
    ax.set_title("Reel eksende hiçbir sorun yok: sonsuz kez türevlenebilir, sınırlı")
    ax.set_ylabel("f(x)")
    ax.legend()

    ax = eksenler[1]
    ax.plot(xs, f(xs), color=ortam.PALET["fonksiyon"], lw=2.6, label="f(x)", zorder=5)
    for i, N in enumerate((4, 8, 16, 28)):
        P = T.polinom_fonksiyonu(expr, a, N)
        ax.plot(xs, P(xs), lw=1.6,
                color=ortam.SERI_RENKLERI[i % len(ortam.SERI_RENKLERI)],
                label=f"$P_{{{N}}}$")
    for kenar in (-1.0, 1.0):
        ax.axvline(kenar, color="#7CF5C2", ls="--", lw=1.4, alpha=0.9)
    ax.text(1.02, 1.35, "R = 1", color="#7CF5C2", fontsize=11)
    ax.set_ylim(-0.6, 1.6)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_title("Ama Taylor polinomları tam $x=\\pm 1$'de kopuyor — "
                 "sebebi reel eksende görünmüyor")
    ax.legend(fontsize=9, ncol=3)

    fig.tight_layout()
    yol = ortam.gorsel_yolu("reel_eksende_ipucu_yok.png")
    fig.savefig(yol)
    plt.close(fig)
    print(f"  yazıldı: {yol.relative_to(ortam.PROJE_KOK)}")


def yaricap_ile_bozulma() -> None:
    """|z| = r üzerinde hatanın N ile davranışı: (r/R)^N geometrik yasası.

    İçeride (r < R) hata her N'de R'ye göre geometrik olarak küçülür; dışarıda
    (r > R) aynı oranla BÜYÜR. Yarıçap tam olarak bu işaret değişiminin
    yaşandığı yerdir -- bir eşik değil, bir denge noktası.
    """
    import matplotlib.pyplot as plt

    expr, a, R = 1 / (1 + T.x**2), 0.0, 1.0
    f = sp.lambdify(T.x, expr, "numpy")
    N_listesi = np.arange(2, 41, 2)

    fig, ax = plt.subplots(figsize=(9, 6))
    for i, r in enumerate((0.5, 0.8, 0.95, 1.05, 1.3, 1.8)):
        # Çember üzerinde ortalama hata (tek bir nokta yanıltıcı olabilir)
        aci = np.linspace(0, 2 * np.pi, 257)[:-1]
        Z = a + r * np.exp(1j * aci)
        F = np.asarray(f(Z), dtype=complex)
        hatalar = []
        for N in N_listesi:
            katsayilar = T.katsayi_dizisi(expr, a, int(N))
            P = np.zeros_like(Z, dtype=complex)
            guc = np.ones_like(Z, dtype=complex)
            for c in katsayilar:
                P = P + c * guc
                guc = guc * (Z - a)
            hatalar.append(float(np.mean(np.abs(F - P))))
        stil = "-" if r < R else "--"
        ax.semilogy(N_listesi, np.maximum(hatalar, 1e-18), stil, marker="o", ms=3,
                    color=ortam.SERI_RENKLERI[i % len(ortam.SERI_RENKLERI)],
                    label=f"|z| = {r}  ({'içeride' if r < R else 'dışarıda'})")

    ax.axhline(1.0, color=ortam.PALET["soluk"], lw=1.0, ls=":")
    ax.set_xlabel("N")
    ax.set_ylabel(r"$|z|=r$ çemberinde ortalama $|f-P_N|$")
    ax.set_title(r"$1/(1+z^2)$, $a=0$, $R=1$:  hata $(r/R)^N$ gibi davranıyor"
                 "\niçeride üstel çöküş, dışarıda üstel patlama")
    ax.legend(fontsize=9)
    fig.tight_layout()
    yol = ortam.gorsel_yolu("yaricap_gecisi.png")
    fig.savefig(yol)
    plt.close(fig)
    print(f"  yazıldı: {yol.relative_to(ortam.PROJE_KOK)}")


def main() -> int:
    ortam.baslik_yaz("Kompleks düzlemde hata haritaları")
    print(f"  N = {N_DERECE}, ızgara = {IZGARA}×{IZGARA}, {len(DURUMLAR)} durum\n")
    satirlar = ciz()

    ortam.baslik_yaz("Reel eksen: sebep burada görünmüyor")
    reel_eksen_karsilastirmasi()

    ortam.baslik_yaz("Yarıçap geçişi: (r/R)^N yasası")
    yaricap_ile_bozulma()

    icerik = (
        "Her harita, merkez `a` etrafında kompleks düzlemde "
        f"`(1/N)·log10|f(z) - P_{N_DERECE}(z)|` değerini gösterir. Bu büyüklük "
        "`log10(|z-a|/R)`'ye yakınsar: **işareti** yakınsaklığı söyler "
        "(negatif = yakınsıyor, pozitif = ıraksıyor) ve sıfır düzeyi tam olarak "
        "`|z-a| = R` çemberidir. Yakınsaklık diski "
        "harita tarafından **çizilmez**; hatanın kendi davranışından doğar. "
        "`haritadan okunan R`, bu haritanın **kendi** sıfır düzeyinin merkeze "
        "en kısa uzaklığıdır — yani teorik değer hiç kullanılmadan elde edilmiş "
        "bağımsız bir kestirimdir.\n\n"
        + ortam.markdown_tablo(
            ["durum", "a", "tekillikler", "teorik R", "haritadan okunan R"],
            satirlar)
        + "\n\nSon iki satır işin özünü söyler: fonksiyon aynı, merkez farklı, "
          "yarıçap farklı. `1/(1+z²)` için `a=0` iken R=1 (±i'ye uzaklık), "
          "`a=1` iken R=√2≈1.4142 (yine ±i'ye uzaklık, ama artık 1'den). "
          "`1/(1-z)` için `a=0` iken R=1, `a=-1` iken R=2. "
          "**Yarıçap fonksiyonun değil, (fonksiyon, merkez) çiftinin "
          "özelliğidir ve her seferinde en yakın tekilliğe olan uzaklıktır.**\n\n"
          "`e^z` panelinde disk yoktur, çünkü tekillik yoktur: R = ∞. "
          "Pencerenin tamamı yakınsama bölgesidir ve haritadan bir sınır "
          "okunamaz (tablodaki `—`).\n\n"
          "## Sonlu N'in dürüst payı\n\n"
          "Haritadan okunan değerler teorik R'nin sistematik olarak biraz "
          "altında çıkıyor (%5–8). Bu bir hata değil, sonlu N'in kaçınılmaz "
          "payı: `(1/N)·log|hata| → log(|z-a|/R)` yakınsaması ancak N→∞ "
          "limitinde tamdır. Sonlu N'de kuyruktaki cebirsel çarpanlar "
          "(`C`, `N+1` yerine `N`'e bölmek, vb.) sıfır düzeyini biraz içeri "
          "çeker.\n\n"
          "Aynı sebeple `ln(1+z)` panelinde siyah kontur gözle görülür "
          "biçimde **çember değildir** — sola, tekilliğin bulunduğu `z=-1` "
          "yönüne doğru basıktır. `ln(1+z)` katsayıları `1/n` gibi cebirsel "
          "azaldığı için (kutuplu fonksiyonlardaki geometrik azalmanın "
          "aksine) yakınsama N ile daha yavaş sıkışır. N büyütüldükçe kontur "
          "çembere oturur; teoremin söylediği de zaten limitteki şekildir."
    )
    ortam.tablo_yaz("kompleks_yaricap.md",
                    "Yakınsaklık yarıçapı = en yakın tekilliğe uzaklık", icerik)
    print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
