function [kats, R, tekillikler] = taylor_katsayilari(ad, a, N)
%TAYLOR_KATSAYILARI  a merkezli Taylor katsayilarini KAPALI BICIMDEN uretir.
%
%   [kats, R, tekillikler] = TAYLOR_KATSAYILARI(ad, a, N)
%
%   ad   : 'exp' | 'sin' | 'cos' | '1/(1-x)' | '1/(1+x^2)' | 'ln(1+x)' |
%          'sqrt(1+x)'
%   a    : acilim merkezi (reel ya da KOMPLEKS olabilir)
%   N    : en buyuk derece
%
%   kats : 1x(N+1) vektor; kats(n+1) = c_n, yani f^(n)(a)/n!
%   R    : yakinsaklik yaricapi = merkezin en yakin tekillige uzakligi
%          (tekillik yoksa Inf)
%   tekillikler : tekillik noktalari (kompleks), yoksa bos
%
%   Sayisal turev BILEREK kullanilmadi. Yuksek mertebeli sayisal turev
%   coker; bu laboratuvarin iddiasi ise tam olarak yuksek mertebelerin
%   davranisidir. Kapali bicimler a merkezli acilimdan gelir, dolayisiyla
%   merkez kaydirma da tamdir.
%
%   MATLAB uyumlu alt kumede yazildi; Octave 10.3.0 ile dogrulandi.

  if nargin < 3
    error('taylor_katsayilari:girdi', 'Uc girdi gerekli: ad, a, N.');
  end
  if N < 0 || N ~= floor(N)
    error('taylor_katsayilari:derece', 'N negatif olmayan tam sayi olmali.');
  end

  kats = zeros(1, N + 1);

  switch ad
    case 'exp'
      % f^(n)(a) = e^a  =>  c_n = e^a / n!
      ea = exp(a);
      for n = 0:N
        kats(n + 1) = ea / factorial(n);
      end
      R = Inf;
      tekillikler = [];

    case 'sin'
      % turev dongusu: sin, cos, -sin, -cos
      d = [sin(a), cos(a), -sin(a), -cos(a)];
      for n = 0:N
        kats(n + 1) = d(mod(n, 4) + 1) / factorial(n);
      end
      R = Inf;
      tekillikler = [];

    case 'cos'
      d = [cos(a), -sin(a), -cos(a), sin(a)];
      for n = 0:N
        kats(n + 1) = d(mod(n, 4) + 1) / factorial(n);
      end
      R = Inf;
      tekillikler = [];

    case '1/(1-x)'
      % 1/(1-z) = 1/((1-a) - (z-a))  =>  c_n = 1/(1-a)^(n+1)
      u = 1 - a;
      if u == 0
        error('taylor_katsayilari:tekillik', 'a = 1 tekillik noktasi.');
      end
      p = u;
      for n = 0:N
        kats(n + 1) = 1 / p;
        p = p * u;
      end
      tekillikler = 1;
      R = abs(1 - a);

    case '1/(1+x^2)'
      % 1/(1+z^2) = (1/2i)[1/(z-i) - 1/(z+i)]
      % 1/(z-i) = 1/((a-i)+(z-a)) = sum (-1)^n (z-a)^n / (a-i)^(n+1)
      ai = a - 1i;
      am = a + 1i;
      if ai == 0 || am == 0
        error('taylor_katsayilari:tekillik', 'a = +-i tekillik noktasi.');
      end
      p1 = ai;
      p2 = am;
      for n = 0:N
        c = (1 / p1 - 1 / p2) / (2i);
        if mod(n, 2) == 1
          c = -c;
        end
        kats(n + 1) = c;
        p1 = p1 * ai;
        p2 = p2 * am;
      end
      tekillikler = [1i, -1i];
      R = min(abs(a - 1i), abs(a + 1i));

    case 'ln(1+x)'
      % ln(1+z) = ln(1+a) + sum_{n>=1} (-1)^(n+1) (z-a)^n / (n (1+a)^n)
      u = 1 + a;
      if u == 0
        error('taylor_katsayilari:tekillik', 'a = -1 tekillik noktasi.');
      end
      kats(1) = log(u);
      p = u;
      for n = 1:N
        c = 1 / (n * p);
        if mod(n, 2) == 0
          c = -c;
        end
        kats(n + 1) = c;
        p = p * u;
      end
      tekillikler = -1;
      R = abs(1 + a);

    case 'sqrt(1+x)'
      % (1+z)^(1/2) etrafinda a: c_n = C(1/2,n) (1+a)^(1/2-n)
      u = 1 + a;
      if u == 0
        error('taylor_katsayilari:tekillik', 'a = -1 dallanma noktasi.');
      end
      kok = sqrt(u);
      binom = 1;
      p = 1;
      for n = 0:N
        kats(n + 1) = binom * kok / p;
        binom = binom * (0.5 - n) / (n + 1);
        p = p * u;
      end
      tekillikler = -1;
      R = abs(1 + a);

    otherwise
      error('taylor_katsayilari:ad', 'Bilinmeyen fonksiyon adi: %s', ad);
  end
end
