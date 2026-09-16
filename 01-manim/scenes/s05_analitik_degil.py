"""Sahne 5: Pürüzsüz ama analitik değil — e^(-1/x^2).

Anlatı:
  Bu fonksiyon sonsuz kez türevlenebilir ve 0'daki TÜM türevleri sıfırdır.
  Dolayısıyla Maclaurin serisi 0 + 0x + 0x^2 + ... = 0'dır. Seri her x için
  yakınsar (R = sonsuz) ama yakınsadığı şey sıfır fonksiyonudur -- oysa f,
  x != 0 için asla sıfır değildir.

  Buradan çıkan ders: "Taylor serisi yakınsıyor" demek "fonksiyona eşit"
  demek DEĞİLDİR. Pürüzsüzlük (C^oo) analitiklikten (C^omega) kesinlikle
  zayıftır.

  Sebep yine kompleks düzlemdedir: z = iy boyunca -1/z^2 = +1/y^2 olur ve
  e^(1/y^2) patlar. Aynı noktaya reel eksenden 0, hayali eksenden sonsuz
  gelmek, orada bir esas tekillik olduğunu söyler.

Render:  manim -qh 01-manim/scenes/s05_analitik_degil.py AnalitikDegilSahnesi
"""

from __future__ import annotations

import numpy as np
from manim import *

from tema import (FONKSIYON, HATA, KUCUK_BOYUT, POLINOM, SOLUK, TEKILLIK,
                  VURGU, baslik, etiket_kutusu, formul, hepsini_kapat,
                  sahne_kur)


def f_guvenli(x: float) -> float:
    """e^(-1/x^2), x=0'da 0 — taşma/sıfıra bölme korumalı."""
    if abs(x) < 1e-8:
        return 0.0
    us = -1.0 / (x * x)
    return float(np.exp(us)) if us > -700 else 0.0


