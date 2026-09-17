function [P, fdeg] = taylor_yaklasim(ad, a, N, x)
%TAYLOR_YAKLASIM  N. dereceden Taylor polinomunu ve fonksiyonun kendisini hesaplar.
%
%   [P, fdeg] = TAYLOR_YAKLASIM(ad, a, N, x)
%
%   P    : P_N(x), Horner semasiyla hesaplanir
%   fdeg : f(x), karsilastirma icin
%
%   x reel ya da kompleks, skaler ya da dizi olabilir. a kompleks olabilir.
%
%   Ornek:
%       [P, f] = taylor_yaklasim('1/(1+x^2)', 0, 8, 0.5);
%       abs(f - P)      % 1.2e-03 mertebesinde
%
%   MATLAB uyumlu alt kumede yazildi; Octave 10.3.0 ile dogrulandi.

  if nargin < 4
    error('taylor_yaklasim:girdi', 'Dort girdi gerekli: ad, a, N, x.');
  end

  kats = taylor_katsayilari(ad, a, N);

  % Horner: P = ((c_N*u + c_{N-1})*u + ...)*u + c_0,  u = x - a
  u = x - a;
  P = zeros(size(x));
  for n = (N + 1):-1:1
    P = P .* u + kats(n);
  end

  if nargout > 1
    fdeg = fonksiyon_degeri(ad, x);
  end
end


function y = fonksiyon_degeri(ad, x)
%FONKSIYON_DEGERI  Katalogdaki f'in x'teki degeri (yerel yardimci).
  switch ad
    case 'exp'
      y = exp(x);
    case 'sin'
      y = sin(x);
    case 'cos'
      y = cos(x);
    case '1/(1-x)'
      y = 1 ./ (1 - x);
    case '1/(1+x^2)'
      y = 1 ./ (1 + x .^ 2);
    case 'ln(1+x)'
      y = log(1 + x);
    case 'sqrt(1+x)'
      y = sqrt(1 + x);
    otherwise
      error('taylor_yaklasim:ad', 'Bilinmeyen fonksiyon adi: %s', ad);
  end
end
