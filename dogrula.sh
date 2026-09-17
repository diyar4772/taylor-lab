#!/usr/bin/env bash
#
# Taylor Laboratuvarı — tek komutluk doğrulama koşucusu
#
# Deponun iddiası şudur: "çalıştırılmamış hiçbir şey için çalışıyor denmez."
# Bu betik o iddiayı tek komutla yeniden üretilebilir kılar: her katmanın
# kendi testini çalıştırır, her biri için GEÇTİ / KALDI / ATLANDI basar ve
# bir tanesi bile KALDI ise çıkış kodu 1 döner.
#
# Kullanım:
#   bash dogrula.sh            # hepsi
#   bash dogrula.sh --hizli    # Lean'i atla (lake build uzun sürer)
#   make dogrula               # aynısı
#
# ATLANDI, KALDI değildir: bir araç bu makinede kurulu değilse o katman
# atlanır ve özette ayrıca listelenir. Kurulu olmayan bir araç yüzünden
# "kaldı" demek, çalıştırılmamış bir şey hakkında hüküm vermek olurdu.

set -uo pipefail

# Betik nereden çağrılırsa çağrılsın kendi konumunu bulur.
BURASI="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$BURASI" || { echo "depo köküne girilemedi: $BURASI" >&2; exit 2; }

HIZLI=0
for arg in "$@"; do
  case "$arg" in
    --hizli)
      HIZLI=1
      ;;
    -h|--yardim)
      # Baştaki yorum bloğunu bas: 2. satırdan ilk yorum-olmayan satıra kadar.
      # Sabit satır aralığı ('2,20p') dosya büyüyünce koda taşar.
      awk 'NR==1 {next} /^#/ {sub(/^# ?/, ""); print; next} {exit}' \
        "${BASH_SOURCE[0]}"
      exit 0
      ;;
    *)
      echo "Bilinmeyen seçenek: $arg  (yardım için: bash dogrula.sh --yardim)" >&2
      exit 2
      ;;
  esac
done

GUNLUK="$(mktemp -d)"
trap 'rm -rf "$GUNLUK"' EXIT

GECEN=0
KALAN=0
ATLANAN=0
KALANLAR=()
ATLANANLAR=()
BASLANGIC=$SECONDS

CIZGI="====================================================================="

