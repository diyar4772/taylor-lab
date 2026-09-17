// Taylor Laboratuvarı — web katmanının matematik çekirdeği testi
//
// Çalıştırmak için:
//     node 06-web/test_matematik.mjs
//
// Beklenen: "SONUC: 0 hata" ve çıkış kodu 0.
//
// Neden var: index.html'deki Taylor katsayıları elle türetilmiş KAPALI
// BİÇİMLERDİR (sayısal türev bilerek kullanılmadı, çünkü yüksek mertebede
// çöker). Elle türetme hata yapar. Burada o katsayılar bilinen değerlerle
// ve 02-python/src/ altındaki betiklerin ÜRETTİĞİ sayılarla karşılaştırılır.
//
// Test, index.html'in kendisini okur; yani sayfada bir şey değişirse test
// onu görür. Kopya bir çekirdek tutulmaz.

import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";

const burasi = dirname(fileURLToPath(import.meta.url));
const html = readFileSync(join(burasi, "index.html"), "utf8");

// --- sayfadan DOM'a dokunmayan matematik çekirdeğini çıkar
const js = html.split("<script>")[1].split("</script>")[0];

function kesit(bas, son) {
  const i = js.indexOf(bas);
  const j = js.indexOf(son);
  if (i < 0 || j < 0) {
    throw new Error(`index.html içinde beklenen işaret bulunamadı: ${i < 0 ? bas : son}`);
  }
  return js.slice(i, j);
}

// Ana çekirdek, 3. bölümün başlığını taşıyan yorum bloğunun HEMEN
// öncesinde biter; o yarım kalan "/*" atılmalı, yoksa kaynak bozulur.
let ana = kesit('"use strict";', "   3. Sekme anahtarı");
ana = ana.slice(0, ana.lastIndexOf("/*"));

const cekirdek =
  ana +
  "\n" +
  kesit("const G_YER", "let sDurum") +
  "\nexport { C, KATALOG, polinom, periyotOlc, periyotTam, T0, ivmeTam };\n";

const M = await import(
  "data:text/javascript," + encodeURIComponent(cekirdek)
);

// ---------------------------------------------------------------------
let hata = 0;
let toplam = 0;

function esit(ad, bulunan, beklenen, tolerans) {
  toplam++;
  const fark = Math.abs(bulunan - beklenen);
  const ok = fark <= tolerans;
  if (!ok) hata++;
  console.log(
    `${ok ? "OK  " : "HATA"}  ${ad.padEnd(44)} ${bulunan.toPrecision(10)}` +
      `  (beklenen ${beklenen.toPrecision(10)}, fark ${fark.toExponential(2)})`
  );
}

console.log("Taylor Laboratuvarı — web katmanı matematik testi");
console.log("==================================================");

console.log("\n1. Fonksiyon değerleri");
esit("exp(1)", M.KATALOG["exp(x)"].f([1, 0])[0], Math.E, 1e-12);
esit("sin(1)", M.KATALOG["sin(x)"].f([1, 0])[0], Math.sin(1), 1e-12);
esit("1/(1-0.5)", M.KATALOG["1/(1-x)"].f([0.5, 0])[0], 2, 1e-12);
esit("1/(1+2^2)", M.KATALOG["1/(1+x^2)"].f([2, 0])[0], 0.2, 1e-12);
esit("ln(1+1)", M.KATALOG["ln(1+x)"].f([1, 0])[0], Math.LN2, 1e-12);
esit("sqrt(1+3)", M.KATALOG["sqrt(1+x)"].f([3, 0])[0], 2, 1e-12);

console.log("\n2. Taylor katsayıları kapalı biçimden (a=0)");
const ks = M.KATALOG["sin(x)"].kats([0, 0], 7).map((c) => c[0]);
esit("sin a_1 = 1", ks[1], 1, 1e-15);
esit("sin a_3 = -1/6", ks[3], -1 / 6, 1e-15);
esit("sin a_5 = 1/120", ks[5], 1 / 120, 1e-15);
const kl = M.KATALOG["ln(1+x)"].kats([0, 0], 5).map((c) => c[0]);
esit("ln a_1 = 1", kl[1], 1, 1e-15);
esit("ln a_2 = -1/2", kl[2], -0.5, 1e-15);
esit("ln a_3 = 1/3", kl[3], 1 / 3, 1e-15);
const kq = M.KATALOG["sqrt(1+x)"].kats([0, 0], 3).map((c) => c[0]);
esit("sqrt a_1 = 1/2", kq[1], 0.5, 1e-15);
esit("sqrt a_2 = -1/8", kq[2], -0.125, 1e-15);
esit("sqrt a_3 = 1/16", kq[3], 1 / 16, 1e-15);

console.log("\n3. P_N diskin içinde f'e yakınsıyor mu (N=40)");
for (const ad of Object.keys(M.KATALOG)) {
  const F = M.KATALOG[ad];
  const a = [0.3, 0];
  const R = F.R(a);
  const x = [0.3 + (isFinite(R) ? 0.4 * R : 0.4), 0];
  const kats = F.kats(a, 40);
  esit(`${ad} hata`, Math.abs(F.f(x)[0] - M.polinom(kats, a, x)[0]), 0, 1e-9);
}

console.log("\n4. Merkez kaydırma: R = en yakın tekilliğe uzaklık");
esit("1/(1+x^2) a=0 -> 1", M.KATALOG["1/(1+x^2)"].R([0, 0]), 1, 1e-15);
esit("1/(1+x^2) a=1 -> sqrt2", M.KATALOG["1/(1+x^2)"].R([1, 0]), Math.SQRT2, 1e-15);
esit("1/(1+x^2) a=2 -> sqrt5", M.KATALOG["1/(1+x^2)"].R([2, 0]), Math.sqrt(5), 1e-15);
esit("1/(1-x) a=-1 -> 2", M.KATALOG["1/(1-x)"].R([-1, 0]), 2, 1e-15);

console.log("\n5. Kompleks merkez");
{
  const F = M.KATALOG["1/(1+x^2)"];
  const a = [0.4, 0.3];
  const z = [0.5, 0.1];
  const kats = F.kats(a, 45);
  esit("1/(1+z^2) kompleks a, N=45",
    M.C.mutlak(M.C.cikar(F.f(z), M.polinom(kats, a, z))), 0, 1e-9);
  esit("R = |a - i|", F.R(a), Math.hypot(0.4, 0.3 - 1), 1e-15);
}

console.log("\n6. Sarkaç — 02-python/src/sarkac.py çıktısıyla karşılaştırma");
esit("T0", M.T0, 2.006409, 1e-6);
for (const [d, bek] of [[10, 2.010236], [45, 2.086612], [90, 2.368246], [150, 3.535702]]) {
  esit(`T(${d} derece) eliptik`, M.periyotTam((d * Math.PI) / 180), bek, 5e-6);
}
esit("T(45) RK4 ölçümü ~ eliptik",
  M.periyotOlc((45 * Math.PI) / 180, M.ivmeTam),
  M.periyotTam((45 * Math.PI) / 180), 1e-5);

console.log(`\nSONUC: ${hata} hata / ${toplam} kontrol`);
process.exit(hata ? 1 : 0);
