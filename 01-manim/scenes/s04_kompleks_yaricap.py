"""Sahne 4: Yakınsaklık yarıçapı kompleks düzlemin geometrisidir.

Bu laboratuvarın en önemli sahnesi. Anlatı üç perdede ilerler:

  1. REEL EKSEN. f(x) = 1/(1+x^2) burada kusursuzdur: her yerde tanımlı,
     sınırlı, sonsuz kez türevlenebilir. Ama Taylor polinomları tam x = ±1'de
     kopar. Reel eksende bunun sebebini gösteren HİÇBİR ŞEY yoktur.

  2. BİR BOYUT YUKARI. Ekseni kompleks düzleme açarız. z = ±i noktalarında
     fonksiyonun kutupları vardır ve bu noktalar orijine tam 1 uzaklıktadır.

  3. HARİTA. Kompleks düzlemde (1/N)·log|f - P_N| çizilir. Bu büyüklük
     log(|z-a|/R)'ye yakınsar; işareti yakınsaklığı söyler. N büyüdükçe
     harita ikiye ayrılır ve aradaki sınır KENDİLİĞİNDEN bir çember olur.
     Sonra merkez a kaydırılır: disk, tekilliğe olan uzaklığa göre yeniden
     boyutlanır. Yarıçap fonksiyonun değil, (fonksiyon, merkez) çiftinin
     özelliğidir.

Isı haritası numpy ile hesaplanıp ImageMobject olarak sahneye konur;
Manim'in nokta nokta çizmesini beklemek yerine tek seferde piksel üretmek
hem çok daha hızlı hem de çok daha keskin olur.

Render:  manim -qh 01-manim/scenes/s04_kompleks_yaricap.py KompleksYaricapSahnesi
"""

from __future__ import annotations

import math

import numpy as np
from manim import *

from tema import (DISK, FONKSIYON, KUCUK_BOYUT, POLINOM, SOLUK, TEKILLIK,
                  VURGU, baslik, etiket_kutusu, formul, hepsini_kapat,
                  sahne_kur)

PENCERE = 2.6        # harita [-PENCERE, PENCERE]^2 bölgesini kapsar
IZGARA = 420         # piksel (kare)


# --------------------------------------------------------------------------
# Matematik
# --------------------------------------------------------------------------

def katsayilar_1_bolu_1_arti_z2(a: float, N: int) -> np.ndarray:
    """1/(1+z^2)'nin a merkezli Taylor katsayıları — kapalı biçimden.

    1/(1+z^2) = 1/((z-i)(z+i)) kısmi kesirlere ayrılır:

        1/(1+z^2) = (i/2)/(z-i) - (i/2)/(z+i)

    Her bir 1/(z-p) terimi a etrafında geometrik seri olarak açılır:

        1/(z-p) = -1/(p-a) * 1/(1 - (z-a)/(p-a))
                = -sum_n (z-a)^n / (p-a)^(n+1)

    Sonuç reel çıkar (eşlenik kutuplar birbirini tamamlar). Bu yol sayısal
    türev almaktan çok daha kararlıdır ve N=40'a kadar rahatça gider.
    """
    kutuplar = [1j, -1j]
    # Kalıntılar: z=i'de 1/(i+i) = 1/(2i) = -i/2,  z=-i'de 1/(-2i) = +i/2.
    # (İşareti ters yazmak bütün seriyi -f'e çevirir ve hata haritası her
    #  yerde ıraksıyor gibi görünür; aşağıdaki a_0 kontrolü bunu yakalar.)
    kalintilar = [-0.5j, 0.5j]
    kats = np.zeros(N + 1, dtype=complex)
    for p, r in zip(kutuplar, kalintilar):
        for n in range(N + 1):
            kats[n] += -r / (p - a) ** (n + 1)

    # İki bağımsız akıl sağlığı kontrolü:
    assert np.max(np.abs(kats.imag)) < 1e-9, "katsayılar reel çıkmadı"
    a_0_beklenen = 1.0 / (1.0 + a * a)
    assert abs(kats[0].real - a_0_beklenen) < 1e-12, (
        f"a_0 = {kats[0].real} olmalıydı {a_0_beklenen}")
    return kats.real


