"""B maddesi: Taylor polinomu ile Taylor serisi arasındaki fark ve Lagrange kalanı.

Bu betiğin iddiası şu: Taylor teoremi bir "yaklaşım tekniği" değil, bir
EŞİTLİKTİR. Sonlu N için

    f(x) = P_N(x) + f^(N+1)(ksi) / (N+1)! * (x-a)^(N+1)

ve buradaki ksi, a ile x arasında GERÇEKTEN var olan bir sayıdır. Serinin
yakınsayıp yakınsamaması bunu etkilemez; eşitlik her N için, R'nin dışında
bile geçerlidir.

Betik iki şeyi sayısal olarak gösterir:

1. **Sınır hiç ihlal edilmiyor.** Yüz binin üzerinde (f, a, N, x) dörtlüsünde
   |f(x) - P_N(x)| <= sup|f^(N+1)|/(N+1)! * |x-a|^(N+1) test edilir.

   Burada dikkat edilmesi gereken bir tuzak var: float64 ile bakıldığında
   binlerce nokta sınırı aşıyor GÖRÜNÜR. Bunlar teorem ihlali değildir.
   Sınır çok küçüldüğünde (örn. 1e-41) çift duyarlıklı aritmetik o hatayı
   ölçemez; ölçtüğü şey kendi yuvarlama gürültüsüdür (~eps·|f| ≈ 1e-16).
   Bu yüzden float64 yalnızca ADAY işaretler; hüküm, adayların tamamının
   mpmath ile 60 basamakta yeniden ölçülmesinden çıkar. Teyit edilen ihlal
   sayısı 0'dır.

2. **ksi gerçekten bulunabiliyor.** Eşitliğin gerektirdiği ksi değeri kök
   bulma ile (a, x) aralığında aranır ve bulunur. Yani teorem yalnızca bir
   üst sınır vermiyor; tam değeri üreten bir nokta var olduğunu söylüyor.

Çalıştırma:  python 02-python/src/kalan_dogrulama.py
"""

from __future__ import annotations

import numpy as np
import sympy as sp
from scipy.optimize import brentq

import ortam
import taylor as T

ortam.grafik_temasi()

# --------------------------------------------------------------------------
# Test kümesi: (ad, sympy ifadesi, merkez a, alt sınır, üst sınır)
#
# Aralıklar tekilliklere çarpmayacak biçimde seçildi: ln(1+x) için x > -1,
# 1/(1-x) için x < 1. Bunlar keyfi kısıtlar değil, fonksiyonun tanım
# kümesinin sınırları.
# --------------------------------------------------------------------------

TESTLER = [
    ("sin(x)",       sp.sin(T.x),        0.0,             -4.0,  4.0),
    ("cos(x)",       sp.cos(T.x),        0.0,             -4.0,  4.0),
    ("exp(x)",       sp.exp(T.x),        0.0,             -3.0,  3.0),
    ("ln(1+x)",      sp.log(1 + T.x),    0.0,             -0.85, 2.0),
    ("1/(1-x)",      1 / (1 - T.x),      0.0,             -0.9,  0.9),
    ("sqrt(1+x)",    sp.sqrt(1 + T.x),   0.0,             -0.7,  2.0),
    ("sin(x), a=pi/4", sp.sin(T.x),      float(np.pi / 4), -3.0, 3.0),
    ("exp(x), a=1",  sp.exp(T.x),        1.0,             -2.0,  4.0),
]

DERECELER = list(range(1, 13))   # N = 1..12
NOKTA_SAYISI = 1501              # her (f, N) çifti için


# --------------------------------------------------------------------------
# 1. Toplu sınır doğrulaması
# --------------------------------------------------------------------------

