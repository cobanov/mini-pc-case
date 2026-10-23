# Mini PC kasası v4 — PSU yan yatık, CPU soğutucusunun karşısında; gövde Z=80'den iki parça.
# FreeCAD'de çalıştır: exec(open(".../build_case.py").read()); STL için export_stl().
# Koordinatlar (mm, iç hacim): X sol iç yüz=0 → anakart tablası (sağ) W,
# Y ön iç yüz=0 → arka iç yüz D, Z taban üstü=0 → yukarı.
# Ölçü kaynakları: NOTES.md (ATX 2.2, ATX12V PSDG 2.2, ASUS PRIME H310M-K kılavuzu).
# Vida ve montaj listesi: MONTAJ.md
import math
import FreeCAD as App
import Part
from FreeCAD import Vector as V

T = 2.2            # duvar kalınlığı (1 kg PETG hedefi; 3 çevre × 0.42 = 1.26 + dolgu)
T_LID = 3.0        # üst kapak (yan kapak dili için 2 mm oluk taşır; 2.5'te oluk dış kenarı ayırıyor)
W, D = 172.0, 200.0
H = 258.0          # iç yükseklik (üst kapağın alt yüzü); PSU üstü 230 + 25 mm egzoz fanı + 3 mm pay
EDGE = 1.5         # alt/üst dış kenar pahı (45°, desteksiz basılır)
CORNER_R = 5.0     # dikey dış köşe yuvarlatması (dik baskıda sorunsuz)
FIT = 0.4          # birbirine geçen parçalarda boşluk (0.3 + PETG için 0.1)
TOL = 0.3          # baskıda küçülen deliklere pay
MAX_BRIDGE = 18.0  # desteksiz köprü sınırı; daha geniş açıklıklara kırılabilir destek konur

# Bağlantı elemanları — hepsi M3, tek tip insert
INSERT_D, INSERT_L = 4.0, 6.0   # M3 x 5 x 4.5 pirinç heat-set insert yuvası
M3 = 3.4                        # M3 geçiş deliği
UNC632 = 3.8                    # PSU vidası (6-32 UNC) geçiş deliği

STANDOFF = 6.35
X_BB = W - STANDOFF          # anakart arka yüzü
X_BF = X_BB - 1.6            # anakart ön (bileşen) yüzü
Y_R = D - 2.1                # anakart arka kenarı (ATX: panel 0.483", kenar 0.400")
Z_B = 12.0                   # anakart alt kenarı (SATA kablo payı)
Z_TOP = Z_B + 226.0          # anakart üst kenarı
# Delikler: (arka kenardan, üst kenardan) — F, J, C, H, B, R
HOLES = [(33.02, 6.35), (165.1, 6.35), (10.16, 163.83),
         (165.1, 163.83), (10.16, 209.55), (165.1, 209.55)]
Z_C = Z_TOP - 163.83         # PCIEX16 merkez hattı (C/H deliği hizası)
COOLER_H = 61.0              # anakart yüzeyinden soğutucu üstü (53 mm + soket/CPU)
CPU_Y, CPU_Z = Y_R - 98.2, Z_TOP - 85.8

GPU_TAB_H = 112.5            # anakart yüzeyi → braket kulağının alt yüzü (deneme parçasıyla doğrula)
X_TAB = X_BF - GPU_TAB_H
GPU_SLOT_OFF = (12.4, 32.72) # kart PCB'sinden braket vida çentiklerine (fotoğraftan)

# PSU yan yatık: 86 kalınlık X'te (fan yüzü sol kapağa bakar), 150 Z'de, 140 Y'de
PSU_X0, PSU_Z0 = 8.0, 80.0   # alt gövdenin üstüne (ek düzlemi) oturur
PSU_Y0 = D - 140.0
# ATX12V PSDG Fig.9 arka yüz delikleri (arkadan bakınca sol-alt köşeden x, y);
# yan yatık: kasa X = PSU_X0 + y, kasa Z = PSU_Z0 + 150 - x (priz altta, kullanıcının PSU'suna göre)
PSU_HOLES = [(6, 16), (6, 80), (144, 80), (120, 6)]

