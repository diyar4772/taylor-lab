"""E maddesi: sin(theta) ~ theta'da ATILAN terim nereye gitti?

Sarkaç denklemi tamdır ve doğrusal değildir:

    theta'' = -(g/L) sin(theta)

"Küçük açı yaklaşımı" sin(theta) yerine theta yazar ve geriye harmonik
osilatör kalır. Bu bir hile değil, Taylor açılımının ilk teriminde kesilmesidir:

    sin(theta) = theta - theta^3/6 + theta^5/120 - ...

Atılan ilk terim -theta^3/6'dır. Bu terim yok olmaz; sistemin davranışında
bir yerde geri döner. Nerede? PERİYOTTA.

Tam periyot eliptik integralle verilir ve theta_0'a göre açılırsa

    T = T_0 * (1 + theta_0^2/16 + 11*theta_0^4/3072 + ...)

Baştaki 1 harmonik yaklaşımdır; theta_0^2/16 terimi ise tam olarak atılan
theta^3/6'nın faturasıdır. Harmonik osilatörde periyot genlikten bağımsızdır
(izokronizm); gerçek sarkaçta değildir ve bağımlılığın İLK mertebesi
Taylor'ın attığı terimden gelir.

Bu betik:
1. Tam denklemi scipy.solve_ivp ile çözer, periyodu sıfır geçişlerinden ÖLÇER.
2. Ölçülen periyodu (a) harmonik T_0, (b) eliptik integralden gelen tam
   değer, (c) T_0(1 + theta_0^2/16) Taylor kestirimi ile karşılaştırır.
3. Taylor düzeltmesinin hata mertebesinin gerçekten O(theta_0^4) olduğunu
   log-log eğimden doğrular.

Çalıştırma:  python 02-python/src/sarkac.py
"""

from __future__ import annotations

import numpy as np
from scipy.integrate import solve_ivp
from scipy.special import ellipk

import ortam

ortam.grafik_temasi()

G = 9.80665     # m/s^2, standart yerçekimi
L = 1.0         # m, sarkaç uzunluğu
OMEGA0 = np.sqrt(G / L)
T0 = 2 * np.pi / OMEGA0      # harmonik (genlikten bağımsız) periyot


# --------------------------------------------------------------------------
# Dinamik
# --------------------------------------------------------------------------

def tam_sarkac(t, y):
    """theta'' = -(g/L) sin(theta) -- hiçbir yaklaşım yok."""
    theta, omega = y
    return [omega, -(G / L) * np.sin(theta)]


def harmonik_sarkac(t, y):
    """theta'' = -(g/L) theta -- Taylor'ın birinci terimde kesilmiş hâli."""
    theta, omega = y
    return [omega, -(G / L) * theta]


def periyodu_olc(theta0: float) -> float:
    """Tam çözümün periyodunu sıfır geçişlerinden ölçer.

    Sarkaç theta_0'dan sıfır hızla bırakılır. İlk kez theta=0'a ulaştığı an
    çeyrek periyottur; bu yüzden T = 4 * t_ilk_gecis. Geçiş anı solve_ivp'nin
    olay (event) mekanizmasıyla, adım aralığında kök bularak bulunur --
    ızgaraya bakıp "en yakın nokta" demekten çok daha hassastır.
    """
    def sifir_gecisi(t, y):
        return y[0]
    sifir_gecisi.terminal = True
    sifir_gecisi.direction = -1 if theta0 > 0 else 1

    coz = solve_ivp(tam_sarkac, (0.0, 20 * T0), [theta0, 0.0],
                    events=sifir_gecisi, rtol=1e-12, atol=1e-14,
                    dense_output=True, max_step=T0 / 50)
    if coz.t_events[0].size == 0:
        return float("nan")
    return 4.0 * float(coz.t_events[0][0])


def tam_periyot_eliptik(theta0: float) -> float:
    """Kapalı biçim: T = 4 sqrt(L/g) K(sin^2(theta_0/2)).

    scipy.special.ellipk parametreyi m = k^2 olarak alır (modül k değil).
    Bu, sayısal ölçümden bağımsız bir referans sağlar.
    """
    m = np.sin(theta0 / 2.0) ** 2
    return 4.0 * np.sqrt(L / G) * ellipk(m)


