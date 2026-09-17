% DEMO_CALISTIR  03-matlab-octave katmaninin tamamini calistirir.
%
%   Octave:  octave-cli --no-gui --quiet demo_calistir.m
%   MATLAB:  >> demo_calistir
%
% Bu betik uc sey gosterir:
%   1. Taylor polinomu diskin icinde yakinsar, disinda IRAKSAR
%   2. Lagrange siniri tutar -- ama float64 ihlal SANABILIR
%   3. Yakinsaklik diski veriden cikar, cizilmez
%
% Cikan sayilar 02-python/src/ altindaki betiklerin sonuclariyla
% karsilastirilir. Iki bagimsiz uygulamanin ayni sayida bulusmasi,
% sonuclarin tek bir uygulamanin hatasi olmadiginin gostergesidir.

fprintf('\n');
fprintf('=====================================================================\n');
fprintf(' TAYLOR LABORATUVARI -- MATLAB/Octave katmani\n');
fprintf('=====================================================================\n');

v = version();
fprintf('\nCalisma ortami: ');
if exist('OCTAVE_VERSION', 'builtin') ~= 0
  fprintf('GNU Octave %s\n', v);
else
  fprintf('MATLAB %s\n', v);
end

% ---------------------------------------------------------------------
fprintf('\n\n1. Diskin ICI ve DISI\n');
fprintf('---------------------------------------------------------------------\n');
fprintf('f = 1/(1+x^2), a = 0, R = 1. Ayni N ile iki noktada hata:\n\n');
fprintf('    %3s | %14s | %14s\n', 'N', 'x=0.5 (icerde)', 'x=1.5 (disarda)');
fprintf('    %3s-+-%14s-+-%14s\n', '---', '--------------', '---------------');
for N = [4 8 16 32 64]
  [Pi_, fi_] = taylor_yaklasim('1/(1+x^2)', 0, N, 0.5);
  [Pd_, fd_] = taylor_yaklasim('1/(1+x^2)', 0, N, 1.5);
  fprintf('    %3d | %14.3e | %14.3e\n', N, abs(fi_ - Pi_), abs(fd_ - Pd_));
end
fprintf('\n    Icerde N ile hata duser. Disarda N ile hata BUYUR.\n');
fprintf('    N''i artirmak iraksak bolgede ise yaramaz; zarar verir.\n');

% ---------------------------------------------------------------------
fprintf('\n\n2. Lagrange siniri ve float64''un durust payi\n');
fprintf('---------------------------------------------------------------------\n');
fprintf('|f - P_N| <= sup|f^(N+1)| |x-a|^(N+1) / (N+1)!\n\n');
fprintf('    %-10s %3s | %6s | %10s | %13s\n', ...
        'f', 'N', 'aday', 'yuvarlama', 'en kotu oran');
fprintf('    %-10s %3s-+-%6s-+-%10s-+-%13s\n', ...
        '----------', '---', '------', '----------', '-------------');

testler = { 'sin',       0, 5,  linspace(-2, 2, 401); ...
            'cos',       0, 7,  linspace(-2, 2, 401); ...
            'exp',       0, 8,  linspace(-2, 2, 401); ...
            'ln(1+x)',   0, 7,  linspace(-0.9, 0.9, 401); ...
            'sqrt(1+x)', 0, 5,  linspace(-0.9, 0.9, 401); ...
            '1/(1-x)',   0, 3,  linspace(-0.9, 0.9, 401) };

toplam_aday = 0;
for k = 1:size(testler, 1)
  r = kalan_sinir(testler{k, 1}, testler{k, 2}, testler{k, 3}, testler{k, 4});
  fprintf('    %-10s %3d | %6d | %10d | %13.4f\n', ...
          testler{k, 1}, testler{k, 3}, r.aday_sayisi, ...
          r.yuvarlama_sayisi, r.en_kotu_oran);
  toplam_aday = toplam_aday + r.aday_sayisi;
end