# dikey direkler (x0, x1, y0, y1, z0, z1); arka-sol direk PSU'nun altında biter
POSTS = [(0, 12, 0, 12, 0, H), (W - 9, W, 0, 10, 0, H), (0, 7.5, D - 10, D, 0, H)]   # ön direkler kapak vidası için geniş
Z_JOINT = 80.0               # gövde eki: GPU açıklığı (≤78.2) altta, I/O (≥81.4) ve PSU üstte
SPLIT = Z_JOINT              # yan kapakların bindirme ekleminin ortası (±6 mm), gövde ekiyle aynı
JOINT_SCREWS = [("on", 34), ("on", 110), ("arka", 14), ("arka", 108)]  # (duvar, x); ön vidalar Steam plakasının arkasında (plaka çıkınca erişilir)
JOINT_FRONT_Z = 95.0   # ön ek vidası: plaka açıklığının (z ≥ 110) altındaki duvar bandında, mıknatıs bloklarının (x 14–24, 148–158) dışında
PEGS = [(2.5, 7.5, 2.5, 7.5), (1.5, 6, D - 7.5, D - 2.5)]   # sol direklerde hizalama pimleri
LOWER_SCREWS = [(5, 15), (5, 45), (D - 5, 15), (D - 5, 45)]
UPPER_SCREWS = [(5, 120), (5, 220), (D - 5, 120), (D - 5, 220)]
LID_SCREWS = [(4.5, 4.5), (W - 4, 4.5), (105, D - 4)]   # üst panel plakasının (x 8–164) dışında, köşe R5 içinde
# 2.5" SSD alt yan kapağın iç yüzüne yatık (x 1.5–8.5, GPU'nun önündeki şerit); SFF-8201 alt yüz delikleri:
# konnektör ucundan 14 ve 90.6 mm, genişlikte merkezden ±30.86. Kapaktan 4 havşa M3, 1.5 mm aralayıcı.
SSD_Y0, SSD_Z0 = 45.0, 5.0
SSD_HOLES = [(SSD_Y0 + dy, SSD_Z0 + 34.925 + dz) for dy in (14, 90.6) for dz in (-30.86, 30.86)]
FEET = [(12, 12), (W - 9, 12), (12, D - 12), (W - 9, D - 12)]
FOOT_D, FOOT_H = 22.0, 12.0   # basılan ayaklar: tabanın altından hava için 12 mm boşluk
# Ön alt panel: değiştirilebilir plaka (düz / petek / ekran / kendi tasarımın). Açıklık (x0, x1, z0, z1),
# plaka T kalınlığında, 4 M3 havşa vida içerideki bosslara; arkasında SSD (z ≤ 9) ve GPU (y ≥ 8) var.
# Değiştirilebilir paneller: dış plaka 1.25 mm gömmeye oturur (dışla hizalı), iç kademe açıklığa girer,
# 4 M3 havşa vida köşelerdeki bosslara. plate = plakanın dış sınırı, open = duvardaki açıklık (u0,u1,v0,v1).
# Ön alt 156 x 72, ön üst 156 x 156 (kare), üst (kapak önü) 156 x 30: tuşlar, USB-C vb. için.
PANELS = {
    "on_alt": dict(plate=(8, 164, 2, 74), open=(22, 150, 12, 64), screws=[(14, 7), (158, 7), (14, 69), (158, 69)]),
    # Ön üst: Steam Machine ön plakasıyla birebir uyumlu (Valve'ın resmi STEP'i: 156 x 126.1 x 6.5 mm, 4 adet
    # K&J SB443-OUT 6.35 x 6.35 x 4.76 blok mıknatıs, plaka merkezinden (±67, ±52.5), plaka arkasından 4 mm
    # çıkar). Plaka gömmesiz, ön duvarın dış yüzüne oturur; kasada mıknatıs cepleri aynı yerde.
    "on_ust": dict(plate=(8, 164, 88, 214.1), open=(30, 142, 110, 192), screws=[],   # açıklık mıknatıs ceplerinden 6 mm uzak
                   magnets=[(19, 98.55), (153, 98.55), (19, 203.55), (153, 203.55)]),
    # Steam plakasının üstündeki kontrol şeridi: ortada güç, solda reset + USB-C, sağda 2 × USB-A
    "on_serit": dict(plate=(8, 164, 218, 250), open=(22, 150, 225, 243),
                     screws=[(14, 221.5), (158, 221.5), (14, 246.5), (158, 246.5)]),
}
PANEL_R = 3.0                # sökülebilir panellerin dış köşe yuvarlatması
MAGNET = (6.35, 4.76)        # SB443-OUT blok mıknatıs: kenar, kalınlık
# Güç ve reset: Cherry MX tipi anahtar + keycap, üst paneldeki (u, v); keycap 18 mm, aralık 19.05
SWITCHES = [(86.0, 234.0), (40.0, 234.0)]   # (x, z) şeritte: güç ortada, reset solda
USB_C = (60.0, 234.0)                       # panel tipi USB-C uzatma: 9.6 x 3.9 açıklık
USB_A = [(112.0, 234.0), (134.0, 234.0)]    # panel tipi USB-A uzatma: 13.6 x 6.4 açıklık
# 120 × 25 mm Molex fanlar: üst kapakta egzoz (PSU'nun üstünde), önde giriş; vida aralığı 105
FAN_D, FAN_PITCH, FAN_HOLE, FAN_T = 118.0, 105.0, 4.5, 25.0
FAN_TOP = (102.0, 100.0)     # (x, y) — anakart ön yüzüne (x = 164) 2 mm kala
FAN_FRONT = (86.0, 164.0)    # (x, z) — isteğe bağlı 3. fan: ön üst panelin 'fan' çeşidinde
FAN_BOTTOM = (96.0, 104.0)   # (x, y) — GPU fanının altında; SATA portlarına (x ≥ 157) 1 mm kala

# Baskı yönleri: gövde dik, üst kapak ters (düz yüzü tablada), alt yan kapak dış yüzü
# tablada, üst yan kapak iç yüzü tablada (dil ve bindirme tablaya oturur).
PRINT_ORIENT = {"govde_alt": None, "govde_ust": None, "ust_kapak": (V(1, 0, 0), 180), "ayak": (V(1, 0, 0), 180),
                "on_serit": (V(1, 0, 0), 90), "on_serit_duz": (V(1, 0, 0), 90),
                "yan_alt": (V(0, 1, 0), -90), "yan_ust": (V(0, 1, 0), 90)}
# I/O açıklığı 158.75 x 44.45 (+pay); alt kenarı anakart alt yüzünün 2.24 mm altında
IO_X1 = X_BB + 2.24
IO = (IO_X1 - 44.45 - TOL, IO_X1 + TOL, Z_TOP - 156.31 - TOL, Z_TOP + 2.44 + TOL)

def box(x0, x1, y0, y1, z0, z1):
    return Part.makeBox(x1 - x0, y1 - y0, z1 - z0, V(x0, y0, z0))

def cyl(r, h, base, d):
    return Part.makeCylinder(r, h, V(*base), V(*d))

def chamfered_box(x0, x1, y0, y1, z0, z1, c, top=False, bottom=False, r=None):
    # dikey kenarlar CORNER_R ile yuvarlatılır, üst/alt kenarlar isteğe göre c ile pahlanır
    b = box(x0, x1, y0, y1, z0, z1)
    vert = [e for e in b.Edges if abs(e.Vertexes[0].Point.z - e.Vertexes[1].Point.z) > 1e-6]
    b = b.makeFillet(CORNER_R if r is None else r, vert)
    edges = [e for e in b.Edges
             if (top and abs(e.BoundBox.ZMin - z1) < 1e-6 and abs(e.BoundBox.ZMax - z1) < 1e-6)
             or (bottom and abs(e.BoundBox.ZMin - z0) < 1e-6 and abs(e.BoundBox.ZMax - z0) < 1e-6)]
    return b.makeChamfer(c, edges) if edges else b

def outer_envelope():
    # dış zarf: yan kapaklar ve paneller bununla kesişerek köşe yuvarlatmasını alır
    return chamfered_box(-T, W + T, -T, D + T, -T - 1, H + T_LID + 1, EDGE)

def teardrop_x(y, z, r, x0, x1):
    # X ekseninde boss; alt tarafı 45° — dik duvarda desteksiz basılır
    c = cyl(r, x1 - x0, (x0, y, z), (1, 0, 0))
    s = Part.makeBox(x1 - x0, r, r, V(x0, y, z))
    s.rotate(V(x0, y, z), V(1, 0, 0), 225)
    return c.fuse(s)

def hex_centers(u0, u1, v0, v1, r, web=2.2, inside=None):
    du = r * math.sqrt(3) + web
    dv = du * math.sqrt(3) / 2
    out, row, v = [], 0, v0 + r
    while v <= v1 - r:
        u = u0 + r * math.sqrt(3) / 2 + (du / 2 if row % 2 else 0)
        while u <= u1 - r * math.sqrt(3) / 2:
            if inside is None or inside(u, v):
                out.append((u, v))
            u += du
        v += dv
        row += 1
    return out

def hex_cutters(centers, r, to3d, ext):
    # sivri ucu +v yönünde: dik duvarda köprüsüz basılır
    out = []
    for u, v in centers:
        pts = [to3d(u + r * math.cos(math.radians(30 + 60 * i)),
                    v + r * math.sin(math.radians(30 + 60 * i))) for i in range(7)]
        out.append(Part.Face(Part.makePolygon(pts)).extrude(ext))
    return out

def cut_all(shape, tools):
    return shape.cut(Part.makeCompound(tools)) if tools else shape