def taylor_periyot(theta0: float, mertebe: int = 2) -> float:
    """T_0 (1 + theta_0^2/16 [+ 11 theta_0^4/3072]).

    Eliptik integralin genliğe göre seri açılımından gelir. mertebe=2 ile
    yalnızca ilk düzeltme, mertebe=4 ile bir sonraki de dahil edilir.
    """
    duzeltme = 1.0 + theta0**2 / 16.0
    if mertebe >= 4:
        duzeltme += 11.0 * theta0**4 / 3072.0
    return T0 * duzeltme


# --------------------------------------------------------------------------
# 1. Yörünge karşılaştırması
# --------------------------------------------------------------------------

def yorunge_karsilastirmasi() -> None:
    import matplotlib.pyplot as plt

    fig, eksenler = plt.subplots(1, 3, figsize=(16, 5), sharey=False)
    genlikler = [np.deg2rad(a) for a in (10, 60, 150)]

    for ax, th0 in zip(eksenler, genlikler):
        sure = 4 * T0
        ts = np.linspace(0, sure, 4000)
        tam = solve_ivp(tam_sarkac, (0, sure), [th0, 0.0], t_eval=ts,
                        rtol=1e-11, atol=1e-13)
        har = solve_ivp(harmonik_sarkac, (0, sure), [th0, 0.0], t_eval=ts,
                        rtol=1e-11, atol=1e-13)

        ax.plot(ts, np.rad2deg(tam.y[0]), color=ortam.PALET["fonksiyon"],
                lw=2.2, label="tam: $\\ddot\\theta=-\\frac{g}{L}\\sin\\theta$")
        ax.plot(ts, np.rad2deg(har.y[0]), color=ortam.PALET["polinom"],
                lw=1.8, ls="--", label="harmonik: $\\ddot\\theta=-\\frac{g}{L}\\theta$")
        ax.set_xlabel("t (s)")
        ax.set_ylabel(r"$\theta$ (derece)")
        ax.set_title(f"$\\theta_0 = {np.rad2deg(th0):.0f}°$")
        if ax is eksenler[0]:
            ax.legend(fontsize=8, loc="lower left")

    fig.suptitle("Atılan $\\theta^3/6$ terimi genlik büyüdükçe geri dönüyor: "
                 "faz kayması birikiyor",
                 fontsize=14, color=ortam.PALET["fonksiyon"])
    fig.tight_layout()
    yol = ortam.gorsel_yolu("sarkac_yorungeler.png")
    fig.savefig(yol)
    plt.close(fig)
    print(f"  yazıldı: {yol.relative_to(ortam.PROJE_KOK)}")


# --------------------------------------------------------------------------
# 2. Periyot - genlik ilişkisi
# --------------------------------------------------------------------------

def periyot_tablosu() -> tuple[list[list[str]], np.ndarray, np.ndarray, np.ndarray]:
    dereceler = np.array([1, 5, 10, 20, 30, 45, 60, 90, 120, 150, 170], dtype=float)
    acilar = np.deg2rad(dereceler)

    olculen = np.array([periyodu_olc(a) for a in acilar])
    eliptik = np.array([tam_periyot_eliptik(a) for a in acilar])
    taylor2 = np.array([taylor_periyot(a, 2) for a in acilar])
    taylor4 = np.array([taylor_periyot(a, 4) for a in acilar])

    satirlar = []
    for d, o, e, t2, t4 in zip(dereceler, olculen, eliptik, taylor2, taylor4):
        satirlar.append([
            f"{d:.0f}°",
            f"{T0:.6f}",
            f"{o:.6f}",
            f"{e:.6f}",
            f"{abs(o - e) / e * 100:.2e}%",
            f"{t2:.6f}",
            f"{abs(t2 - e) / e * 100:.4f}%",
            f"{abs(t4 - e) / e * 100:.4f}%",
        ])
        print(f"  θ₀={d:>4.0f}°   ölçülen T={o:.6f}   eliptik T={e:.6f}   "
              f"(fark {abs(o-e)/e*100:.1e}%)   "
              f"Taylor-2 hatası {abs(t2-e)/e*100:6.3f}%   "
              f"Taylor-4 hatası {abs(t4-e)/e*100:6.4f}%")

    return satirlar, acilar, olculen, eliptik