def hata_haritasi(a: float, N: int, pencere: float, izgara: int) -> np.ndarray:
    """(1/N)·log10|f(z) - P_N(z)| dizisi (izgara x izgara)."""
    ekseni = np.linspace(a - pencere, a + pencere, izgara)
    dikey = np.linspace(-pencere, pencere, izgara)
    RE, IM = np.meshgrid(ekseni, dikey)
    Z = RE + 1j * IM

    with np.errstate(over="ignore", invalid="ignore", divide="ignore"):
        F = 1.0 / (1.0 + Z**2)
        kats = katsayilar_1_bolu_1_arti_z2(a, N)
        P = np.zeros_like(Z)
        guc = np.ones_like(Z)
        for c in kats:
            P = P + c * guc
            guc = guc * (Z - a)
        hata = np.abs(F - P)

    hata = np.where(np.isnan(hata), np.inf, hata)
    hata = np.maximum(hata, 1e-18)
    with np.errstate(divide="ignore", invalid="ignore"):
        L = np.log10(hata) / N
    return np.where(np.isfinite(L), L, 30.0 / N)


def haritayi_goruntule(L: np.ndarray) -> np.ndarray:
    """Haritayı RGB piksel dizisine çevirir (mavi: yakınsıyor, kırmızı: ıraksıyor).

    matplotlib'in RdBu_r paleti kullanılır; sıfır düzeyi paletin ortasına
    (beyaza) denk gelir, yani sınır kendiliğinden bir ışık halkası olur.
    """
    from matplotlib import colormaps

    norm = np.clip((L + 0.75) / 1.5, 0.0, 1.0)       # [-0.75, 0.75] -> [0,1]
    renkli = colormaps["RdBu_r"](norm)               # (H, W, 4) float
    # ImageMobject üst satırı yukarıda varsayar; meshgrid alt satırı -pencere
    # olarak üretti, bu yüzden dikeyde ters çevrilir.
    return (renkli[::-1, :, :3] * 255).astype(np.uint8)


# --------------------------------------------------------------------------

