extends Node2D
##
## Sahne 1 — Taylor keşfi
##
## Bir polinomun fonksiyonu nerede bıraktığını gösterir. Derece ve merkez
## kaydırıldıkça yakınsaklık aralığının nasıl değiştiği izlenir.
##
## Katsayılar SAYISAL TÜREVLE DEĞİL kapalı biçimden üretilir; yüksek
## mertebede sayısal türev çöker ve bu sahnenin konusu tam olarak yüksek
## mertebelerin davranışıdır.

const KATALOG := ["1/(1+x^2)", "1/(1-x)", "ln(1+x)", "sin", "exp"]

var fonksiyon_no: int = 0
var derece: int = 5
var merkez: float = 0.0

# çizim penceresi (matematik koordinatları)
const XMIN := -3.2
const XMAX := 3.2
const YMIN := -3.0
const YMAX := 3.0

const PANEL_GENISLIK := 280.0
const KENAR := 40.0

var _durum_etiketi: Label


## Çizim alanı pencere boyutundan hesaplanır; project.godot'taki görüntü
## alanı değişirse (ya da pencere yeniden boyutlandırılırsa) grafik onunla
## birlikte büyür. Sabit 1280x720 varsaymak kırılgandı.
func _cizim_alani() -> Rect2:
	var v := get_viewport_rect().size
	return Rect2(
		KENAR + 30.0,
		KENAR,
		maxf(v.x - PANEL_GENISLIK - 2.0 * KENAR - 60.0, 100.0),
		maxf(v.y - 2.0 * KENAR, 100.0))


func _ready() -> void:
	_arayuzu_kur()
	queue_redraw()


func _arayuzu_kur() -> void:
	var katman := CanvasLayer.new()
	add_child(katman)

	var panel := PanelContainer.new()
	panel.anchor_left = 1.0
	panel.anchor_right = 1.0
	panel.offset_left = -(PANEL_GENISLIK + KENAR)
	panel.offset_right = -KENAR
	panel.offset_top = KENAR
	katman.add_child(panel)

	var kutu := VBoxContainer.new()
	kutu.add_theme_constant_override("separation", 10)
	panel.add_child(kutu)

	var baslik := Label.new()
	baslik.text = "AYARLAR"
	kutu.add_child(baslik)

	# --- fonksiyon seçimi
	var secim := OptionButton.new()
	for ad in KATALOG:
		secim.add_item(ad)
	secim.selected = fonksiyon_no
	secim.item_selected.connect(_fonksiyon_secildi)
	kutu.add_child(secim)

	# --- derece
	var derece_etiket := Label.new()
	derece_etiket.text = "Derece N"
	kutu.add_child(derece_etiket)

	var derece_kaydirici := HSlider.new()
	derece_kaydirici.min_value = 0
	derece_kaydirici.max_value = 30
	derece_kaydirici.step = 1
	derece_kaydirici.value = derece
	derece_kaydirici.value_changed.connect(_derece_degisti)
	kutu.add_child(derece_kaydirici)

	# --- merkez
	var merkez_etiket := Label.new()
	merkez_etiket.text = "Merkez a"
	kutu.add_child(merkez_etiket)

	var merkez_kaydirici := HSlider.new()
	merkez_kaydirici.min_value = -2.0
	merkez_kaydirici.max_value = 2.0
	merkez_kaydirici.step = 0.05
	merkez_kaydirici.value = merkez
	merkez_kaydirici.value_changed.connect(_merkez_degisti)
	kutu.add_child(merkez_kaydirici)

	_durum_etiketi = Label.new()
	_durum_etiketi.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	_durum_etiketi.custom_minimum_size = Vector2(PANEL_GENISLIK - 20.0, 0)
	kutu.add_child(_durum_etiketi)

	_durumu_tazele()


func _fonksiyon_secildi(indeks: int) -> void:
	fonksiyon_no = indeks
	_durumu_tazele()
	queue_redraw()


func _derece_degisti(deger: float) -> void:
	derece = int(deger)
	_durumu_tazele()
	queue_redraw()


func _merkez_degisti(deger: float) -> void:
	merkez = deger
	_durumu_tazele()
	queue_redraw()


func _durumu_tazele() -> void:
	if _durum_etiketi == null:
		return
	var R := yaricap(merkez)
	var metin := "N = %d\na = %.2f\n" % [derece, merkez]
	if is_inf(R):
		metin += "R = ∞ (tekillik yok)"
	else:
		metin += "R = %.4f\nyakınsaklık: (%.2f, %.2f)" % [R, merkez - R, merkez + R]
	_durum_etiketi.text = metin


# =====================================================================
# Matematik
# =====================================================================

## f(x) — katalogdaki fonksiyonun değeri. Tanımsızsa NAN döner.
func f(x: float) -> float:
	match KATALOG[fonksiyon_no]:
		"1/(1+x^2)":
			return 1.0 / (1.0 + x * x)
		"1/(1-x)":
			if absf(x - 1.0) < 1e-9:
				return NAN
			return 1.0 / (1.0 - x)
		"ln(1+x)":
			if x <= -1.0:
				return NAN
			return log(1.0 + x)
		"sin":
			return sin(x)
		"exp":
			return exp(x)
	return NAN


