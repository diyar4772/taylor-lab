function rapor = kalan_sinir(ad, a, N, x)
%KALAN_SINIR  Gercek hatayi Lagrange siniriyla karsilastirir.
%
%   rapor = KALAN_SINIR(ad, a, N, x)
%
%   Lagrange kalani sonlu N icin bir ESITLIKTIR:
%       f(x) - P_N(x) = f^(N+1)(ksi) (x-a)^(N+1) / (N+1)!
%   Buradan cikan sinir:
%       |f(x) - P_N(x)| <= sup|f^(N+1)| * |x-a|^(N+1) / (N+1)!
%
%   rapor alanlari:
%       .gercek_hata     float64 ile olculen |f - P_N|
%       .sinir           Lagrange ust siniri
%       .yuvarlama_taban float64'un bu noktada olcebilecegi en kucuk hata
%       .oran            gercek_hata ./ sinir
%       .aday_sayisi     sinirin asildigi GORUNEN nokta sayisi
%       .yuvarlama_sayisi  sinirin yuvarlama tabaninin altinda kaldigi nokta
%       .en_kotu_oran    yalnizca ANLAMLI bolgede max(oran)
%
%   ONEMLI: aday_sayisi > 0 "teorem ihlal edildi" DEMEK DEGILDIR.
%   float64 ile olculen hata, gercek matematiksel hata sinirin cok altina
%   indiginde olcum tabanina (~eps*|f|) takilir ve sinirdan buyuk GORUNUR.
%   Bu bir teorem ihlali degil, hesap makinesinin cozunurlugudur. Hukum
%   float64'e birakilamaz; Python laboratuvarinda (02-python/src/
%   kalan_dogrulama.py) her aday mpmath ile 60 basamakta yeniden olculdu ve
%   TEYIT EDILEN ihlal sayisi 0 cikti.
%
%   MATLAB uyumlu alt kumede yazildi; Octave 10.3.0 ile dogrulandi.

  if nargin < 4
    error('kalan_sinir:girdi', 'Dort girdi gerekli: ad, a, N, x.');
  end

  x = x(:).';                      % satir vektoru
  [P, f] = taylor_yaklasim(ad, a, N, x);

  rapor.gercek_hata = abs(f - P);

  % --- Lagrange siniri
  M = turev_ustsiniri(ad, a, x, N + 1);
  rapor.sinir = M .* abs(x - a) .^ (N + 1) / factorial(N + 1);

  % --- float64 olcum tabani: n terimli toplamin klasik yuvarlama siniri
  %     |hesaplanan - gercek| <= n * eps * sum |terim_i|
  kats = taylor_katsayilari(ad, a, N);
  u = x - a;
  terim_toplami = zeros(size(x));
  for n = 0:N
    terim_toplami = terim_toplami + abs(kats(n + 1) * u .^ n);
  end
  rapor.yuvarlama_taban = (N + 2) * eps * terim_toplami;

  % --- siniflandirma
  rapor.oran = rapor.gercek_hata ./ rapor.sinir;
  rapor.aday_sayisi = sum(rapor.gercek_hata > rapor.sinir);
  yuvarlama = rapor.sinir < rapor.yuvarlama_taban;
  rapor.yuvarlama_sayisi = sum(yuvarlama);

  anlamli = ~yuvarlama & isfinite(rapor.oran);
  if any(anlamli)
    rapor.en_kotu_oran = max(rapor.oran(anlamli));
  else
    rapor.en_kotu_oran = NaN;
  end
end


function M = turev_ustsiniri(ad, a, x, m)
%TUREV_USTSINIRI  [min(a,x), max(a,x)] araliginda sup|f^(m)| (yerel yardimci).
%
%   Kapali bicimden hesaplanir. Sayisal turev kullanilmaz: m burada
%   tipik olarak 10-20 mertebesindedir ve sayisal turev o mertebede
%   tamamen anlamsizdir.

  if ~isreal(a) || ~isreal(x)
    error('kalan_sinir:reel', ...
          'Lagrange kalani reel degiskenli teoremdir; a ve x reel olmali.');
  end

  alt = min(a, x);
  ust = max(a, x);

  switch ad
    case 'exp'
      % f^(m) = e^t, en buyuk ucta
      M = exp(ust);

    case {'sin', 'cos'}
      % butun turevler +-sin, +-cos
      M = ones(size(x));

    case '1/(1-x)'
      % f^(m)(t) = m! / (1-t)^(m+1);  |1-t| en kucuk => t en buyuk
      if any(ust >= 1)
        error('kalan_sinir:aralik', ...
              '1/(1-x) icin aralik t=1 tekilligini icermemeli.');
      end
      M = factorial(m) ./ (1 - ust) .^ (m + 1);

    case 'ln(1+x)'
      % f^(m)(t) = (-1)^(m-1) (m-1)! / (1+t)^m;  |1+t| en kucuk => t en kucuk
      if any(alt <= -1)
        error('kalan_sinir:aralik', ...
              'ln(1+x) icin aralik t=-1 tekilligini icermemeli.');
      end
      M = factorial(m - 1) ./ (1 + alt) .^ m;

    case 'sqrt(1+x)'
      % f^(m)(t) = [prod_{k=0}^{m-1}(1/2 - k)] (1+t)^(1/2-m)
      if any(alt <= -1)
        error('kalan_sinir:aralik', ...
              'sqrt(1+x) icin aralik t=-1 dallanma noktasini icermemeli.');
      end
      carpim = 1;
      for k = 0:(m - 1)
        carpim = carpim * (0.5 - k);
      end
      M = abs(carpim) ./ (1 + alt) .^ (m - 0.5);

    case '1/(1+x^2)'
      error('kalan_sinir:desteklenmiyor', ...
            ['1/(1+x^2) icin kapali turev ust siniri bu dosyada yok. ' ...
             'Bu fonksiyonun ilgi cekici tarafi zaten reel eksende degil ' ...
             'kompleks duzlemdedir: yakinsaklik_diski.m kullan.']);

    otherwise
      error('kalan_sinir:ad', 'Bilinmeyen fonksiyon adi: %s', ad);
  end

  M = M .* ones(size(x));          % skalerse dizi boyuna yay
end