class KompleksYaricapSahnesi(Scene):
    def construct(self):
        sahne_kur(self)

        # ==============================================================
        # PERDE 1 — Reel eksende hiçbir ipucu yok
        # ==============================================================
        ust = baslik("Yakınsaklık yarıçapı",
                     "reel eksende değil, kompleks düzlemde yaşar")
        self.play(FadeIn(ust, shift=DOWN * 0.2), run_time=1.0)

        ax = Axes(x_range=[-2.6, 2.6, 1], y_range=[-0.4, 1.4, 0.5],
                  x_length=9.0, y_length=3.4,
                  axis_config={"color": SOLUK, "stroke_width": 2,
                               "include_tip": True, "tip_width": 0.15,
                               "tip_height": 0.15}).shift(DOWN * 1.0)

        f_egri = ax.plot(lambda x: 1.0 / (1.0 + x * x),
                         x_range=[-2.6, 2.6, 0.01],
                         color=FONKSIYON, stroke_width=5)
        f_etiket = formul(r"f(x)=\frac{1}{1+x^2}", boyut=34, renk=FONKSIYON)
        f_etiket.next_to(ax, UP, buff=0.25).shift(RIGHT * 3.0)

        self.play(Create(ax), run_time=1.0)
        self.play(Create(f_egri), FadeIn(f_etiket), run_time=1.8)

        temiz = Text("Reel eksende hiçbir sorun yok: sınırlı, pürüzsüz, "
                     "her yerde tanımlı.",
                     font_size=KUCUK_BOYUT, color=VURGU)
        temiz.next_to(ax, DOWN, buff=0.35)
        self.play(FadeIn(temiz), run_time=1.2)
        self.wait(1.8)
        self.play(FadeOut(temiz), run_time=0.5)

        # Polinomlar kopuyor
        def P_reel(N, x):
            kats = katsayilar_1_bolu_1_arti_z2(0.0, N)
            t = 0.0
            for n, c in enumerate(kats):
                t += c * x**n
            return float(np.clip(t, -0.5, 1.5))

        polinom = None
        derece_yazi = formul(r"P_4", boyut=30, renk=POLINOM)
        derece_yazi.next_to(ax, UP, buff=0.25).shift(LEFT * 3.4)
        for N in (4, 8, 16, 28):
            yeni = ax.plot(lambda x, N=N: P_reel(N, x),
                           x_range=[-2.6, 2.6, 0.008],
                           color=POLINOM, stroke_width=3.2)
            yeni_yazi = formul(rf"P_{{{N}}}", boyut=30, renk=POLINOM).move_to(derece_yazi)
            if polinom is None:
                self.play(Create(yeni), FadeIn(yeni_yazi), run_time=1.2)
                derece_yazi = yeni_yazi
            else:
                self.play(ReplacementTransform(polinom, yeni),
                          Transform(derece_yazi, yeni_yazi), run_time=1.0)
            polinom = yeni

        # x = ±1 çizgileri
        cizgiler = VGroup(*[
            DashedLine(ax.c2p(k, -0.4), ax.c2p(k, 1.4), color=DISK,
                       stroke_width=2.5, dash_length=0.1)
            for k in (-1.0, 1.0)])
        soru = Text("Neden tam burada kopuyor?", font_size=KUCUK_BOYUT, color=DISK)
        soru.next_to(ax, DOWN, buff=0.35)
        self.play(Create(cizgiler), FadeIn(soru), run_time=1.4)
        self.wait(2.2)

        self.play(FadeOut(VGroup(ax, f_egri, f_etiket, polinom, derece_yazi,
                                 cizgiler, soru)), run_time=1.0)

        # ==============================================================
        # PERDE 2 — Bir boyut yukarı
        # ==============================================================
        yeni_ust = baslik("Bir boyut yukarı",
                          "sebep reel eksende değil, kompleks düzlemde")
        self.play(Transform(ust, yeni_ust), run_time=1.0)

        # Harita alanının yerleşimi
        harita_boy = 6.0
        merkez_konum = DOWN * 0.55 + LEFT * 3.4

        def dunya(z: complex, a: float) -> np.ndarray:
            """Kompleks sayıyı sahne koordinatına çevirir."""
            olcek = harita_boy / (2 * PENCERE)
            return merkez_konum + np.array([(z.real - a) * olcek,
                                            z.imag * olcek, 0.0])

        # Kompleks düzlem ızgarası
        izgara = NumberPlane(
            x_range=[-PENCERE, PENCERE, 1], y_range=[-PENCERE, PENCERE, 1],
            x_length=harita_boy, y_length=harita_boy,
            background_line_style={"stroke_color": SOLUK, "stroke_width": 1,
                                   "stroke_opacity": 0.35},
            axis_config={"stroke_color": SOLUK, "stroke_width": 2},
        ).move_to(merkez_konum)
        self.play(Create(izgara), run_time=1.6)

        # Kutuplar
        kutup_ust = Dot(dunya(1j, 0.0), color=TEKILLIK, radius=0.09)
        kutup_alt = Dot(dunya(-1j, 0.0), color=TEKILLIK, radius=0.09)
        kutup_ust_e = formul("i", boyut=28, renk=TEKILLIK).next_to(kutup_ust, RIGHT, buff=0.15)
        kutup_alt_e = formul("-i", boyut=28, renk=TEKILLIK).next_to(kutup_alt, RIGHT, buff=0.15)
        merkez_nokta = Dot(dunya(0j, 0.0), color=VURGU, radius=0.07)
        merkez_e = formul("a=0", boyut=24, renk=VURGU).next_to(merkez_nokta, DL, buff=0.1)

        aciklama = VGroup(
            formul(r"\frac{1}{1+z^2}=\frac{1}{(z-i)(z+i)}", boyut=32, renk=FONKSIYON),
            Text("Payda z = ±i'de sıfırlanıyor:\nfonksiyon orada patlıyor.",
                 font_size=KUCUK_BOYUT, color=TEKILLIK, line_spacing=0.9),
        ).arrange(DOWN, buff=0.35)
        aciklama_kutu = etiket_kutusu(aciklama, renk=SOLUK)
        aciklama_kutu.scale(0.85).to_edge(RIGHT, buff=0.4).shift(DOWN * 0.2)

        self.play(FadeIn(merkez_nokta), FadeIn(merkez_e), run_time=0.6)
        self.play(FadeIn(kutup_ust, scale=1.6), FadeIn(kutup_alt, scale=1.6),
                  FadeIn(kutup_ust_e), FadeIn(kutup_alt_e), run_time=1.0)
        self.play(FadeIn(aciklama_kutu, shift=LEFT * 0.2), run_time=1.3)
        self.wait(1.5)

        # Uzaklık oku
        ok = Arrow(dunya(0j, 0.0), dunya(1j, 0.0), color=DISK,
                   buff=0.08, stroke_width=4, max_tip_length_to_length_ratio=0.15)
        ok_etiket = formul(r"|0-i|=1", boyut=26, renk=DISK)
        ok_etiket.next_to(ok, LEFT, buff=0.12)
        self.play(GrowArrow(ok), FadeIn(ok_etiket), run_time=1.2)
        self.wait(1.8)

        self.play(FadeOut(aciklama_kutu), run_time=0.6)

        # ==============================================================
        # PERDE 3 — Harita: disk kendiliğinden beliriyor
        # ==============================================================
        yeni_ust2 = baslik("Disk kendiliğinden beliriyor",
                           "renk: (1/N)·log|f − P_N| — mavi yakınsıyor, kırmızı ıraksıyor")
        self.play(Transform(ust, yeni_ust2), run_time=1.0)

        bilgi = VGroup(
            formul(r"N = 2", boyut=32, renk=POLINOM),
            Text("sınır henüz bulanık", font_size=KUCUK_BOYUT, color=SOLUK),
        ).arrange(DOWN, buff=0.2)
        bilgi_kutu = etiket_kutusu(bilgi, renk=SOLUK)
        bilgi_kutu.to_edge(RIGHT, buff=0.55).shift(UP * 1.0)
        self.play(FadeIn(bilgi_kutu), run_time=0.6)

        def resim_yap(a: float, N: int) -> ImageMobject:
            gorsel = ImageMobject(haritayi_goruntule(hata_haritasi(a, N, PENCERE, IZGARA)))
            gorsel.height = harita_boy
            gorsel.move_to(merkez_konum)
            gorsel.set_z_index(-5)      # ızgara ve noktalar üstte kalsın
            return gorsel

        resim = resim_yap(0.0, 2)
        self.play(FadeIn(resim), izgara.animate.set_opacity(0.25), run_time=1.4)
        self.wait(0.8)

        aciklamalar = {
            4: "sınır belirmeye başlıyor",
            8: "çember netleşiyor",
            16: "kutuplardan tam\n1 uzaklıkta",
            30: "N büyüdükçe sınır\nkeskinleşiyor",
        }
        for N in (4, 8, 16, 30):
            yeni_resim = resim_yap(0.0, N)
            yeni_bilgi = VGroup(
                formul(rf"N = {N}", boyut=32, renk=POLINOM),
                Text(aciklamalar[N], font_size=KUCUK_BOYUT, color=SOLUK),
            ).arrange(DOWN, buff=0.2).move_to(bilgi)
            self.play(FadeIn(yeni_resim), FadeOut(resim),
                      Transform(bilgi, yeni_bilgi), run_time=1.1)
            self.remove(resim)
            resim = yeni_resim
            self.wait(0.5)

        # Teorik çember üstüne
        cember = Circle(radius=harita_boy / (2 * PENCERE), color=DISK,
                        stroke_width=3.5).move_to(merkez_konum)
        cember_e = Text("R = 1", font_size=KUCUK_BOYUT, color=DISK)
        cember_e.next_to(cember, UP, buff=0.12)
        self.play(Create(cember), FadeIn(cember_e), run_time=1.5)
        self.wait(2.0)

        # ==============================================================
        # PERDE 4 — Merkezi kaydır: yarıçap tekilliğe göre değişir
        # ==============================================================
        yeni_ust3 = baslik("Merkezi kaydır, yarıçap değişir",
                           "R = merkezden en yakın tekilliğe uzaklık")
        self.play(Transform(ust, yeni_ust3), run_time=1.0)
        self.play(FadeOut(ok), FadeOut(ok_etiket), FadeOut(cember_e), run_time=0.6)

        for a_yeni in (0.7, 1.4, 2.0):
            R_yeni = math.hypot(a_yeni, 1.0)     # |a - i|
            yeni_resim = resim_yap(a_yeni, 30)
            yeni_cember = Circle(radius=R_yeni * harita_boy / (2 * PENCERE),
                                 color=DISK, stroke_width=3.5).move_to(merkez_konum)
            yeni_merkez = Dot(dunya(complex(a_yeni, 0), a_yeni), color=VURGU, radius=0.07)
            yeni_merkez_e = formul(rf"a={a_yeni}", boyut=24, renk=VURGU).next_to(
                yeni_merkez, DL, buff=0.1)
            # Kutuplar sabit; ama harita a merkezli kaydığı için ekranda kayarlar
            yeni_kutup_ust = Dot(dunya(1j, a_yeni), color=TEKILLIK, radius=0.09)
            yeni_kutup_alt = Dot(dunya(-1j, a_yeni), color=TEKILLIK, radius=0.09)
            yeni_bilgi = VGroup(
                formul(rf"a = {a_yeni}", boyut=30, renk=VURGU),
                formul(rf"R=|a-i|={R_yeni:.4f}", boyut=26, renk=DISK),
            ).arrange(DOWN, buff=0.2).move_to(bilgi)

            self.play(
                FadeIn(yeni_resim), FadeOut(resim),
                Transform(cember, yeni_cember),
                Transform(merkez_nokta, yeni_merkez),
                Transform(merkez_e, yeni_merkez_e),
                Transform(kutup_ust, yeni_kutup_ust),
                Transform(kutup_alt, yeni_kutup_alt),
                kutup_ust_e.animate.next_to(yeni_kutup_ust, RIGHT, buff=0.15),
                kutup_alt_e.animate.next_to(yeni_kutup_alt, RIGHT, buff=0.15),
                Transform(bilgi, yeni_bilgi),
                run_time=1.8)
            self.remove(resim)
            resim = yeni_resim
            self.wait(1.4)

        mesaj = Text(
            "Yarıçap fonksiyonun değil,\n"
            "(fonksiyon, merkez) çiftinin\n"
            "özelliğidir.\n"
            "\n"
            "Reel eksende hiçbir şey\n"
            "olmuyor — sınırı koyan, bir\n"
            "boyut yukarıdaki tekilliğe\n"
            "olan uzaklık.",
            font_size=KUCUK_BOYUT, color=FONKSIYON, line_spacing=0.95)
        mesaj_kutu = etiket_kutusu(mesaj, renk=DISK)
        mesaj_kutu.set_z_index(10)      # ısı haritasının üstünde kalsın
        mesaj_kutu.scale(0.92).to_edge(RIGHT, buff=0.45).shift(DOWN * 1.4)
        self.play(FadeIn(mesaj_kutu, shift=UP * 0.2), run_time=1.3)
        self.wait(4.0)

        hepsini_kapat(self)