fprintf('\n    Toplam aday ihlal: %d\n', toplam_aday);
fprintf('\n    DIKKAT: "aday" teorem ihlali DEMEK DEGILDIR. Gercek hata\n');
fprintf('    sinirin cok altina indiginde float64 kendi olcum tabanina\n');
fprintf('    (~eps*|f|) takilir ve sinirdan buyuk GORUNUR. Hukum float64''e\n');
fprintf('    birakilamaz. Python katmani (kalan_dogrulama.py) 144096 nokta\n');
fprintf('    tarayip 2224 aday buldu, hepsini mpmath ile 60 basamakta\n');
fprintf('    yeniden olctu ve TEYIT EDILEN ihlal sayisini 0 buldu.\n');
fprintf('\n    Capraz kontrol: sin, a=0, N=5 icin en kotu oran yukarida\n');
fprintf('    0.2704 cikmali -- taylor.py''nin kendi testi de 0.2704 verir.\n');

% ---------------------------------------------------------------------
fprintf('\n\n3. Yakinsaklik diski VERIDEN cikiyor\n');
fprintf('---------------------------------------------------------------------\n');
fprintf('L_N(z) = (1/N) log10|f(z) - P_N(z)| -> log10(|z-a|/R)\n');
fprintf('Isaret degistirdigi yer = disk siniri. Teorik deger hic kullanilmadi.\n\n');
fprintf('    %-12s %5s | %8s | %8s | %7s | %8s\n', ...
        'f', 'a', 'teorik R', 'okunan R', 'sapma', 'python');
fprintf('    %-12s %5s-+-%8s-+-%8s-+-%7s-+-%8s\n', ...
        '------------', '-----', '--------', '--------', '-------', '--------');

% son sutun: 02-python/src/kompleks_harita.py'nin urettigi degerler
% (out/tablolar/kompleks_yaricap.md)
diskler = { '1/(1+x^2)',  0, 0.9366; ...
            '1/(1-x)',    0, 0.9219; ...
            'ln(1+x)',    0, 0.9953; ...
            '1/(1+x^2)',  1, 1.3321; ...
            '1/(1-x)',   -1, 1.8681 };

for k = 1:size(diskler, 1)
  ad = diskler{k, 1};
  a  = diskler{k, 2};
  [Ro, Rt] = yakinsaklik_diski(ad, a, 28);
  fprintf('    %-12s %5g | %8.4f | %8.4f | %+6.1f%% | %8.4f\n', ...
          ad, a, Rt, Ro, (Ro / Rt - 1) * 100, diskler{k, 3});
end

fprintf('\n    Son iki sutun iki BAGIMSIZ uygulamanin ayni olcumu.\n');
fprintf('    Aradaki kucuk fark izgara cozunurlugundendir.\n');
fprintf('\n    Sapmanin hep NEGATIF olmasi bir hata degil: (1/N)log|hata| ->\n');
fprintf('    log(|z-a|/R) yakinsamasi ancak N->Inf''ta tamdir.\n');

% ---------------------------------------------------------------------
fprintf('\n\n4. Merkez kaydirmak: yaricap fonksiyonun degil,\n');
fprintf('   (fonksiyon, merkez) CIFTININ ozelligidir\n');
fprintf('---------------------------------------------------------------------\n');
fprintf('f = 1/(1+x^2), tekillikler z = +-i (yerinde duruyor)\n\n');
fprintf('    %6s | %10s | %s\n', 'a', 'R', 'aciklama');
fprintf('    %6s-+-%10s-+-%s\n', '------', '----------', '--------------------');
for a = [0 1 2]
  [~, R] = taylor_katsayilari('1/(1+x^2)', a, 1);
  fprintf('    %6g | %10.4f | |a - i| = sqrt(%g)\n', a, R, a^2 + 1);
end
fprintf('\n    Fonksiyon ayni, merkez farkli, yaricap farkli.\n');
fprintf('    "Bu fonksiyonun yaricapi kactir?" merkez soylenmeden\n');
fprintf('    EKSIK bir sorudur.\n');

fprintf('\n=====================================================================\n');
fprintf(' Bitti.\n');
fprintf('=====================================================================\n\n');
