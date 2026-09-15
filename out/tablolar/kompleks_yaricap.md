# Yakınsaklık yarıçapı = en yakın tekilliğe uzaklık

Her harita, merkez `a` etrafında kompleks düzlemde `(1/N)·log10|f(z) - P_28(z)|` değerini gösterir. Bu büyüklük `log10(|z-a|/R)`'ye yakınsar: **işareti** yakınsaklığı söyler (negatif = yakınsıyor, pozitif = ıraksıyor) ve sıfır düzeyi tam olarak `|z-a| = R` çemberidir. Yakınsaklık diski harita tarafından **çizilmez**; hatanın kendi davranışından doğar. `haritadan okunan R`, bu haritanın **kendi** sıfır düzeyinin merkeze en kısa uzaklığıdır — yani teorik değer hiç kullanılmadan elde edilmiş bağımsız bir kestirimdir.

| durum                     | a  | tekillikler | teorik R | haritadan okunan R |
|---------------------------|----|-------------|----------|--------------------|
| 1/(1+z^2),  a=0           | 0  | 0+1j, -0-1j | 1.0000   | 0.9366             |
| 1/(1-z),  a=0             | 0  | 1+0j        | 1.0000   | 0.9219             |
| ln(1+z),  a=0             | 0  | -1+0j       | 1.0000   | 0.9953             |
| e^z,  a=0  (tekillik yok) | 0  | yok         | ∞        | —                  |
| 1/(1+z^2),  a=1           | 1  | 0+1j, -0-1j | 1.4142   | 1.3321             |
| 1/(1-z),  a=-1            | -1 | 1+0j        | 2.0000   | 1.8681             |

Son iki satır işin özünü söyler: fonksiyon aynı, merkez farklı, yarıçap farklı. `1/(1+z²)` için `a=0` iken R=1 (±i'ye uzaklık), `a=1` iken R=√2≈1.4142 (yine ±i'ye uzaklık, ama artık 1'den). `1/(1-z)` için `a=0` iken R=1, `a=-1` iken R=2. **Yarıçap fonksiyonun değil, (fonksiyon, merkez) çiftinin özelliğidir ve her seferinde en yakın tekilliğe olan uzaklıktır.**

`e^z` panelinde disk yoktur, çünkü tekillik yoktur: R = ∞. Pencerenin tamamı yakınsama bölgesidir ve haritadan bir sınır okunamaz (tablodaki `—`).

## Sonlu N'in dürüst payı

Haritadan okunan değerler teorik R'nin sistematik olarak biraz altında çıkıyor (%5–8). Bu bir hata değil, sonlu N'in kaçınılmaz payı: `(1/N)·log|hata| → log(|z-a|/R)` yakınsaması ancak N→∞ limitinde tamdır. Sonlu N'de kuyruktaki cebirsel çarpanlar (`C`, `N+1` yerine `N`'e bölmek, vb.) sıfır düzeyini biraz içeri çeker.

Aynı sebeple `ln(1+z)` panelinde siyah kontur gözle görülür biçimde **çember değildir** — sola, tekilliğin bulunduğu `z=-1` yönüne doğru basıktır. `ln(1+z)` katsayıları `1/n` gibi cebirsel azaldığı için (kutuplu fonksiyonlardaki geometrik azalmanın aksine) yakınsama N ile daha yavaş sıkışır. N büyütüldükçe kontur çembere oturur; teoremin söylediği de zaten limitteki şekildir.
