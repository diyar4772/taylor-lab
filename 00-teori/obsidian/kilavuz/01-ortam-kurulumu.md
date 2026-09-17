---
title: Ortam kurulumu (Windows ve Linux)
tags: [kilavuz, kilavuz/kurulum]
created: 2026-09-17
status: tamam
lang: tr
---

# Ortam kurulumu

↑ [[00-BASLA-BURADAN]] · → [[02-calisma-plani]] · English: [[01-environment-setup]]

Bütün komutlar **depo kökünden** (`taylor-lab/`) çalıştırılır. Her araç için
önce **Windows (PowerShell)**, sonra **Linux (bash, Fedora)** bloğu var.
Her katmanın hangi aracı istediği:

| Katman | Gereken | Zorunlu mu? |
|---|---|---|
| [[03-katman-python]] | Python + `requirements.txt` | Evet; çoğu oturumun temeli |
| [[04-katman-manim]] | manim 0.19 + ffmpeg + LaTeX | Hayır; videolar `out/videolar/`'da hazır |
| [[05-katman-teori-latex]] | pdflatex | Hayır; PDF `out/taylor-teori.pdf`'te hazır |
| [[06-katman-octave]] | GNU Octave | Oturum 5 için |
| [[07-katman-lean]] | elan + Lean 4.34.0 + Mathlib (~11 GB) | Oturum 10 için |
| [[08-katman-godot]] | Godot 4.7 | Oturum 8 için |
| [[09-katman-web]] | Python (yerel sunucu) + tarayıcı; testi için Node | Oturum 1, 4, 8 |