class AnalitikDegilSahnesi(Scene):
    def construct(self):
        sahne_kur(self)

        ust = baslik("Pürüzsüz ama analitik değil",
                     "yakınsamak, eşit olmak demek değildir")
        self.play(FadeIn(ust, shift=DOWN * 0.2), run_time=1.0)

        tanim = formul(
            r"f(x)=\begin{cases} e^{-1/x^2} & x\neq 0\\[4pt] 0 & x=0\end{cases}",
            boyut=38, renk=FONKSIYON)
        tanim.shift(UP * 1.3)
        self.play(Write(tanim), run_time=2.2)
        self.wait(1.2)

        # --------------------------------------------------------------
        # Türevler sırayla sıfır çıkıyor
        # --------------------------------------------------------------
        turevler = VGroup(*[
            formul(rf"f^{{({n})}}(0)=0", boyut=30, renk=VURGU)
            for n in range(6)
        ]).arrange_in_grid(rows=2, cols=3, buff=(1.0, 0.45))
        turevler.next_to(tanim, DOWN, buff=0.75)

        for t in turevler:
            self.play(FadeIn(t, scale=1.2), run_time=0.45)
        self.wait(0.6)

        nokta_nokta = formul(r"\cdots\ \text{ve bu sonsuza kadar sürüyor}",
                             boyut=28, renk=SOLUK)
        nokta_nokta.next_to(turevler, DOWN, buff=0.45)
        self.play(FadeIn(nokta_nokta), run_time=1.0)
        self.wait(1.5)

        # Seri
        seri = formul(r"\Rightarrow\quad \sum_{n=0}^{\infty}\frac{f^{(n)}(0)}{n!}x^n"
                      r"\;=\;0+0\cdot x+0\cdot x^2+\cdots\;=\;0",
                      boyut=34, renk=HATA)
        seri.next_to(nokta_nokta, DOWN, buff=0.5)
        self.play(Write(seri), run_time=2.2)
        self.wait(2.0)

        self.play(FadeOut(VGroup(tanim, turevler, nokta_nokta, seri)), run_time=0.9)

        # --------------------------------------------------------------
        # Grafik: f ile sıfır serisi yan yana
        # --------------------------------------------------------------
        ax = Axes(x_range=[-2.2, 2.2, 1], y_range=[-0.15, 1.1, 0.5],
                  x_length=9.5, y_length=4.0,
                  axis_config={"color": SOLUK, "stroke_width": 2,
                               "include_tip": True, "tip_width": 0.15,
                               "tip_height": 0.15}).shift(DOWN * 0.7)

        f_egri = ax.plot(f_guvenli, x_range=[-2.2, 2.2, 0.005],
                         color=FONKSIYON, stroke_width=5)
        sifir_egri = ax.plot(lambda x: 0.0, x_range=[-2.2, 2.2, 0.01],
                             color=HATA, stroke_width=4)
        sifir_kesikli = DashedVMobject(sifir_egri, num_dashes=60, dashed_ratio=0.55)
        sifir_kesikli.set_z_index(3)

        self.play(Create(ax), run_time=1.0)
        self.play(Create(f_egri), run_time=1.8)

        f_etiket = formul(r"f(x)=e^{-1/x^2}", boyut=30, renk=FONKSIYON)
        f_etiket.next_to(ax.c2p(1.7, 0.78), UR, buff=0.05)
        self.play(FadeIn(f_etiket), run_time=0.7)
        self.wait(0.6)

        self.play(Create(sifir_kesikli), run_time=1.4)
        seri_etiket = formul(r"\text{Maclaurin serisi}\equiv 0", boyut=28, renk=HATA)
        seri_etiket.next_to(ax.c2p(-1.6, 0.0), UP, buff=0.35)
        self.play(FadeIn(seri_etiket), run_time=0.8)
        self.wait(1.5)

        # Fark oku
        x_isaret = 1.0
        y_isaret = f_guvenli(x_isaret)
        fark_ok = DoubleArrow(ax.c2p(x_isaret, 0.0), ax.c2p(x_isaret, y_isaret),
                              color=VURGU, buff=0.03, stroke_width=3.5,
                              max_tip_length_to_length_ratio=0.12)
        fark_e = formul(rf"f(1)={y_isaret:.4f}\neq 0", boyut=26, renk=VURGU)
        fark_e.next_to(fark_ok, RIGHT, buff=0.2)
        self.play(GrowFromCenter(fark_ok), FadeIn(fark_e), run_time=1.2)
        self.wait(2.2)

        ders = Text("Seri her x için yakınsıyor — ama f'e değil, sıfıra.",
                    font_size=KUCUK_BOYUT, color=FONKSIYON)
        ders_kutu = etiket_kutusu(ders, renk=HATA)
        ders_kutu.to_edge(DOWN, buff=0.3)
        self.play(FadeIn(ders_kutu, shift=UP * 0.2), run_time=1.2)
        self.wait(2.5)

        self.play(FadeOut(VGroup(ax, f_egri, sifir_kesikli, f_etiket,
                                 seri_etiket, fark_ok, fark_e, ders_kutu)),
                  run_time=0.9)

        # --------------------------------------------------------------
        # Sebep: kompleks düzlemde esas tekillik
        # --------------------------------------------------------------
        yeni_ust = baslik("Sebep yine kompleks düzlemde",
                          "z = 0'a iki yönden yaklaşın")
        self.play(Transform(ust, yeni_ust), run_time=1.0)

        sol = VGroup(
            Text("reel eksen boyunca  z = x", font_size=KUCUK_BOYUT, color=POLINOM),
            formul(r"-\frac{1}{x^2}<0 \;\Rightarrow\; e^{-1/x^2}\to 0",
                   boyut=30, renk=POLINOM),
        ).arrange(DOWN, buff=0.3)
        sag = VGroup(
            Text("hayali eksen boyunca  z = iy", font_size=KUCUK_BOYUT, color=TEKILLIK),
            formul(r"-\frac{1}{(iy)^2}=+\frac{1}{y^2}>0 \;\Rightarrow\; e^{1/y^2}\to\infty",
                   boyut=30, renk=TEKILLIK),
        ).arrange(DOWN, buff=0.3)

        sol_kutu = etiket_kutusu(sol, renk=POLINOM)
        sag_kutu = etiket_kutusu(sag, renk=TEKILLIK)
        ikisi = VGroup(sol_kutu, sag_kutu).arrange(DOWN, buff=0.55).shift(UP * 0.35)

        self.play(FadeIn(sol_kutu, shift=RIGHT * 0.2), run_time=1.2)
        self.wait(1.2)
        self.play(FadeIn(sag_kutu, shift=LEFT * 0.2), run_time=1.2)
        self.wait(1.8)

        # Somut sayılar
        tablo = VGroup(
            Text("|z| = 0.05 için:", font_size=KUCUK_BOYUT, color=FONKSIYON),
            formul(r"\text{reel:}\ \ 1.9\times 10^{-174}", boyut=26, renk=POLINOM),
            formul(r"\text{hayali:}\ 5.2\times 10^{+173}", boyut=26, renk=TEKILLIK),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        tablo_kutu = etiket_kutusu(tablo, renk=SOLUK)
        tablo_kutu.next_to(ikisi, DOWN, buff=0.5)
        self.play(FadeIn(tablo_kutu), run_time=1.2)
        self.wait(2.2)

        sonuc = Text(
            "Aynı noktaya iki yönden yaklaşıp biri 0, diğeri ∞ veriyorsa\n"
            "orada limit yoktur: z = 0 bir ESAS TEKİLLİKTİR.\n"
            "Reel eksende bunun hiçbir izi görünmez.",
            font_size=KUCUK_BOYUT, color=FONKSIYON, line_spacing=0.95)
        sonuc_kutu = etiket_kutusu(sonuc, renk=VURGU)
        sonuc_kutu.to_edge(DOWN, buff=0.25)
        self.play(FadeOut(tablo_kutu), run_time=0.4)
        self.play(FadeIn(sonuc_kutu, shift=UP * 0.2), run_time=1.3)
        self.wait(3.5)

        hepsini_kapat(self)