def countersink(x, y, z, d, depth=T):
    # M3 havşa başlı (DIN 7991, baş Ø6) için delik + 90° havşa; (x, y, z) yüzey, d içeri yön
    hole = cyl(M3 / 2, depth + 2, (x - d[0], y - d[1], z - d[2]), d)
    cone = Part.makeCone(3.3, 1.7, 1.6, V(x, y, z) - V(*d) * 0.01, V(*d))
    return [hole, cone]

def breakaway_ribs(x0, x1, y0, y1, z0, z1, t=0.8, gap=0.2):
    # dik duvardaki geniş açıklığın üst kenarı köprü olmasın diye ince dikey kaburgalar;
    # üstte 0.2 mm boşluk (destek arayüzü gibi), baskıdan sonra pense ile kırılır
    n = math.ceil((x1 - x0) / MAX_BRIDGE) - 1
    step = (x1 - x0) / (n + 1)
    return [box(x0 + step * i - t / 2, x0 + step * i + t / 2, y0, y1, z0, z1 - gap)
            for i in range(1, n + 1)]

def fan_cut(cu, cv, to3d, ext):
    # fan ızgarası (petek, daire içinde) + 4 vida deliği; to3d(u, v) yüzeydeki noktayı verir
    out = hex_cutters(hex_centers(cu - FAN_D / 2, cu + FAN_D / 2, cv - FAN_D / 2, cv + FAN_D / 2, 4.5,
                                  inside=lambda u, v: math.hypot(u - cu, v - cv) < FAN_D / 2 - 2 and
                                  all(math.hypot(u - cu - a * FAN_PITCH / 2, v - cv - b * FAN_PITCH / 2) > 7.5
                                      for a in (-1, 1) for b in (-1, 1))), 4.5, to3d, ext)
    for du, dv in ((-1, -1), (1, -1), (-1, 1), (1, 1)):
        u, v = cu + du * FAN_PITCH / 2, cv + dv * FAN_PITCH / 2
        out.append(Part.makeCylinder(FAN_HOLE / 2, ext.Length, to3d(u, v), ext))
    return out

def insert(x, y, z, d):
    # insert yuvası; (x, y, z) yüzeyde, d içeri yön
    return cyl((INSERT_D + TOL) / 2, INSERT_L, (x - d[0] * 0.1, y - d[1] * 0.1, z - d[2] * 0.1), d)

# ---------------------------------------------------------------- gövde
def body():
    # dış kabuk (pahlı) − iç hacim − sol kapak yuvası (kapaklar ön/arka duvar ve taban arasına oturur)
    s = chamfered_box(-T, W + T, -T, D + T, -T, H, EDGE, bottom=True)
    s = s.cut(box(0, W, 0, D, 0, H + 1))
    s = s.cut(box(-T - 1, 0, 0, D, 0, H + 1))
    for p in POSTS:
        s = s.fuse(box(*p))
    for dy, dz in HOLES:                                       # standoff bossları
        s = s.fuse(teardrop_x(Y_R - dy, Z_TOP - dz, 4.5, X_BB, W))
    # GPU braket kulağı rafı (arka duvarın dışında, altı 45°)
    prof = [V(0, D + T, Z_C - 54), V(0, D + T + 10, Z_C - 44), V(0, D + T + 10, Z_C + 4),
            V(0, D + T, Z_C + 4), V(0, D + T, Z_C - 54)]
    shelf = Part.Face(Part.makePolygon(prof)).extrude(V(10, 0, 0))
    shelf.translate(V(X_TAB, 0, 0))
    s = s.fuse(shelf)
    s = s.fuse(box(100, 110, D - 8, D, H - 8, H))              # üst kapak vidası (arka)
    gus = [V(0, D, H - 16), V(0, D, H - 8), V(0, D - 8, H - 8), V(0, D, H - 16)]
    s = s.fuse(Part.Face(Part.makePolygon(gus)).extrude(V(10, 0, 0)).translated(V(100, 0, 0)))
    s = s.fuse(box(PSU_X0 + 2, 34, PSU_Y0 + 2, PSU_Y0 + 10, 0, PSU_Z0))  # PSU ön ayağı (alt fana 2 mm kala)
    s = s.fuse(box(PSU_X0 + 2, 40, D - 8, D, 0, PSU_Z0))                # PSU arka ayağı
    for x, y in FEET:                                          # ayak vidası bossları (içeride)
        s = s.fuse(cyl(5, 6, (x, y, 0), (0, 0, 1)))
    for key in ("on_alt", "on_ust", "on_serit"):               # ön panel bossları (ön duvarın içi)
        for x, z in PANELS[key]["screws"]:
            s = s.fuse(cyl(4.5, 7.5, (x, 0, z), (0, 1, 0)))
        for x, z in PANELS[key].get("magnets", []):            # mıknatıs blokları (ön duvarın içi)
            s = s.fuse(box(x - 5, x + 5, 0, 7.5, z - 5, z + 5))

    cuts = []
    for dy, dz in HOLES:
        cuts.append(insert(X_BB, Y_R - dy, Z_TOP - dz, (1, 0, 0)))
    io = IO
    cuts.append(box(io[0], io[1], D - 1, D + T + 1, io[2], io[3]))
    # I/O kalkanı yayları için çevresinde 1.2 mm duvar (dıştan cep)
    # alt kenarda inceltme yok: GPU açıklığı ile arasındaki 3.2 mm'lik şerit tam kalınlıkta kalsın
    cuts.append(box(io[0] - 2.5, io[1] + 2.5, D + 1.2, D + T + 1, io[2], io[3] + 2.5))
    # GPU açıklığı + braket kulağının geçtiği yarık + vida yuvaları
    cuts.append(box(X_TAB + 10.5, W - 2, D - 1, D + T + 1, Z_C - 44, Z_C + 4))
    cuts.append(box(X_TAB - 2.2, X_TAB, D - 1, D + T + 1, Z_C - 44, Z_C + 4))
    for off in GPU_SLOT_OFF:
        cuts.append(insert(X_TAB, D + T + 5, Z_C - off, (1, 0, 0)))
    # PSU: vidalar, ızgara, priz/anahtar (standart yerleşim; PSU fotoğrafıyla güncellenecek)
    for hx, hy in PSU_HOLES:
        cuts.append(cyl(UNC632 / 2, T + 2, (PSU_X0 + hy, D - 1, PSU_Z0 + 150 - hx), (0, 1, 0)))
    cuts += hex_cutters(hex_centers(PSU_X0 + 10, PSU_X0 + 76, PSU_Z0 + 52, PSU_Z0 + 138, 4.5),
                        4.5, lambda u, v: V(u, D - 1, v), V(0, T + 2, 0))
    cuts.append(box(PSU_X0 + 26, PSU_X0 + 76, D - 1, D + T + 1, PSU_Z0 + 6, PSU_Z0 + 36))    # priz (orta) + anahtar (solu)
    # kapak insertleri: üst kapak için dikey, yan kapaklar için yatay
    for x, y in LID_SCREWS:
        cuts.append(insert(x, y, H, (0, 0, -1)))
    for y, z in LOWER_SCREWS + UPPER_SCREWS:
        cuts.append(insert(0, y, z, (1, 0, 0)))
    for x, y in FEET:                                          # ayak insert'leri, alttan
        cuts.append(insert(x, y, -T, (0, 0, 1)))
    for key in ("on_alt", "on_ust", "on_serit"):               # ön panel açıklıkları, gömmeler, insert'ler
        pl, op = PANELS[key]["plate"], PANELS[key]["open"]
        cuts.append(box(op[0], op[1], -T - 1, 0.5, op[2], op[3]))
        if PANELS[key]["screws"]:
            g = box(pl[0], pl[1], -T - 1, -T + 1.25, pl[2], pl[3])
            cuts.append(g.makeFillet(PANEL_R, [e for e in g.Edges if abs(e.Vertexes[0].Point.y - e.Vertexes[1].Point.y) > 1e-6]))
        for x, z in PANELS[key]["screws"]:
            cuts.append(cyl(4.3, 2.0, (x, -T + 1.25 - 0.01, z), (0, 1, 0)))   # panel pad yuvası
            cuts.append(insert(x, 0.75, z, (0, 1, 0)))
        # mıknatıs cebi: plaka mıknatısı 4 mm girer (Y -T..1.5), kasa mıknatısı arkasında (Y 1.5..6.26)
        for x, z in PANELS[key].get("magnets", []):
            h = MAGNET[0] / 2 + 0.15
            cuts.append(box(x - h, x + h, -T - 1, 1.5 + MAGNET[1], z - h, z + h))
    # havalandırma: ön yüz (soğutucu hava yolu) ve taban (GPU fanı altı)
    cuts += fan_cut(FAN_BOTTOM[0], FAN_BOTTOM[1], lambda u, v: V(u, v, -T - 1), V(0, 0, T + 2))   # alt giriş fanı
    # anakart tablasında CPU arkası (sağ dış yüz)
    cuts += hex_cutters(hex_centers(CPU_Y - 40, CPU_Y + 40, CPU_Z - 40, CPU_Z + 40, 4.5),
                        4.5, lambda u, v: V(W - 1, u, v), V(T + 2, 0, 0))
    s = cut_all(s, cuts)
    # kırılabilir destekler: I/O, GPU ve priz açıklıklarının üst kenarı
    ribs = breakaway_ribs(io[0], io[1], D, D + 1.2, io[2], io[3])
    ribs += breakaway_ribs(X_TAB + 10.5, W - 2, D, D + T, Z_C - 44, Z_C + 4)
    ribs += breakaway_ribs(PSU_X0 + 26, PSU_X0 + 76, D, D + T, PSU_Z0 + 6, PSU_Z0 + 36)
    for key in ("on_alt", "on_ust", "on_serit"):
        op = PANELS[key]["open"]
        y0 = -T + 1.25 if PANELS[key]["screws"] else -T   # gömmesiz (Steam) açıklıkta kaburga tam duvar
        ribs += breakaway_ribs(op[0], op[1], y0, 0, op[2], op[3])
    global RIBS
    RIBS = Part.makeCompound(ribs)   # çakışma kontrolünde yok sayılır (baskıdan sonra kırılır)
    for r in ribs:
        s = s.fuse(r)
    return s

