"""Sahne 6: Her kararlı denge neden harmonik osilatördür?

Anlatı:
  Keyfi, çirkin, hiçbir simetrisi olmayan bir potansiyel V(x) alalım. Bir
  kararlı denge noktası x_0'da V'(x_0) = 0'dır -- denge noktası olmasının
  tanımı bu. Taylor açalım:

      V(x_0+u) = V(x_0) + V'(x_0)u + (1/2)V''(x_0)u^2 + (1/6)V'''(x_0)u^3 + ...

  Birinci terim sabit (kuvvete katkısı yok, enerjinin sıfır noktası).
  İkinci terim V'(x_0) = 0 olduğu için YOK.
  Geriye ilk terim olarak (1/2)V''(x_0)u^2 kalıyor -- yani yay potansiyeli.

  Bu bir benzetme değil. Küçük u için hangi potansiyeli seçerseniz seçin,
  kararlı denge civarında ilk hayatta kalan terim karesel olandır. Doğa
  harmonik osilatörü "seçmiyor"; Taylor serisi başka seçenek bırakmıyor.

  Sahnenin ikinci yarısında genlik büyütülür: atılan u^3 terimi geri döner,
  gerçek hareket ile harmonik hayalet ayrışır.

Render:  manim -qh 01-manim/scenes/s06_denge.py DengeSahnesi
"""

from __future__ import annotations

import numpy as np
from scipy.optimize import brentq
from manim import *

from tema import (FONKSIYON, HATA, KUCUK_BOYUT, POLINOM, SINIR, SOLUK, VURGU,
                  baslik, etiket_kutusu, formul, hepsini_kapat, sahne_kur)


# --------------------------------------------------------------------------
# Keyfi bir potansiyel — özellikle "güzel" olmayan bir şey seçildi
# --------------------------------------------------------------------------

def V(x):
    """Keyfi potansiyel. Simetrisi yok, kapalı biçimi çirkin; kasıtlı."""
    x = np.asarray(x, dtype=float)
    return 0.22 * x**4 - 0.35 * x**3 - 1.1 * x**2 + 0.6 * x + 3.0


def dV(x):
    x = np.asarray(x, dtype=float)
    return 0.88 * x**3 - 1.05 * x**2 - 2.2 * x + 0.6


def ddV(x):
    x = np.asarray(x, dtype=float)
    return 2.64 * x**2 - 2.1 * x - 2.2


def denge_bul() -> float:
    """V'(x) = 0 köklerinden V'' > 0 olanı (kararlı denge) döndürür."""
    kokler = []
    izgara = np.linspace(-3.0, 3.5, 2000)
    d = dV(izgara)
    for i in range(len(izgara) - 1):
        if d[i] * d[i + 1] < 0:
            kokler.append(brentq(lambda t: float(dV(t)), izgara[i], izgara[i + 1]))
    kararli = [k for k in kokler if float(ddV(k)) > 0]
    # En derin olanı seç
    return float(min(kararli, key=lambda k: float(V(k))))


