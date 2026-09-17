---
title: Başla Buradan — Taylor Laboratuvarı Öğrenme Kılavuzu
tags: [kilavuz, kilavuz/moc, taylor]
created: 2026-09-17
status: tamam
aliases: [Kılavuz MOC, Taylor Lab kılavuzu]
lang: tr
---

# Başla Buradan

> [!info] Bu kılavuz ne değildir
> README'nin özeti değildir. Depoyu **sırayla, elle çalıştırarak** öğrenmek için
> yazılmış bir ders planıdır. İngilizce sürümü: [[00-START-HERE]].

## Depo ne iddia ediyor? (tek paragraf)

Taylor serisi bir hesap hilesi değil, bir fonksiyonun bir nokta civarındaki
davranışının **tam muhasebesidir**: $P_N(x)=\sum_{n\le N} \frac{f^{(n)}(a)}{n!}(x-a)^n$
yazdığında attığın her terimin faturası bir yerde kesilir. Depo bu faturanın
dört yerde kesildiğini **ölçerek** gösterir: hatada (Lagrange kalanı),
yakınsaklık yarıçapında (kompleks tekillikler), sarkacın periyodunun genliğe
bağlı olmasında (anharmonisite) ve bir enerji seviyesinin tam sayı çıkmasında
(kuantizasyon). Deponun kuralı da şudur: **çalıştırılmamış hiçbir şey için
"çalışıyor" denmez.**

## Yedi katman ve neden ayrı olduklarıyla

Katmanların hepsi **aynı sayılara farklı yollardan** varır. Bir sayı tek bir
programdan çıksaydı o programın hatasıyla ayırt edilemezdi. Bağımsız iki
uygulama aynı sayıyı veriyorsa, hata ancak ikisinde birden aynı biçimde
yapılmış olabilir, ki bu çok daha az olasıdır.

| Katman | Klasör | Soru | Neden ayrı? |
|---|---|---|---|
| Teori | `00-teori/` | Teoremler ne diyor, ispatın iskeleti ne? | Sayı değil, **gerekçe** üretir. |
| Animasyon | `01-manim/` | Bunu gözle nasıl görürüm? | Sezgi; sayılar anlık hesaplanır, uydurulmaz. |
| Sayısal çekirdek | `02-python/` | Teorem sayılarla tutuyor mu? | `out/` altındaki **bütün** tablo ve grafikler buradan çıkar. |
| MATLAB/Octave | `03-matlab-octave/` | Başka dil, başka yöntem aynı sayıyı veriyor mu? | Katsayıları sembolik türev yerine **kapalı biçimden** üretir. |
| Biçimsel | `04-lean/` | Teorem gerçekten doğru mu? | Ölçüm kanıt değildir; Lean + Mathlib makinede denetler. |
| Oyun motoru | `05-godot/` | Elle kurcalayınca ne olur? | Üçüncü bağımsız uygulama (GDScript) + etkileşim. |
| Web | `06-web/` | Kurulumsuz, tarayıcıda görebilir miyim? | Dördüncü bağımsız uygulama (JavaScript), bağımlılıksız. |

Somut örnek: 150° genlikli sarkacın periyodu Python'da (`solve_ivp`)
**3,535702 s**, JavaScript'te (RK4 + AGM) **3,535701938 s**, GDScript'te (AGM)
**3,5357019383 s** çıkıyor. Ayrıntısı [[10-yedi-sonuc#5. Küçük açı yaklaşımının faturası]].

## Önerilen okuma sırası

1. [[00-BASLA-BURADAN]] ← buradasın
2. [[01-ortam-kurulumu]]: önce araçlar
3. [[02-calisma-plani]]: **asıl ders planı** (10 oturum)
4. Katman notları; oturumlar sırasında başvuru kaynağı olarak:
   - [[05-katman-teori-latex]]
   - [[04-katman-manim]]
   - [[09-katman-web]]
   - [[03-katman-python]]
   - [[06-katman-octave]]
   - [[08-katman-godot]]
   - [[07-katman-lean]]
5. [[10-yedi-sonuc]]: yedi ana sonucun derin okuması
6. [[11-kavram-haritasi]]: kavramların birbirine bağlanması
7. [[12-eksikler-ve-devam]]: depoda **olmayan** şeyler ve bulunan hatalar

Deponun kendi atomik notları (bu kılavuzdan önce yazıldı):

- [[Taylor açılımı bir tanım değil zorunluluktur]]
- [[Yakınsaklık yarıçapı kompleks düzlemde belirlenir]]
- [[Pürüzsüz olmak analitik olmak değildir]]
- [[Her kararlı denge harmonik osilatördür]]

Görsel özet: [[kilavuz-haritasi.canvas|Kılavuz haritası (Canvas)]]

## Üç rota

> [!tip] Sadece 30 dakikam var
> 1. Web sayfasını aç ([[01-ortam-kurulumu#Web]]) ve **2 · Kompleks disk**
>    sekmesinde merkezi kaydır. (10 dk)
> 2. Videolardan `4-KompleksYaricapSahnesi.mp4`'yi izle. (1 dk)
> 3. [[10-yedi-sonuc]] içinde **3** ve **7** numaralı sonuçları oku. (15 dk)
>
> Kazanç: "yarıçap kompleks düzlemde belirlenir" ve "yakınsamak, eşit olmak
> demek değildir" fikirleri.

> [!tip] Bir akşamım var (~3 saat)
> [[02-calisma-plani]] içinde **Oturum 1, 3, 4, 7 ve 8**. Kurulum olarak
> yalnızca Python ortamı gerekir ([[01-ortam-kurulumu#Python]]).

> [!tip] Bir haftam var
> Günde 1–2 oturum: [[02-calisma-plani]]'nın tamamı (10 oturum, ~11 saat),
> ardından [[12-eksikler-ve-devam]]'daki "kendin dene" projelerinden biri.

## Bu kılavuzu Obsidian'da açmak

- Görsellerin, videoların ve kaynak kod bağlantılarının çalışması için
  **depo kökünü (`taylor-lab/`) kasa olarak aç** (Obsidian → *Open folder as
  vault*). Kılavuz göreli yollar kullanır (`../../../out/...`).
- Kılavuz hiçbir Obsidian ayarı dayatmaz; `.obsidian/` klasörü depoda yoktur.
- İstersen grafik görünümü için öneriler ve not şablonları:
  [[_sablonlar/sablonlar-hakkinda|Şablonlar hakkında]].
- Matematik `$...$` ile yazıldı; diyagramlar Mermaid bloklarıdır. İkisi de
  Obsidian'da eklentisiz çalışır.