# ---------------------------------------------------------------- gövde eki
# Alt gövde Z_JOINT'e kadar; iç yüzünde 2 mm etek (ön, sağ) ve sol direklerde pimler üst
# gövdeyi hizalar. Ön: 2 yatay M3 havşa vida dıştan alt gövdedeki iç bloklara. Arka: iç taraf
# GPU/PSU ile dolu, o yüzden dışarıda 7 mm'lik kulaklar; üst kulaktan dikey vida alt kulağa.
# Her iki parça dik basılır.
def split_body(full):
    zj = Z_JOINT
    alt = full.common(box(-T - 1, W + T + 1, -T - 1, D + T + 12, -T - 1, zj))
    ust = full.common(box(-T - 1, W + T + 1, -T - 1, D + T + 12, zj, H + 1))
    def lip(x0, x1, y0, y1, dx, dy):
        # (dx, dy): duvara doğru yön; ekin üstünde duvardan FIT kadar içeride
        a = box(x0, x1, y0, y1, zj - 4, zj)
        b = box(x0 - dx * FIT if dx > 0 else x0, x1 - dx * FIT if dx < 0 else x1,
                y0 - dy * FIT if dy > 0 else y0, y1 - dy * FIT if dy < 0 else y1, zj - 0.01, zj + 6)
        return a.fuse(b)
    add = [lip(12 + FIT, W - 9 - FIT, 0, 2, 0, -1),                    # ön
           lip(W - 2, W, 10 + FIT, D - FIT, 1, 0)]                      # sağ (anakart arkası)
    cuts_alt, cuts_ust = [], []
    for wall, x in JOINT_SCREWS:
        if wall == "on":
            add.append(box(x - 4, x + 4, 0, 8, zj - 10, zj).fuse(box(x - 4, x + 4, FIT, 8, zj - 0.01, JOINT_FRONT_Z + 5)))
            cuts_alt.append(insert(x, FIT, JOINT_FRONT_Z, (0, 1, 0)))
            cuts_ust += countersink(x, -T, JOINT_FRONT_Z, (0, 1, 0))
        else:
            add.append(box(x - 4, x + 4, D + T - 1, D + T + 7, zj - 10, zj))
            cuts_alt.append(insert(x, D + T + 3.5, zj, (0, 0, -1)))
            ust = ust.fuse(box(x - 4, x + 4, D + T - 1, D + T + 7, zj, zj + 8))
            cuts_ust += countersink(x, D + T + 3.5, zj + 8, (0, 0, -1), depth=8)
    for x0, x1, y0, y1 in PEGS:
        add.append(box(x0, x1, y0, y1, zj - 1, zj + 4))
        cuts_ust.append(box(x0 - FIT, x1 + FIT, y0 - FIT, y1 + FIT, zj - 1, zj + 4 + FIT))
    for a in add:
        alt = alt.fuse(a)
    return cut_all(alt, cuts_alt), cut_all(ust, cuts_ust)

# ---------------------------------------------------------------- üst kapak
def lid():
    s = chamfered_box(-T, W + T, -T, D + T, H, H + T_LID, EDGE, top=True)
    # iç etek: duvarların içine FIT boşlukla oturur, kapağı hizalar
    rim = [box(12 + FIT, W - 9 - FIT, FIT, FIT + 2, H - 4, H),           # ön
           box(W - FIT - 2, W - FIT, 10 + FIT, D - FIT, H - 4, H),        # sağ
           box(7.5 + FIT, 100 - FIT, D - FIT - 2, D - FIT, H - 4, H)]     # arka (direk → I/O kalkanı)
    for r in rim:
        s = s.fuse(r)
    cuts = []
    for x, y in LID_SCREWS:
        cuts += countersink(x, y, H + T_LID, (0, 0, -1), depth=T_LID)
    # üst yan kapağın dilinin girdiği oluk
    cuts.append(box(-1.0 - FIT, FIT, FIT, D - FIT, H - 0.1, H + 1.5))   # dil oluğu; dış kenar şeridi 0.8, üstünde 0.8 köprü
    cuts += fan_cut(FAN_TOP[0], FAN_TOP[1], lambda u, v: V(u, v, H - 5), V(0, 0, T_LID + 6))
    return cut_all(s, cuts)