def toplu_dogrulama() -> tuple[list[list[str]], int, int, int, list[tuple]]:
    """float64 taraması: aday ihlalleri toplar. Nihai hüküm mpmath'e aittir."""
    satirlar: list[list[str]] = []
    toplam_nokta = 0
    toplam_aday = 0
    toplam_yuvarlama = 0
    adaylar: list[tuple] = []

    for ad, expr, a, alt, ust in TESTLER:
        noktalar = np.linspace(alt, ust, NOKTA_SAYISI)
        aday_f = 0
        yuvarlama_f = 0
        en_kotu_f = 0.0
        en_kotu_N = 0

        for N in DERECELER:
            r = T.kalan_raporu(expr, a, N, noktalar)
            aday_f += r.aday_sayisi
            yuvarlama_f += r.yuvarlama_sayisi
            toplam_nokta += noktalar.size
            if r.en_kotu_oran > en_kotu_f:
                en_kotu_f = r.en_kotu_oran
                en_kotu_N = N
            for xd in r.aday_noktalar:
                adaylar.append((ad, expr, a, N, float(xd)))

        toplam_aday += aday_f
        toplam_yuvarlama += yuvarlama_f
        satirlar.append([
            ad,
            f"{a:.4g}",
            f"[{alt:g}, {ust:g}]",
            f"{len(DERECELER) * NOKTA_SAYISI:,}".replace(",", " "),
            str(aday_f),
            f"{en_kotu_f:.4f}",
            f"N={en_kotu_N}",
            f"{yuvarlama_f}",
        ])
        print(f"  {ad:<16} aday ihlal: {aday_f:>4}   en kötü hata/sınır = "
              f"{en_kotu_f:.4f} (N={en_kotu_N})   yuvarlama rejimi: {yuvarlama_f}")

    return satirlar, toplam_nokta, toplam_aday, toplam_yuvarlama, adaylar


def adaylari_teyit_et(adaylar: list[tuple]) -> tuple[list[list[str]], int]:
    """float64'ün ihlal sandığı HER noktayı mpmath ile 60 basamakta yeniden ölçer.

    Nihai hüküm buradan çıkar. float64 ile bakıldığında sınır kimi yerde 10^25
    kat aşılmış görünür; hassasiyet artırılınca oran 1'in altına döner. Aşılan
    şey teorem değil, ölçüm aletidir.

    Döndürür: (tablo satırları -- en kötü oranlı ilk 10 aday, teyit edilen ihlal
    sayısı -- TÜM adaylar üzerinden).
    """
    if not adaylar:
        print("  (aday yok)")
        return [], 0

    # Aynı (f, a, N) üçlüsüne düşen adayları grupla: float64 tarafındaki
    # lambdify ve sınır hesabı grup başına bir kez yapılır.
    gruplar: dict[tuple, list[float]] = {}
    kimlik: dict[tuple, tuple] = {}
    for ad, expr, a, N, xd in adaylar:
        anahtar = (ad, a, N)
        gruplar.setdefault(anahtar, []).append(xd)
        kimlik[anahtar] = (expr,)

    sonuclar = []
    for (ad, a, N), xler in gruplar.items():
        (expr,) = kimlik[(ad, a, N)]
        dizi = np.array(xler, dtype=float)
        f = T.sayisal_fonksiyon(expr)
        P = T.polinom_fonksiyonu(expr, a, N)
        d_hatalar = np.abs(np.asarray(f(dizi), dtype=float) - P(dizi))
        d_sinirlar = T.lagrange_sinir(expr, a, N, dizi)

        for xd, d_hata, m_sinir in zip(xler, d_hatalar, d_sinirlar):
            # Sınır sup|f^(N+1)| üzerinden kurulur ve O(1) mertebesindedir;
            # float64 onu zaten doğru hesaplar. Yüksek hassasiyet yalnızca
            # yıkıcı sadeleşme yaşayan hata farkı için gerekli.
            m_hata = T.yuksek_hassasiyet_sadece_hata(expr, a, N, float(xd))
            d_hata, m_sinir = float(d_hata), float(m_sinir)
            d_oran = d_hata / m_sinir if m_sinir > 0 else float("inf")
            m_oran = m_hata / m_sinir if m_sinir > 0 else float("inf")
            sonuclar.append((m_oran, [ad, str(N), f"{xd:.4f}", f"{d_hata:.3e}",
                                      f"{m_hata:.3e}", f"{m_sinir:.3e}",
                                      f"{d_oran:.3e}", f"{m_oran:.6f}"]))

    # mpmath'in de ihlal dediği noktalar: bunlar gerçek olur.
    # Kayan nokta kalıntısına karşı çok küçük bir pay bırakılır; mpmath 60
    # basamakta çalıştığı için 1e-12'lik pay fazlasıyla güvenli.
    teyitli = sum(1 for oran, _ in sonuclar if oran > 1.0 + 1e-12)

    sonuclar.sort(key=lambda p: -p[0])
    for oran, satir in sonuclar[:10]:
        print(f"  {satir[0]:<10} N={satir[1]:<2} x={float(satir[2]):<8.4f} "
              f"float64 oran={float(satir[6]):>10.2e}  →  mpmath oran={oran:.6f}  "
              f"{'OK' if oran <= 1.0 + 1e-12 else 'IHLAL!'}")
    if len(sonuclar) > 10:
        print(f"  ... ({len(sonuclar) - 10} aday daha; en kötü oranlı 10 tanesi "
              f"gösterildi)")
    return [satir for _, satir in sonuclar[:10]], teyitli


