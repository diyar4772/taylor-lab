"""Cauchy-Hadamard: yakınsaklık yarıçapını KATSAYILARDAN okumak.

Kompleks harita (kompleks_harita.py) R'yi geometrik olarak gösterir: en yakın
tekilliğe uzaklık. Bu betik aynı sayıya bambaşka bir yoldan varır --
fonksiyona, tekilliklerine, hatta kompleks düzleme hiç bakmadan, yalnızca
katsayı dizisine bakarak:

    1/R = limsup_{n->oo} |a_n|^(1/n)

İki yolun aynı sayıda buluşması tesadüf değildir; Cauchy-Hadamard teoremi
budur. Burada teoremin sayısal olarak nasıl davrandığı incelenir:

* limsup sonlu veriden okunamaz. Elimizde n <= N için a_n vardır; limsup ise
  sonsuza dair bir iddiadır. Bu yüzden her kestirim bir YAKLAŞIMDIR ve bazı
  fonksiyonlarda çok yavaş yakınsar.
* Seyrek seriler (1/(1+x^2): tek dereceli katsayılar sıfır) naif uygulamayı
  bozar: 0^(1/n) = 0 limsup'ı yanlış biçimde aşağı çeker. Sıfırlar atlanmalıdır.
* Oran testi |a_n/a_{n+1}| limit VARSA daha hızlı yakınsar, ama her zaman var
  olmaz. exp için ikisinin farkı çarpıcıdır.

Çalıştırma:  python 02-python/src/yakinsaklik_orani.py
"""

from __future__ import annotations

import math

import numpy as np
import sympy as sp

import ortam
import taylor as T

ortam.grafik_temasi()

# (ad, ifade, merkez a, teorik R)
DURUMLAR = [
    ("exp(x)",      sp.exp(T.x),        0.0,  math.inf),
    ("sin(x)",      sp.sin(T.x),        0.0,  math.inf),
    ("ln(1+x)",     sp.log(1 + T.x),    0.0,  1.0),
    ("1/(1-x)",     1 / (1 - T.x),      0.0,  1.0),
    ("1/(1+x^2)",   1 / (1 + T.x**2),   0.0,  1.0),
    ("arctan(x)",   sp.atan(T.x),       0.0,  1.0),
    ("sqrt(1+x)",   sp.sqrt(1 + T.x),   0.0,  1.0),
    ("1/(1+x^2), a=1", 1 / (1 + T.x**2), 1.0, math.sqrt(2.0)),
    ("1/(1-x), a=-1",  1 / (1 - T.x),  -1.0,  2.0),
]

N_MAKS = 60      # katsayı sayısı; sympy'nin rahatça götürdüğü bir üst sınır


