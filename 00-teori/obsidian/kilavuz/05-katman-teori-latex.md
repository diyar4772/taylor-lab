---
title: Katman — Teori (LaTeX)
tags: [kilavuz, kilavuz/katman, teori]
created: 2026-09-17
status: tamam
lang: tr
---

# Katman: Teori (`00-teori/`)

↑ [[00-BASLA-BURADAN]] · Plan: Oturum 1, 4, 7, 9 · English: [[05-layer-theory-latex]]

## Hangi soruyu cevaplıyor?

"Sayıların **neden** böyle çıktığını söyleyen teorem hangisi, ve ispatının
iskeleti ne?" Diğer katmanlar ölçer; bu katman gerekçelendirir.

## Dosyalar

| Dosya | İçerik |
|---|---|
| `taylor-teori.tex` | 8 sayfalık metnin kaynağı |
| `obsidian/*.md` | Dört atomik not (aşağıda) |
| `obsidian/kilavuz/`, `obsidian/guide/` | Bu kılavuz (TR / EN) |
| `../out/taylor-teori.pdf` | Derlenmiş PDF |

### `taylor-teori.tex` bölüm bölüm

| § | Başlık | Ana sonuç | Hangi betik ölçüyor |
|---|---|---|---|
| 1 | Katsayılar: $n!$ bir süsleme değildir | Önerme: $P^{(n)}(a)=n!\,c_n$ ⇒ $c_n=f^{(n)}(a)/n!$; polinom / seri tanımı | `taylor.py` testi |
| 2 | Taylor teoremi ve Lagrange kalanı | Teorem (Rolle'ün $N+1$ kez uygulanmasıyla ispat); hata sınırı sonucu | `kalan_dogrulama.py` |
| 3 | Yakınsaklık yarıçapı kompleks düzlemin geometrisidir | Cauchy–Hadamard; $R=\operatorname{dist}(a,\Sigma)$; merkez kaydırma tablosu; $L_N(z)$ haritası | `kompleks_harita.py`, `yakinsaklik_orani.py` |
| 4 | Pürüzsüz ama analitik değil | $e^{-1/x^2}$ teoremi, $f^{(n)}(x)=p_n(1/x)e^{-1/x^2}$ tümevarımı | `analitik_degil.py` |
| 5 | Her kararlı denge harmonik osilatördür | $V(x_0+u)$ açılımı; sarkaç ve $T=T_0(1+\theta_0^2/16+11\theta_0^4/3072+\cdots)$ | `sarkac.py` |
| 6 | Bonus: Frobenius serileri | Legendre ve Hermite reküransları, kesilme şartı | `frobenius.py` |
| 7 | Toparlama | Altı maddelik özet | — |
| — | Kaynakça | Rudin, Ahlfors, Stein–Shakarchi, Whittaker–Watson, Arfken, Landau–Lifshitz, Griffiths | — |

### Dört atomik not

- [[Taylor açılımı bir tanım değil zorunluluktur]]: §1
- [[Yakınsaklık yarıçapı kompleks düzlemde belirlenir]]: §3
- [[Pürüzsüz olmak analitik olmak değildir]]: §4
- [[Her kararlı denge harmonik osilatördür]]: §5, §6

## Nasıl derlenir

Ayrıntı ve tuzaklar: [[01-ortam-kurulumu#LaTeX]]. **Üç geçiş** gerekir.

```powershell
cd 00-teori
1..3 | ForEach-Object { pdflatex -interaction=nonstopmode -enable-installer taylor-teori.tex | Out-Null }
cd ..
```

```bash
make teori
```

## Çıktı nerede?

`00-teori/taylor-teori.pdf` (git-dışı) ve `make teori` ile
`out/taylor-teori.pdf`. Ara dosyalar (`.aux`, `.log`, `.out`, `.toc`)
`.gitignore`'dadır.

## Ön bilgi

- Analiz I: Rolle teoremi, ortalama değer teoremi, türev.
- Kuvvet serileri, $\limsup$.
- Kompleks analiz: holomorf fonksiyon, kutup, esas tekillik.
- Fizik: potansiyel enerji, küçük salınımlar; kuantum harmonik osilatörün ne olduğu.

## Metindeki iki küçük tutarsızlık

- §2 float64'te **2232** aday ihlal yazar. Bu Windows sayısıdır; README ve
  tablo Fedora'daki **2224**'ü verir. İkisi de doğrudur, platforma bağlıdır
  ([[10-yedi-sonuc#1. Lagrange sınırı hiç ihlal edilmedi]]).
- Dosyanın 2. satırındaki yorum "iki kez" derler der; doğrusu üç geçiştir
  (`Makefile` açıklaması).
- §3'ün "oran testi %22,66 sapar" cümlesi için bkz. [[12-eksikler-ve-devam]].

## Kurcalama önerileri

1. **Tabloyu genişlet.** §3'teki "Merkezi kaydırmak" tablosuna $a=-1$ ve
   $a=0{,}5$ satırlarını ekle ($R=\sqrt2$, $R=\sqrt{1{,}25}\approx1{,}118$).
   Değerleri `godot --headless … test_dogrulama.gd`'nin kullandığı `yaricap()`
   formülüyle karşılaştır.
2. **İspatı kendin yaz.** §2'deki Rolle ispatını kapat ve $N=1$ için
   ($f(x)=f(a)+f'(a)(x-a)+\tfrac12 f''(\xi)(x-a)^2$) kâğıtta baştan kur.
   Sonra `ksi_varligi.md`'deki `sin, N=3, x=1.2` satırını elle doğrula:
   $\sin\xi=(\sin1{,}2-P_3(1{,}2))\cdot 4!/1{,}2^4$ ⇒ $\xi\approx0{,}2341$.
3. **Yeni bölüm.** [[12-eksikler-ve-devam]]'daki "sarkaç serisinin yarıçapı
   $\pi$" gözlemini §5'e bir "Not" kutusu (`notkutusu` ortamı) olarak ekle ve
   üç geçişle derle.

## İlgili

[[03-katman-python]] · [[07-katman-lean]] · [[11-kavram-haritasi]]
