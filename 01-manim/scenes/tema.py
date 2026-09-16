"""Bütün sahnelerin ortak teması: renkler, yazı boyutları, yardımcı nesneler.

Tek bir yerden yönetilir; hiçbir sahne kendi rengini uydurmaz. Palet
02-python/src/ortam.py içindeki PALET ile birebir aynıdır -- böylece video
ile PNG çıktıları aynı görsel dile sahip olur.

Manim Community v0.19.0 API'si kullanılır.
"""

from __future__ import annotations

from manim import *

# --------------------------------------------------------------------------
# Palet — ortam.py ile birebir aynı
# --------------------------------------------------------------------------

ZEMIN     = "#0E1117"
FONKSIYON = "#E8E3D3"   # gerçek f(x)
POLINOM   = "#4CC9F0"   # Taylor polinomu
HATA      = "#F72585"   # gerçek hata
SINIR     = "#FFB703"   # Lagrange sınırı
VURGU     = "#90BE6D"   # kabul / doğrulama
TEKILLIK  = "#F94144"   # kutup, tekillik
SOLUK     = "#6C757D"   # ızgara, ikincil metin
DISK      = "#7CF5C2"   # yakınsaklık diski / çember

#: Artan derece animasyonlarında sırayla kullanılacak renkler
DERECE_RENKLERI = [
    "#4CC9F0", "#4895EF", "#4361EE", "#3F37C9",
    "#7209B7", "#B5179E", "#F72585", "#FF6392",
]

# --------------------------------------------------------------------------
# Yazı boyutları
# --------------------------------------------------------------------------

BASLIK_BOYUT   = 40
ALTBASLIK_BOYUT = 28
FORMUL_BOYUT   = 36
ETIKET_BOYUT   = 26
KUCUK_BOYUT    = 22


def sahne_kur(sahne: Scene) -> None:
    """Her sahnenin ilk satırında çağrılır: arka planı ayarlar."""
    sahne.camera.background_color = ZEMIN


def baslik(metin: str, alt: str | None = None) -> VGroup:
    """Ekranın üstüne oturan başlık (ve isteğe bağlı altbaşlık).

    Türkçe metinler için ``Text`` kullanılır: ManimPango, LaTeX'in aksine
    'ı', 'ğ', 'ş' gibi karakterleri ek paket gerektirmeden basar.
    """
    b = Text(metin, font_size=BASLIK_BOYUT, color=FONKSIYON, weight=BOLD)
    if alt is None:
        return VGroup(b).to_edge(UP, buff=0.35)
    a = Text(alt, font_size=ALTBASLIK_BOYUT, color=SOLUK)
    grup = VGroup(b, a).arrange(DOWN, buff=0.18)
    return grup.to_edge(UP, buff=0.3)


def formul(tex: str, boyut: int = FORMUL_BOYUT, renk: str = FONKSIYON) -> MathTex:
    """LaTeX formülü — matematiksel gösterim için (Türkçe metin için Text)."""
    return MathTex(tex, font_size=boyut, color=renk)


def etiket_kutusu(*satirlar: Mobject, renk: str = SOLUK) -> VGroup:
    """Köşeye yerleştirilecek, çerçeveli bilgi kutusu."""
    icerik = VGroup(*satirlar).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
    cerceve = SurroundingRectangle(
        icerik, color=renk, buff=0.22, stroke_width=1.6,
        fill_color=ZEMIN, fill_opacity=0.85, corner_radius=0.08)
    return VGroup(cerceve, icerik)


def eksen(
    x_araligi: tuple, y_araligi: tuple,
    x_uzunluk: float = 10.0, y_uzunluk: float = 5.2,
    x_etiket: str = "x", y_etiket: str = "y",
) -> tuple[Axes, VGroup]:
    """Laboratuvarın standart eksen takımı; (axes, etiketler) döndürür."""
    ax = Axes(
        x_range=x_araligi, y_range=y_araligi,
        x_length=x_uzunluk, y_length=y_uzunluk,
        axis_config={
            "color": SOLUK,
            "stroke_width": 2,
            "include_tip": True,
            "tip_width": 0.18,
            "tip_height": 0.18,
        },
        tips=True,
    )
    etiketler = VGroup(
        MathTex(x_etiket, font_size=ETIKET_BOYUT, color=SOLUK).next_to(
            ax.x_axis.get_end(), DR, buff=0.15),
        MathTex(y_etiket, font_size=ETIKET_BOYUT, color=SOLUK).next_to(
            ax.y_axis.get_end(), UL, buff=0.15),
    )
    return ax, etiketler


def merkez_noktasi(ax: Axes, a: float, etiket: str = "a") -> VGroup:
    """Açılım merkezini işaretleyen nokta + etiket."""
    nokta = Dot(ax.c2p(a, 0), color=VURGU, radius=0.07)
    yazi = MathTex(etiket, font_size=ETIKET_BOYUT, color=VURGU).next_to(
        nokta, DOWN, buff=0.18)
    return VGroup(nokta, yazi)


def hepsini_kapat(sahne: Scene, sure: float = 1.0) -> None:
    """Sahnedeki her şeyi söndürür.

    ``FadeOut(VGroup(*sahne.mobjects))`` kullanmak cazip ama HATALIDIR:
    Axes'in ok uçları düz ``Mobject`` olabilir ve VGroup yalnızca VMobject
    kabul eder. Tek tek FadeOut vermek bu ayrımı tamamen atlar.
    """
    if not sahne.mobjects:
        return
    sahne.play(*[FadeOut(m) for m in sahne.mobjects], run_time=sure)
