extends SceneTree
##
## Sahnelerin matematiğini denetler — oyunu açmadan.
##
## Çalıştırmak için:
##     godot --headless --path 05-godot --script res://test_dogrulama.gd
##
## Beklenen çıktı: "SONUC: 0 hata" ve çıkış kodu 0.
##
## Neden var: GDScript'teki katsayılar elle türetilmiş kapalı biçimlerdir.
## Elle türetme hata yapar (bu dosya yazılırken 1/(1+x^2) katsayısında
## gerçekten bir işaret hatası yakalandı). Sayılar burada bağımsız olarak
## bilinen değerlerle karşılaştırılır.

var hata_sayisi := 0


func _initialize() -> void:
	print("Taylor Laboratuvarı — Godot katmanı doğrulaması")
	print("=================================================")

	var kesif := Node2D.new()
	kesif.set_script(load("res://taylor_explorer.gd"))
	var denge := Node2D.new()
	denge.set_script(load("res://denge_oyunu.gd"))

	_katsayi_testleri(kesif)
	_yakinsama_testleri(kesif)
	_yaricap_testleri(kesif)
	_denge_testleri(denge)

	# Sahne agacina eklenmedikleri icin elle serbest birakiliyorlar;
	# aksi halde Godot cikista "ObjectDB instances were leaked" der.
	kesif.free()
	denge.free()

	print("")
	print("SONUC: %d hata" % hata_sayisi)
	quit(1 if hata_sayisi > 0 else 0)


func _esit(ad: String, bulunan: float, beklenen: float, tolerans: float) -> void:
	var fark := absf(bulunan - beklenen)
	var gecti := fark <= tolerans
	if not gecti:
		hata_sayisi += 1
	print("%s  %-44s %+.10f (beklenen %+.10f)" % [
		"OK  " if gecti else "HATA", ad, bulunan, beklenen])


func _katsayi_testleri(k: Node2D) -> void:
	print("\n1. Taylor katsayıları (a=0)")

	# 1/(1+x^2) -> 1 - x^2 + x^4 - x^6 + ...
	k.fonksiyon_no = 0
	var c = k.katsayilar(0.0, 6)
	_esit("1/(1+x^2) c_0", c[0], 1.0, 1e-12)
	_esit("1/(1+x^2) c_1", c[1], 0.0, 1e-12)
	_esit("1/(1+x^2) c_2", c[2], -1.0, 1e-12)
	_esit("1/(1+x^2) c_4", c[4], 1.0, 1e-12)
	_esit("1/(1+x^2) c_6", c[6], -1.0, 1e-12)

	# 1/(1-x) -> hepsi 1
	k.fonksiyon_no = 1
	var c2 = k.katsayilar(0.0, 4)
	_esit("1/(1-x) c_0", c2[0], 1.0, 1e-12)
	_esit("1/(1-x) c_3", c2[3], 1.0, 1e-12)

	# ln(1+x) -> x - x^2/2 + x^3/3
	k.fonksiyon_no = 2
	var c3 = k.katsayilar(0.0, 3)
	_esit("ln(1+x) c_0", c3[0], 0.0, 1e-12)
	_esit("ln(1+x) c_1", c3[1], 1.0, 1e-12)
	_esit("ln(1+x) c_2", c3[2], -0.5, 1e-12)
	_esit("ln(1+x) c_3", c3[3], 1.0 / 3.0, 1e-12)

	# sin -> x - x^3/6 + x^5/120
	k.fonksiyon_no = 3
	var c4 = k.katsayilar(0.0, 5)
	_esit("sin c_1", c4[1], 1.0, 1e-12)
	_esit("sin c_3", c4[3], -1.0 / 6.0, 1e-12)
	_esit("sin c_5", c4[5], 1.0 / 120.0, 1e-12)

	# exp -> 1/n!
	k.fonksiyon_no = 4
	var c5 = k.katsayilar(0.0, 5)
	_esit("exp c_0", c5[0], 1.0, 1e-12)
	_esit("exp c_5", c5[5], 1.0 / 120.0, 1e-12)


func _yakinsama_testleri(k: Node2D) -> void:
	print("\n2. P_N gerçekten f'e yakınsıyor mu (diskin içinde)")
	# merkez kaydırılmış hâl de sınanır: kapalı biçim yanlışsa burada patlar
	for no in range(5):
		k.fonksiyon_no = no
		var a := 0.3
		var R: float = k.yaricap(a)
		var x: float = a + (0.4 * R if is_finite(R) else 0.4)
		var c = k.katsayilar(a, 40)
		var fark: float = absf(k.f(x) - k.polinom(c, a, x))
		_esit("%s  a=0.3 N=40" % k.KATALOG[no], fark, 0.0, 1e-9)


func _yaricap_testleri(k: Node2D) -> void:
	print("\n3. Yarıçap = en yakın tekilliğe uzaklık")
	k.fonksiyon_no = 0
	_esit("1/(1+x^2) a=0 -> 1", k.yaricap(0.0), 1.0, 1e-12)
	_esit("1/(1+x^2) a=1 -> sqrt(2)", k.yaricap(1.0), sqrt(2.0), 1e-12)
	_esit("1/(1+x^2) a=2 -> sqrt(5)", k.yaricap(2.0), sqrt(5.0), 1e-12)
	k.fonksiyon_no = 1
	_esit("1/(1-x) a=-1 -> 2", k.yaricap(-1.0), 2.0, 1e-12)


func _denge_testleri(denge: Node2D) -> void:
	print("\n4. Sarkaç: tam periyot ile harmonik periyot")
	# 02-python/src/sarkac.py çıktısı (L=1 m, g=9.80665 m/s^2)
	_esit("T0", denge.T0, 2.006409, 1e-6)
	_esit("T(10 derece)", denge.tam_periyot(deg_to_rad(10.0)), 2.010236, 5e-6)
	_esit("T(45 derece)", denge.tam_periyot(deg_to_rad(45.0)), 2.086612, 5e-6)
	_esit("T(90 derece)", denge.tam_periyot(deg_to_rad(90.0)), 2.368246, 5e-6)
	_esit("T(150 derece)", denge.tam_periyot(deg_to_rad(150.0)), 3.535702, 5e-6)
	print("      (beklenen değerler 02-python/src/sarkac.py çıktısıdır)")