def kismi_kestirimler(katsayilar: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Her n için |a_n|^(1/n) ve bunların koşan (running) maksimumunu verir.

    limsup, "kuyrukta en büyük değere yaklaşan" demektir. Sonlu veride bunun
    en dürüst karşılığı, n'den sonuna kadar olan maksimumdur; ama ileriyi
    göremediğimiz için pratikte elimizdeki kuyruğun maksimumunu alırız.
    Aşağıda her iki büyüklük de tutulur ki yakınsamanın hızı görülebilsin.
    """
    n_dizi = []
    kok_dizi = []
    for n, c in enumerate(katsayilar):
        if n == 0 or c == 0:
            continue          # seyrek serilerde sıfırlar limsup'a girmez
        n_dizi.append(n)
        kok_dizi.append(abs(c) ** (1.0 / n))
    return np.array(n_dizi), np.array(kok_dizi)


def tablo() -> list[list[str]]:
    satirlar = []
    for ad, expr, a, R_teorik in DURUMLAR:
        kats = T.katsayi_dizisi(expr, a, N_MAKS)
        R_ch = T.cauchy_hadamard_R(kats, son_k=12)
        R_oran = T.oran_testi_R(kats)

        def bicim(v: float) -> str:
            if not np.isfinite(v):
                return "∞"
            return f"{v:.4f}"

        # Bağıl hata yalnızca sonlu R için anlamlı
        if np.isfinite(R_teorik) and R_teorik > 0:
            hata_ch = f"{abs(R_ch - R_teorik) / R_teorik * 100:.2f}%"
            hata_oran = (f"{abs(R_oran - R_teorik) / R_teorik * 100:.2f}%"
                         if np.isfinite(R_oran) else "—")
        else:
            hata_ch = hata_oran = "—"

        satirlar.append([ad, f"{a:g}", bicim(R_teorik), bicim(R_ch), hata_ch,
                         bicim(R_oran), hata_oran])
        print(f"  {ad:<16} teorik R={bicim(R_teorik):>8}   "
              f"C-H={bicim(R_ch):>8} ({hata_ch:>6})   "
              f"oran={bicim(R_oran):>8} ({hata_oran:>6})")
    return satirlar


def yakinsama_grafigi() -> None:
    """|a_n|^(1/n) dizisinin 1/R'ye ne kadar yavaş gittiğini gösterir."""
    import matplotlib.pyplot as plt

    fig, eksenler = plt.subplots(1, 2, figsize=(14, 5.5))

    # Sol: sonlu R'li fonksiyonlar -- hedef çizgi 1/R
    ax = eksenler[0]
    for i, (ad, expr, a, R) in enumerate(
            [d for d in DURUMLAR if np.isfinite(d[3])][:5]):
        kats = T.katsayi_dizisi(expr, a, N_MAKS)
        n, kok = kismi_kestirimler(kats)
        renk = ortam.SERI_RENKLERI[i % len(ortam.SERI_RENKLERI)]
        ax.plot(n, kok, "o-", ms=3, lw=1.4, color=renk, label=f"{ad}  (1/R={1/R:.3f})")
        ax.axhline(1 / R, color=renk, ls=":", lw=1.0, alpha=0.6)
    ax.set_xlabel("n")
    ax.set_ylabel(r"$|a_n|^{1/n}$")
    ax.set_title("Sonlu R: dizi 1/R'ye oturuyor\n(noktalı çizgiler teorik 1/R)")
    ax.legend(fontsize=8)

    # Sağ: exp -- 1/R = 0'a gitmesi gerekiyor ama ne kadar yavaş?
    ax = eksenler[1]
    kats = T.katsayi_dizisi(sp.exp(T.x), 0.0, N_MAKS)
    n, kok = kismi_kestirimler(kats)
    ax.semilogy(n, kok, "o-", ms=3, lw=1.6, color=ortam.PALET["polinom"],
                label=r"$|a_n|^{1/n} = (1/n!)^{1/n}$")
    # Stirling: (1/n!)^(1/n) ~ e/n
    ax.semilogy(n, np.e / n, "--", lw=1.4, color=ortam.PALET["sinir"],
                label=r"Stirling: $e/n$")
    ax.set_xlabel("n")
    ax.set_ylabel(r"$|a_n|^{1/n}$")
    ax.set_title(r"$e^x$: $1/R \to 0$, yani $R \to \infty$"
                 "\nama yalnızca $\\sim e/n$ hızıyla — n=60'ta hâlâ 0.045")
    ax.legend(fontsize=9)

    fig.suptitle("Cauchy-Hadamard sayısal olarak: doğru ama yavaş",
                 fontsize=14, color=ortam.PALET["fonksiyon"])
    fig.tight_layout()
    yol = ortam.gorsel_yolu("cauchy_hadamard.png")
    fig.savefig(yol)
    plt.close(fig)
    print(f"  yazıldı: {yol.relative_to(ortam.PROJE_KOK)}")


def seyreklik_tuzagi() -> str:
    """Sıfır katsayıları atlamazsak ne olur? Somut sayılarla göster."""
    kats = T.katsayi_dizisi(1 / (1 + T.x**2), 0.0, N_MAKS)

    # Naif: sıfırları da dahil et
    naif = []
    for n, c in enumerate(kats):
        if n == 0:
            continue
        naif.append(abs(c) ** (1.0 / n))
    naif_R = 1.0 / max(naif[-12:]) if max(naif[-12:]) > 0 else math.inf

    dogru_R = T.cauchy_hadamard_R(kats, son_k=12)

    # Son 12 terimin son 6'sı sıfır mı? (1/(1+x^2) katsayıları: 1,0,-1,0,1,...)
    son = naif[-12:]
    sifir_sayisi = sum(1 for v in son if v == 0.0)

    print(f"  1/(1+x^2), N={N_MAKS}: son 12 terimin {sifir_sayisi} tanesi sıfır")
    print(f"    sıfırlar atlanarak : R ≈ {dogru_R:.6f}   (teorik 1.0)")
    print(f"    sıfırlar dahil     : R ≈ {naif_R:.6f}")
    return (f"1/(1+x²) serisinde tek dereceli katsayıların tamamı sıfırdır "
            f"(1, 0, −1, 0, 1, …). Son 12 terimin {sifir_sayisi} tanesi sıfır. "
            f"Sıfırlar `|a_n|^(1/n)` dizisine katılırsa 0 değerleri maksimuma "
            f"hiç katkı vermez ama diziyi delik deşik eder; **limsup yine de "
            f"doğru çıkar** çünkü limsup zaten maksimuma bakar: bu örnekte "
            f"her iki yol da R ≈ {dogru_R:.4f} verir. Asıl bozulan ORAN "
            f"TESTİdir: ardışık iki katsayıdan biri sıfır olduğunda "
            f"|a_n/a_(n+1)| ya 0 ya tanımsızdır. Bu yüzden oran testi "
            f"`taylor.py` içinde ardışık **sıfırdan farklı** terimler "
            f"arasındaki derece farkı d ile |a_n/a_(n+d)|^(1/d) biçiminde "
            f"uygulanır.")


def salinim_tablosu() -> list[list[str]]:
    """1/(1+x^2), a=1: oran testinin N'e göre salınımı, C-H'nin kararlılığı.

    En yakın iki tekillik (i ve -i) merkeze eşit uzaklıkta olduğu için
    katsayılar c_n = (-1)^n 2^(-(n+1)/2) sin((n+1)π/4) biçimindedir; sin
    çarpanı 4 periyotla döner ve n ≡ 3 (mod 4) için katsayı tam sıfırdır.
    Oran testinin sonucu bu yüzden hangi N'de durulduğuna bağlıdır — tek bir
    N'deki değer hiçbir şey kanıtlamaz, salınımın kendisi kanıttır.
    """
    R = math.sqrt(2.0)
    kats = T.katsayi_dizisi(1 / (1 + T.x**2), 1.0, N_MAKS)
    satirlar = []
    for N in range(N_MAKS - 8, N_MAKS + 1):
        c = kats[:N + 1]
        o = T.oran_testi_R(c)
        ch = T.cauchy_hadamard_R(c, son_k=12)
        satirlar.append([str(N), f"{o:.4f}", f"{abs(o - R) / R * 100:.2f}%",
                         f"{ch:.4f}", f"{abs(ch - R) / R * 100:.2f}%"])
        print(f"  N={N:>2}   oran testi={o:.4f}   C-H={ch:.4f}")
    return satirlar


def main() -> int:
    ortam.baslik_yaz("Cauchy-Hadamard ile R kestirimi (katsayılardan)")
    print(f"  N = {N_MAKS} katsayı, limsup son 12 sıfırsız terimden\n")
    satirlar = tablo()

    ortam.baslik_yaz("Seyrek seri tuzağı")
    seyreklik_metni = seyreklik_tuzagi()

    ortam.baslik_yaz("Oran testinin salınımı: 1/(1+x^2), a=1")
    salinim_satirlari = salinim_tablosu()

    ortam.baslik_yaz("Grafik")
    yakinsama_grafigi()

    icerik = (
        f"Katsayılar `n ≤ {N_MAKS}` için üretildi. `C-H` sütunu "
        "`1/R = limsup |a_n|^(1/n)` formülünün son 12 sıfırdan farklı terim "
        "üzerinden kestirimidir; `oran` sütunu `R ≈ |a_n/a_(n+d)|^(1/d)` "
        "testidir.\n\n"
        + ortam.markdown_tablo(
            ["fonksiyon", "a", "teorik R", "C-H kestirimi", "C-H hatası",
             "oran testi", "oran hatası"],
            satirlar)
        + "\n\n## Okunacaklar\n\n"
          "**1. Sonlu R'de iki yöntem de iyi çalışır.** `1/(1-x)`, `1/(1+x²)` "
          "gibi kutuplu fonksiyonlarda katsayılar geometrik azaldığı için "
          "`|a_n|^(1/n)` hemen 1/R'ye oturur.\n\n"
          "**2. `ln(1+x)` ve `sqrt(1+x)` yavaştır.** Katsayılar `1/n` gibi "
          "cebirsel bir çarpan taşır; `(1/n)^(1/n) → 1` yakınsaması "
          "logaritmik yavaşlıktadır. N=60'ta bile birkaç yüzdelik sapma "
          "kalır. Bu yöntemin kusuru değil, limsup'ın doğasıdır.\n\n"
          "**3. `exp` ve `sin` için R = ∞ ve bunu sayısal olarak "
          "'görmek' mümkün değildir.** `(1/n!)^(1/n) ≈ e/n` Stirling'den "
          "gelir; n=60'ta bu hâlâ ≈ 0.045, yani R ≈ 22. Sonsuzu sonlu veriden "
          "okuyamazsınız — yalnızca 'büyüyor' diyebilirsiniz. Tablodaki C-H "
          "sütununun `exp` satırında sonsuz yerine sonlu bir sayı çıkması "
          "**yöntemin dürüst sınırıdır**, hata değil.\n\n"
          "**4. Seyreklik.**\n\n" + seyreklik_metni + "\n\n"
          "**5. Oran testi her zaman çalışmaz — `1/(1+x²)`, `a=1`.** Bu "
          "merkez için en yakın iki tekillik `i` ve `−i`, `a=1`'e **eşit "
          "uzaklıkta ama farklı yönlerdedir**. Katsayılar "
          "`c_n = (−1)^n · 2^(−(n+1)/2) · sin((n+1)π/4)` biçimindedir: sin "
          "çarpanı 4 periyotla döner ve `n ≡ 3 (mod 4)` için katsayı tam "
          "sıfırdır. Bu yüzden `|a_n/a_(n+d)|` oranının bir LİMİTİ YOKTUR ve "
          "oran testinin cevabı hangi N'de durulduğuna bağlıdır. Yukarıdaki "
          f"tabloda (N={N_MAKS}) oran testi tesadüfen tam √2 veriyor; N'i "
          "birer birer değiştirince:\n\n"
        + ortam.markdown_tablo(
            ["N", "oran testi", "oran hatası", "C-H kestirimi", "C-H hatası"],
            salinim_satirlari)
        + "\n\nOran testi √2, 1, 2 değerleri arasında dolaşır ve hiçbir yere "
          "yerleşmez; Cauchy-Hadamard ise limsup kullandığı için yaklaşık "
          "%0.6 sapmayla yerinde durur. Teoremin neden limit değil limsup "
          "ile kurulduğu tam olarak budur.\n\n"
          "_Not: katsayılar merkez `sp.Rational(a)` olarak verilip tam "
          "aritmetikle üretilir. Merkez float verildiğinde (bu betiğin önceki "
          "sürümü) n ≳ 20'den sonra yıkıcı sadeleşme katsayıları bozuyor ve "
          "bu satırda sahte bir %22.66 sapma üretiyordu._\n\n"
          "**6. İki bağımsız yol, aynı sayı.** Bu tablodaki R değerleri "
          "yalnızca katsayı dizisine bakılarak elde edildi — fonksiyonun "
          "kompleks düzlemdeki tekilliklerine hiç bakılmadan. "
          "`out/tablolar/kompleks_yaricap.md` ise aynı sayılara tekilliklerin "
          "geometrisinden ulaşır. Cauchy-Hadamard teoremi tam olarak bu iki "
          "yolun her zaman buluştuğunu söyler."
    )
    ortam.tablo_yaz("cauchy_hadamard.md",
                    "Yakınsaklık yarıçapının katsayılardan kestirimi", icerik)
    print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