def periyot_grafigi(acilar, olculen, eliptik) -> tuple[float, float]:
    """Periyot-genlik eğrisi + Taylor düzeltmesinin hata mertebesi.

    Döndürür: (Taylor-2 hatasının log-log eğimi, Taylor-4 eğimi).
    Beklenen: 4 ve 6 -- yani ilk düzeltmenin hatası O(theta^4), ikincisininki
    O(theta^6). Bu, seride bir sonraki terimin mertebesi olduğu için
    kaçınılmazdır.
    """
    import matplotlib.pyplot as plt

    fig, eksenler = plt.subplots(1, 2, figsize=(14, 5.5))

    # Sol: T(theta_0)
    ax = eksenler[0]
    ince = np.linspace(1e-3, np.deg2rad(175), 400)
    ax.plot(np.rad2deg(ince), [tam_periyot_eliptik(a) for a in ince],
            color=ortam.PALET["fonksiyon"], lw=2.4, label="tam (eliptik integral)")
    ax.plot(np.rad2deg(ince), [taylor_periyot(a, 2) for a in ince],
            color=ortam.PALET["polinom"], lw=1.8, ls="--",
            label=r"$T_0(1+\theta_0^2/16)$")
    ax.plot(np.rad2deg(ince), [taylor_periyot(a, 4) for a in ince],
            color=ortam.PALET["vurgu"], lw=1.6, ls="-.",
            label=r"$T_0(1+\theta_0^2/16+11\theta_0^4/3072)$")
    ax.axhline(T0, color=ortam.PALET["soluk"], ls=":", lw=1.4,
               label=r"harmonik $T_0$ (genlikten bağımsız)")
    ax.plot(np.rad2deg(acilar), olculen, "o", color=ortam.PALET["hata"], ms=6,
            label="solve_ivp ile ÖLÇÜLEN", zorder=5)
    ax.set_xlabel(r"$\theta_0$ (derece)")
    ax.set_ylabel("T (s)")
    ax.set_ylim(1.9, 4.2)
    ax.set_title("Periyot genliğe bağlı — izokronizm bir yaklaşımdı")
    ax.legend(fontsize=8)

    # Sağ: Taylor düzeltmelerinin hata mertebesi
    ax = eksenler[1]
    kucuk = np.deg2rad(np.logspace(np.log10(0.5), np.log10(40), 60))
    tam = np.array([tam_periyot_eliptik(a) for a in kucuk])
    h0 = np.abs(T0 - tam) / tam                                   # düzeltmesiz
    h2 = np.abs(np.array([taylor_periyot(a, 2) for a in kucuk]) - tam) / tam
    h4 = np.abs(np.array([taylor_periyot(a, 4) for a in kucuk]) - tam) / tam

    for dizi, etiket, renk in ((h0, r"harmonik $T_0$  (hata $\sim\theta_0^2$)",
                                ortam.PALET["sinir"]),
                               (h2, r"$+\theta_0^2/16$  (hata $\sim\theta_0^4$)",
                                ortam.PALET["polinom"]),
                               (h4, r"$+11\theta_0^4/3072$  (hata $\sim\theta_0^6$)",
                                ortam.PALET["vurgu"])):
        ax.loglog(np.rad2deg(kucuk), np.maximum(dizi, 1e-18), "o-", ms=3, lw=1.6,
                  color=renk, label=etiket)

    def egim(h):
        m = (h > 1e-15) & np.isfinite(h)
        return float(np.polyfit(np.log(kucuk[m]), np.log(h[m]), 1)[0])

    egim2, egim4 = egim(h2), egim(h4)
    ax.set_xlabel(r"$\theta_0$ (derece)")
    ax.set_ylabel("bağıl hata")
    ax.set_title(f"log-log eğimler:  {egim(h0):.2f},  {egim2:.2f},  {egim4:.2f}\n"
                 "her düzeltme mertebeyi tam 2 artırıyor")
    ax.legend(fontsize=8)

    fig.suptitle("Taylor'ın attığı terim periyotta geri dönüyor",
                 fontsize=14, color=ortam.PALET["fonksiyon"])
    fig.tight_layout()
    yol = ortam.gorsel_yolu("sarkac_periyot.png")
    fig.savefig(yol)
    plt.close(fig)
    print(f"  yazıldı: {yol.relative_to(ortam.PROJE_KOK)}")
    return egim2, egim4


# --------------------------------------------------------------------------

