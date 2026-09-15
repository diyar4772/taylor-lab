# Taylor Laboratuvarı — derleme hedefleri
#
# DURUM: Bu Makefile bu makinede ÇALIŞTIRILMADI; `make` kurulu değil.
#        Windows'ta kurmak için:  winget install ezwinports.make
#        (veya GnuWin32.Make). Aynı işleri yapan ve bu makinede gerçekten
#        test edilen PowerShell muadili için: ./yap.ps1 <hedef>
#
# Hedefler:  make python | make manim | make teori | make octave | make lean
#            make web | make all | make clean

PY      ?= python
MANIM   ?= manim
OCTAVE  ?= octave-cli
QUALITY ?= -qh          # 1920x1080 @ 60fps

SCENES  := ArtanDereceSahnesi TuretmeSahnesi KalanTerimiSahnesi \
           KompleksYaricapSahnesi AnalitikDegilSahnesi DengeSahnesi

.PHONY: all python manim teori octave lean web clean

all: python manim teori web

## Sayısal laboratuvar: tüm betikleri sırayla çalıştırır, out/ altını doldurur
python:
	$(PY) 02-python/src/kalan_dogrulama.py
	$(PY) 02-python/src/kompleks_harita.py
	$(PY) 02-python/src/yakinsaklik_orani.py
	$(PY) 02-python/src/analitik_degil.py
	$(PY) 02-python/src/sarkac.py
	$(PY) 02-python/src/frobenius.py

## Altı Manim sahnesini -qh ile render eder ve out/videolar altına kopyalar
manim:
	bash 01-manim/render.sh

## LaTeX teorik metni derler, PDF'i out/ altına koyar
teori:
	cd 00-teori && pdflatex -interaction=nonstopmode taylor-teori.tex
	cd 00-teori && pdflatex -interaction=nonstopmode taylor-teori.tex
	cp 00-teori/taylor-teori.pdf out/taylor-teori.pdf

## Octave betikleri (MATLAB uyumlu)
octave:
	cd 03-matlab-octave && $(OCTAVE) --no-gui --quiet demo_calistir.m

## Lean 4 + Mathlib biçimsel ispatlar
lean:
	cd 04-lean && lake exe cache get && lake build

## Web sürümü sadece statik bir dosya; "derleme" adımı yok
web:
	@echo "06-web/index.html tarayıcıda dogrudan acilir; derleme gerekmez."

clean:
	rm -rf 01-manim/media media
	rm -f 00-teori/*.aux 00-teori/*.log 00-teori/*.out 00-teori/*.toc
	find . -name "__pycache__" -type d -exec rm -rf {} +