## a merkezli Taylor katsayıları, kapalı biçimden.
func katsayilar(a: float, N: int) -> PackedFloat64Array:
	var c := PackedFloat64Array()
	c.resize(N + 1)
	match KATALOG[fonksiyon_no]:
		"1/(1+x^2)":
			# 1/(1+x^2) = (1/2i)[1/(z-i) - 1/(z+i)] açılımının reel hali:
			# c_n = -Im( (a-i)^(-(n+1)) ) biçiminde toplanır. Burada
			# kompleks aritmetiği elle yürütüyoruz: p = (a-i)^(n+1)
			var pr := a
			var pi := -1.0
			for n in range(N + 1):
				# 1/p'nin sanal kısmı
				var payda := pr * pr + pi * pi
				var im_ters := -pi / payda
				# Reel a icin (a+i) = conj(a-i) oldugundan
				#   c_n = (-1)^n * Im( 1/(a-i)^(n+1) )
				# cikar; im_ters tam olarak o sanal kisimdir.
				var deger := im_ters
				c[n] = deger if n % 2 == 0 else -deger
				# p *= (a - i)
				var yr := pr * a - pi * (-1.0)
				var yi := pr * (-1.0) + pi * a
				pr = yr
				pi = yi
		"1/(1-x)":
			var u := 1.0 - a
			var p := u
			for n in range(N + 1):
				c[n] = 1.0 / p
				p *= u
		"ln(1+x)":
			var u2 := 1.0 + a
			c[0] = log(u2)
			var p2 := u2
			for n in range(1, N + 1):
				var deger2 := 1.0 / (n * p2)
				c[n] = deger2 if n % 2 == 1 else -deger2
				p2 *= u2
		"sin":
			var dongu := [sin(a), cos(a), -sin(a), -cos(a)]
			var fakt := 1.0
			for n in range(N + 1):
				if n > 0:
					fakt *= n
				c[n] = dongu[n % 4] / fakt
		"exp":
			var ea := exp(a)
			var fakt2 := 1.0
			for n in range(N + 1):
				if n > 0:
					fakt2 *= n
				c[n] = ea / fakt2
	return c


## Yakınsaklık yarıçapı = merkezin en yakın tekilliğe uzaklığı.
func yaricap(a: float) -> float:
	match KATALOG[fonksiyon_no]:
		"1/(1+x^2)":
			return sqrt(a * a + 1.0)   # |a - i|
		"1/(1-x)":
			return absf(1.0 - a)
		"ln(1+x)":
			return absf(1.0 + a)
	return INF


## Horner ile P_N(x).
func polinom(c: PackedFloat64Array, a: float, x: float) -> float:
	var u := x - a
	var s := 0.0
	for n in range(c.size() - 1, -1, -1):
		s = s * u + c[n]
	return s


# =====================================================================
# Çizim
# =====================================================================

func _ekran(x: float, y: float) -> Vector2:
	var r := _cizim_alani()
	var px := r.position.x + (x - XMIN) / (XMAX - XMIN) * r.size.x
	var py := r.position.y + (YMAX - y) / (YMAX - YMIN) * r.size.y
	return Vector2(px, py)


func _draw() -> void:
	draw_rect(Rect2(Vector2.ZERO, get_viewport_rect().size), Color("0f1419"))
	_izgara_ciz()

	var a := merkez
	var c := katsayilar(a, derece)
	var R := yaricap(a)

	# yakınsaklık aralığı
	if not is_inf(R):
		var sol := _ekran(maxf(a - R, XMIN), YMAX)
		var sag := _ekran(minf(a + R, XMAX), YMIN)
		draw_rect(Rect2(sol, sag - sol), Color(0.30, 0.70, 0.91, 0.07))

	_egri_ciz(func(x): return f(x), Color("e8c84d"), 3.0)
	_egri_ciz(func(x): return polinom(c, a, x), Color("4db2e8"), 3.0)

	# merkez
	draw_circle(_ekran(a, 0.0), 6.0, Color.WHITE)


func _izgara_ciz() -> void:
	var izgara := Color("232e3b")
	for i in range(-3, 4):
		draw_line(_ekran(i, YMIN), _ekran(i, YMAX), izgara, 1.0)
		draw_line(_ekran(XMIN, i), _ekran(XMAX, i), izgara, 1.0)
	var eksen := Color("4a5a6e")
	draw_line(_ekran(XMIN, 0), _ekran(XMAX, 0), eksen, 2.0)
	draw_line(_ekran(0, YMIN), _ekran(0, YMAX), eksen, 2.0)


## Bir eğriyi parça parça çizer; tanımsız ya da ekran dışına taşan
## noktalarda kalemi kaldırır (aksi halde sahte dikey çizgiler oluşur).
func _egri_ciz(deger: Callable, renk: Color, kalinlik: float) -> void:
	const ADIM := 900
	var parca := PackedVector2Array()
	for i in range(ADIM + 1):
		var x: float = XMIN + (XMAX - XMIN) * i / float(ADIM)
		var y: float = deger.call(x)
		if is_nan(y) or is_inf(y) or absf(y) > 50.0:
			if parca.size() > 1:
				draw_polyline(parca, renk, kalinlik)
			parca = PackedVector2Array()
			continue
		parca.append(_ekran(x, clampf(y, YMIN - 1.0, YMAX + 1.0)))
	if parca.size() > 1:
		draw_polyline(parca, renk, kalinlik)