# ---------------------------------------------------------------- yan kapaklar
# Her yan kapak kendi gövde yarısını örter; ek gövde ekiyle aynı hizada (Z_JOINT), düz.
# Üst yan kapağın üst kenarındaki dil üst kapağın oluğuna girer, kapak dışa açılamaz.
def lower_cover():
    s = box(-T, 0, FIT, D - FIT, FIT, SPLIT - FIT / 2).common(outer_envelope())
    cuts = []
    for y, z in SSD_HOLES:                                     # SSD aralayıcıları (iç yüz)
        s = s.fuse(cyl(4, 1.5, (0, y, z), (1, 0, 0)))
    for y, z in LOWER_SCREWS + SSD_HOLES:
        cuts += countersink(-T, y, z, (1, 0, 0), depth=T + 2)
    return cut_all(s, cuts)

def upper_cover():
    s = box(-T, 0, FIT, D - FIT, SPLIT + FIT / 2, H - FIT).common(outer_envelope())
    s = s.fuse(box(-1.0, 0, FIT + 1, D - FIT - 1, H - FIT, H + 1.3))               # üst dil
    cuts = []
    for y, z in UPPER_SCREWS:
        cuts += countersink(-T, y, z, (1, 0, 0))
    cy, cz = PSU_Y0 + 70, PSU_Z0 + 75      # PSU fanı (alt yüzün merkezi)
    cuts += hex_cutters(hex_centers(cy - 60, cy + 60, cz - 60, cz + 60, 4.5,
                                    inside=lambda u, v: math.hypot(u - cy, v - cz) < 56),
                        4.5, lambda u, v: V(-T - 1, u, v), V(T + 2, 0, 0))
    return cut_all(s, cuts)

# ---------------------------------------------------------------- ayak (4 adet basılır)
def foot():
    # Ø22 × 12 silindir, alttan Ø7 × 8 havşa yuvası; M3 × 8 silindir başlı vida tabandaki insert'e.
    # Düz yüzü (üstü) tablaya gelir; montaj koordinatında tabanın altında, ilk ayak konumunda.
    x, y = FEET[0]
    s = cyl(FOOT_D / 2, FOOT_H, (x, y, -T - FOOT_H), (0, 0, 1))
    s = s.makeChamfer(1.0, [e for e in s.Edges if abs(e.BoundBox.ZMin - (-T - FOOT_H)) < 1e-6])
    s = s.cut(cyl(3.5, 8, (x, y, -T - FOOT_H - 0.01), (0, 0, 1)))
    s = s.cut(cyl(M3 / 2, FOOT_H + 1, (x, y, -T - FOOT_H - 0.5), (0, 0, 1)))
    return s

# ---------------------------------------------------------------- ön panel (3 örnek)
def front_panel(key, kind="petek"):
    sp = PANELS[key]
    x0, x1, z0, z1 = sp["plate"]
    o = sp["open"]
    cuts = []
    def rbox(a0, a1, y0, y1, b0, b1, r):   # XZ düzleminde köşeleri r ile yuvarlatılmış plaka
        bx = box(a0, a1, y0, y1, b0, b1)
        return bx.makeFillet(r, [e for e in bx.Edges if abs(e.Vertexes[0].Point.y - e.Vertexes[1].Point.y) > 1e-6])
    if sp.get("magnets"):
        # Steam Machine tipi: 6.5 mm plaka duvarın dış yüzüne oturur (Y -T-6.5..-T); arkasında 4 mıknatıs
        # bossu 4 mm çıkar, mıknatıs bossun ucuyla hizalı (cep 4.76 derin, 0.76'sı plakanın içinde)
        s = rbox(x0, x1, -T - 6.5, -T, z0, z1, PANEL_R)
        for x, z in sp["magnets"]:          # arka yüzde sığ cep (0.8 mm), mıknatıs yapıştırılır, 4 mm dışarı çıkar
            h = MAGNET[0] / 2 + 0.1
            cuts.append(box(x - h, x + h, -T - 0.8, -T + 1, z - h, z + h))
        yf = -T - 6.5   # dış yüz
    else:
        # vidalı paneller: dış plaka Y -T..-T+1.25 (gömmede), iç kademe Y -T+1.25..0 (açıklıkta)
        s = rbox(x0 + FIT / 2, x1 - FIT / 2, -T, -T + 1.25, z0 + FIT / 2, z1 - FIT / 2, PANEL_R)
        s = s.fuse(box(o[0] + FIT / 2, o[1] - FIT / 2, -T + 1.25 - 0.01, 0, o[2] + FIT / 2, o[3] - FIT / 2))
        yf = -T
        for x, z in sp["screws"]:
            s = s.fuse(cyl(4, 2.0 - FIT / 2, (x, -T + 1.25 - 0.01, z), (0, 1, 0)))
            cuts += countersink(x, -T, z, (0, 1, 0), depth=4)
    cx, cz = (o[0] + o[1]) / 2, (o[2] + o[3]) / 2
    if kind == "petek":
        cuts += hex_cutters(hex_centers(o[0] + 3, o[1] - 3, o[2] + 3, o[3] - 3, 4.0),
                            4.0, lambda u, v: V(u, yf - 1, v), V(0, 10, 0))
    elif kind == "ekran":   # 3.5" IPS modülü (480x320) için pencere 75 x 46
        cuts.append(box(cx - 37.5, cx + 37.5, yf - 1, 1, cz - 23, cz + 23))
    elif kind == "fan":     # 120 mm fan: ızgara + 4 vida deliği (fan içeriden panele vidalanır)
        cuts += fan_cut(cx, cz, lambda u, v: V(u, yf - 1, v), V(0, 10, 0))
    elif kind == "tus":     # kontrol şeridi: 2 Cherry MX (14 x 14, çevresi 1.5 mm plaka), USB-C, 2 x USB-A
        for x, z in SWITCHES:
            cuts.append(box(x - 7.05, x + 7.05, yf - 1, 1, z - 7.05, z + 7.05))
            cuts.append(box(x - 10, x + 10, yf + 1.5, 1, z - 10, z + 10))
        cuts.append(box(USB_C[0] - 4.8, USB_C[0] + 4.8, yf - 1, 1, USB_C[1] - 1.95, USB_C[1] + 1.95))
        for x, z in USB_A:
            cuts.append(box(x - 6.8, x + 6.8, yf - 1, 1, z - 3.2, z + 3.2))
    return cut_all(s, cuts)

