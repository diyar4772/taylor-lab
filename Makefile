# Taylor Laboratuvarı — derleme hedefleri
#
# DURUM: `make` bu makinede kurulu (GNU Make, /usr/bin/make). Çalıştırılan
#        hedefler: `make dogrula` (8/8 geçti) ve onun içinden `make teori`.
#        `python`, `manim`, `octave`, `lean`, `all` hedefleri make üzerinden
#        tek tek çalıştırılmadı — altlarındaki komutlar `dogrula.sh` içinde
#        doğrudan koşturuluyor.
#        Windows'ta make yoktur; katmanlar komutlarıyla tek tek çalıştırılır
#        (00-teori/obsidian/kilavuz/01-ortam-kurulumu.md).
#
# Hedefler:  make dogrula | make dogrula-hizli
#            make python | make manim | make teori | make octave | make lean
#            make web | make all | make clean

PY      ?= python
MANIM   ?= manim
OCTAVE  ?= octave-cli
QUALITY ?= -qh          # 1920x1080 @ 60fps

SCENES  := ArtanDereceSahnesi TuretmeSahnesi KalanTerimiSahnesi \
           KompleksYaricapSahnesi AnalitikDegilSahnesi DengeSahnesi

.PHONY: all python manim teori octave lean web dogrula dogrula-hizli clean

all: python manim teori web

## Tek komutluk doğrulama: her katmanın kendi testini sırayla çalıştırır,
## her biri için GEÇTİ / KALDI / ATLANDI basar, sonunda özet verir.
## Bir katman bile KALDI ise çıkış kodu 1 döner.
##
## ATLANDI, KALDI değildir: bu makinede kurulu olmayan bir aracın katmanı
## atlanır ve özette ayrıca listelenir.
dogrula:
	bash dogrula.sh

## Aynısı, ama Lean'i atlar (lake build uzun sürebilir)
dogrula-hizli:
	bash dogrula.sh --hizli

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
##
## ÜÇ geçiş: temiz bir dizinden iki geçiş yetmiyor. 1. geçiş sonunda 17
## "undefined reference" uyarısı, 2. geçiş sonunda hâlâ "Label(s) may have
## changed. Rerun to get cross-references right." kalıyor. Ancak 3. geçişte
## içindekiler, çapraz göndermeler ve hyperref yer imleri oturuyor.
teori:
	cd 00-teori && pdflatex -interaction=nonstopmode taylor-teori.tex
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