def main() -> int:
    ortam.baslik_yaz("1. Tam çözüm ile harmonik yaklaşımın yörüngeleri")
    print(f"  g = {G} m/s², L = {L} m,  harmonik periyot T₀ = {T0:.6f} s\n")
    yorunge_karsilastirmasi()

    ortam.baslik_yaz("2. Periyot - genlik: ölçüm, kapalı biçim, Taylor")
    print("  'ölçülen' = solve_ivp + olay tabanlı sıfır geçişi (rtol=1e-12)\n")
    satirlar, acilar, olculen, eliptik = periyot_tablosu()
    en_kotu = float(np.max(np.abs(olculen - eliptik) / eliptik))
    print(f"\n  Sayısal ölçüm ile kapalı biçim arasındaki en büyük fark: "
          f"{en_kotu*100:.2e}%  → çözücü doğru çalışıyor")

    ortam.baslik_yaz("3. Düzeltmelerin mertebesi")
    egim2, egim4 = periyot_grafigi(acilar, olculen, eliptik)
    print(f"  θ₀²/16 düzeltmesinin kalan hatası ~ θ₀^{egim2:.2f}  (beklenen 4)")
    print(f"  bir sonraki düzeltme ile      ~ θ₀^{egim4:.2f}  (beklenen 6)")

    icerik = (
        f"Sarkaç: `g = {G} m/s²`, `L = {L} m`, harmonik periyot "
        f"`T₀ = 2π√(L/g) = {T0:.6f} s`.\n\n"
        "`ölçülen T` sütunu, tam doğrusal-olmayan denklemin `solve_ivp` ile "
        "(`rtol=1e-12`) çözülüp periyodun **olay tabanlı sıfır geçişinden** "
        "okunmasıyla elde edildi — ızgaradan değil, adım aralığında kök "
        "bularak. `eliptik T` ise kapalı biçim "
        "`T = 4√(L/g)·K(sin²(θ₀/2))`.\n\n"
        + ortam.markdown_tablo(
            ["θ₀", "harmonik T₀", "ölçülen T", "eliptik T", "ölçüm-kapalı fark",
             "T₀(1+θ₀²/16)", "Taylor-2 hatası", "Taylor-4 hatası"],
            satirlar)
        + f"\n\nÖlçüm ile kapalı biçim arasındaki en büyük fark "
          f"**{en_kotu*100:.1e}%** — yani sayısal çözücü ile analitik sonuç "
          f"birbirini doğruluyor. Bundan sonraki her fark, Taylor kesmesinden "
          f"gelir, sayısal hatadan değil.\n\n"
        "## Atılan terim nereye gitti?\n\n"
        "`sin θ ≈ θ` yaklaşımı `−θ³/6` terimini atar. Harmonik osilatörde "
        "periyot genlikten **bağımsızdır** (izokronizm) — tabloda "
        "`harmonik T₀` sütunu sabittir. Gerçek sarkaçta ise periyot genlikle "
        "büyür: 10°'de fark binde 2, 90°'de %18, 170°'de iki katından fazla.\n\n"
        "Bu büyümenin ilk mertebesi tam olarak `θ₀²/16`'dır ve doğrudan "
        "atılan `θ³/6` teriminden doğar. Yani:\n\n"
        "> Atılan terim yok olmaz; sistemin gözlenebilir bir özelliğinde "
        "geri döner. Burada o özellik periyodun genliğe bağımlılığı, yani "
        "**anharmonisite**dir.\n\n"
        "## Mertebe kontrolü\n\n"
        f"Düzeltmelerin kalan hatası log-log eğimlerinden okundu:\n\n"
        f"* düzeltmesiz (`T₀` tek başına): hata ~ `θ₀^2`\n"
        f"* `+θ₀²/16` ile: hata ~ `θ₀^{egim2:.2f}`  (beklenen 4)\n"
        f"* `+11θ₀⁴/3072` ile: hata ~ `θ₀^{egim4:.2f}`  (beklenen 6)\n\n"
        "Her düzeltme mertebeyi tam olarak 2 artırıyor, çünkü periyodun "
        "genlik açılımı yalnızca çift kuvvetler içerir (`θ₀ → −θ₀` "
        "simetrisi). Bu, Taylor kesmesinin hata mertebesinin bir tahmin "
        "değil, **ölçülebilir bir öngörü** olduğunu gösterir."
    )
    ortam.tablo_yaz("sarkac.md", "Sarkaç: küçük açı yaklaşımının faturası", icerik)
    print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
