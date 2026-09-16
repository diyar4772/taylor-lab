#!/usr/bin/env bash
# Bütün sahneleri -qh (1920x1080, 60 fps) ile render eder ve out/videolar/
# altına kopyalar.
#
# Kullanım:
#   bash 01-manim/render.sh              # hepsi
#   bash 01-manim/render.sh 4            # yalnızca 4. sahne
#   KALITE=-ql bash 01-manim/render.sh   # hızlı önizleme (854x480, 15 fps)
#
# Not: -qh manim'de 1920x1080@60fps demektir. Görev tanımındaki "kare"
# ifadesi 1920x1080 ile çelişiyordu; 16:9 tercih edildi çünkü -qh'ın
# standardı budur ve sahneler bu en-boy oranına göre yerleştirildi.

set -euo pipefail

BURASI="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
KOK="$(cd "$BURASI/.." && pwd)"
KALITE="${KALITE:--qh}"
CIKTI="$KOK/out/videolar"

mkdir -p "$CIKTI"

# sıra:dosya:sınıf
SAHNELER=(
  "1:s01_artan_derece:ArtanDereceSahnesi"
  "2:s02_turetme:TuretmeSahnesi"
  "3:s03_kalan_terimi:KalanTerimiSahnesi"
  "4:s04_kompleks_yaricap:KompleksYaricapSahnesi"
  "5:s05_analitik_degil:AnalitikDegilSahnesi"
  "6:s06_denge:DengeSahnesi"
)

SECILEN="${1:-hepsi}"
BASARILI=0
BASARISIZ=0

echo "Kalite: $KALITE   Çıktı: $CIKTI"
echo "======================================================"

for KAYIT in "${SAHNELER[@]}"; do
  IFS=':' read -r SIRA DOSYA SINIF <<< "$KAYIT"

  if [[ "$SECILEN" != "hepsi" && "$SECILEN" != "$SIRA" ]]; then
    continue
  fi

  echo ""
  echo "[$SIRA/6] $SINIF"
  echo "------------------------------------------------------"

  # Render'dan hemen önce bir zaman işareti bırak. Aşağıdaki arama yalnızca
  # bundan YENİ dosyaları kabul eder; böylece başka bir kalitede daha önce
  # üretilmiş eski bir .mp4 yanlışlıkla kopyalanamaz.
  ISARET="$(mktemp)"

  if (cd "$BURASI" && manim "$KALITE" --disable_caching "scenes/$DOSYA.py" "$SINIF"); then
    # manim çıktıyı media/videos/<dosya>/<çözünürlük>/<Sınıf>.mp4 yazar;
    # çözünürlük klasörünün adı kaliteye göre değiştiği için aranarak bulunur.
    # Birden fazla eşleşme olursa en yenisi alınır (zaman damgasına göre sırala).
    # head/awk ile boru kesmek `set -o pipefail` altında sorun çıkardığı için
    # liste önce değişkene alınıp ilk satırı kabuk içinde ayrıştırılıyor.
    LISTE="$(find "$BURASI/media/videos/$DOSYA" -name "$SINIF.mp4" -type f \
             -newer "$ISARET" -printf '%T@ %p\n' 2>/dev/null | sort -rn || true)"
    KAYNAK="${LISTE%%$'\n'*}"   # ilk satır
    KAYNAK="${KAYNAK#* }"       # baştaki zaman damgasını at (yol boşluk içerebilir)
    if [[ -n "$KAYNAK" ]]; then
      HEDEF="$CIKTI/${SIRA}-${SINIF}.mp4"
      cp "$KAYNAK" "$HEDEF"
      SURE="$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$HEDEF" 2>/dev/null || echo "?")"
      BOYUT="$(ffprobe -v error -select_streams v:0 -show_entries stream=width,height \
               -of csv=s=x:p=0 "$HEDEF" 2>/dev/null || echo "?")"
      FPS="$(ffprobe -v error -select_streams v:0 -show_entries stream=r_frame_rate \
             -of csv=p=0 "$HEDEF" 2>/dev/null || echo "?")"
      printf "  ✓ %s   (%s sn, %s, %s fps)\n" "$(basename "$HEDEF")" "$SURE" "$BOYUT" "$FPS"
      BASARILI=$((BASARILI + 1))
    else
      echo "  ! render bitti ama çıktı dosyası bulunamadı"
      BASARISIZ=$((BASARISIZ + 1))
    fi
  else
    echo "  ✗ RENDER BAŞARISIZ: $SINIF"
    BASARISIZ=$((BASARISIZ + 1))
  fi

  rm -f "$ISARET"
done

echo ""
echo "======================================================"
echo "Başarılı: $BASARILI    Başarısız: $BASARISIZ"
[[ "$BASARISIZ" -eq 0 ]] || exit 1
