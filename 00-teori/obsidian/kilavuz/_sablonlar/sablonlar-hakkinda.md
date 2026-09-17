---
title: Şablonlar ve Obsidian önerileri
tags: [kilavuz, kilavuz/sablon]
created: 2026-09-17
status: tamam
lang: tr
---

# Şablonlar ve Obsidian önerileri

↑ [[00-BASLA-BURADAN]] · English: [[templates-readme]]

Bu klasördeki üç dosya, Obsidian'ın **yerleşik Templates eklentisi**
sözdizimiyle (`{{title}}`, `{{date}}`) yazıldı; topluluk eklentisi gerekmez.

| Şablon | Ne zaman |
|---|---|
| [[oturum-kaydi]] | [[02-calisma-plani]]'ndaki her oturumun sonunda |
| [[deney-kaydi]] | Katman notlarındaki "kurcalama önerileri"nden birini denediğinde |
| [[kavram-karti]] | [[11-kavram-haritasi]]'na kendi kavramını eklemek istediğinde |

## Kullanmak için (senin kasanda, senin kararınla)

Bu depo hiçbir `.obsidian/` ayarı içermez. İstersen:

1. *Settings → Core plugins → Templates*'i aç.
2. *Template folder location* = `00-teori/obsidian/kilavuz/_sablonlar`
   (depo kökünü kasa olarak açtıysan).
3. Yeni notta *Insert template* komutunu kullan.

Templater kullanıyorsan `{{date}}` yerine `<% tp.date.now("YYYY-MM-DD") %>`
yazabilirsin.

## Grafik görünümü için öneri

*Graph view → Groups* bölümüne şu sorguları renkli grup olarak eklersen
kılavuzun yapısı görünür hâle gelir:

| Sorgu | Anlamı |
|---|---|
| `tag:#kilavuz/moc` | giriş noktası |
| `tag:#kilavuz/plan` | çalışma planı |
| `tag:#kilavuz/katman` | yedi katman notu |
| `tag:#kilavuz/sonuc OR tag:#kilavuz/kavram` | sonuçlar ve kavramlar |
| `path:00-teori/obsidian -path:kilavuz -path:guide` | deponun dört atomik notu |
| `path:guide` | İngilizce sürüm |

Filtre olarak `path:00-teori/obsidian` kullanmak, kaynak kod ve çıktı
dosyalarını grafikten gizler.

Görsel harita: [[kilavuz-haritasi.canvas|Canvas]].
