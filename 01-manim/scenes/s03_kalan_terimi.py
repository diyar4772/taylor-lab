"""Sahne 3: Lagrange kalanı — gerçek hata ile sınır aynı eksende.

Anlatı:
  Taylor teoremi bir yaklaşım tavsiyesi değil, bir EŞİTLİKTİR:

      f(x) = P_N(x) + f^(N+1)(ksi)/(N+1)! * (x-a)^(N+1)

  Sağdaki son terim "kalan"dır ve bir üst sınırı vardır. Sahnede gerçek hata
  (düz çizgi) ile bu sınır (kesikli) aynı log eksende çizilir; sınır hiçbir
  zaman altta kalmaz. N büyüdükçe ikisi birlikte aşağı iner ve eğim dikleşir
  -- yani yakınsama hızlanır.

Sayılar sahnede uydurulmaz; aynı formüllerden anlık hesaplanır.

Render:  manim -qh 01-manim/scenes/s03_kalan_terimi.py KalanTerimiSahnesi
"""

from __future__ import annotations

import math

import numpy as np
from manim import *

from tema import (FONKSIYON, HATA, KUCUK_BOYUT, POLINOM, SINIR, SOLUK, VURGU,
                  baslik, eksen, etiket_kutusu, formul, hepsini_kapat,
                  sahne_kur)

DERECELER = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]


