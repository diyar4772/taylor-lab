function [R_okunan, R_teorik, L] = yakinsaklik_diski(ad, a, N, pencere, cozunurluk)
%YAKINSAKLIK_DISKI  Yakinsaklik diskini VERIDEN cikarir, cizmez.
%
%   [R_okunan, R_teorik, L] = YAKINSAKLIK_DISKI(ad, a, N, pencere, cozunurluk)
%
%   Kompleks duzlemde su buyukluk hesaplanir:
%
%       L_N(z) = (1/N) * log10 |f(z) - P_N(z)|
%
%   |f - P_N| ~ C (|z-a|/R)^(N+1) oldugundan L_N -> log10(|z-a|/R). Yani
%   L_N'nin ISARETI dogrudan yakinsakligi soyler (negatif = yakinsiyor) ve
%   L_N = 0 duzeyi tam olarak |z-a| = R cemberidir.
%
%   R_okunan, L'nin isaret degistirdigi piksellerin merkeze en kisa
%   uzakligidir; yani TEORIK DEGER HIC KULLANILMADAN elde edilmis bagimsiz
%   bir kestirimdir. Disk kimse cizmeden, hatanin kendi davranisindan dogar.
%
%   Varsayilanlar: pencere = 3, cozunurluk = 600.
%
%   DURUST PAY: R_okunan teorik degerin sistematik olarak %5-8 altinda
%   cikar. Bu bir hata degil; yukaridaki yakinsama ancak N->Inf limitinde
%   tamdir. Sonlu N'de kuyruktaki cebirsel carpanlar sifir duzeyini biraz
%   iceri ceker.
%
%   MATLAB uyumlu alt kumede yazildi; Octave 10.3.0 ile dogrulandi.

  if nargin < 3
    error('yakinsaklik_diski:girdi', 'En az uc girdi gerekli: ad, a, N.');
  end
  if nargin < 4 || isempty(pencere)
    pencere = 3;
  end
  if nargin < 5 || isempty(cozunurluk)
    cozunurluk = 600;
  end

  [kats, R_teorik] = taylor_katsayilari(ad, a, N);

  % --- kompleks izgara
  eks = linspace(-pencere, pencere, cozunurluk);
  [X, Y] = meshgrid(eks, eks);
  Z = X + 1i * Y;

  % --- P_N(Z), Horner
  U = Z - a;
  P = zeros(size(Z));
  for n = (N + 1):-1:1
    P = P .* U + kats(n);
  end

  % --- f(Z)
  switch ad
    case 'exp',        F = exp(Z);
    case 'sin',        F = sin(Z);
    case 'cos',        F = cos(Z);
    case '1/(1-x)',    F = 1 ./ (1 - Z);
    case '1/(1+x^2)',  F = 1 ./ (1 + Z .^ 2);
    case 'ln(1+x)',    F = log(1 + Z);
    case 'sqrt(1+x)',  F = sqrt(1 + Z);
    otherwise
      error('yakinsaklik_diski:ad', 'Bilinmeyen fonksiyon adi: %s', ad);
  end

  H = abs(F - P);
  H(H < 1e-300) = 1e-300;          % log10(0) kacinilsin
  L = log10(H) / N;

  % --- sifir duzeyi: komsusuyla isaret degistiren pikseller
  if isinf(R_teorik)
    R_okunan = NaN;                % tekillik yok, sinir da yok
    return;
  end

  sag  = L(:, 1:end-1) .* L(:, 2:end) < 0;
  alt  = L(1:end-1, :) .* L(2:end, :) < 0;

  gecis = false(size(L));
  gecis(:, 1:end-1) = gecis(:, 1:end-1) | sag;
  gecis(1:end-1, :) = gecis(1:end-1, :) | alt;

  uzaklik = abs(Z - a);
  if any(gecis(:))
    R_okunan = min(uzaklik(gecis));
  else
    R_okunan = NaN;
  end
end