# --------------------------------------------------------------------------
# 2. ksi'nin varlığını sayısal olarak gösterme
# --------------------------------------------------------------------------

def ksi_bul(expr: sp.Expr, a: float, N: int, xd: float) -> float | None:
    """Lagrange eşitliğini SAĞLAYAN ksi'yi (a, xd) aralığında arar.

    Eşitlikten gerekli türev değeri tek başına belirlenir:

        f^(N+1)(ksi) = (f(x) - P_N(x)) * (N+1)! / (x-a)^(N+1)

    Sağ taraf bilinen bir sayı. Sol tarafı bu sayıya eşitleyen ksi, sürekli
    bir fonksiyonun ara değer teoremiyle garanti edilir. Burada brentq ile
    fiilen bulunur -- yani teoremin varlık iddiası somutlanır.
    """
    f = T.sayisal_fonksiyon(expr)
    P = T.polinom_fonksiyonu(expr, a, N)
    turev_f = sp.lambdify(T.x, sp.diff(expr, T.x, N + 1), "numpy")

    kalan = float(f(np.array([xd]))[0] - P(np.array([xd]))[0])
    gerekli = kalan * float(sp.factorial(N + 1)) / (xd - a) ** (N + 1)

    def g(t: float) -> float:
        return float(turev_f(t)) - gerekli

    alt, ust = (a, xd) if a < xd else (xd, a)
    # Uçlardan biraz içeride tara: uçlarda g sıfıra çok yakın olabilir.
    tarama = np.linspace(alt, ust, 4001)[1:-1]
    with np.errstate(over="ignore", invalid="ignore"):
        degerler = np.array([g(t) for t in tarama])

    isaret_degisimi = np.where(np.sign(degerler[:-1]) * np.sign(degerler[1:]) < 0)[0]
    if isaret_degisimi.size == 0:
        return None
    i = int(isaret_degisimi[0])
    return float(brentq(g, tarama[i], tarama[i + 1], xtol=1e-14))


