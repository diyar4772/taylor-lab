"""Sahne 2: Katsayılar nereden geliyor? — n! bir süsleme değil.

Anlatı:
  P(x) = c_0 + c_1(x-a) + c_2(x-a)^2 + ... yazalım ve tek bir şey isteyelim:
  P'nin a noktasındaki türevleri f'inkilerle aynı olsun.

  * x = a koy  -> (x-a) çarpanı taşıyan HER terim ölür, geriye c_0 kalır.
  * Türev al, sonra x = a koy -> c_1 kalır.
  * İki kez türev al -> c_2'nin önüne 2! düşer; x = a koyunca 2!c_2 kalır.
  * n kez türev al -> n!c_n kalır.

  Yani c_n = f^(n)(a) / n!. Bölme işlemi bir seçim değil, türevlemenin
  ürettiği n! çarpanını geri almanın TEK yoludur.

Render:  manim -qh 01-manim/scenes/s02_turetme.py TuretmeSahnesi
"""

from __future__ import annotations

from manim import *

from tema import (FONKSIYON, HATA, KUCUK_BOYUT, POLINOM, SOLUK, VURGU,
                  baslik, etiket_kutusu, formul, hepsini_kapat, sahne_kur)


class TuretmeSahnesi(Scene):
    def construct(self):
        sahne_kur(self)

        ust = baslik("Katsayılar nereden geliyor?",
                     "n! bir süsleme değil, türevlemenin faturası")
        self.play(FadeIn(ust, shift=DOWN * 0.2), run_time=1.0)

        # --- Genel polinom ---
        P = MathTex(
            r"P(x)=",                      # 0
            r"c_0", r"+",                  # 1 2
            r"c_1(x-a)", r"+",             # 3 4
            r"c_2(x-a)^2", r"+",           # 5 6
            r"c_3(x-a)^3", r"+\cdots",     # 7 8
            font_size=44, color=FONKSIYON,
        )
        P.shift(UP * 1.35)
        self.play(Write(P), run_time=2.0)
        self.wait(0.5)

        istek = Text("Tek isteğimiz: P'nin a'daki türevleri f'inkilerle aynı olsun.",
                     font_size=KUCUK_BOYUT, color=VURGU)
        istek.next_to(P, DOWN, buff=0.55)
        self.play(FadeIn(istek, shift=UP * 0.15), run_time=1.2)
        self.wait(1.2)
        self.play(FadeOut(istek), run_time=0.5)

        # Sonucun birikeceği yer
        sonuclar = VGroup().to_edge(DOWN, buff=0.7)

        # --------------------------------------------------------------
        # Adım adım: n. türevi al, x=a koy, hangi terimler ölüyor?
        # --------------------------------------------------------------
        adimlar = [
            # (islem metni, olen terim indeksleri, hayatta kalan indeks,
            #  kalan ifade, sonuc ifadesi)
            ("x = a koy", [3, 4, 5, 6, 7, 8], 1,
             r"P(a) = c_0",
             r"c_0 = f(a)"),
            ("bir kez türev al, sonra x = a koy", [1, 2, 5, 6, 7, 8], 3,
             r"P'(a) = c_1",
             r"c_1 = f'(a)"),
            ("iki kez türev al, sonra x = a koy", [1, 2, 3, 4, 7, 8], 5,
             r"P''(a) = 2!\,c_2",
             r"c_2 = \dfrac{f''(a)}{2!}"),
            ("üç kez türev al, sonra x = a koy", [1, 2, 3, 4, 5, 6], 7,
             r"P'''(a) = 3!\,c_3",
             r"c_3 = \dfrac{f'''(a)}{3!}"),
        ]

        islem_yazi = None
        for i, (islem, olenler, kalan, kalan_tex, sonuc_tex) in enumerate(adimlar):
            yeni_islem = Text(islem, font_size=KUCUK_BOYUT, color=POLINOM)
            yeni_islem.next_to(P, DOWN, buff=0.5)
            if islem_yazi is None:
                self.play(FadeIn(yeni_islem), run_time=0.7)
                islem_yazi = yeni_islem
            else:
                self.play(Transform(islem_yazi, yeni_islem), run_time=0.7)

            # Ölen terimleri kırmızıya boyayıp söndür, kalanı vurgula
            olen_grup = VGroup(*[P[j] for j in olenler])
            self.play(olen_grup.animate.set_color(HATA), run_time=0.6)
            self.play(olen_grup.animate.set_opacity(0.12),
                      P[kalan].animate.set_color(VURGU).scale(1.18),
                      run_time=0.8)

            kalan_formul = formul(kalan_tex, boyut=38, renk=VURGU)
            kalan_formul.next_to(islem_yazi, DOWN, buff=0.45)
            self.play(FadeIn(kalan_formul, shift=UP * 0.15), run_time=0.9)
            self.wait(0.8)

            # Sonucu alt şeride ekle
            sonuc = formul(sonuc_tex, boyut=32, renk=FONKSIYON)
            self.play(FadeOut(kalan_formul), run_time=0.4)
            sonuclar.add(sonuc)
            sonuclar.arrange(RIGHT, buff=0.85).to_edge(DOWN, buff=0.75)
            self.play(FadeIn(sonuc, shift=UP * 0.2), run_time=0.7)

            # Polinomu eski hâline döndür
            self.play(P.animate.set_color(FONKSIYON).set_opacity(1.0),
                      P[kalan].animate.scale(1 / 1.18),
                      run_time=0.5)

        self.play(FadeOut(islem_yazi), run_time=0.4)
        self.wait(0.5)

        # --------------------------------------------------------------
        # Genel kural
        # --------------------------------------------------------------
        genel = formul(r"n\ \text{kez türev}\ \Rightarrow\ "
                       r"P^{(n)}(a) = n!\,c_n \quad\Rightarrow\quad "
                       r"c_n = \frac{f^{(n)}(a)}{n!}",
                       boyut=40, renk=POLINOM)
        genel.move_to(ORIGIN + UP * 0.1)
        self.play(FadeOut(P), run_time=0.6)
        self.play(Write(genel), run_time=2.2)
        self.wait(1.5)

        vurgu_kutusu = SurroundingRectangle(genel, color=VURGU, buff=0.3,
                                            stroke_width=2.5, corner_radius=0.1)
        self.play(Create(vurgu_kutusu), run_time=1.0)

        mesaj = Text(
            "n! kimsenin koyduğu bir çarpan değil.\n"
            "(x−a)ⁿ terimini n kez türevlerken kendiliğinden doğuyor;\n"
            "n!'e bölmek onu geri almanın tek yolu.",
            font_size=KUCUK_BOYUT, color=FONKSIYON, line_spacing=0.95)
        kutu = etiket_kutusu(mesaj, renk=SOLUK)
        kutu.next_to(vurgu_kutusu, DOWN, buff=0.6)
        # Alt şerit ile çakışmasın
        self.play(sonuclar.animate.set_opacity(0.35), run_time=0.4)
        self.play(FadeIn(kutu, shift=UP * 0.2), run_time=1.2)
        self.wait(3.5)

        hepsini_kapat(self)
