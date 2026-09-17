extends Node2D
##
## Sahne 2 — Denge oyunu
##
## Soru: "küçük açı yaklaşımı" ne zaman bozulur?
##
## Solda TAM denklem  θ̈ = −(g/L)·sin θ
## Sağda HARMONİK yaklaşım  θ̈ = −(g/L)·θ
## İkisi aynı anda, aynı genlikle başlar.
##
## Oyun şu: genliği seç ve iki sarkacın kaç saniye "birlikte" kaldığını
## izle. Dayanma süresi = |Δθ| ilk kez 10°'yi aştığı an. Genlik küçüldükçe
## süre hızla uzar; 5° ve altında |Δθ| ≤ 2θ₀ ≤ 10° olduğu için eşik hiç
## aşılmaz. 150°'de ise süre saniyenin altına iner. Atılan −θ³/6 teriminin
## faturası budur.

const G := 9.80665
const L := 1.0
const ESIK_DERECE := 10.0

var T0: float = TAU * sqrt(L / G)

var genlik_derece: float = 45.0
var tam := Vector2.ZERO        # (θ, ω) tam denklem
var harmonik := Vector2.ZERO   # (θ, ω) harmonik yaklaşım
var gecen: float = 0.0
var dayanma: float = -1.0      # -1 = henüz aşılmadı
var oynuyor := true

var _bilgi: Label
var _skor: Label


func _ready() -> void:
	_arayuzu_kur()
	_sifirla()


func _arayuzu_kur() -> void:
	var katman := CanvasLayer.new()
	add_child(katman)

	var panel := PanelContainer.new()
	panel.position = Vector2(20, 20)
	panel.custom_minimum_size = Vector2(300, 0)
	katman.add_child(panel)

	var kutu := VBoxContainer.new()
	kutu.add_theme_constant_override("separation", 10)
	panel.add_child(kutu)

	var baslik := Label.new()
	baslik.text = "DENGE OYUNU"
	kutu.add_child(baslik)

	var aciklama := Label.new()
	aciklama.text = "Genliği seç. İki sarkaç kaç saniye birlikte kalıyor?"
	aciklama.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	aciklama.custom_minimum_size = Vector2(280, 0)
	kutu.add_child(aciklama)

	var kaydirici := HSlider.new()
	kaydirici.min_value = 2.0
	kaydirici.max_value = 170.0
	kaydirici.step = 1.0
	kaydirici.value = genlik_derece
	kaydirici.value_changed.connect(_genlik_degisti)
	kutu.add_child(kaydirici)

	_bilgi = Label.new()
	_bilgi.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	_bilgi.custom_minimum_size = Vector2(280, 0)
	kutu.add_child(_bilgi)

	_skor = Label.new()
	_skor.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	_skor.custom_minimum_size = Vector2(280, 0)
	kutu.add_child(_skor)

	var dugme := Button.new()
	dugme.text = "Yeniden başlat"
	dugme.pressed.connect(_sifirla)
	kutu.add_child(dugme)


func _genlik_degisti(deger: float) -> void:
	genlik_derece = deger
	_sifirla()


func _sifirla() -> void:
	var t0 := deg_to_rad(genlik_derece)
	tam = Vector2(t0, 0.0)
	harmonik = Vector2(t0, 0.0)
	gecen = 0.0
	dayanma = -1.0
	oynuyor = true
	_bilgiyi_tazele()
	queue_redraw()


func _bilgiyi_tazele() -> void:
	if _bilgi == null:
		return
	var t0 := deg_to_rad(genlik_derece)
	var T := tam_periyot(t0)
	_bilgi.text = "genlik: %.0f°\nT0 (harmonik): %.6f s\nT (tam): %.6f s\nsapma: %.2f %%" % [
		genlik_derece, T0, T, (T / T0 - 1.0) * 100.0]