def ksi_tablosu() -> list[list[str]]:
    """Birkaç somut (f, N, x) için bulunan ksi değerlerini tablolar."""
    ornekler = [
        ("sin(x)", sp.sin(T.x), 0.0, 3, 1.2),
        ("sin(x)", sp.sin(T.x), 0.0, 6, 2.5),
        ("exp(x)", sp.exp(T.x), 0.0, 4, 1.0),
        ("exp(x)", sp.exp(T.x), 0.0, 4, -1.5),
        ("ln(1+x)", sp.log(1 + T.x), 0.0, 5, 0.7),
        ("1/(1-x)", 1 / (1 - T.x), 0.0, 3, 0.5),
        # R'nin DIŞINDA bir nokta: seri ıraksıyor ama eşitlik hâlâ geçerli.
        ("ln(1+x)", sp.log(1 + T.x), 0.0, 6, 1.8),
    ]
    satirlar = []
    for ad, expr, a, N, xd in ornekler:
        ksi = ksi_bul(expr, a, N, xd)
        if ksi is None:
            satirlar.append([ad, str(N), f"{xd:g}", "bulunamadı", "-", "-"])
            print(f"  {ad:<10} N={N:<2} x={xd:<5g}  ksi BULUNAMADI")
            continue
        icinde = min(a, xd) < ksi < max(a, xd)
        f = T.sayisal_fonksiyon(expr)
        P = T.polinom_fonksiyonu(expr, a, N)
        turev_f = sp.lambdify(T.x, sp.diff(expr, T.x, N + 1), "numpy")
        sol = float(f(np.array([xd]))[0])
        sag = float(P(np.array([xd]))[0]) + float(turev_f(ksi)) / float(
            sp.factorial(N + 1)) * (xd - a) ** (N + 1)
        satirlar.append([
            ad, str(N), f"{xd:g}", f"{ksi:.10f}",
            "evet" if icinde else "HAYIR",
            f"{abs(sol - sag):.2e}",
        ])
        print(f"  {ad:<10} N={N:<2} x={xd:<5g}  ksi={ksi:.8f}  "
              f"(a,x) içinde: {'evet' if icinde else 'HAYIR'}  "
              f"eşitlik artığı: {abs(sol - sag):.2e}")
    return satirlar


# --------------------------------------------------------------------------
# 3. Görseller
# --------------------------------------------------------------------------

def grafikleri_ciz() -> None:
    import matplotlib.pyplot as plt

    expr, a = sp.sin(T.x), 0.0
    noktalar = np.linspace(-4, 4, 1201)

    fig, eksenler = plt.subplots(1, 2, figsize=(13, 5))

    # Sol: x'e göre hata ve sınır, birkaç N için
    ax = eksenler[0]
    taban = None
    for i, N in enumerate((1, 3, 5, 7, 9)):
        r = T.kalan_raporu(expr, a, N, noktalar)
        renk = ortam.SERI_RENKLERI[i % len(ortam.SERI_RENKLERI)]
        ax.semilogy(noktalar, np.maximum(r.gercek_hata, 1e-18),
                    color=renk, lw=1.8, label=f"gerçek hata, N={N}")
        ax.semilogy(noktalar, np.maximum(r.lagrange_sinir, 1e-18),
                    color=renk, lw=1.0, ls="--", alpha=0.7)
        taban = r.yuvarlama_tabani if taban is None else np.maximum(taban, r.yuvarlama_tabani)

    # float64'ün ölçüm tabanı: bu bandın ALTINDA hiçbir "gerçek hata" eğrisine
    # güvenilemez. Eğrilerin x=0 civarında dibe vurup yatay bir zemine oturması
    # matematikten değil, çift duyarlıklı aritmetiğin çözünürlüğünden gelir.
    ax.fill_between(noktalar, 1e-18, taban, color=ortam.PALET["soluk"],
                    alpha=0.35, lw=0, label="float64 ölçüm tabanı")
    ax.set_title("sin(x), a=0 — düz: gerçek hata, kesikli: Lagrange sınırı")
    ax.set_xlabel("x")
    ax.set_ylabel(r"$|f(x)-P_N(x)|$")
    ax.set_ylim(1e-17, 1e3)
    ax.legend(fontsize=8, ncol=2, loc="lower center")

    # Sağ: sabit x'te N'e göre düşüş — eğim N ile nasıl değişiyor?
    ax = eksenler[1]
    N_listesi = list(range(1, 21))
    for i, xd in enumerate((0.5, 1.0, 2.0, 3.0)):
        hatalar, sinirlar = [], []
        for N in N_listesi:
            r = T.kalan_raporu(expr, a, N, np.array([xd]))
            hatalar.append(max(float(r.gercek_hata[0]), 1e-18))
            sinirlar.append(max(float(r.lagrange_sinir[0]), 1e-18))
        renk = ortam.SERI_RENKLERI[i % len(ortam.SERI_RENKLERI)]
        ax.semilogy(N_listesi, hatalar, "o-", color=renk, ms=3, lw=1.6, label=f"x={xd}")
        ax.semilogy(N_listesi, sinirlar, "--", color=renk, lw=1.0, alpha=0.7)
    ax.set_title("N arttıkça hata: sınır her zaman üstte")
    ax.set_xlabel("N (polinom derecesi)")
    ax.set_ylabel("hata")
    ax.set_ylim(1e-17, 1e2)
    ax.legend(fontsize=9)

    fig.suptitle("Lagrange kalanı: sınır hiçbir noktada aşılmıyor",
                 color=ortam.PALET["fonksiyon"], fontsize=14)
    fig.tight_layout()
    yol = ortam.gorsel_yolu("kalan_dogrulama.png")
    fig.savefig(yol)
    plt.close(fig)
    print(f"  yazıldı: {yol.relative_to(ortam.PROJE_KOK)}")


