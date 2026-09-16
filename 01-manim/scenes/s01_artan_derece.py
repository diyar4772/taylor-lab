"""Sahne 1: Artan derece — polinomlar sin(x) üzerine sırayla oturuyor.

Anlatı:
  N=1'de yalnızca teğet doğru var; yaklaşım merkezin hemen yanında iyi,
  uzakta umutsuz. N büyüdükçe iyi davranan bölge merkezden DIŞARI DOĞRU
  büyür. Ama bu büyüme, "her yerde iyi olma"ya doğru gitmez -- her sonlu N
  için bir yerden sonra polinom kaçar. sin için R = sonsuz olduğundan
  N -> sonsuz limitinde bölge tüm ekseni kaplar; bunu görmek için N'in
  15'e kadar çıkması yeter.

Render:  manim -qh 01-manim/scenes/s01_artan_derece.py ArtanDereceSahnesi
"""

from __future__ import annotations

import math

import numpy as np
from manim import *

from tema import (DERECE_RENKLERI, FONKSIYON, KUCUK_BOYUT, POLINOM, SOLUK,
                  VURGU, baslik, eksen, etiket_kutusu, formul, hepsini_kapat,
                  merkez_noktasi, sahne_kur)

DERECELER = [1, 3, 5, 7, 9, 11, 13, 15]


def sin_taylor(N: int):
    """sin(x)'in N. dereceden Maclaurin polinomu (katsayılar tanımdan).

    sin'in 0'daki türevleri 0, 1, 0, -1, 0, 1, ... diye devreder; çift
    mertebeli türevler sıfır olduğu için seri yalnızca tek kuvvetler içerir.
    Katsayı a_n = f^(n)(0)/n! tanımından doğrudan yazılır.
    """
    katsayilar = []
    for n in range(N + 1):
        if n % 2 == 0:
            katsayilar.append(0.0)
        else:
            isaret = (-1.0) ** ((n - 1) // 2)
            katsayilar.append(isaret / float(math.factorial(n)))

    def P(x):
        toplam = 0.0
        for n, c in enumerate(katsayilar):
            if c != 0.0:
                toplam = toplam + c * x**n
        return toplam

    return P


def iyi_bolge(N: int, tolerans: float = 0.05, ust: float = 10.0) -> float:
    """|sin(x) - P_N(x)| < tolerans koşulunun bozulduğu ilk x (merkezden sağa).

    "Yaklaşımın geçerli olduğu bölge" bir metafor değil; ölçülebilir bir
    büyüklüktür. Sahnede büyüyen bant tam olarak budur.
    """
    P = sin_taylor(N)
    xs = np.linspace(0, ust, 4000)
    hata = np.abs(np.sin(xs) - P(xs))
    kotu = np.nonzero(hata > tolerans)[0]
    return float(xs[kotu[0]]) if kotu.size else ust


class ArtanDereceSahnesi(Scene):
    def construct(self):
        sahne_kur(self)

        ust = baslik("Artan derece", "sin(x) üzerine oturan Taylor polinomları")
        self.play(FadeIn(ust, shift=DOWN * 0.2), run_time=1.0)

        ax, eksen_etiketleri = eksen((-8, 8, 2), (-3, 3, 1),
                                     x_uzunluk=11.5, y_uzunluk=4.6)
        ax.shift(DOWN * 0.55)
        eksen_etiketleri.shift(DOWN * 0.55)

        egri = ax.plot(np.sin, x_range=[-8, 8, 0.02], color=FONKSIYON,
                       stroke_width=4.5)
        egri_etiket = formul(r"f(x)=\sin x", boyut=30, renk=FONKSIYON)
        egri_etiket.next_to(ax.c2p(6.4, 1.0), UR, buff=0.05)

        self.play(Create(ax), FadeIn(eksen_etiketleri), run_time=1.2)
        self.play(Create(egri), FadeIn(egri_etiket), run_time=1.6)

        merkez = merkez_noktasi(ax, 0.0, "a=0")
        self.play(FadeIn(merkez, scale=1.4), run_time=0.8)
        self.wait(0.4)

        # --- Derece sayacı ve hata bilgisi kutusu ---
        derece_yazi = formul(r"N = 1", boyut=34, renk=POLINOM)
        bolge_yazi = Text("geçerli bölge: |x| < 0.6",
                          font_size=KUCUK_BOYUT, color=VURGU)
        kutu = etiket_kutusu(derece_yazi, bolge_yazi, renk=SOLUK)
        kutu.to_corner(UL, buff=0.45).shift(DOWN * 0.9)
        self.play(FadeIn(kutu), run_time=0.6)

        # --- Geçerli bölgeyi gösteren bant ---
        def bant_yap(genislik: float) -> Rectangle:
            sol, sag = ax.c2p(-genislik, -3)[0], ax.c2p(genislik, -3)[0]
            alt, ust_y = ax.c2p(0, -3)[1], ax.c2p(0, 3)[1]
            r = Rectangle(width=sag - sol, height=ust_y - alt,
                          stroke_width=0, fill_color=VURGU, fill_opacity=0.10)
            r.move_to(ax.c2p(0, 0))
            return r

        mevcut_bant = bant_yap(iyi_bolge(1))
        self.play(FadeIn(mevcut_bant), run_time=0.6)

        # --- Polinomları sırayla çiz ---
        mevcut_polinom = None
        for i, N in enumerate(DERECELER):
            renk = DERECE_RENKLERI[i % len(DERECE_RENKLERI)]
            P = sin_taylor(N)
            # Ekranın dışına taşan kısımları kırp: yüksek dereceli polinomlar
            # kenarda 10^3 mertebesine fırlar ve eksen takımını ezer.
            yeni = ax.plot(lambda x, P=P: float(np.clip(P(x), -3.2, 3.2)),
                           x_range=[-8, 8, 0.01], color=renk, stroke_width=3.4)

            g = iyi_bolge(N)
            yeni_derece = formul(rf"N = {N}", boyut=34, renk=renk).move_to(derece_yazi)
            yeni_bolge = Text(f"geçerli bölge: |x| < {g:.1f}",
                              font_size=KUCUK_BOYUT, color=VURGU).move_to(bolge_yazi)
            yeni_bant = bant_yap(g)

            if mevcut_polinom is None:
                self.play(Create(yeni), Transform(derece_yazi, yeni_derece),
                          Transform(bolge_yazi, yeni_bolge),
                          Transform(mevcut_bant, yeni_bant), run_time=1.5)
            else:
                self.play(ReplacementTransform(mevcut_polinom, yeni),
                          Transform(derece_yazi, yeni_derece),
                          Transform(bolge_yazi, yeni_bolge),
                          Transform(mevcut_bant, yeni_bant),
                          run_time=1.25)
            mevcut_polinom = yeni
            self.wait(0.35)

        self.wait(0.8)

        # --- Kapanış mesajı ---
        mesaj = Text(
            "İyi davranan bölge merkezden dışarı doğru büyüyor.\n"
            "sin için R = ∞ — ama her SONLU N'de polinom bir yerden sonra kaçar.",
            font_size=KUCUK_BOYUT, color=FONKSIYON, line_spacing=0.9)
        mesaj_kutu = etiket_kutusu(mesaj, renk=VURGU)
        mesaj_kutu.to_edge(DOWN, buff=0.3)
        self.play(FadeIn(mesaj_kutu, shift=UP * 0.2), run_time=1.2)
        self.wait(3.0)
        hepsini_kapat(self)
