"""Ortak ortam ayarları: UTF-8 çıktı, dosya yolları, grafik teması.

Laboratuvardaki her betik bunu ilk satırlarda import eder. İki somut sorunu
çözer:

1. Windows konsolu varsayılan olarak cp1254 ile kodluyor; Türkçe karakterler
   ve matematiksel semboller (✓, ≤, π) çıktıda patlıyor. stdout/stderr
   UTF-8'e çevrilir.
2. Çıktı yolları tek yerde tanımlanır; betikler nereden çağrılırsa çağrılsın
   (repo kökü, 02-python/, src/) aynı out/ klasörüne yazarlar.
"""

from __future__ import annotations

import sys
from pathlib import Path

# --------------------------------------------------------------------------
# 1. UTF-8 çıktı
# --------------------------------------------------------------------------

def utf8_cikti() -> None:
    """stdout/stderr'i UTF-8'e çevirir (Windows konsolu için gerekli)."""
    for akis in (sys.stdout, sys.stderr):
        kodlama = getattr(akis, "encoding", "") or ""
        if kodlama.lower().replace("-", "") != "utf8":
            try:
                akis.reconfigure(encoding="utf-8", errors="replace")
            except (AttributeError, ValueError):
                pass  # yönlendirilmiş/olağandışı akış: sessizce vazgeç


utf8_cikti()

# --------------------------------------------------------------------------
# 2. Dosya yolları
# --------------------------------------------------------------------------

#: Bu dosya: <kok>/02-python/src/ortam.py  ->  iki üst klasör proje köküdür.
PROJE_KOK: Path = Path(__file__).resolve().parents[2]
OUT: Path = PROJE_KOK / "out"
GORSELLER: Path = OUT / "gorseller"
TABLOLAR: Path = OUT / "tablolar"
VIDEOLAR: Path = OUT / "videolar"

for _k in (OUT, GORSELLER, TABLOLAR, VIDEOLAR):
    _k.mkdir(parents=True, exist_ok=True)


# --------------------------------------------------------------------------
# 3. Renk paleti — Manim tema dosyasıyla aynı değerler
# --------------------------------------------------------------------------

PALET = {
    "zemin":    "#0E1117",
    "fonksiyon": "#E8E3D3",   # gerçek f(x): kırık beyaz
    "polinom":  "#4CC9F0",    # Taylor polinomu: camgöbeği
    "hata":     "#F72585",    # gerçek hata: macenta
    "sinir":    "#FFB703",    # Lagrange sınırı: amber
    "vurgu":    "#90BE6D",    # kabul/doğrulama: yeşil
    "tekillik": "#F94144",    # kutuplar, tekillikler: kırmızı
    "soluk":    "#6C757D",    # ızgara, ikincil metin
}

#: Birden çok eğri üst üste çizilirken kullanılacak sıra.
SERI_RENKLERI = [PALET["polinom"], PALET["hata"], PALET["sinir"],
                 PALET["vurgu"], PALET["tekillik"], "#B5179E", "#4895EF"]


def grafik_temasi() -> None:
    """matplotlib'i laboratuvarın koyu temasına ayarlar."""
    import matplotlib as mpl

    mpl.rcParams.update({
        "figure.facecolor":  PALET["zemin"],
        "axes.facecolor":    PALET["zemin"],
        "savefig.facecolor": PALET["zemin"],
        "axes.edgecolor":    PALET["soluk"],
        "axes.labelcolor":   PALET["fonksiyon"],
        "text.color":        PALET["fonksiyon"],
        "xtick.color":       PALET["soluk"],
        "ytick.color":       PALET["soluk"],
        "grid.color":        "#2A2F3A",
        "grid.linestyle":    "-",
        "grid.linewidth":    0.6,
        "axes.grid":         True,
        "axes.prop_cycle":   mpl.cycler(color=SERI_RENKLERI),
        "font.size":         11,
        "figure.dpi":        120,
        "savefig.dpi":       160,
        "savefig.bbox":      "tight",
        "legend.framealpha": 0.85,
        "legend.facecolor":  "#161B25",
        "legend.edgecolor":  "#2A2F3A",
        "axes.titlesize":    13,
    })


# --------------------------------------------------------------------------
# 4. Markdown tablo yazıcı — README ve RAPOR'a gömülecek tablolar için
# --------------------------------------------------------------------------

def markdown_tablo(basliklar: list[str], satirlar: list[list[str]]) -> str:
    """Basit bir GitHub-uyumlu markdown tablosu üretir."""
    genislik = [len(b) for b in basliklar]
    for s in satirlar:
        for i, h in enumerate(s):
            genislik[i] = max(genislik[i], len(str(h)))

    def sira(hucreler) -> str:
        return "| " + " | ".join(str(h).ljust(genislik[i]) for i, h in enumerate(hucreler)) + " |"

    cizgi = "|" + "|".join("-" * (g + 2) for g in genislik) + "|"
    return "\n".join([sira(basliklar), cizgi] + [sira(s) for s in satirlar])


def tablo_yaz(dosya_adi: str, baslik: str, icerik: str) -> Path:
    """out/tablolar/ altına başlıklı bir markdown parçası yazar."""
    yol = TABLOLAR / dosya_adi
    yol.write_text(f"# {baslik}\n\n{icerik}\n", encoding="utf-8")
    print(f"  yazıldı: {yol.relative_to(PROJE_KOK)}")
    return yol


def gorsel_yolu(dosya_adi: str) -> Path:
    """out/gorseller/ altında bir dosya yolu döndürür."""
    return GORSELLER / dosya_adi


def baslik_yaz(metin: str) -> None:
    """Betik çıktılarında tutarlı bölüm başlığı."""
    print("\n" + metin)
    print("=" * max(46, len(metin)))
