# Sarkaç: küçük açı yaklaşımının faturası

Sarkaç: `g = 9.80665 m/s²`, `L = 1.0 m`, harmonik periyot `T₀ = 2π√(L/g) = 2.006409 s`.

`ölçülen T` sütunu, tam doğrusal-olmayan denklemin `solve_ivp` ile (`rtol=1e-12`) çözülüp periyodun **olay tabanlı sıfır geçişinden** okunmasıyla elde edildi — ızgaradan değil, adım aralığında kök bularak. `eliptik T` ise kapalı biçim `T = 4√(L/g)·K(sin²(θ₀/2))`.

| θ₀   | harmonik T₀ | ölçülen T | eliptik T | ölçüm-kapalı fark | T₀(1+θ₀²/16) | Taylor-2 hatası | Taylor-4 hatası |
|------|-------------|-----------|-----------|-------------------|--------------|-----------------|-----------------|
| 1°   | 2.006409    | 2.006447  | 2.006447  | 2.01e-12%         | 2.006447     | 0.0000%         | 0.0000%         |
| 5°   | 2.006409    | 2.007365  | 2.007365  | 1.37e-12%         | 2.007364     | 0.0000%         | 0.0000%         |
| 10°  | 2.006409    | 2.010236  | 2.010236  | 6.41e-13%         | 2.010229     | 0.0003%         | 0.0000%         |
| 20°  | 2.006409    | 2.021796  | 2.021796  | 6.59e-13%         | 2.021689     | 0.0053%         | 0.0000%         |
| 30°  | 2.006409    | 2.041338  | 2.041338  | 2.18e-14%         | 2.040789     | 0.0269%         | 0.0005%         |
| 45°  | 2.006409    | 2.086612  | 2.086612  | 1.92e-13%         | 2.083763     | 0.1366%         | 0.0055%         |
| 60°  | 2.006409    | 2.153242  | 2.153242  | 2.02e-12%         | 2.143926     | 0.4326%         | 0.0314%         |
| 90°  | 2.006409    | 2.368246  | 2.368246  | 1.03e-11%         | 2.315823     | 2.2136%         | 0.3667%         |
| 120° | 2.006409    | 2.754560  | 2.754560  | 1.63e-12%         | 2.556478     | 7.1911%         | 2.1726%         |
| 150° | 2.006409    | 3.535702  | 3.535702  | 7.46e-12%         | 2.865891     | 18.9442%        | 9.3989%         |
| 170° | 2.006409    | 4.894360  | 4.894360  | 1.28e-11%         | 3.110366     | 36.4500%        | 25.0737%        |

Ölçüm ile kapalı biçim arasındaki en büyük fark **1.3e-11%** — yani sayısal çözücü ile analitik sonuç birbirini doğruluyor. Bundan sonraki her fark, Taylor kesmesinden gelir, sayısal hatadan değil.

## Atılan terim nereye gitti?

`sin θ ≈ θ` yaklaşımı `−θ³/6` terimini atar. Harmonik osilatörde periyot genlikten **bağımsızdır** (izokronizm) — tabloda `harmonik T₀` sütunu sabittir. Gerçek sarkaçta ise periyot genlikle büyür: 10°'de fark binde 2, 90°'de %18, 170°'de iki katından fazla.

Bu büyümenin ilk mertebesi tam olarak `θ₀²/16`'dır ve doğrudan atılan `θ³/6` teriminden doğar. Yani:

> Atılan terim yok olmaz; sistemin gözlenebilir bir özelliğinde geri döner. Burada o özellik periyodun genliğe bağımlılığı, yani **anharmonisite**dir.

## Mertebe kontrolü

Düzeltmelerin kalan hatası log-log eğimlerinden okundu:

* düzeltmesiz (`T₀` tek başına): hata ~ `θ₀^2`
* `+θ₀²/16` ile: hata ~ `θ₀^4.00`  (beklenen 4)
* `+11θ₀⁴/3072` ile: hata ~ `θ₀^6.01`  (beklenen 6)

Her düzeltme mertebeyi tam olarak 2 artırıyor, çünkü periyodun genlik açılımı yalnızca çift kuvvetler içerir (`θ₀ → −θ₀` simetrisi). Bu, Taylor kesmesinin hata mertebesinin bir tahmin değil, **ölçülebilir bir öngörü** olduğunu gösterir.