class DengeSahnesi(Scene):
    def construct(self):
        sahne_kur(self)

        x0 = denge_bul()
        k = float(ddV(x0))            # yay sabiti: V''(x_0)
        V0 = float(V(x0))
        omega = np.sqrt(k)            # birim kütle

        ust = baslik("Her kararlı denge harmonik osilatördür",
                     "doğa seçmiyor — Taylor serisi başka seçenek bırakmıyor")
        self.play(FadeIn(ust, shift=DOWN * 0.2), run_time=1.0)

        ax = Axes(x_range=[-2.6, 3.4, 1], y_range=[0, 6, 2],
                  x_length=9.5, y_length=4.2,
                  axis_config={"color": SOLUK, "stroke_width": 2,
                               "include_tip": True, "tip_width": 0.15,
                               "tip_height": 0.15}).shift(DOWN * 0.75)

        V_egri = ax.plot(lambda t: float(np.clip(V(t), 0, 6)),
                         x_range=[-2.6, 3.4, 0.01],
                         color=FONKSIYON, stroke_width=5)
        V_etiket = formul(r"V(x)", boyut=32, renk=FONKSIYON)
        V_etiket.next_to(ax.c2p(-2.2, 5.0), RIGHT, buff=0.1)

        self.play(Create(ax), run_time=1.0)
        self.play(Create(V_egri), FadeIn(V_etiket), run_time=2.0)

        keyfi = Text("Keyfi bir potansiyel. Simetrisi yok, özel bir yanı yok.",
                     font_size=KUCUK_BOYUT, color=SOLUK)
        keyfi.next_to(ax, DOWN, buff=0.3)
        self.play(FadeIn(keyfi), run_time=1.1)
        self.wait(1.6)
        self.play(FadeOut(keyfi), run_time=0.5)

        # --- Denge noktası ---
        denge = Dot(ax.c2p(x0, V0), color=VURGU, radius=0.09)
        denge_e = formul(rf"x_0={x0:.4f}", boyut=26, renk=VURGU)
        denge_e.next_to(denge, DOWN, buff=0.25)
        tegent = Line(ax.c2p(x0 - 0.8, V0), ax.c2p(x0 + 0.8, V0),
                      color=VURGU, stroke_width=3)

        self.play(FadeIn(denge, scale=1.5), FadeIn(denge_e), run_time=0.9)
        self.play(Create(tegent), run_time=0.9)
        sifir = formul(r"V'(x_0)=0", boyut=30, renk=VURGU)
        sifir.next_to(tegent, UP, buff=0.25).shift(LEFT * 1.6)
        self.play(FadeIn(sifir), run_time=0.9)
        self.wait(1.6)

        # --- Açılım ---
        acilim = MathTex(
            r"V(x_0+u)=",                                   # 0
            r"V(x_0)", r"+",                                # 1 2
            r"V'(x_0)\,u", r"+",                            # 3 4
            r"\tfrac{1}{2}V''(x_0)\,u^2", r"+",             # 5 6
            r"\tfrac{1}{6}V'''(x_0)\,u^3", r"+\cdots",      # 7 8
            font_size=34, color=FONKSIYON)
        acilim.to_edge(UP, buff=1.55)
        self.play(Write(acilim), run_time=2.4)
        self.wait(1.0)

        # 1. terim: sabit
        self.play(acilim[1].animate.set_color(SOLUK), run_time=0.5)
        not1 = Text("sabit — kuvvete katkısı yok", font_size=20, color=SOLUK)
        not1.next_to(acilim[1], DOWN, buff=0.3)
        self.play(FadeIn(not1), run_time=0.7)
        self.wait(1.2)

        # 2. terim: SIFIR
        self.play(acilim[3].animate.set_color(HATA), run_time=0.5)
        not2 = Text("= 0  (denge noktası!)", font_size=20, color=HATA)
        not2.next_to(acilim[3], DOWN, buff=0.3)
        self.play(FadeIn(not2), run_time=0.7)
        self.wait(1.0)
        self.play(acilim[3].animate.set_opacity(0.12),
                  acilim[4].animate.set_opacity(0.12),
                  FadeOut(not2), run_time=0.8)

        # 3. terim: hayatta kalan
        self.play(acilim[5].animate.set_color(POLINOM).scale(1.15), run_time=0.7)
        not3 = Text("ilk hayatta kalan terim = yay potansiyeli", font_size=20,
                    color=POLINOM)
        not3.next_to(acilim[5], DOWN, buff=0.3)
        self.play(FadeIn(not3), run_time=0.8)
        self.wait(1.8)
        self.play(FadeOut(not1), FadeOut(not3), run_time=0.5)

        # --- Parabol belirir ---
        parabol = ax.plot(lambda t: float(np.clip(V0 + 0.5 * k * (t - x0) ** 2, 0, 6)),
                          x_range=[-2.6, 3.4, 0.01],
                          color=POLINOM, stroke_width=3.6)
        parabol_e = formul(rf"V_0+\tfrac{{1}}{{2}}({k:.3f})u^2", boyut=26, renk=POLINOM)
        parabol_e.next_to(ax.c2p(x0, V0 + 2.6), UP, buff=0.05)
        self.play(FadeOut(tegent), FadeOut(sifir), run_time=0.4)
        self.play(Create(parabol), FadeIn(parabol_e), run_time=1.8)
        self.wait(1.5)

        # --- Zoom: yakınlaştıkça ayırt edilemez oluyorlar ---
        zoom = Text("Dengeye yaklaştıkça ikisi ayırt edilemez hâle geliyor",
                    font_size=KUCUK_BOYUT, color=VURGU)
        zoom.next_to(ax, DOWN, buff=0.3)
        self.play(FadeIn(zoom), run_time=0.9)

        cerceve = Rectangle(width=1.0, height=0.8, color=VURGU, stroke_width=2.5)
        cerceve.move_to(ax.c2p(x0, V0 + 0.25))
        # Not: gerçek kamera zoom'u MovingCameraScene ister. Burada düz Scene
        # kullanıldığı için "yakınlaşma" çerçeveyi daraltarak anlatılıyor --
        # aynı fikri veriyor, sınıf değiştirmeye değmez.
        self.play(Create(cerceve), run_time=0.8)
        for olcek in (0.6, 0.35):
            self.play(cerceve.animate.stretch_to_fit_width(1.0 * olcek)
                      .stretch_to_fit_height(0.8 * olcek)
                      .move_to(ax.c2p(x0, V0 + 0.12 * olcek)), run_time=0.9)
        self.wait(1.4)
        self.play(FadeOut(cerceve), FadeOut(zoom), run_time=0.6)

        self.play(FadeOut(VGroup(acilim, denge_e)), run_time=0.6)

        # --------------------------------------------------------------
        # Hareket: gerçek vs harmonik hayalet
        # --------------------------------------------------------------
        yeni_ust = baslik("Genlik büyüyünce atılan terim geri dönüyor",
                          "gerçek hareket ile harmonik hayalet ayrışıyor")
        self.play(Transform(ust, yeni_ust), run_time=1.0)

        # Gerçek hareketi bir kez sayısal olarak çöz, sonra oynat.
        from scipy.integrate import solve_ivp

        def gercek_yorunge(genlik: float, sure: float, n: int = 900):
            def f(t, y):
                return [y[1], -float(dV(x0 + y[0]))]
            ts = np.linspace(0, sure, n)
            coz = solve_ivp(f, (0, sure), [genlik, 0.0], t_eval=ts,
                            rtol=1e-10, atol=1e-12)
            return ts, coz.y[0]

        sure = 4 * 2 * np.pi / omega
        genlikler = [0.25, 0.7, 1.3]

        alt_ax = Axes(x_range=[0, sure, sure / 4], y_range=[-1.6, 1.6, 0.5],
                      x_length=9.0, y_length=2.8,
                      axis_config={"color": SOLUK, "stroke_width": 2,
                                   "include_tip": False}).shift(DOWN * 2.0)
        alt_etiket = VGroup(
            Text("t", font_size=22, color=SOLUK).next_to(alt_ax.x_axis.get_end(), DR, buff=0.1),
            Text("u", font_size=22, color=SOLUK).next_to(alt_ax.y_axis.get_end(), UL, buff=0.1),
        )
        self.play(FadeOut(VGroup(ax, V_egri, V_etiket, parabol, parabol_e, denge)),
                  run_time=0.7)
        self.play(Create(alt_ax), FadeIn(alt_etiket), run_time=1.2)

        gosterge = VGroup(
            VGroup(Line(ORIGIN, RIGHT * 0.45, color=FONKSIYON, stroke_width=4),
                   Text("gerçek V(x)", font_size=20, color=FONKSIYON)).arrange(RIGHT, buff=0.15),
            VGroup(Line(ORIGIN, RIGHT * 0.45, color=POLINOM, stroke_width=3),
                   Text("harmonik hayalet", font_size=20, color=POLINOM)).arrange(RIGHT, buff=0.15),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        gosterge_kutu = etiket_kutusu(gosterge, renk=SOLUK).scale(0.9)
        gosterge_kutu.to_corner(UR, buff=0.3).shift(DOWN * 1.2)
        self.play(FadeIn(gosterge_kutu), run_time=0.6)

        mevcut = None
        bilgi = None
        for A in genlikler:
            ts, us = gercek_yorunge(A, sure)
            gercek_cizgi = VMobject(color=FONKSIYON, stroke_width=4.5)
            gercek_cizgi.set_points_as_corners(
                [alt_ax.c2p(t, float(np.clip(u, -1.6, 1.6))) for t, u in zip(ts, us)])
            har_cizgi = VMobject(color=POLINOM, stroke_width=3.0)
            har_cizgi.set_points_as_corners(
                [alt_ax.c2p(t, float(np.clip(A * np.cos(omega * t), -1.6, 1.6)))
                 for t in ts])
            har_kesikli = DashedVMobject(har_cizgi, num_dashes=110, dashed_ratio=0.55)
            har_kesikli.set_z_index(4)

            # Son çeyrekteki faz farkı: ayrışmanın ölçüsü
            ayrisma = float(np.max(np.abs(us[-len(us)//4:] -
                                          A * np.cos(omega * ts[-len(ts)//4:]))))
            yeni_bilgi = VGroup(
                formul(rf"\text{{genlik}}=({A})", boyut=26, renk=VURGU),
                Text(f"ayrışma: {ayrisma:.3f}", font_size=20,
                     color=HATA if ayrisma > 0.05 else VURGU),
            ).arrange(DOWN, buff=0.15)
            yeni_kutu = etiket_kutusu(yeni_bilgi, renk=SOLUK).scale(0.9)
            yeni_kutu.to_corner(UL, buff=0.3).shift(DOWN * 1.2)

            yeni = VGroup(gercek_cizgi, har_kesikli)
            if mevcut is None:
                self.play(Create(gercek_cizgi), Create(har_kesikli),
                          FadeIn(yeni_kutu), run_time=2.2)
                bilgi = yeni_kutu
            else:
                self.play(ReplacementTransform(mevcut, yeni),
                          Transform(bilgi, yeni_kutu), run_time=1.8)
            mevcut = yeni
            self.wait(1.8)

        mesaj = Text(
            "Küçük genlikte harmonik yaklaşım kusursuz görünüyor.\n"
            "Genlik büyüdükçe atılan  (1/6)V'''(x₀)u³  terimi geri dönüyor:\n"
            "periyot kayıyor, iki eğri ayrışıyor. Anharmonisite budur.",
            font_size=KUCUK_BOYUT, color=FONKSIYON, line_spacing=0.95)
        mesaj_kutu = etiket_kutusu(mesaj, renk=VURGU)
        mesaj_kutu.scale(0.88).to_edge(UP, buff=1.5)
        self.play(FadeIn(mesaj_kutu, shift=DOWN * 0.2), run_time=1.3)
        self.wait(4.0)

        hepsini_kapat(self)