# --------------------------------------------------------------------------

def main() -> int:
    ortam.baslik_yaz("1. Lagrange sınırı toplu doğrulaması")
    print(f"  {len(TESTLER)} fonksiyon × {len(DERECELER)} derece × "
          f"{NOKTA_SAYISI} nokta\n")
    satirlar, toplam_nokta, toplam_aday, toplam_yuvarlama, adaylar = toplu_dogrulama()
    print(f"\n  TOPLAM: {toplam_nokta:,} nokta tarandı, {toplam_aday} aday ihlal, "
          f"{toplam_yuvarlama} nokta yuvarlama rejiminde.".replace(",", " "))

    ortam.baslik_yaz("1b. Her aday ihlalin mpmath ile teyidi (60 basamak)")
    print(f"  float64 taraması {toplam_aday} adayı işaretledi. Hüküm float64'e\n"
          "  bırakılmıyor: adayların TAMAMI yüksek hassasiyette yeniden ölçülüyor.\n")
    mp_satirlari, mp_ihlal = adaylari_teyit_et(adaylar)
    print(f"\n  mpmath ile TEYİT EDİLEN ihlal sayısı: {mp_ihlal}")

    ortam.baslik_yaz("2. Hızlı ve naif sınır hesabı tutuyor mu?")
    fark_satirlari = []
    for ad, expr, a, alt, ust in TESTLER[:4]:
        pts = np.linspace(alt, ust, 41)
        for N in (2, 5, 8):
            h = T.lagrange_sinir(expr, a, N, pts)
            y = T.lagrange_sinir_yavas(expr, a, N, pts)
            m = np.isfinite(h) & np.isfinite(y) & (y > 0)
            rel = float(np.max(np.abs(h[m] - y[m]) / y[m])) if m.any() else 0.0
            fark_satirlari.append([ad, str(N), f"{rel:.2e}"])
    en_buyuk = max(float(s[2]) for s in fark_satirlari)
    print(f"  en büyük bağıl fark: {en_buyuk:.2e}  "
          f"(yalnızca ızgara ayrıklığından; aynı formül)")

    ortam.baslik_yaz("3. ksi gerçekten var mı? (eşitliğin somutlanması)")
    ksi_satirlari = ksi_tablosu()

    ortam.baslik_yaz("4. Görseller")
    grafikleri_ciz()

    # ---- Tabloları diske yaz ----
    icerik = (
        "Her satır, o fonksiyon için N=1..12 ve " + str(NOKTA_SAYISI) +
        " nokta üzerinde yapılan tüm testlerin özetidir.\n"
        "`en kötü oran` = max(gerçek hata / Lagrange sınırı), **float64 ile** "
        "ölçülmüş ve yalnızca \"anlamlı rejim\"de (sınır > yuvarlama tabanı) "
        "alınmıştır. Teorem gerçek oranın 1'i asla geçmemesini söyler; bu "
        "sütunda 1'in üstünde görünen değerler ise float64 artığıdır: "
        "yuvarlama tabanı `(N+2)·eps` ile kestirilen yaklaşık bir eşiktir ve "
        "sınırın tabanın hemen üstünde kaldığı noktalar \"anlamlı\" sayılır. "
        "Örneğin `ln(1+x)`, `N=7`, `x≈0.0126`: sınır 7.9e-17, float64 oranı "
        "2.36, mpmath oranı 0.989. Bu yüzden hüküm bu sütuna değil, aşağıdaki "
        "mpmath teyidine bırakılır.\n\n"
        "`yuvarlama rejimi` sütunu, Lagrange sınırının float64'ün ölçebileceğinin "
        "altına düştüğü nokta sayısıdır. Oralarda ölçüm anlamsızdır ve ayrıca "
        "mpmath ile test edilirler (aşağıdaki ikinci tablo).\n\n"
        + ortam.markdown_tablo(
            ["fonksiyon", "a", "aralık", "taranan nokta", "float64 aday ihlal",
             "en kötü oran", "nerede", "yuvarlama rejimi"],
            satirlar)
        + f"\n\n**Toplam: {toplam_nokta:,} nokta tarandı, {toplam_aday} aday ihlal "
          f"({toplam_yuvarlama} nokta yuvarlama rejiminde). "
          f"mpmath ile TEYİT EDİLEN ihlal: {mp_ihlal}.**".replace(",", " ")
        + "\n\nOranın 1'e yaklaştığı yerler, sınırın *keskin* olduğu yerlerdir: "
          "orada eşitliği sağlayan ksi, türevin supremumunu aldığı noktaya denk "
          "düşer. Oranın küçük kaldığı yerlerde ise sınır gevşektir — ama hiçbir "
          "zaman yanlış değildir.\n\n"
          "## float64'ün tabanı: sahte ihlaller\n\n"
          "Aşağıdaki noktalar float64 ile bakıldığında sınırı katbekat aşıyor "
          "görünür. Örneğin `exp`, `a=1`, `N=12`, `x=0.996` için gerçek hata "
          "`2.93e-41`, ama çift duyarlıklı aritmetiğin `exp(0.996)≈2.7` "
          "civarında ölçebildiği en küçük fark `eps·|f| ≈ 6e-16`. Ölçülen "
          "\"hata\" tamamen yuvarlama gürültüsüdür.\n\n"
          "Aynı noktalar mpmath ile 60 basamakta yeniden ölçüldüğünde oran "
          "1'in altına döner — yani aşılan şey teorem değil, **ölçüm aletiydi**.\n\n"
        + (ortam.markdown_tablo(
            ["fonksiyon", "N", "x", "float64 hata", "mpmath hata", "mpmath sınır",
             "float64 oran", "mpmath oran"],
            mp_satirlari) if mp_satirlari else "_(şüpheli nokta çıkmadı)_")
        + f"\n\n**{toplam_aday} adayın tamamı teyit edildi; mpmath ile ihlal sayısı: {mp_ihlal}.**"
    )
    ortam.tablo_yaz("kalan_dogrulama.md", "Lagrange kalan sınırı doğrulaması", icerik)

    ksi_icerik = (
        "Lagrange kalanı bir eşitliktir:\n\n"
        "```\nf(x) = P_N(x) + f^(N+1)(ksi)/(N+1)! * (x-a)^(N+1)\n```\n\n"
        "Aşağıdaki ksi değerleri **arandı ve bulundu**; son sütun eşitliğin iki "
        "yanı arasındaki farktır (kayan nokta gürültüsü mertebesinde).\n\n"
        + ortam.markdown_tablo(
            ["fonksiyon", "N", "x", "bulunan ksi", "(a,x) içinde mi?", "eşitlik artığı"],
            ksi_satirlari)
        + "\n\nSon satır özellikle önemli: `ln(1+x)`, `x=1.8` noktası "
          "yakınsaklık yarıçapının (R=1) **dışındadır**. Seri orada ıraksar, "
          "yani N→∞ limitinde P_N(1.8) hiçbir yere gitmez. Buna rağmen sonlu "
          "N için eşitlik hâlâ geçerlidir ve ksi hâlâ vardır. "
          "**Taylor polinomu ile Taylor serisi aynı şey değildir.**"
    )
    ortam.tablo_yaz("ksi_varligi.md", "Lagrange kalanındaki ksi'nin somutlanması", ksi_icerik)

    print()
    return 0 if mp_ihlal == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