func _process(delta: float) -> void:
	if not oynuyor:
		return
	# sabit adımla entegre et; kare süresi değişse de fizik aynı kalsın
	var h := 0.002
	var adet := int(clampf(delta, 0.0, 0.05) / h)
	for i in range(adet):
		tam = _rk4(tam, h, true)
		harmonik = _rk4(harmonik, h, false)
		gecen += h
		if dayanma < 0.0 and absf(tam.x - harmonik.x) > deg_to_rad(ESIK_DERECE):
			dayanma = gecen
			_skor.text = "Dayanma süresi: %.2f s\n(|Δθ| ilk kez %.0f°'yi aştı)" % [
				dayanma, ESIK_DERECE]
	queue_redraw()


## RK4, y = (θ, ω). tam_mi=false ise sin θ yerine θ kullanılır.
func _rk4(y: Vector2, h: float, tam_mi: bool) -> Vector2:
	var k1 := _turev(y, tam_mi)
	var k2 := _turev(y + k1 * (h / 2.0), tam_mi)
	var k3 := _turev(y + k2 * (h / 2.0), tam_mi)
	var k4 := _turev(y + k3 * h, tam_mi)
	return y + (k1 + k2 * 2.0 + k3 * 2.0 + k4) * (h / 6.0)


func _turev(y: Vector2, tam_mi: bool) -> Vector2:
	var ivme := -(G / L) * (sin(y.x) if tam_mi else y.x)
	return Vector2(y.y, ivme)


# =====================================================================
# Tam periyot — eliptik integral, AGM ile
# =====================================================================

## K(m), birinci tür tam eliptik integral (aritmetik-geometrik ortalama).
func ellipK(m: float) -> float:
	var a := 1.0
	var b := sqrt(1.0 - m)
	for i in range(60):
		var ya := (a + b) / 2.0
		var yb := sqrt(a * b)
		a = ya
		b = yb
	return PI / (2.0 * a)


## Tam sarkaç periyodu: T = 4 sqrt(L/g) K(sin^2(θ0/2)).
func tam_periyot(theta0: float) -> float:
	return 4.0 * sqrt(L / G) * ellipK(pow(sin(theta0 / 2.0), 2.0))


# =====================================================================
# Çizim
# =====================================================================

## Yerleşim pencere boyutundan hesaplanır. Sabit 1280x720 varsaymak
## kırılgandı: project.godot'taki görüntü alanı büyüdüğünde sahne
## sol üst köşeye sıkışıyordu.
func _draw() -> void:
	var v := get_viewport_rect().size
	draw_rect(Rect2(Vector2.ZERO, v), Color("0f1419"))

	# sol panel 340 px; kalan genişlik ikiye bölünür
	var sol := 340.0
	var genislik := v.x - sol
	var uzunluk := minf(genislik * 0.20, v.y * 0.42)
	var tepe := v.y * 0.18

	_sarkac_ciz(Vector2(sol + genislik * 0.27, tepe), tam, uzunluk, Color("e8c84d"))
	_sarkac_ciz(Vector2(sol + genislik * 0.73, tepe), harmonik, uzunluk, Color("4db2e8"))

	# faz farkı çubuğu
	var fark := absf(tam.x - harmonik.x)
	var oran := clampf(fark / deg_to_rad(ESIK_DERECE), 0.0, 1.0)
	var yer := Vector2(sol + genislik * 0.15, v.y - 60.0)
	var tam_en := genislik * 0.70
	draw_rect(Rect2(yer, Vector2(tam_en, 18)), Color("232e3b"))
	draw_rect(Rect2(yer, Vector2(tam_en * oran, 18)),
		Color("e8567a") if oran >= 1.0 else Color("6ece8a"))


func _sarkac_ciz(merkez: Vector2, durum: Vector2, uzunluk: float, renk: Color) -> void:
	var uc := merkez + Vector2(sin(durum.x), cos(durum.x)) * uzunluk
	# başlangıç genliğini gösteren yay referansı
	draw_line(merkez - Vector2(50, 0), merkez + Vector2(50, 0), Color("39465a"), 3.0)
	draw_line(merkez, uc, renk, 4.0)
	draw_circle(uc, maxf(uzunluk * 0.08, 10.0), renk)