def sin_polinom(N: int, x):
    """sin(x)'in N. dereceden Maclaurin polinomu."""
    toplam = np.zeros_like(np.asarray(x, dtype=float))
    for n in range(1, N + 1, 2):
        toplam = toplam + (-1.0) ** ((n - 1) // 2) / math.factorial(n) * np.asarray(x, float) ** n
    return toplam


def gercek_hata(N: int, x):
    return np.abs(np.sin(np.asarray(x, float)) - sin_polinom(N, x))


def lagrange_sinir(N: int, x):
    """|R_N(x)| <= sup|f^(N+1)| / (N+1)! * |x|^(N+1).

    sin'in tüm türevleri mutlak değerce 1'i geçmez, bu yüzden supremum tam
    olarak 1'dir -- kestirmeye gerek yok, sınır kapalı biçimde bilinir.
    """
    return np.abs(np.asarray(x, float)) ** (N + 1) / math.factorial(N + 1)


class KalanTerimiSahnesi(Scene):
    def construct(self):
        sahne_kur(self)

        ust = baslik("Lagrange kalanı", "bu bir yaklaşım değil, eşitlik")
        self.play(FadeIn(ust, shift=DOWN * 0.2), run_time=1.0)

        # --- Teorem ---
        teorem = formul(
            r"f(x)=P_N(x)+\underbrace{\frac{f^{(N+1)}(\xi)}{(N+1)!}(x-a)^{N+1}}"
            r"_{\text{kalan } R_N(x)}",
            boyut=38, renk=FONKSIYON)
        teorem.shift(UP * 0.8)
        self.play(Write(teorem), run_time=2.4)
        self.wait(1.0)

        vurgu = Text("ξ, a ile x arasında GERÇEKTEN var olan bir sayı — "
                     "eşitlik tam olarak sağlanır.",
                     font_size=KUCUK_BOYUT, color=VURGU)
        vurgu.next_to(teorem, DOWN, buff=0.6)
        self.play(FadeIn(vurgu, shift=UP * 0.15), run_time=1.2)
        self.wait(2.0)
        self.play(FadeOut(teorem), FadeOut(vurgu), run_time=0.8)

        # --------------------------------------------------------------
        # Log eksende hata ve sınır
        # --------------------------------------------------------------
        alt_us, ust_us = -14, 2          # 10^-14 .. 10^2
        ax = Axes(
            x_range=[0, 4, 1], y_range=[alt_us, ust_us, 2],
            x_length=8.4, y_length=4.3,
            axis_config={"color": SOLUK, "stroke_width": 2,
                         "include_tip": True, "tip_width": 0.16,
                         "tip_height": 0.16},
        ).shift(DOWN * 0.75)

        x_etiket = MathTex("x", font_size=26, color=SOLUK).next_to(
            ax.x_axis.get_end(), DR, buff=0.12)
        y_etiket = MathTex(r"\log_{10}|\text{hata}|", font_size=24,
                           color=SOLUK).next_to(ax.y_axis.get_end(), UP, buff=0.15)

        # y ekseni işaretleri
        y_isaretler = VGroup()
        for us in range(alt_us, ust_us + 1, 2):
            t = MathTex(f"10^{{{us}}}", font_size=20, color=SOLUK)
            t.next_to(ax.c2p(0, us), LEFT, buff=0.18)
            y_isaretler.add(t)
        x_isaretler = VGroup()
        for xv in (1, 2, 3, 4):
            t = MathTex(str(xv), font_size=22, color=SOLUK)
            t.next_to(ax.c2p(xv, alt_us), DOWN, buff=0.18)
            x_isaretler.add(t)

        self.play(Create(ax), FadeIn(x_etiket), FadeIn(y_etiket),
                  FadeIn(y_isaretler), FadeIn(x_isaretler), run_time=1.6)

        def log_kirp(dizi):
            return np.clip(np.log10(np.maximum(dizi, 1e-300)), alt_us - 1, ust_us + 1)

        def hata_egrisi(N):
            return ax.plot(
                lambda x: float(log_kirp(gercek_hata(N, np.array([max(x, 1e-6)])))[0]),
                x_range=[0.02, 4, 0.01], color=HATA, stroke_width=5.0)

        def sinir_egrisi(N):
            # Kesikli çizilir: N büyüdükçe sınır gerçek hataya o kadar
            # yaklaşır ki (N=10, x=2 için oran 0.97) düz çizilseydi altında
            # tamamen kaybolurdu. Görsel olarak ayırt edilebilmesi şart.
            duz = ax.plot(
                lambda x: float(log_kirp(lagrange_sinir(N, np.array([max(x, 1e-6)])))[0]),
                x_range=[0.02, 4, 0.01], color=SINIR, stroke_width=4.5)
            kesikli = DashedVMobject(duz, num_dashes=90, dashed_ratio=0.55)
            kesikli.set_z_index(5)   # hata eğrisinin ÜSTÜNDE kalsın
            return kesikli

        # Gösterge
        gosterge = VGroup(
            VGroup(Line(ORIGIN, RIGHT * 0.5, color=HATA, stroke_width=4),
                   Text("gerçek hata  |f − P_N|", font_size=KUCUK_BOYUT,
                        color=HATA)).arrange(RIGHT, buff=0.2),
            VGroup(Line(ORIGIN, RIGHT * 0.5, color=SINIR, stroke_width=3),
                   Text("Lagrange sınırı  |x|^(N+1)/(N+1)!", font_size=KUCUK_BOYUT,
                        color=SINIR)).arrange(RIGHT, buff=0.2),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        gosterge_kutu = etiket_kutusu(gosterge, renk=SOLUK)
        gosterge_kutu.scale(0.85).to_corner(UR, buff=0.25).shift(DOWN * 1.15)

        derece = formul(r"N = 1", boyut=34, renk=POLINOM)
        derece_kutu = etiket_kutusu(derece, renk=SOLUK)
        derece_kutu.to_corner(UL, buff=0.25).shift(DOWN * 1.15)

        h = hata_egrisi(1)
        s = sinir_egrisi(1)
        self.play(Create(s), Create(h), FadeIn(gosterge_kutu),
                  FadeIn(derece_kutu), run_time=1.8)
        self.wait(0.8)

        # N'i artır
        for N in DERECELER[1:]:
            yeni_h, yeni_s = hata_egrisi(N), sinir_egrisi(N)
            yeni_derece = formul(rf"N = {N}", boyut=34, renk=POLINOM).move_to(derece)
            self.play(ReplacementTransform(h, yeni_h),
                      ReplacementTransform(s, yeni_s),
                      Transform(derece, yeni_derece),
                      run_time=0.95)
            h, s = yeni_h, yeni_s
            self.wait(0.15)

        self.wait(0.8)

        # --- Sayısal doğrulama: bir noktada oran ---
        x_test = 2.0
        N_test = DERECELER[-1]
        gh = float(gercek_hata(N_test, np.array([x_test]))[0])
        ls = float(lagrange_sinir(N_test, np.array([x_test]))[0])
        nokta_h = Dot(ax.c2p(x_test, float(log_kirp(np.array([gh]))[0])),
                      color=HATA, radius=0.075)
        nokta_s = Dot(ax.c2p(x_test, float(log_kirp(np.array([ls]))[0])),
                      color=SINIR, radius=0.075)
        bag = DashedLine(nokta_h.get_center(), nokta_s.get_center(),
                         color=VURGU, stroke_width=2.5, dash_length=0.08)

        olcum = VGroup(
            Text(f"x = {x_test},  N = {N_test}", font_size=KUCUK_BOYUT, color=FONKSIYON),
            MathTex(rf"|f-P_N| = {gh:.3e}".replace("e-", r"\times 10^{-") + "}",
                    font_size=24, color=HATA),
            MathTex(rf"\text{{sınır}} = {ls:.3e}".replace("e-", r"\times 10^{-") + "}",
                    font_size=24, color=SINIR),
            MathTex(rf"\text{{oran}} = {gh/ls:.4f} \le 1", font_size=26, color=VURGU),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        olcum_kutu = etiket_kutusu(olcum, renk=VURGU)
        olcum_kutu.scale(0.8).to_corner(DR, buff=0.3)

        self.play(FadeIn(nokta_h), FadeIn(nokta_s), Create(bag), run_time=1.0)
        self.play(FadeIn(olcum_kutu, shift=UP * 0.2), run_time=1.2)
        self.wait(3.0)

        mesaj = Text("Sınır hiçbir zaman altta kalmıyor. N büyüdükçe eğim "
                     "dikleşiyor:\nyakınsama hızlanıyor.",
                     font_size=KUCUK_BOYUT, color=FONKSIYON, line_spacing=0.95)
        mesaj_kutu = etiket_kutusu(mesaj, renk=SOLUK)
        mesaj_kutu.scale(0.85).to_corner(DL, buff=0.3)
        self.play(FadeIn(mesaj_kutu, shift=UP * 0.2), run_time=1.2)
        self.wait(3.0)

        hepsini_kapat(self)