# ---------------------------------------------------------------- referans parçalar (basılmaz)
def fan(cx, cy, cz, axis, size, depth, blades=7, split=False):
    # eksenel fan: çerçeve − hava deliği + hub + kanatlar; axis = (1,0,0)/(0,1,0)/(0,0,1) birim yön
    ax = V(*axis)
    c = V(cx, cy, cz)
    base = c - ax * (depth / 2)
    r = size / 2 - 1.5
    # çerçeveyi eksene göre kur: kare prizma eksen boyunca
    u = V(0, 0, 1).cross(ax) if abs(ax.z) < 0.9 else V(1, 0, 0)
    v = ax.cross(u)
    corner = base - u * (size / 2) - v * (size / 2)
    frame = Part.makeBox(size, size, depth).copy()
    m = App.Matrix(u.x, v.x, ax.x, corner.x, u.y, v.y, ax.y, corner.y, u.z, v.z, ax.z, corner.z, 0, 0, 0, 1)
    frame = frame.transformGeometry(m)
    frame = frame.cut(Part.makeCylinder(r, depth + 2, base - ax, ax))
    hub = Part.makeCylinder(size * 0.18, depth - 2, base + ax, ax)
    s = hub
    for i in range(blades):
        bl = Part.makeBox(r - size * 0.18 - 1, 2, depth - 4, V(size * 0.18, -1, -(depth - 4) / 2))
        bl.rotate(V(0, 0, 0), V(1, 0, 0), 35)
        bl.rotate(V(0, 0, 0), V(0, 0, 1), 360 * i / blades)
        bl.Placement = App.Placement(c, App.Rotation(V(0, 0, 1), ax)).multiply(bl.Placement)
        s = s.fuse(bl)
    return (frame, s) if split else frame.fuse(s)

def references():
    # Basılmayan donanım; ölçüler ATX/PCIe standartlarından ve ürün ölçülerinden (yaklaşık).
    pcb = box(X_BF, X_BB, Y_R - 185, Y_R, Z_B, Z_TOP)
    # I/O port bloğu: açıklığın içinde, duvara 0.5 mm kala
    board = pcb.fuse(box(X_BF - 14, X_BF, Y_R - 18, D - 0.5, IO[2] + 3, IO[3] - 6))
    board = board.fuse(box(X_BF - 16, X_BF, Y_R - 18, D - 0.5, IO[2] + 3, IO[2] + 17))    # PS/2 + USB
    board = board.fuse(box(X_BF - 8, X_BF, CPU_Y - 18.75, CPU_Y + 18.75, CPU_Z - 18.75, CPU_Z + 18.75))  # soket + CPU
    board = board.fuse(box(X_BF - 11, X_BF, Y_R - 99, Y_R - 10, Z_C - 4.5, Z_C + 3))           # PCIEX16
    board = board.fuse(box(X_BF - 11, X_BF, Y_R - 35, Y_R - 10, Z_C - 40.64 - 4, Z_C - 40.64 + 3))  # PCIEX1
    for dz in (58, 68.2):                                                                      # 2 × DIMM
        board = board.fuse(box(X_BF - 7, X_BF, Y_R - 168, Y_R - 35, CPU_Z - dz - 3, CPU_Z - dz + 3))
    board = board.fuse(box(X_BF - 9, X_BF, Y_R - 180, Y_R - 168, CPU_Z - 60, CPU_Z - 8))      # 24 pin
    board = board.fuse(box(X_BF - 8, X_BF, Y_R - 60, Y_R - 30, Z_TOP - 190, Z_TOP - 160))     # yonga seti
    for i in range(4):                                                                         # SATA
        board = board.fuse(box(X_BF - 7, X_BF, Y_R - 150 + i * 13, Y_R - 141 + i * 13, Z_B, Z_B + 16))
    # GPU: PCB + soğutucu kaputu + fan; braket plakası + dışarı çıkan kulak + portlar
    gpu = box(X_BF - 115, X_BF - 4, D - 192, D - 3, Z_C - 1.6, Z_C)
    gpu = gpu.fuse(box(X_BF - 108, X_BF - 10, D - 180, D - 12, Z_C - 37, Z_C - 1.6))
    gpu = gpu.cut(Part.makeCylinder(44, 12, V(X_BF - 59, D - 96, Z_C - 38), V(0, 0, 1)))
    gf, gpu_rotor = fan(X_BF - 59, D - 96, Z_C - 31, (0, 0, 1), 86, 12, 9, split=True)
    gpu = gpu.fuse(gf)
    bracket = box(X_TAB - 1.2, X_BF + 5, D - 1.2, D, Z_C - 38, Z_C + 3)
    bracket = bracket.fuse(box(X_TAB - 1.2, X_TAB, D - 1.2, D + T + 9, Z_C - 38, Z_C + 3))
    for off in GPU_SLOT_OFF:
        bracket = bracket.cut(box(X_TAB - 2, X_TAB + 1, D + T + 3, D + T + 10, Z_C - off - 1.8, Z_C - off + 1.8))
    for x0, x1 in ((X_TAB + 12, X_TAB + 36), (X_TAB + 40, X_TAB + 56), (X_TAB + 60, X_TAB + 76)):  # DVI, HDMI, DP
        bracket = bracket.fuse(box(x0, x1, D - 1.2, D - 0.2, Z_C - 15, Z_C - 9))   # duvara 0.2 kala (kaburgalar)
    # soğutucu: kanat paketi (Y boyunca 24 plaka) + 4 ısı borusu + 90 mm fan
    cooler = None
    for i in range(24):
        y = CPU_Y - 46 + i * 4
        pl = box(X_BF - 46, X_BF - 10, y, y + 0.8, CPU_Z - 46, CPU_Z + 46)
        cooler = pl if cooler is None else cooler.fuse(pl)
    for dy in (-15, -5, 5, 15):
        cooler = cooler.fuse(Part.makeCylinder(3, 92, V(X_BF - 28, CPU_Y + dy, CPU_Z - 46), V(0, 0, 1)))
    cooler = cooler.fuse(box(X_BF - 10, X_BF - 8, CPU_Y - 19, CPU_Y + 19, CPU_Z - 19, CPU_Z + 19))
    cf, cpu_rotor = fan(X_BF - 53.5, CPU_Y, CPU_Z, (1, 0, 0), 90, 15, split=True)
    cooler = cooler.fuse(cf)
    # PSU: kasa + fan (sol yüz) + priz/anahtar (arka) + kablo demeti (ön)
    psu = box(PSU_X0, PSU_X0 + 86, PSU_Y0, D, PSU_Z0, PSU_Z0 + 150)
    psu = psu.cut(Part.makeCylinder(58, 3, V(PSU_X0 - 1, PSU_Y0 + 70, PSU_Z0 + 75), V(1, 0, 0)))
    pf, psu_rotor = fan(PSU_X0 + 8, PSU_Y0 + 70, PSU_Z0 + 75, (1, 0, 0), 120, 15, split=True)
    psu = psu.fuse(pf)
    psu = psu.cut(box(PSU_X0 + 26, PSU_X0 + 76, D - 1, D + 1, PSU_Z0 + 6, PSU_Z0 + 36))
    psu = psu.fuse(box(PSU_X0 + 29, PSU_X0 + 57, D - 6, D - 1, PSU_Z0 + 10, PSU_Z0 + 32))     # C14 priz, alt orta
    psu = psu.fuse(box(PSU_X0 + 61, PSU_X0 + 73, D - 6, D - 1, PSU_Z0 + 12, PSU_Z0 + 30))    # anahtar, solunda
    psu = psu.fuse(Part.makeCylinder(12, 30, V(PSU_X0 + 43, PSU_Y0, PSU_Z0 + 22), V(0, -1, 0)))   # kablolar, ön alt
    ssd = box(1.5, 8.5, SSD_Y0, SSD_Y0 + 100, SSD_Z0, SSD_Z0 + 69.85)
    o = PANELS["on_alt"]["open"]; cx, cz = (o[0] + o[1]) / 2, (o[2] + o[3]) / 2
    lcd = box(cx - 42.5, cx + 42.5, 0, 5, cz - 27.5, cz + 27.5)        # 3.5" IPS modülü 85 x 55 x 5, panelin arkasında
    case_fan, top_rotor = fan(FAN_TOP[0], FAN_TOP[1], H - FAN_T / 2, (0, 0, 1), FAN_D + 2, FAN_T, split=True)     # üst, egzoz
    bot_fan, bot_rotor = fan(FAN_BOTTOM[0], FAN_BOTTOM[1], FAN_T / 2, (0, 0, 1), FAN_D + 2, FAN_T, split=True)   # alt, giriş
    return dict(ref_board=(board, (0.1, 0.45, 0.2)), ref_gpu=(gpu, (0.15, 0.3, 0.75)),
                ref_bracket=(bracket, (0.75, 0.75, 0.75)), ref_cooler=(cooler, (0.3, 0.3, 0.3)),
                ref_psu=(psu, (0.2, 0.2, 0.2)), ref_ssd=(ssd, (0.6, 0.2, 0.2)),
                ref_fan=(case_fan, (0.25, 0.25, 0.3)), ref_fan_alt=(bot_fan, (0.25, 0.25, 0.3)),
                rotor_ust=(top_rotor, (0.45, 0.45, 0.5)), rotor_alt=(bot_rotor, (0.45, 0.45, 0.5)),
                rotor_cpu=(cpu_rotor, (0.45, 0.45, 0.5)), rotor_gpu=(gpu_rotor, (0.45, 0.45, 0.5)),
                rotor_psu=(psu_rotor, (0.45, 0.45, 0.5)), ref_lcd=(lcd, (0.1, 0.1, 0.12)))