> [!note] Doğrulama kaydı
> Aşağıdaki Windows komutları Windows 11 + Python 3.13.7 üzerinde,
> Linux komutları ise deponun kendi kayıtlarına göre (README "Doğrulama
> durumu", `ENVANTER.md`) Fedora 44 üzerinde çalıştırıldı. Çalıştırılmamış
> bir komut varsa yanında **(denenmedi)** yazar.

---

## Python

### İki sanal ortam meselesi: `.venv` ve `.venv313`

Bu yalnızca **Python 3.14** olan sistemlerde (ör. Fedora 44) bir sorundur.

- `manim==0.19.0`, `av>=9,<14` ister. `av`'nin Python 3.14 için hazır tekerleği
  yok (en eskisi 15.1.0). Bu yüzden pip `av`'yi kaynaktan derlemeye çalışır ve
  ffmpeg başlıkları yüzünden düşer.
- Çözüm: sayısal betikler için 3.14'lük `.venv/`, **yalnızca manim** için
  3.13'lük `.venv313/`.
- **Windows'ta ya da Python 3.13 olan her sistemde** tek ortam yeter:
  `requirements.txt` (manim dahil) 3.13'e sorunsuz kurulur.

**Windows (PowerShell):**

Sanal ortam adımları **(denenmedi)**: doğrulama sistem Python 3.13'üne
doğrudan kurulu paketlerle yapıldı. `taylor.py` satırı ise çalıştırıldı.

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\Activate.ps1
# "running scripts is disabled" hatası alırsan (bir kez):
#   Set-ExecutionPolicy -Scope CurrentUser RemoteSigned

python 02-python\src\taylor.py      # son satır: "Tüm kontroller geçti."
```

**Linux (bash, Python 3.14):**

```bash
python3 -m venv .venv
grep -v '^manim' requirements.txt > /tmp/req-sayisal.txt   # manim'i dışarıda bırak (aşağıdaki tuzak 1)
.venv/bin/pip install -r /tmp/req-sayisal.txt
source .venv/bin/activate

# yalnızca manim için:
python3.13 -m venv .venv313
.venv313/bin/pip install -r requirements.txt

python 02-python/src/taylor.py
```

> [!warning] `grep -v` satırı hakkında
> README `.venv/bin/pip install -r requirements.txt` der. `requirements.txt`
> içinde `manim==0.19.0` olduğu için bu komut 3.14'te büyük olasılıkla
> `av` derlemesinde düşer (`ENVANTER.md`'deki hata). Manim'i ayıklayan
> satır bu kılavuzun önerisidir; Fedora'da **(denenmedi)**.

Defteri açmak için (`jupyterlab` requirements'ta var):

```powershell
jupyter lab 02-python\notebooks\taylor-laboratuvari.ipynb
```

```bash
jupyter lab 02-python/notebooks/taylor-laboratuvari.ipynb
```

---

## Manim (isteğe bağlı)

Sistem bağımlılıkları: **ffmpeg** ve bir **LaTeX** dağıtımı (`MathTex` için).

**Windows:**

```powershell
winget install Gyan.FFmpeg
winget install MiKTeX.MiKTeX

# Hızlı önizleme (854x480, 15 fps). out/videolar'a DOKUNMAZ:
cd 01-manim
manim -ql --disable_caching scenes\s01_artan_derece.py ArtanDereceSahnesi
# çıktı: 01-manim\media\videos\s01_artan_derece\480p15\ArtanDereceSahnesi.mp4
cd ..
```

**Linux:**

```bash
sudo dnf install -y ffmpeg python3.13 texlive-dvisvgm texlive-doublestroke

# Hızlı önizleme, out/videolar'a dokunmaz:
(cd 01-manim && PATH="$PWD/../.venv313/bin:$PATH" manim -ql --disable_caching scenes/s01_artan_derece.py ArtanDereceSahnesi)

# Altı sahnenin hepsi 1080p60 ve out/videolar ÜZERİNE YAZAR (tuzak 3):
PATH="$PWD/.venv313/bin:$PATH" bash 01-manim/render.sh
```

---

## LaTeX

Teori metni **üç geçiş** ister (iki geçişten sonra hâlâ "Label(s) may have
changed" uyarısı kalır).

**Windows (MiKTeX):**

```powershell
cd 00-teori
1..3 | ForEach-Object { pdflatex -interaction=nonstopmode -enable-installer taylor-teori.tex | Out-Null }
cd ..
# çıktı: 00-teori\taylor-teori.pdf (8 sayfa)
```

**Linux (TeX Live):**

```bash
sudo dnf install -y texlive-enumitem texlive-babel-turkish texlive-hyphen-turkish
make teori          # 3 geçiş + out/taylor-teori.pdf'e kopyalar
```

---

## Octave

**Windows:** winget, Octave'ı PATH'e **eklemez**; tam yol gerekir.

```powershell
winget install --id GNU.Octave --exact
$oct = (Get-ChildItem "$env:LOCALAPPDATA\Programs\GNU Octave\*\mingw64\bin\octave-cli.exe" | Select-Object -First 1).FullName
cd 03-matlab-octave
& $oct --no-gui --quiet demo_calistir.m
cd ..
```

**Linux:**

```bash
sudo dnf install -y octave
(cd 03-matlab-octave && octave-cli --no-gui --quiet demo_calistir.m)
```

---

## Lean

Proje **açık sürüm** ister (`04-lean/lean-toolchain` →
`leanprover/lean4:v4.34.0`). Toplam indirme ~11 GB'tır (toolchain + Mathlib).

**Windows:**

```powershell
winget install --id Lean.Elan --exact
cd 04-lean
elan toolchain install leanprover/lean4:v4.34.0
lake exe cache get      # Mathlib'in derlenmiş .olean dosyaları (~8900 dosya)
lake build              # beklenen son satır: "Build completed successfully (2777 jobs)."
cd ..
```

`elan toolchain install` şu hatayla düşerse ağın `release.lean-lang.org` adını
çözemiyor demektir (Tuzak 5):

```text
error: error during download
info: caused by: [6] Could not resolve hostname (Could not resolve host: release.lean-lang.org)
```

Toolchain'i doğrudan GitHub'dan kur. Aşağıdaki blok **Git Bash**'te
çalıştırıldı ve doğrulandı:

```bash
curl -L -o /tmp/lean.zip https://github.com/leanprover/lean4/releases/download/v4.34.0/lean-4.34.0-windows.zip   # ~850 MB
mkdir -p ~/.elan/toolchains/_tmp && unzip -q /tmp/lean.zip -d ~/.elan/toolchains/_tmp
mv ~/.elan/toolchains/_tmp/lean-4.34.0-windows ~/.elan/toolchains/leanprover--lean4---v4.34.0
rmdir ~/.elan/toolchains/_tmp
elan toolchain list      # -> leanprover/lean4:v4.34.0
```

**Linux:**

```bash
curl https://elan.lean-lang.org/elan-init.sh -sSf | sh     # elan yoksa
export PATH="$HOME/.elan/bin:$PATH"
cd 04-lean && lake exe cache get && lake build
```

Linux'ta aynı DNS engeli çıkarsa `LEAN-DURUM.md` → "Windows'taki engel nasıl
aşıldı" bölümündeki elle kurma adımlarını izle.

---

## Godot

**Windows:**

```powershell
winget install --id GodotEngine.GodotEngine --exact
godot --path 05-godot                            # 1. sahne: Taylor keşfi
godot --path 05-godot res://denge_oyunu.tscn     # 2. sahne: denge oyunu
godot --headless --path 05-godot --script res://test_dogrulama.gd   # "SONUC: 0 hata"
```

**Linux:**

```bash
sudo dnf install -y godot
godot --path 05-godot
godot --path 05-godot res://denge_oyunu.tscn
godot --headless --path 05-godot --script res://test_dogrulama.gd
```

---

## Web

`06-web/index.html` tek dosyadır, dış bağımlılığı yoktur. Deponun notuna göre
Chrome onu `file://` ile açmaz; yerel sunucu kullan.

**Windows:**

```powershell
python -m http.server 8765
# tarayıcı: http://localhost:8765/06-web/index.html
node 06-web\test_matematik.mjs      # "SONUC: 0 hata / 34 kontrol"
```

**Linux:**

```bash
python3 -m http.server 8765
node 06-web/test_matematik.mjs
```

Node yoksa: Windows `winget install OpenJS.NodeJS.LTS` **(denenmedi)**,
Linux `sudo dnf install -y nodejs`.

---

## Her şeyi tek komutla doğrulamak

**Linux:**

```bash
make dogrula          # hepsi
make dogrula-hizli    # Lean hariç
```

**Windows:** `make` yok. `bash dogrula.sh` Git Bash'te çalışır, ama
Python'u `.venv/bin/python` yolunda aradığı için (Windows'ta
`.venv\Scripts\python.exe`) Python katmanlarını **ATLANDI** sayar; Octave PATH'te
olmadığı için onu da atlar. Denendiğinde sonuç `GEÇTİ 3 · KALDI 0 · ATLANDI 5`
oldu. Windows'ta katmanları yukarıdaki komutlarla tek tek doğrula:

```powershell
python 02-python\src\taylor.py
python 02-python\src\kalan_dogrulama.py      # dikkat: out\ altını yeniden yazar (tuzak 4)
node 06-web\test_matematik.mjs
godot --headless --path 05-godot --script res://test_dogrulama.gd
cd 03-matlab-octave; & $oct --no-gui --quiet demo_calistir.m; cd ..
cd 04-lean; lake build; cd ..
```

---

## Tuzaklar

Kaynak: `DEVAM.md` §5, `RAPOR.md` §2, `ENVANTER.md` ve bu kılavuz
yazılırken yapılan denemeler.

1. **manim, Python 3.14'e kurulmaz.** `av<14`'ün cp314 tekerleği yok. Manim'i
   3.13 ortamında çalıştır; 3.14 ortamına `requirements.txt`'i olduğu gibi
   kurmaya çalışma.
2. **İki sanal ortamı karıştırma.** `.venv313`'ü aktive ettiysen sayısal
   betikleri orada çalıştırma. Manim'i `PATH="$PWD/.venv313/bin:$PATH"`
   önekiyle çağır.
3. **`render.sh` `out/videolar/` üzerine yazar.** Düşük kaliteyle deneme
   yapacaksan `manim -ql`'yi doğrudan çağır (çıktı `01-manim/media/`'ya,
   git-dışı), `render.sh`'ı değil.
4. **Python betikleri `out/` altını yeniden yazar.** `kalan_dogrulama.py`
   gibi betikler tabloları ve PNG'leri yeniden üretir. Platform farkı
   yüzünden (aday sayısı Windows'ta 2232, Fedora'da 2224) `git status`'ta
   değişiklik görebilirsin. Geri almak için: `git restore out/`.
5. **Lean: `release.lean-lang.org` bazı ağlarda çözülmez.** Kanal adı
   isteyen komutlar (`elan default stable`, `elan toolchain install
   stable`) bu yüzden düşer. `elan default stable`'ı **çalıştırma**: başarılı
   olsa bile varsayılan sürümü v4.34.0'ın dışına taşır ve Mathlib'in
   `.olean`'ları uyumsuz kalır. Açık sürümü GitHub'dan kur (yukarıda).
6. **`04-lean/.lake` ~8 GB'tır.** `.gitignore`'dadır; asla commit'leme.
   Silersen `lake exe cache get` ile yeniden iner.
7. **TeX Live eksik `.sty` indirmez** (MiKTeX indirir). "File ... not found"
   hatasında ilgili `texlive-*` paketini `dnf` ile kur.
8. **MiKTeX sessizce asılı kalabilir.** `-interaction=nonstopmode` tek
   başına yetmedi: eksik paket için onay beklerken `pdflatex` hiç çıktı
   üretmeden bekledi. `-enable-installer` ile çözüldü. Windows'ta son
   geçişte 1 uyarı kalır (`Package babel Warning: Configuration files are
   deprecated`); bu MiKTeX'e özgüdür, Fedora'da 0 uyarı raporlanmıştır.
9. **Web sayfası `file://` ile açılmaz** (Chrome). `python -m http.server`
   kullan.
10. **Octave Windows'ta PATH'te değildir.** `$oct` değişkeniyle tam yolu kullan.
11. **MATLAB bu depoda hiç çalıştırılamadı.** `.m` dosyaları yalnızca Octave'da
    doğrulandı; MATLAB Fedora 44'te açılışta çöktü (`RAPOR.md` §2.1).
12. **Windows konsolu Türkçe karakterleri bozabilir.** Betikler `ortam.py`
    ile kendi çıktılarını UTF-8'e çevirir. Tek satırlık `python -c`
    komutlarında ise `$env:PYTHONIOENCODING="utf-8"` gerekir.
