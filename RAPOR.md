# RAPOR — ne çalıştı, ne çalışmadı

Bu dosyanın tek işi dürüstlük. Projenin kuralı baştan beri şuydu:
**çalıştırılmamış hiçbir şey için "çalışıyor" denmez.** Aşağıdaki her
"✅", bu makinede gerçekten koşturulmuş bir komutun karşılığıdır; her "❌"
ise neyin neden yapılamadığını söyler.

- **Makine:** Fedora Linux 44, KDE Plasma 6.7.5, x86_64, glibc 2.43, GCC 16.2.1
- **Tarih:** 2026-09-17
- **Önceki makine:** Windows 11 Home, Python 3.13.7 (geçiş notları `ENVANTER.md`'de)

---

## 1. Katman katman durum

| Katman | Dosya sayısı | Durum | Nasıl doğrulandı |
|---|---|---|---|
| `00-teori/` LaTeX | 1 `.tex` | ✅ | `pdflatex` ×3 → 8 sayfa, **0 hata, 0 uyarı, 0 taşma** |
| `00-teori/obsidian/` | 4 not | ✅ | 19 wikilink tarandı, **0 kırık** |
| `01-manim/` | 6 sahne | ⚠️ kısmi | 1. sahne Fedora'da yeniden render edildi; 2–6 Windows çıktıları |
| `02-python/` | 7 betik | ✅ | `taylor.py` ve `kalan_dogrulama.py` koşturuldu |
| `03-matlab-octave/` | 5 `.m` | ⚠️ kısmi | Octave 10.3.0'da koştu; **MATLAB'da denenemedi** |
| `04-lean/` | 4 `.lean` | ✅ | `lake build` 2777 iş, **0 `sorry`** |
| `05-godot/` | 2 sahne | ⚠️ kısmi | Mantık ve yükleme doğrulandı; **görüntüsü doğrulanmadı** |
| `06-web/` | 1 `.html` | ✅ | 34 birim testi + Chrome'da 3 panel, konsol hatası yok |

### Çalıştırılan komutlar ve sonuçları

| Komut | Sonuç |
|---|---|
| `python 02-python/src/taylor.py` | ✅ "Tüm kontroller geçti." |
| `python 02-python/src/kalan_dogrulama.py` | ✅ çıkış kodu 0, 11,7 sn |
| `pdflatex -interaction=nonstopmode taylor-teori.tex` **×3** | ✅ 8 sayfa A4, 0 hata / 0 uyarı |
| `bash 01-manim/render.sh 1` (`-qh`) | ✅ 25,250000 sn · 1920×1080 · 60 fps |
| `octave-cli --no-gui --quiet demo_calistir.m` | ✅ çıkış kodu 0 |
| `make octave` | ✅ çıkış kodu 0 |
| `lake build` (04-lean) | ✅ 2777 iş, hatasız |
| `#print axioms` × 7 teorem | ✅ yalnız `propext`, `Classical.choice`, `Quot.sound` |
| `godot --headless --script res://test_dogrulama.gd` | ✅ **30/30** kontrol |
| `godot --headless --quit-after 90` (iki sahne) | ✅ ikisi de hatasız |
| `node 06-web/test_matematik.mjs` | ✅ **34/34** kontrol |
| `06-web/index.html` Chrome'da | ✅ 3 panel çalıştı, konsol hatası yok |

---

## 2. Çalışmayanlar

### 2.1 MATLAB — kurulu, lisanslı, **açılmıyor**

Bu projenin en büyük eksiği. MATLAB R2026a Update 5 kurulu ve lisanslı, ama
yorumlayıcı başlamadan çöküyor:

```
MATLAB: builtin/registry_file_utils.cpp:335: ... InstallBuiltinFunctions(...):
Assertion `Builtin Parsing Error found in:
  .../builtins/matlab_toolbox_strfun_string/mwstring_builtinimpl.so.
Details: Error while trying to save LXE Object runtime information. ...
missing 'mxClassName' and/or 'variantId' as keys' failed.
```

Teşhis:

- **Lisans sorunu değil** — çöküş lisans denetiminden önce, yerleşik fonksiyon
  kaydı kurulurken oluşuyor.
- **Tek bozuk dosya da değil** — art arda çalıştırmalarda hata her seferinde
  *başka* bir `*_builtinimpl.so`'da çıkıyor (`mwstring`, `mwdictionary`, …).
- `-nojvm -nodisplay` ve `MW_DISABLE_LXE=1` denendi; ikisi de aynı hatayı verdi.
- En olası sebep: Fedora 44'ün tabanı (glibc 2.43, GCC 16) MathWorks'ün
  desteklediği dağıtımların (RHEL/Ubuntu LTS) çok ilerisinde. MATLAB Fedora'yı
  resmen desteklemez.

**Sonuç:** `03-matlab-octave/*.m` dosyaları MATLAB uyumlu alt kümede yazıldı
ve Octave 10.3.0 ile doğrulandı. MATLAB uyumluluğu **yalnızca statik olarak**
denetlendi: yorumlar ve metin sabitleri ayıklandıktan sonra Octave'a özgü yapı
(`printf`, `endfunction`, `++`, `!=`, `#` yorum, `do…until`, çift tırnaklı
metin) bulunmadı ve her dosyada ana fonksiyon adı dosya adıyla aynı.
**Bu bir söz değildir; MATLAB'da çalıştıkları gösterilemedi.**

### 2.2 Godot sahnelerinin görüntüsü doğrulanmadı

`test_dogrulama.gd` sahnelerin **matematiğini** 30 kontrolle doğruluyor ve iki
sahne de headless olarak 90 kare hatasız koşuyor. Ama `--headless` çizim
yapmaz. Pencere açıp ekran görüntüsü alma adımı kullanıcı tarafından
durduruldu, dolayısıyla **sahnelerin nasıl göründüğü doğrulanmadı.**
Elle açıp bakmak gerekir:

```bash
godot --path 05-godot
```

### 2.3 Manim: 6 sahnenin 5'i Fedora'da yeniden üretilmedi

1. sahne `-qh` ile yeniden render edildi ve Windows çıktısıyla **birebir aynı**
   süreyi/çözünürlüğü/kare hızını verdi (25,25 sn · 1920×1080 · 60 fps). Bu,
   zincirin çalıştığını gösterir. Kalan 5 video hâlâ Windows'ta üretilmiş
   dosyalardır; tümünü yeniden üretmek ~8 dakika sürer:

```bash
PATH="$PWD/.venv313/bin:$PATH" bash 01-manim/render.sh
```

### 2.4 Manim, sistem Python'ıyla kurulamadı

Fedora 44'ün Python'ı 3.14.7. `manim==0.19.0`, `av>=9,<14` istiyor; PyPI'da
Python 3.14 için en eski `av` tekerleği 15.1.0. pip kaynaktan derlemeye düşüyor
ve ffmpeg başlıklarını bulamıyor. `av` **dışındaki** bütün manim bağımlılıkları
için 3.14 tekerleği var (`pip install --only-binary=:all: --dry-run manim`
ile doğrulandı).

Çözüm: manim'e ayrı bir Python 3.13 ortamı verildi. **Depoda artık iki sanal
ortam var** ve karıştırılmamalıdır:

| Ortam | Python | Ne için |
|---|---|---|
| `.venv/` | 3.14.7 | bütün sayısal betikler |
| `.venv313/` | 3.13.15 | **yalnızca** manim |

### 2.5 Lean: DNS engeli vardı, aşıldı

Windows'ta `elan default stable` `Could not resolve host: release.lean-lang.org`
ile düşüyordu. **Fedora'da da aynen tekrarlandı.** Ama teşhis bir adım ileri
götürülünce engelin dar olduğu görüldü:

| Host | Ne için | Yerel ISS çözümleyicisi |
|---|---|---|
| `release.lean-lang.org` | toolchain **index**'i (Cloudflare Pages) | ❌ çözemiyor |
| `releases.lean-lang.org` | toolchain **dosyaları** | ✅ |
| `github.com` | Mathlib deposu | ✅ |
| `cache.mathlib.org` | Mathlib `.olean` önbelleği | ✅ |

Kırık olan tek şey index adının çözümlenmesiydi. Toolchain elle indirilip
`~/.elan/toolchains/leanprover--lean4---v4.34.0` altına açıldı; Mathlib
`lakefile.toml`'da Reservoir yerine doğrudan git ile istendi. **Sudo
gerekmedi, DNS'e dokunulmadı.** Ayrıntı: `LEAN-DURUM.md`.

> Uyarı: `elan default stable` gibi index'e giden komutlar bu ağda hâlâ düşer.

---

## 3. Bulunan ve düzeltilen gerçek hatalar

Bu bölüm projenin en öğretici kısmı. Hataların çoğu **elle türetilmiş kapalı
biçimlerden** ve **hiç çalıştırılmamış koddan** çıktı.

### 3.1 `02-python/src/taylor.py` — hiç çalıştırılmamış test bloğu

```
AttributeError: 'KalanRaporu' object has no attribute 'ihlal_sayisi'.
Did you mean: 'aday_sayisi'?
```

Alan, "float64 ihlal *sanabilir*, karar veremez" ayrımı eklenirken yeniden
adlandırılmış ama kendi kendine test bloğu güncellenmemişti. Bu blok Windows
oturumunda **hiç çalıştırılmamış olmalı.** Geçişin ilk doğrulama komutunda
ortaya çıktı.

### 3.2 `00-teori/taylor-teori.tex` — ortam adı TeX komutuyla çakışıyor

`\newtheorem*{not}{Not}` tanımı TeX'in `\not` matematik komutuyla çakışıyordu.
`\begin{not}` matematik kipi açıyor, ardından Türkçe harfler "matematik
kipinde geçersiz komut" hatası veriyor ve belge bozuluyordu. Hata mesajları
(`Missing $ inserted`) sebebi değil sonucu gösteriyordu. `notkutusu` olarak
yeniden adlandırıldı.

### 3.3 `00-teori/taylor-teori.tex` — babel kısayolu enumitem'i bozuyor

Türkçe babel `:`, `!` ve `=` karakterlerini "kısayol" (shorthand) yapar.
Aktif `=` yüzünden `enumitem`'in `leftmargin=*` anahtarı çözülemiyordu:

```
! Package enumitem Error: leftmargin=* undefined.
```

Çözüm `\usepackage[shorthands=off,turkish]{babel}` — Türkçe heceleme kalır,
kısayollar kalkar.

### 3.4 `00-teori/taylor-teori.tex` — PDF yer imi uyarıları

`hyperref` bölüm başlıklarındaki matematiği PDF yer imine çeviremiyordu.
`[unicode]` seçeneği ve `\texorpdfstring` ile giderildi.

> **Kendi hatam:** bunu ilk raporlarken "0 uyarı" demiştim; oysa yalnızca
> `LaTeX Warning` satırlarını taramıştım, `Package … Warning` satırlarını
> değil. Uyarılar oradaydı. Şimdi **her türde uyarı 0**.

### 3.5 `05-godot/taylor_explorer.gd` — katsayıda işaret hatası

`1/(1+x²)` katsayısı elle türetilmişti. Doğrusu

$$c_n = (-1)^n \operatorname{Im}\!\left(\frac{1}{(a-i)^{n+1}}\right)$$

iken kod `-Im(...)` alıyordu. Yani bütün seri ters işaretliydi. Grafik
"makul" göründüğü için gözle yakalanamazdı; `test_dogrulama.gd` bunu
`c_0 = -1` (olması gereken `+1`) diye anında yakaladı.

**Ders:** elle türetilen her kapalı biçim test edilmeli. Bu yüzden hem
`05-godot/test_dogrulama.gd` hem `06-web/test_matematik.mjs` depoda duruyor.

### 3.6 `05-godot/taylor_explorer.gd` — gizli Kiril harfi

Bir biçim dizgisinde ASCII `a` yerine Kiril `а` (U+0430) vardı. Gözle
ayırt edilemez. ASCII dışı karakter taramasıyla bulundu.

### 3.7 `05-godot/*.gd` — sabit pencere boyutu varsayımı

Çizim kodu 1280×720 varsayıyordu. `project.godot` görüntü alanı 1600×900'e
çıkarılınca sahne sol üst köşeye sıkıştı. Yerleşim `get_viewport_rect()`
üzerinden hesaplanacak şekilde yeniden yazıldı.

### 3.8 `06-web/test_matematik.mjs` — testin kendisindeki hata

Testin `index.html`'den matematik çekirdeğini kesen düzenli ifadesi fazla
geniş eşleşip kaynağı bozuyordu. Testi çalıştırmak testi düzeltti.

---

## 4. Bağımsız çapraz doğrulama

Projenin en güçlü yanı: aynı sayı **birbirinden bağımsız uygulamalarda**
üretildi. Biri yanılsa öbürü tutmazdı.

### 4.1 Sarkaç periyodu — 3 bağımsız uygulama

| θ₀ | Python (`solve_ivp`) | JavaScript (RK4 + AGM) | GDScript (AGM) |
|---|---|---|---|
| 10° | 2,010236 | 2,010235893 | 2,0102358926 |
| 45° | 2,086612 | 2,086612180 | 2,0866121798 |
| 90° | 2,368246 | 2,368246346 | 2,3682463463 |
| 150° | 3,535702 | 3,535701938 | 3,5357019383 |

Üç ayrı dil, üç ayrı sayısal yöntem, yedi haneye kadar aynı sonuç.

### 4.2 Yakınsaklık diski — 2 bağımsız uygulama

Disk **çizilmiyor**, hatanın kendi davranışından çıkarılıyor. Aynı ölçüm
Python ve Octave'da ayrı ayrı yapıldı:

| f | a | teorik R | Python | Octave |
|---|---|---|---|---|
| 1/(1+z²) | 0 | 1,0000 | 0,9366 | 0,9266 |
| 1/(1−z) | 0 | 1,0000 | 0,9219 | 0,9165 |
| ln(1+z) | 0 | 1,0000 | 0,9953 | 0,9967 |
| 1/(1+z²) | 1 | 1,4142 | 1,3321 | 1,3233 |
| 1/(1−z) | −1 | 2,0000 | 1,8681 | 1,8564 |

Aradaki küçük fark ızgara çözünürlüğünden. **Sapmanın hep negatif olması
bir hata değil:** `(1/N)log|hata| → log(|z−a|/R)` yakınsaması ancak
`N → ∞` limitinde tamdır.

### 4.3 Lagrange oranı

`sin`, `a=0`, `N=5` için en kötü hata/sınır oranı:
Python `taylor.py` **0,2704** — Octave `kalan_sinir.m` **0,2704**.

---

## 5. Sayısal iddiaların özeti

- **Lagrange sınırı:** 144 096 nokta tarandı. float64 ile **2224 aday ihlal**
  çıktı; adayların **tamamı** mpmath ile 60 basamakta yeniden ölçüldü ve
  **teyit edilen ihlal sayısı 0**.
- **ξ'nin varlığı:** yakınsaklık yarıçapının *dışındaki* bir noktada bile
  (`ln(1+x)`, `x=1,8`) bulundu: ξ ≈ 0,14356869, eşitlik artığı 4,22×10⁻¹⁵.
- **Sarkaç:** `solve_ivp` ölçümü eliptik kapalı biçimle **1,3×10⁻¹¹ %**
  uyumlu. Taylor düzeltmelerinin kalan hata mertebeleri log–log eğiminden
  **4,00** ve **6,01** (beklenen 4 ve 6).
- **Frobenius:** Legendre ve Hermite polinomları sympy ile denkleme konuldu,
  kalıntı **tam olarak 0**.
- **Lean:** 7 teorem, `lake build` 2777 iş hatasız, **`sorryAx` yok**.

### Platformlar arası fark (beklenen, zararsız)

| | Windows 11 / Py 3.13.7 | Fedora 44 / Py 3.14.7 |
|---|---|---|
| taranan nokta | 144 096 | 144 096 |
| **aday** ihlal (float64) | 2232 | **2224** |
| mpmath ile **teyit edilen** ihlal | 0 | **0** |

Aday sayısı platformun `libm`'ine bağlı olduğu için birkaç birim oynar. Asıl
iddia olan **teyit edilen ihlal = 0** iki platformda da aynı çıktı —
laboratuvarın "hükmü float64'e bırakma" tasarımı tam da bunun içindi.

---

## 6. Bilerek yapılmayanlar

Bunlar eksik değil, kapsam dışı:

1. **Lean'de dört konu ele alınmadı:** "R = en yakın tekilliğe uzaklık"ın
   biçimsel ifadesi, sarkaç/harmonik osilatör, Frobenius/kuantizasyon, ve
   `e^(−1/x²)`'nin kendisi için ayrı tanık (Mathlib'in tanığı `e^(−1/x)`'tir —
   aynı olgunun bir değişkesi). Ayrıntı `LEAN-DURUM.md`.
2. **`1/(1+x²)` için Lagrange sınırı** Octave katmanında yok; kapalı türev üst
   sınırı yazılmadı. O fonksiyonun ilgi çekici tarafı zaten reel eksende değil
   kompleks düzlemdedir (`yakinsaklik_diski.m`).
3. **Web sayfası yalnızca Chrome'da** denendi.

---

## 7. Yeniden üretme

```bash
# ortam
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
python3.13 -m venv .venv313 && .venv313/bin/pip install -r requirements.txt

# katmanlar
.venv/bin/python 02-python/src/kalan_dogrulama.py
PATH="$PWD/.venv313/bin:$PATH" bash 01-manim/render.sh
(cd 00-teori && for i in 1 2 3; do pdflatex -interaction=nonstopmode taylor-teori.tex; done)
(cd 03-matlab-octave && octave-cli --no-gui --quiet demo_calistir.m)
(cd 04-lean && lake build)
godot --headless --path 05-godot --script res://test_dogrulama.gd
node 06-web/test_matematik.mjs
```

Sistem gereksinimleri ve tuzaklar: `ENVANTER.md` ve `DEVAM.md` §5.