PRINTED = ("govde_alt", "govde_ust", "ust_kapak", "yan_alt", "yan_ust", "ayak", "on_panel_alt", "on_panel_ust", "on_serit")
FULL = None   # bölünmemiş gövde (deneme parçası için)
RIBS = None   # kırılabilir destek kaburgaları

def build(doc_name="MiniPCKasa"):
    doc = App.getDocument(doc_name) if doc_name in App.listDocuments() else App.newDocument(doc_name)
    for o in list(doc.Objects):
        doc.removeObject(o.Name)
    global FULL
    FULL = body()
    alt, ust = split_body(FULL)
    parts = dict(govde_alt=(alt, (0.82, 0.82, 0.85)),
                 govde_ust=(ust, (0.7, 0.72, 0.78)),
                 ust_kapak=(lid(), (0.55, 0.57, 0.62)),
                 yan_alt=(lower_cover(), (0.9, 0.6, 0.3)),
                 yan_ust=(upper_cover(), (0.9, 0.6, 0.3)),
                 ayak=(foot(), (0.5, 0.5, 0.55)),
                 on_panel_alt=(front_panel("on_alt", "ekran"), (0.15, 0.15, 0.17)),   # 3.5" LCD penceresi
                 on_panel_ust=(front_panel("on_ust", "duz"), (0.45, 0.25, 0.12)),     # düz: ahşap kaplama / boya
                 on_serit=(front_panel("on_serit", "tus"), (0.2, 0.2, 0.22)))
    parts.update(references())
    for name, (shape, color) in parts.items():
        o = doc.addObject("Part::Feature", name)
        o.Shape = shape
        if App.GuiUp:
            o.ViewObject.ShapeColor = color
            if name.startswith("yan"):
                o.ViewObject.Transparency = 60
    doc.recompute()
    for name in PRINTED:
        sh = doc.getObject(name).Shape
        bb = sh.BoundBox
        print(f"{name}: {bb.XLength:.1f} x {bb.YLength:.1f} x {bb.ZLength:.1f} mm, "
              f"{sh.Volume / 1000:.0f} cm3, geçerli={sh.isValid()}, katı={len(sh.Solids)}")
    # çakışma kontrolü: basılan parçalar birbirine ve donanıma değmemeli
    names = list(PRINTED) + [n for n in parts if n.startswith("ref_")]   # rotorlar fan gövdesinin içinde, atlanır
    clash = []
    for i, a in enumerate(names):
        for b in names[i + 1:]:
            if a.startswith("ref_") and b.startswith("ref_") and not (a.startswith("ref_fan") or b.startswith("ref_fan")):
                continue   # donanım-donanım çakışması sadece kasa fanları için bakılır
            sa = doc.getObject(a).Shape
            if a.startswith("govde"):
                sa = sa.cut(RIBS)
            v = sa.common(doc.getObject(b).Shape).Volume
            if v > 0.5:
                clash.append((a, b, round(v)))
    print("çakışma:", clash or "yok")
    return doc

def test_piece(doc):
    # arka-sağ köşe: GPU açıklığı + braket rafı, I/O açıklığının alt kısmı, B/C standoff'ları.
    # Anakartı 2 vidayla takıp I/O kalkanı ve GPU braketini denemek için.
    return FULL.common(box(X_TAB - 5, W + T, D - 22, D + T + 11, -T, 130))