# printf '%-40s' dolguyu BAYTA göre yapar; "ç", "ğ", "İ" gibi harfler UTF-8'de
# iki bayt olduğu için sütunlar kayar. Bash'in ${#dizge}'si ise karakter sayar.
# Bu yüzden dolgu elle hesaplanıyor.
ad_yaz() {
  local ad="$1" genislik=42 bosluk
  bosluk=$((genislik - ${#ad}))
  [ "$bosluk" -lt 1 ] && bosluk=1
  printf '  %s%*s' "$ad" "$bosluk" ''
}

baslik() {
  printf '\n%s\n %s\n%s\n' "$CIZGI" "$1" "$CIZGI"
}

# kosu <görünen ad> <komut...>
kosu() {
  local ad="$1"
  shift
  local dosya="$GUNLUK/$(printf '%s' "$ad" | tr -c 'A-Za-z0-9' '_').log"
  ad_yaz "$ad"
  if "$@" >"$dosya" 2>&1; then
    printf 'GEÇTİ\n'
    GECEN=$((GECEN + 1))
    return 0
  fi
  printf 'KALDI\n'
  KALAN=$((KALAN + 1))
  KALANLAR+=("$ad")
  echo "      ---- son 15 satır ----"
  tail -15 "$dosya" | sed 's/^/      | /'
  echo "      ----------------------"
  return 1
}

# atla <görünen ad> <sebep>
atla() {
  ad_yaz "$1"
  printf 'ATLANDI  (%s)\n' "$2"
  ATLANAN=$((ATLANAN + 1))
  ATLANANLAR+=("$1 — $2")
}

# --------------------------------------------------------------------
# LaTeX: çıkış kodu yetmez, günlükteki hata/uyarı sayısı da sıfır olmalı
# --------------------------------------------------------------------
teori_dogrula() {
  make teori || return 1
  local gunluk="00-teori/taylor-teori.log"
  if [ ! -f "$gunluk" ]; then
    echo "pdflatex günlüğü bulunamadı: $gunluk"
    return 1
  fi
  # Desen bilerek DAR: 'grep -i warning' paketlerin kendi tanıtım
  # satırlarına da takılır (ör. "infwarerr ... Providing info/warning/error
  # messages"), bu da olmayan bir uyarı uydurur. Gerçek LaTeX uyarıları
  # daima "... Warning:" biçimindedir.
  local hata uyari kutu
  hata=$(grep -c '^!' "$gunluk")
  uyari=$(grep -c 'Warning:' "$gunluk")
  kutu=$(grep -c '^\(Overfull\|Underfull\)' "$gunluk")
  echo "son geçiş: $hata hata, $uyari uyarı, $kutu aşırı dolu/boş kutu"
  [ "$hata" -eq 0 ] && [ "$uyari" -eq 0 ]
}

# --------------------------------------------------------------------
# Obsidian: her [[wikilink]] gerçek bir dosyaya gitmeli
# --------------------------------------------------------------------
wikilink_dogrula() {
  local dizin="00-teori/obsidian"
  if [ ! -d "$dizin" ]; then
    echo "dizin yok: $dizin"
    return 1
  fi
  local toplam=0 kirik=0 not hedef cozum
  for not in "$dizin"/*.md; do
    [ -e "$not" ] || continue
    while IFS= read -r hedef; do
      [ -n "$hedef" ] || continue
      toplam=$((toplam + 1))
      hedef="${hedef%%|*}"    # [[hedef|takma ad]] -> hedef
      hedef="${hedef%%#*}"    # [[hedef#başlık]]   -> hedef
      if [[ "$hedef" == */* || "$hedef" == *.* ]]; then
        # yol biçimli bağ: notun bulunduğu dizine göre çözülür
        cozum="$(dirname "$not")/$hedef"
      else
        # çıplak not adı: aynı kasada .md olarak aranır
        cozum="$dizin/$hedef.md"
      fi
      if [ ! -e "$cozum" ]; then
        echo "KIRIK  $(basename "$not")  ->  $hedef"
        kirik=$((kirik + 1))
      fi
    done < <(grep -o '\[\[[^]]*\]\]' "$not" | sed 's/^\[\[//; s/\]\]$//')
  done
  echo "$toplam wikilink tarandı, $kirik kırık"
  [ "$kirik" -eq 0 ]
}

# ====================================================================
baslik "TAYLOR LABORATUVARI — DOĞRULAMA"
echo "  Depo   : $BURASI"
echo "  Tarih  : $(date '+%Y-%m-%d %H:%M:%S')"
echo "  Makine : $(uname -sr)"
[ "$HIZLI" -eq 1 ] && echo "  Kip    : --hizli (Lean atlanacak)"

PY="$BURASI/.venv/bin/python"
# Windows (Git Bash): sanal ortamın yorumlayıcısı Scripts/ altındadır.
[ -x "$PY" ] || [ ! -x "$BURASI/.venv/Scripts/python.exe" ] || PY="$BURASI/.venv/Scripts/python.exe"

# Octave: Linux'ta PATH'te; Windows'ta winget onu PATH'e eklemez.
OCTAVE="$(command -v octave-cli 2>/dev/null || true)"
if [ -z "$OCTAVE" ] && [ -n "${LOCALAPPDATA:-}" ]; then
  for aday in "$LOCALAPPDATA"/Programs/"GNU Octave"/*/mingw64/bin/octave-cli.exe; do
    [ -x "$aday" ] && OCTAVE="$aday" && break
  done
fi

# --------------------------------------------------------------------
baslik "1. Sayısal katman (02-python)"
if [ -x "$PY" ]; then
  kosu "Taylor çekirdeği (taylor.py)"        "$PY" 02-python/src/taylor.py
  kosu "Lagrange kalan taraması"             "$PY" 02-python/src/kalan_dogrulama.py
else
  atla "Taylor çekirdeği (taylor.py)"        "sanal ortam (.venv) yok"
  atla "Lagrange kalan taraması"             "sanal ortam (.venv) yok"
fi

# --------------------------------------------------------------------
baslik "2. Teori katmanı (00-teori)"
if ! command -v make >/dev/null 2>&1; then
  atla "LaTeX (make teori, 3 geçiş)"         "make kurulu değil"
elif ! command -v pdflatex >/dev/null 2>&1; then
  atla "LaTeX (make teori, 3 geçiş)"         "pdflatex kurulu değil"
else
  kosu "LaTeX (make teori, 3 geçiş)"         teori_dogrula
fi
kosu "Obsidian wikilink bütünlüğü"           wikilink_dogrula

# --------------------------------------------------------------------
baslik "3. MATLAB uyumlu katman (03-matlab-octave)"
if [ -n "$OCTAVE" ]; then
  kosu "Octave demosu (demo_calistir.m)"     bash -c \
    'cd 03-matlab-octave && "$1" --no-gui --quiet demo_calistir.m' _ "$OCTAVE"
else
  atla "Octave demosu (demo_calistir.m)"     "octave-cli kurulu değil"
fi

# --------------------------------------------------------------------
baslik "4. Biçimsel katman (04-lean)"
if [ "$HIZLI" -eq 1 ]; then
  atla "Lean 4 (lake build)"                 "--hizli verildi"
elif [ -x "$HOME/.elan/bin/lake" ] || command -v lake >/dev/null 2>&1; then
  kosu "Lean 4 (lake build)"                 bash -c \
    'export PATH="$HOME/.elan/bin:$PATH"; cd 04-lean && lake build'
else
  atla "Lean 4 (lake build)"                 "lake kurulu değil"
fi

# --------------------------------------------------------------------
baslik "5. Etkileşimli katmanlar (05-godot, 06-web)"
if command -v godot >/dev/null 2>&1; then
  kosu "Godot sahne matematiği (headless)"   godot --headless --path 05-godot \
    --script res://test_dogrulama.gd
else
  atla "Godot sahne matematiği (headless)"   "godot kurulu değil"
fi
if command -v node >/dev/null 2>&1; then
  kosu "Web matematik çekirdeği (node)"      node 06-web/test_matematik.mjs
else
  atla "Web matematik çekirdeği (node)"      "node kurulu değil"
fi

# ====================================================================
SURE=$((SECONDS - BASLANGIC))
baslik "ÖZET"
printf '  GEÇTİ   : %d\n' "$GECEN"
printf '  KALDI   : %d\n' "$KALAN"
printf '  ATLANDI : %d\n' "$ATLANAN"
printf '  Süre    : %d sn\n' "$SURE"

if [ "$ATLANAN" -gt 0 ]; then
  echo
  echo "  Atlananlar (bu makinede çalıştırılmadı, hakkında hüküm verilmedi):"
  for s in "${ATLANANLAR[@]}"; do echo "    - $s"; done
fi

if [ "$KALAN" -gt 0 ]; then
  echo
  echo "  Kalanlar:"
  for s in "${KALANLAR[@]}"; do echo "    - $s"; done
  echo
  echo "  SONUÇ: DOĞRULAMA BAŞARISIZ"
  exit 1
fi

echo
if [ "$ATLANAN" -gt 0 ]; then
  echo "  SONUÇ: çalıştırılan her test geçti ($ATLANAN katman atlandı)"
else
  echo "  SONUÇ: BÜTÜN KATMANLAR GEÇTİ"
fi
exit 0