def export_stl(out_dir="/Users/cobanov/Developer/mini-pc-kasa/stl", doc_name="MiniPCKasa"):
    import os
    import MeshPart
    os.makedirs(out_dir, exist_ok=True)
    doc = App.getDocument(doc_name)
    shapes = {n: doc.getObject(n).Shape for n in PRINTED}
    shapes["deneme_parcasi"] = test_piece(doc)
    for key, kinds in (("on_alt", ("duz", "petek")), ("on_ust", ("petek", "ekran"))):
        for k in kinds:
            shapes[f"on_panel_{key[3:]}_{k}"] = front_panel(key, k)
    shapes["on_serit_duz"] = front_panel("on_serit", "duz")
    for n, sh in shapes.items():
        sh.exportStep(os.path.join(out_dir, f"{n}.step"))      # STEP montaj koordinatında
        rot = PRINT_ORIENT.get(n, (V(1, 0, 0), 90) if n.startswith("on_panel") else None)   # STL baskı yönünde
        p = sh.copy()
        if rot:
            p.rotate(V(0, 0, 0), rot[0], rot[1])
        bb = p.BoundBox
        p.translate(V(-bb.XMin, -bb.YMin, -bb.ZMin))
        m = MeshPart.meshFromShape(Shape=p, LinearDeflection=0.05, AngularDeflection=0.25,
                                   Relative=False)
        m.write(os.path.join(out_dir, f"{n}.stl"))
        bb = sh.BoundBox
        print(f"{n}.stl: {bb.XLength:.0f} x {bb.YLength:.0f} x {bb.ZLength:.0f} mm, "
              f"{sh.Volume / 1000:.0f} cm3, kapalı={m.isSolid()}")

def check_fasteners(doc_name="MiniPCKasa"):
    # Her vida için: insert yuvası alıcı parçada boş ve çevresi tam derinlikte dolu mu, karşı parçada
    # delik boş ve çevresi dolu mu. (p = yüzey noktası, d = içeri yön) Kırpılmış/karşılıksız delikleri yakalar.
    doc = App.getDocument(doc_name)
    sh = {o.Name: o.Shape for o in doc.Objects}
    def probe(name, pt):
        return sh[name].isInside(V(*pt), 0.01, True)
    def ring(p, d, depth, r):
        d = V(*d); u = V(0, 0, 1).cross(d) if abs(d.z) < 0.9 else V(1, 0, 0); w = d.cross(u)
        c = V(*p) + d * depth
        return [c + u * r, c - u * r, c + w * r, c - w * r]
    F = []   # (ad, insert parçası, vida parçası, yüzey noktası, yön)
    for x, y in LID_SCREWS: F.append(("üst kapak", "govde_ust", "ust_kapak", (x, y, H), (0, 0, -1)))
    for y, z in LOWER_SCREWS: F.append(("alt yan kapak", "govde_alt", "yan_alt", (0, y, z), (1, 0, 0)))
    for y, z in UPPER_SCREWS: F.append(("üst yan kapak", "govde_ust", "yan_ust", (0, y, z), (1, 0, 0)))
    for wall, x in JOINT_SCREWS:
        if wall == "on": F.append(("gövde eki ön", "govde_alt", "govde_ust", (x, FIT, JOINT_FRONT_Z), (0, 1, 0)))
        else: F.append(("gövde eki arka", "govde_alt", "govde_ust", (x, D + T + 3.5, Z_JOINT), (0, 0, -1)))
    for x, z in PANELS["on_alt"]["screws"]: F.append(("ön alt panel", "govde_alt", "on_panel_alt", (x, 0.75, z), (0, 1, 0)))
    for x, z in PANELS["on_serit"]["screws"]: F.append(("ön şerit", "govde_ust", "on_serit", (x, 0.75, z), (0, 1, 0)))
    for x, y in FEET: F.append(("ayak", "govde_alt", None, (x, y, -T), (0, 0, 1)))
    for dy, dz in HOLES:
        z = Z_TOP - dz
        F.append(("anakart", "govde_ust" if z > Z_JOINT else "govde_alt", None, (X_BB, Y_R - dy, z), (1, 0, 0)))
    for off in GPU_SLOT_OFF: F.append(("GPU braketi", "govde_alt", None, (X_TAB, D + T + 5, Z_C - off), (1, 0, 0)))
    bad = 0
    for name, ins, scr, p, d in F:
        probs = []
        c1 = V(*p) + V(*d) * 2
        if probe(ins, c1): probs.append("insert yuvası dolu")
        for q in ring(p, d, 2, 3.4) + ring(p, d, 5.5, 3.4):
            if not probe(ins, q): probs.append("insert çevresi eksik (kırpılmış)"); break
        if scr:
            c2 = V(*p) - V(*d) * 1.2
            if probe(scr, c2): probs.append("karşı delik yok")
            for q in ring(p, d, -1.9, 3.0):
                if not probe(scr, q): probs.append("karşı delik parça kenarında"); break
        if probs:
            bad += 1
            print(f"  ✗ {name} @ ({p[0]:.1f},{p[1]:.1f},{p[2]:.1f}): {', '.join(sorted(set(probs)))}")
    print(f"bağlantı denetimi: {len(F)} vida, {bad} sorunlu" if bad else f"bağlantı denetimi: {len(F)} vida, hepsi tamam")

def check_print(doc_name="MiniPCKasa", step=0.25):
    # Baskı yönünde aşağı bakan (45°'den yatık), tablaya değmeyen düz yüzlerin altını uzun
    # ekseni boyunca tarar. Bir nokta, yüzün ortasının ya da uzun kenarlarının hemen
    # dışının altında malzeme varsa desteklidir (kenardan çıkıntı / kaburga). Altı boş en
    # uzun kesintisiz aralık = desteksiz köprü boyu; MAX_BRIDGE'i aşanlar listelenir.
    doc = App.getDocument(doc_name)
    for n, rot in PRINT_ORIENT.items():
        sh = doc.getObject(n).Shape.copy()
        if rot:
            sh.rotate(V(0, 0, 0), rot[0], rot[1])
        bed = sh.BoundBox.ZMin
        bad = []
        for f in sh.Faces:
            if f.Surface.TypeId != "Part::GeomPlane" or f.Area < 5 or f.BoundBox.ZMin < bed + 0.01:
                continue
            u0, u1, v0, v1 = f.ParameterRange
            if f.normalAt((u0 + u1) / 2, (v0 + v1) / 2).z > -0.75:
                continue
            bb = f.BoundBox
            along_x = bb.XLength >= bb.YLength
            a0, a1 = (bb.XMin, bb.XMax) if along_x else (bb.YMin, bb.YMax)
            s0, s1 = (bb.YMin, bb.YMax) if along_x else (bb.XMin, bb.XMax)
            pt = (lambda a, b, z: V(a, b, z)) if along_x else (lambda a, b, z: V(b, a, z))
            z = bb.ZMin
            run = longest = 0.0
            t = a0 + step / 2
            while t < a1:
                if f.isInside(pt(t, (s0 + s1) / 2, z), 0.05, True):
                    held = any(sh.isInside(pt(t, c, z - 0.35), 0.01, True)
                               for c in ((s0 + s1) / 2, s0 - 0.3, s1 + 0.3))
                    run = 0.0 if held else run + step
                    longest = max(longest, run)
                t += step
            if longest > MAX_BRIDGE:
                c = bb.Center
                bad.append(dict(boy=round(longest), z=round(z - bed), x=round(c.x), y=round(c.y)))
        print(f"{n}: {'uzun köprü/çıkıntı yok' if not bad else bad}")

build()
