# Mini PC case v4 — PSU on its side opposite the CPU cooler; body split in two at Z = 80.
# Run inside FreeCAD: exec(open(".../build_case.py").read()); export_stl() writes STL + STEP.
# Coordinates (mm, inner volume): X left inner face = 0 → motherboard tray (right) W,
# Y front inner face = 0 → rear inner face D, Z floor top = 0 → up.
# Dimension sources: NOTES.md (ATX 2.2, ATX12V PSDG 2.2, ASUS PRIME H310M-K manual).
# Screws and assembly: ASSEMBLY.md
import math
import FreeCAD as App
import Part
from FreeCAD import Vector as V

T = 2.2            # wall thickness (1 kg PETG target; 3 perimeters × 0.42 = 1.26 + infill)
T_LID = 3.0        # lid (carries the 2 mm groove for the side cover tongue; at 2.5 the groove split the outer edge)
W, D = 172.0, 200.0
H = 258.0          # inner height (underside of the lid); PSU top 230 + 25 mm exhaust fan + 3 mm clearance
EDGE = 1.5         # top/bottom outer edge chamfer (45°, prints without support)
CORNER_R = 5.0     # vertical outer corner radius (fine in upright prints)
FIT = 0.4          # clearance between mating parts (0.3 + 0.1 for PETG)
TOL = 0.3          # allowance for holes shrinking in print
MAX_BRIDGE = 18.0  # unsupported bridge limit; wider openings get breakaway ribs

# Fasteners — all M3, one insert type
INSERT_D, INSERT_L = 4.0, 6.0   # pocket for M3 x 5 x 4.5 brass heat-set insert
M3 = 3.4                        # M3 clearance hole
UNC632 = 3.8                    # PSU screw (6-32 UNC) clearance hole

STANDOFF = 6.35
X_BB = W - STANDOFF          # motherboard back face
X_BF = X_BB - 1.6            # motherboard front (component) face
Y_R = D - 2.1                # motherboard rear edge (ATX: panel 0.483", edge 0.400")
Z_B = 12.0                   # motherboard bottom edge (SATA cable clearance)
Z_TOP = Z_B + 226.0          # motherboard top edge
# Holes: (from rear edge, from top edge) — F, J, C, H, B, R
HOLES = [(33.02, 6.35), (165.1, 6.35), (10.16, 163.83),
         (165.1, 163.83), (10.16, 209.55), (165.1, 209.55)]
Z_C = Z_TOP - 163.83         # PCIEX16 centre line (C/H hole row)
COOLER_H = 61.0              # board surface → top of cooler (53 mm + socket/CPU)
CPU_Y, CPU_Z = Y_R - 98.2, Z_TOP - 85.8

GPU_TAB_H = 112.5            # board surface → underside of the bracket tab (verify with the test piece)
X_TAB = X_BF - GPU_TAB_H
GPU_SLOT_OFF = (12.4, 32.72) # card PCB → bracket screw notches (from photo)

# PSU on its side: 86 thick along X (fan faces the left cover), 150 along Z, 140 along Y
PSU_X0, PSU_Z0 = 8.0, 80.0   # rests on the top of the lower body (joint plane)
PSU_Y0 = D - 140.0
# ATX12V PSDG Fig. 9 rear face holes (x, y from the bottom-left corner seen from the rear);
# on its side: case X = PSU_X0 + y, case Z = PSU_Z0 + 150 - x (socket at the bottom, per the user's PSU)
PSU_HOLES = [(6, 16), (6, 80), (144, 80), (120, 6)]

# vertical posts (x0, x1, y0, y1, z0, z1); the rear-left post ends under the PSU
POSTS = [(0, 12, 0, 12, 0, H), (W - 9, W, 0, 10, 0, H), (0, 7.5, D - 12, D, 0, H)]   # front posts wide for the lid screws
Z_JOINT = 80.0               # body joint: GPU opening (≤ 78.2) below, I/O (≥ 81.4) and PSU above
SPLIT = Z_JOINT              # side cover seam, same height as the body joint
# Removable-part screw standard: screw centre SCREW_IN from the part's visible edge (plate edge, cover seam,
# inner chamfer line on the lid, tab edge) → the Ø6.6 countersunk head ends 2.7 mm before the edge and stays
# clear of the corner radii (R3 panels, R5 body). Mating holes derive from the same constants; check_fasteners
# verifies the insert, the mating hole and the edge margin around the head.
SCREW_IN = 6.0
COVER_IN_Z = 12.0      # side covers, from the top/bottom seams: clears the lid inserts (top) and alignment pegs (joint)
TAB = 12.0             # rear joint tabs TAB × TAB, screw centred (= SCREW_IN to every edge)
# Rear tabs at x 14 and 42: both left of the GPU opening (x ≥ 62) and the bracket tab (x 50.4), on full wall.
# (The old tab at x 108 hung from the 1.8 mm strip above the opening and sat in front of the DP plug.)
JOINT_SCREWS = [("front", 34), ("front", 110), ("rear", 14), ("rear", 42)]  # (wall, x); front screws hide behind the Steam plate
JOINT_FRONT_Z = 95.0   # front joint screw: in the wall band below the plate opening (z ≥ 110), outside the magnet blocks (x 14–24, 148–158)
JOINT_REAR_Y = D + T - 1 + TAB / 2   # rear tab screw (tab sunk 1 mm into the wall, TAB outwards)
PEGS = [(2.5, 7.5, 2.5, 7.5), (1.5, 6, D - 7.5, D - 2.5)]   # alignment pegs on the left posts
_CY = (FIT + SCREW_IN, D - FIT - SCREW_IN)                  # cover screw y: SCREW_IN from the front/rear seam
LOWER_SCREWS = [(y, z) for y in _CY for z in (FIT + COVER_IN_Z, SPLIT - FIT / 2 - COVER_IN_Z)]
UPPER_SCREWS = [(y, z) for y in _CY for z in (SPLIT + FIT / 2 + COVER_IN_Z, H - FIT - COVER_IN_Z)]
LID_IN = EDGE + SCREW_IN                                     # from the outer edge: chamfer + standard margin
LID_SCREWS = [(-T + LID_IN, -T + LID_IN), (W + T - LID_IN, -T + LID_IN), (105, D + T - LID_IN)]   # front posts, rear boss
# 2.5" SSD lying on the inside of the lower side cover (x 1.5–8.5, the strip in front of the GPU); SFF-8201 bottom holes:
# 14 and 90.6 mm from the connector end, ±30.86 from the centre line. 4 countersunk M3 through the cover, 1.5 mm spacers.
SSD_Y0, SSD_Z0 = 45.0, 5.0
SSD_HOLES = [(SSD_Y0 + dy, SSD_Z0 + 34.925 + dz) for dy in (14, 90.6) for dz in (-30.86, 30.86)]
FEET = [(12, 12), (W - 9, 12), (12, D - 12), (W - 9, D - 12)]
FOOT_D, FOOT_H = 22.0, 12.0   # printed feet: 12 mm of air under the floor
# PSU support: removable part; two columns (front/rear) from the floor to the joint plane (PSU underside), a rail
# between them at z 6–10, two countersunk M3 through the rail into floor bosses. A 0.8 mm outline on the floor
# marks the column footprints. Change PSU_SUP_COLS for a different PSU depth.
PSU_SUP_X = (PSU_X0 + 2, 34.0)                                  # 2 mm short of the bottom intake fan
PSU_SUP_COLS = [(PSU_Y0 + 2, PSU_Y0 + 10), (D - 6.4, D - FIT)]  # (y0, y1) front and rear column (rear: 1 mm from the foot boss)
PSU_SUP_SCREWS = [PSU_Y0 + 16, D - 16]                          # screw y (x = column centre)
# Swappable panels: outer plate sits in a 1.25 mm recess (flush with the outside), inner step enters the opening,
# 4 countersunk M3 into corner bosses. plate = outer plate bounds, open = wall opening (u0, u1, v0, v1).
# Lower front 156 x 72, upper front = Steam Machine plate 156 x 126.1, control strip 156 x 32 above it.
PANELS = {
    # screwed panels: opening edge ≥ 2·SCREW_IN from the plate edge so the Ø8.6 pad pocket sits centred in a 12 mm band
    "front_lower": dict(plate=(8, 164, 2, 74), open=(22, 150, 14, 62),
                        screws=[(x, z) for x in (8 + SCREW_IN, 164 - SCREW_IN) for z in (2 + SCREW_IN, 74 - SCREW_IN)]),
    # Upper front: interchangeable with the Steam Machine faceplate (Valve's official STEP: 156 x 126.1 x 6.5 mm,
    # 4 K&J SB443-OUT 6.35 x 6.35 x 4.76 block magnets at (±67, ±52.5) from the plate centre, protruding 4 mm
    # from the back). No recess: the plate sits on the outer face of the front wall; the case has magnet pockets there.
    "faceplate": dict(plate=(8, 164, 88, 214.1), open=(30, 142, 110, 192), screws=[],   # opening 6 mm clear of the magnet pockets
                      magnets=[(19, 98.55), (153, 98.55), (19, 203.55), (153, 203.55)]),
    # Control strip above the Steam plate: power in the centre, reset + USB-C left, 2 × USB-A right
    "strip": dict(plate=(8, 164, 218, 250), open=(22, 150, 225, 243),   # screws in the 14 mm bands either side of the opening
                  screws=[(x, z) for x in (8 + SCREW_IN, 164 - SCREW_IN) for z in (218 + SCREW_IN, 250 - SCREW_IN)]),
}
PANEL_R = 3.0                # outer corner radius of the removable panels
MAGNET = (6.35, 4.76)        # SB443-OUT block magnet: edge, thickness
# Power and reset: Cherry MX style switch + keycap on the strip (x, z); keycap 18 mm, pitch 19.05
SWITCHES = [(86.0, 234.0), (40.0, 234.0)]   # power centre, reset left
USB_C = (60.0, 234.0)                       # panel mount USB-C extension: 9.6 x 3.9 opening
USB_A = [(112.0, 234.0), (134.0, 234.0)]    # panel mount USB-A extension: 13.6 x 6.4 opening
# 120 × 25 mm Molex fans: exhaust in the lid (above the PSU), intake in the floor; hole pitch 105
FAN_D, FAN_PITCH, FAN_HOLE, FAN_T = 118.0, 105.0, 4.5, 25.0
FAN_TOP = (102.0, 100.0)     # (x, y) — 2 mm short of the board's component face (x = 164)
FAN_FRONT = (86.0, 164.0)    # (x, z) — optional 3rd fan: the faceplate's 'fan' variant
FAN_BOTTOM = (96.0, 104.0)   # (x, y) — under the GPU fan; 1 mm short of the SATA ports (x ≥ 157)

# Print orientations: body upright, lid upside down (flat face on the bed), lower side cover outer face
# down, upper side cover inner face down (tongue and overlap rest on the bed), PSU support on its side.
PRINT_ORIENT = {"body_lower": None, "body_upper": None, "lid": (V(1, 0, 0), 180), "foot": (V(1, 0, 0), 180),
                "psu_support": (V(0, 1, 0), 90),
                "strip": (V(1, 0, 0), 90), "strip_plain": (V(1, 0, 0), 90),
                "side_lower": (V(0, 1, 0), -90), "side_upper": (V(0, 1, 0), 90)}
# I/O opening 158.75 x 44.45 (+ allowance); bottom edge 2.24 mm below the board's bottom face
IO_X1 = X_BB + 2.24
IO = (IO_X1 - 44.45 - TOL, IO_X1 + TOL, Z_TOP - 156.31 - TOL, Z_TOP + 2.44 + TOL)

def box(x0, x1, y0, y1, z0, z1):
    return Part.makeBox(x1 - x0, y1 - y0, z1 - z0, V(x0, y0, z0))

def cyl(r, h, base, d):
    return Part.makeCylinder(r, h, V(*base), V(*d))

def chamfered_box(x0, x1, y0, y1, z0, z1, c, top=False, bottom=False, r=None):
    # vertical edges filleted with CORNER_R, top/bottom edges optionally chamfered by c
    b = box(x0, x1, y0, y1, z0, z1)
    vert = [e for e in b.Edges if abs(e.Vertexes[0].Point.z - e.Vertexes[1].Point.z) > 1e-6]
    b = b.makeFillet(CORNER_R if r is None else r, vert)
    edges = [e for e in b.Edges
             if (top and abs(e.BoundBox.ZMin - z1) < 1e-6 and abs(e.BoundBox.ZMax - z1) < 1e-6)
             or (bottom and abs(e.BoundBox.ZMin - z0) < 1e-6 and abs(e.BoundBox.ZMax - z0) < 1e-6)]
    return b.makeChamfer(c, edges) if edges else b

def outer_envelope():
    # outer envelope: side covers and panels intersect it to pick up the corner radius
    return chamfered_box(-T, W + T, -T, D + T, -T - 1, H + T_LID + 1, EDGE)

def teardrop_x(y, z, r, x0, x1):
    # boss along X with a 45° underside — prints without support on an upright wall
    c = cyl(r, x1 - x0, (x0, y, z), (1, 0, 0))
    s = Part.makeBox(x1 - x0, r, r, V(x0, y, z))
    s.rotate(V(x0, y, z), V(1, 0, 0), 225)
    return c.fuse(s)

def hex_centers(u0, u1, v0, v1, r, web=2.2, inside=None):
    # grid centred on the area and mirror-symmetric on both axes: odd number of rows, middle row full
    du = r * math.sqrt(3) + web
    dv = du * math.sqrt(3) / 2
    uc, vc = (u0 + u1) / 2, (v0 + v1) / 2
    nu = int((u1 - u0 - r * math.sqrt(3)) // du) + 1
    nv = int((v1 - v0 - 2 * r) // dv) + 1
    nv -= (nv + 1) % 2
    out = []
    for i in range(nv):
        v = vc + (i - (nv - 1) / 2) * dv
        n = nu if (i - (nv - 1) // 2) % 2 == 0 else nu - 1
        for k in range(n):
            u = uc + (k - (n - 1) / 2) * du
            if inside is None or inside(u, v):
                out.append((u, v))
    return out

def hex_cutters(centers, r, to3d, ext):
    # pointed end towards +v: prints without bridges on an upright wall
    out = []
    for u, v in centers:
        pts = [to3d(u + r * math.cos(math.radians(30 + 60 * i)),
                    v + r * math.sin(math.radians(30 + 60 * i))) for i in range(7)]
        out.append(Part.Face(Part.makePolygon(pts)).extrude(ext))
    return out

def cut_all(shape, tools):
    return shape.cut(Part.makeCompound(tools)) if tools else shape

def countersink(x, y, z, d, depth=T):
    # hole + 90° countersink for an M3 flat head (DIN 7991, head Ø6); (x, y, z) on the surface, d points inward
    hole = cyl(M3 / 2, depth + 2, (x - d[0], y - d[1], z - d[2]), d)
    cone = Part.makeCone(3.3, 1.7, 1.6, V(x, y, z) - V(*d) * 0.01, V(*d))
    return [hole, cone]

def breakaway_ribs(x0, x1, y0, y1, z0, z1, t=0.8, gap=0.2):
    # thin vertical ribs so the top edge of a wide opening in an upright wall is not a bridge;
    # 0.2 mm gap at the top (like a support interface), snapped off with pliers after printing
    n = math.ceil((x1 - x0) / MAX_BRIDGE) - 1
    step = (x1 - x0) / (n + 1)
    return [box(x0 + step * i - t / 2, x0 + step * i + t / 2, y0, y1, z0, z1 - gap)
            for i in range(1, n + 1)]

def fan_cut(cu, cv, to3d, ext):
    # fan grille (hex pattern inside a circle) + 4 screw holes; to3d(u, v) gives the point on the surface
    out = hex_cutters(hex_centers(cu - FAN_D / 2, cu + FAN_D / 2, cv - FAN_D / 2, cv + FAN_D / 2, 4.5,
                                  inside=lambda u, v: math.hypot(u - cu, v - cv) < FAN_D / 2 - 2 and
                                  all(math.hypot(u - cu - a * FAN_PITCH / 2, v - cv - b * FAN_PITCH / 2) > 7.5
                                      for a in (-1, 1) for b in (-1, 1))), 4.5, to3d, ext)
    for du, dv in ((-1, -1), (1, -1), (-1, 1), (1, 1)):
        u, v = cu + du * FAN_PITCH / 2, cv + dv * FAN_PITCH / 2
        out.append(Part.makeCylinder(FAN_HOLE / 2, ext.Length, to3d(u, v), ext))
    return out

def insert(x, y, z, d):
    # insert pocket; (x, y, z) on the surface, d points inward
    return cyl((INSERT_D + TOL) / 2, INSERT_L, (x - d[0] * 0.1, y - d[1] * 0.1, z - d[2] * 0.1), d)

# ---------------------------------------------------------------- body
def body():
    # outer shell (chamfered) − inner volume − left cover slot (covers sit between front/rear walls and the floor)
    s = chamfered_box(-T, W + T, -T, D + T, -T, H, EDGE, bottom=True)
    s = s.cut(box(0, W, 0, D, 0, H + 1))
    s = s.cut(box(-T - 1, 0, 0, D, 0, H + 1))
    for p in POSTS:
        s = s.fuse(box(*p))
    for dy, dz in HOLES:                                       # standoff bosses
        s = s.fuse(teardrop_x(Y_R - dy, Z_TOP - dz, 4.5, X_BB, W))
    # GPU bracket tab shelf (outside the rear wall, 45° underside)
    prof = [V(0, D + T, Z_C - 54), V(0, D + T + TAB - 1, Z_C - 55 + TAB), V(0, D + T + TAB - 1, Z_C + 4),
            V(0, D + T, Z_C + 4), V(0, D + T, Z_C - 54)]
    shelf = Part.Face(Part.makePolygon(prof)).extrude(V(10, 0, 0))
    shelf.translate(V(X_TAB, 0, 0))
    s = s.fuse(shelf)
    s = s.fuse(box(100, 110, D - 10, D, H - 8, H))             # lid screw boss (rear)
    gus = [V(0, D, H - 18), V(0, D, H - 8), V(0, D - 10, H - 8), V(0, D, H - 18)]
    s = s.fuse(Part.Face(Part.makePolygon(gus)).extrude(V(10, 0, 0)).translated(V(100, 0, 0)))
    for y in PSU_SUP_SCREWS:                                   # PSU support: insert bosses on the floor
        s = s.fuse(cyl(5, 6, (PSU_SUP_X[0] + 12, y, 0), (0, 0, 1)))
    for y0, y1 in PSU_SUP_COLS:                                # and a 0.8 mm outline marking its footprint
        x0, x1 = PSU_SUP_X
        rim = box(x0 - FIT - 1.2, x1 + FIT + 1.2, y0 - FIT - 1.2, y1 + FIT + 1.2, 0, 0.8)
        s = s.fuse(rim.cut(box(x0 - FIT, x1 + FIT, y0 - FIT, y1 + FIT, -1, 1)))
    for x, y in FEET:                                          # foot screw bosses (inside)
        s = s.fuse(cyl(5, 6, (x, y, 0), (0, 0, 1)))
    for key in PANELS:                                         # front panel bosses (inside of the front wall)
        for x, z in PANELS[key]["screws"]:
            s = s.fuse(cyl(4.5, 7.5, (x, 0, z), (0, 1, 0)))
        for x, z in PANELS[key].get("magnets", []):            # magnet blocks (inside of the front wall)
            s = s.fuse(box(x - 5, x + 5, 0, 7.5, z - 5, z + 5))

    cuts = []
    for dy, dz in HOLES:
        cuts.append(insert(X_BB, Y_R - dy, Z_TOP - dz, (1, 0, 0)))
    io = IO
    cuts.append(box(io[0], io[1], D - 1, D + T + 1, io[2], io[3]))
    # 1.2 mm wall around the opening for the I/O shield springs (pocket from outside)
    # no thinning at the bottom edge: the 3.2 mm strip to the GPU opening stays full thickness
    cuts.append(box(io[0] - 2.5, io[1] + 2.5, D + 1.2, D + T + 1, io[2], io[3] + 2.5))
    # GPU opening + slot for the bracket tab + screw pockets
    cuts.append(box(X_TAB + 10.5, W - 2, D - 1, D + T + 1, Z_C - 44, Z_C + 4))
    cuts.append(box(X_TAB - 2.2, X_TAB, D - 1, D + T + 1, Z_C - 44, Z_C + 4))
    for off in GPU_SLOT_OFF:
        cuts.append(insert(X_TAB, D + T + 5, Z_C - off, (1, 0, 0)))
    # PSU: screws, grille, socket/switch (standard layout; update from a photo of the PSU)
    for hx, hy in PSU_HOLES:
        cuts.append(cyl(UNC632 / 2, T + 2, (PSU_X0 + hy, D - 1, PSU_Z0 + 150 - hx), (0, 1, 0)))
    cuts += hex_cutters(hex_centers(PSU_X0 + 10, PSU_X0 + 76, PSU_Z0 + 52, PSU_Z0 + 138, 4.5),
                        4.5, lambda u, v: V(u, D - 1, v), V(0, T + 2, 0))
    cuts.append(box(PSU_X0 + 26, PSU_X0 + 76, D - 1, D + T + 1, PSU_Z0 + 6, PSU_Z0 + 36))    # socket (centre) + switch (left of it)
    # cover inserts: vertical for the lid, horizontal for the side covers
    for x, y in LID_SCREWS:
        cuts.append(insert(x, y, H, (0, 0, -1)))
    for y, z in LOWER_SCREWS + UPPER_SCREWS:
        cuts.append(insert(0, y, z, (1, 0, 0)))
    for x, y in FEET:                                          # foot inserts, from below
        cuts.append(insert(x, y, -T, (0, 0, 1)))
    for y in PSU_SUP_SCREWS:                                   # PSU support inserts, from above
        cuts.append(insert(PSU_SUP_X[0] + 12, y, 6, (0, 0, -1)))
    for key in PANELS:                                         # front panel openings, recesses, inserts
        pl, op = PANELS[key]["plate"], PANELS[key]["open"]
        cuts.append(box(op[0], op[1], -T - 1, 0.5, op[2], op[3]))
        if PANELS[key]["screws"]:
            g = box(pl[0], pl[1], -T - 1, -T + 1.25, pl[2], pl[3])
            cuts.append(g.makeFillet(PANEL_R, [e for e in g.Edges if abs(e.Vertexes[0].Point.y - e.Vertexes[1].Point.y) > 1e-6]))
        for x, z in PANELS[key]["screws"]:
            cuts.append(cyl(4.3, 2.0, (x, -T + 1.25 - 0.01, z), (0, 1, 0)))   # panel pad pocket
            cuts.append(insert(x, 0.75, z, (0, 1, 0)))
        # magnet pocket: the plate's magnet enters 4 mm (Y -T..1.5), the case magnet sits behind it (Y 1.5..6.26)
        for x, z in PANELS[key].get("magnets", []):
            h = MAGNET[0] / 2 + 0.15
            cuts.append(box(x - h, x + h, -T - 1, 1.5 + MAGNET[1], z - h, z + h))
    # ventilation: floor (under the GPU fan) and the CPU backplate area of the tray (right outer face)
    cuts += fan_cut(FAN_BOTTOM[0], FAN_BOTTOM[1], lambda u, v: V(u, v, -T - 1), V(0, 0, T + 2))   # bottom intake fan
    cuts += hex_cutters(hex_centers(CPU_Y - 40, CPU_Y + 40, CPU_Z - 40, CPU_Z + 40, 4.5),
                        4.5, lambda u, v: V(W - 1, u, v), V(T + 2, 0, 0))
    s = cut_all(s, cuts)
    # breakaway supports: top edges of the I/O, GPU and socket openings
    ribs = breakaway_ribs(io[0], io[1], D, D + 1.2, io[2], io[3])
    ribs += breakaway_ribs(X_TAB + 10.5, W - 2, D, D + T, Z_C - 44, Z_C + 4)
    ribs += breakaway_ribs(PSU_X0 + 26, PSU_X0 + 76, D, D + T, PSU_Z0 + 6, PSU_Z0 + 36)
    for key in PANELS:
        op = PANELS[key]["open"]
        y0 = -T + 1.25 if PANELS[key]["screws"] else -T   # no recess (Steam plate): ribs span the full wall
        ribs += breakaway_ribs(op[0], op[1], y0, 0, op[2], op[3])
    global RIBS
    RIBS = Part.makeCompound(ribs)   # ignored by the clash check (snapped off after printing)
    for r in ribs:
        s = s.fuse(r)
    return s

# ---------------------------------------------------------------- body joint
# Lower body up to Z_JOINT; a 2 mm lip on its inner face (front, right) and pegs on the left posts align the
# upper body. Front: 2 horizontal countersunk M3 from outside into blocks inside the lower body. Rear: the inside
# is full of GPU/PSU, so 12 mm tabs outside; vertical screw from the upper tab into the lower one.
# Both halves print upright.
def split_body(full):
    zj = Z_JOINT
    lower = full.common(box(-T - 1, W + T + 1, -T - 1, D + T + 12, -T - 1, zj))
    upper = full.common(box(-T - 1, W + T + 1, -T - 1, D + T + 12, zj, H + 1))
    def lip(x0, x1, y0, y1, dx, dy):
        # (dx, dy): direction towards the wall; above the joint the lip is FIT inside the wall
        a = box(x0, x1, y0, y1, zj - 4, zj)
        b = box(x0 - dx * FIT if dx > 0 else x0, x1 - dx * FIT if dx < 0 else x1,
                y0 - dy * FIT if dy > 0 else y0, y1 - dy * FIT if dy < 0 else y1, zj - 0.01, zj + 6)
        return a.fuse(b)
    add = [lip(12 + FIT, W - 9 - FIT, 0, 2, 0, -1),                    # front
           lip(W - 2, W, 10 + FIT, D - FIT, 1, 0)]                      # right (behind the board)
    cuts_lower, cuts_upper = [], []
    for wall, x in JOINT_SCREWS:
        if wall == "front":
            add.append(box(x - 4, x + 4, 0, 8, zj - 10, zj).fuse(box(x - 4, x + 4, FIT, 8, zj - 0.01, JOINT_FRONT_Z + 5)))
            cuts_lower.append(insert(x, FIT, JOINT_FRONT_Z, (0, 1, 0)))
            cuts_upper += countersink(x, -T, JOINT_FRONT_Z, (0, 1, 0))
        else:
            # lower tab TAB × TAB with a 45° underside (no support); upper tab 6 mm (below the PSU socket opening, z ≥ 86), M3 × 12
            h, y0, y1 = TAB / 2, D + T - 1, D + T - 1 + TAB
            prof = [V(x - h, y0, zj - 2 * TAB), V(x - h, y1, zj - TAB), V(x - h, y1, zj), V(x - h, y0, zj), V(x - h, y0, zj - 2 * TAB)]
            add.append(Part.Face(Part.makePolygon(prof)).extrude(V(TAB, 0, 0)))
            cuts_lower.append(insert(x, JOINT_REAR_Y, zj, (0, 0, -1)))
            upper = upper.fuse(box(x - h, x + h, y0, y1, zj, zj + 6))
            cuts_upper += countersink(x, JOINT_REAR_Y, zj + 6, (0, 0, -1), depth=6)
    for x0, x1, y0, y1 in PEGS:
        add.append(box(x0, x1, y0, y1, zj - 1, zj + 4))
        cuts_upper.append(box(x0 - FIT, x1 + FIT, y0 - FIT, y1 + FIT, zj - 1, zj + 4 + FIT))
    for a in add:
        lower = lower.fuse(a)
    return cut_all(lower, cuts_lower), cut_all(upper, cuts_upper)

# ---------------------------------------------------------------- lid
def lid():
    s = chamfered_box(-T, W + T, -T, D + T, H, H + T_LID, EDGE, top=True)
    # inner rim: sits inside the walls with FIT clearance, locates the lid
    rim = [box(12 + FIT, W - 9 - FIT, FIT, FIT + 2, H - 4, H),           # front
           box(W - FIT - 2, W - FIT, 10 + FIT, D - FIT, H - 4, H),        # right
           box(7.5 + FIT, 100 - FIT, D - FIT - 2, D - FIT, H - 4, H)]     # rear (post → I/O shield)
    for r in rim:
        s = s.fuse(r)
    cuts = []
    for x, y in LID_SCREWS:
        cuts += countersink(x, y, H + T_LID, (0, 0, -1), depth=T_LID)
    # groove for the upper side cover's tongue
    cuts.append(box(-1.0 - FIT, FIT, FIT, D - FIT, H - 0.1, H + 1.5))   # tongue groove; 0.8 outer strip, 0.8 bridge above
    cuts += fan_cut(FAN_TOP[0], FAN_TOP[1], lambda u, v: V(u, v, H - 5), V(0, 0, T_LID + 6))
    return cut_all(s, cuts)

# ---------------------------------------------------------------- side covers
# Each side cover closes its own body half; the seam is flush with the body joint (Z_JOINT), plain butt joint.
# The tongue on the upper cover's top edge enters the groove in the lid, so the cover cannot swing out.
def lower_cover():
    s = box(-T, 0, FIT, D - FIT, FIT, SPLIT - FIT / 2).common(outer_envelope())
    cuts = []
    for y, z in SSD_HOLES:                                     # SSD spacers (inner face)
        s = s.fuse(cyl(4, 1.5, (0, y, z), (1, 0, 0)))
    for y, z in LOWER_SCREWS + SSD_HOLES:
        cuts += countersink(-T, y, z, (1, 0, 0), depth=T + 2)
    return cut_all(s, cuts)

def upper_cover():
    s = box(-T, 0, FIT, D - FIT, SPLIT + FIT / 2, H - FIT).common(outer_envelope())
    s = s.fuse(box(-1.0, 0, FIT + 1, D - FIT - 1, H - FIT, H + 1.3))               # top tongue
    cuts = []
    for y, z in UPPER_SCREWS:
        cuts += countersink(-T, y, z, (1, 0, 0))
    cy, cz = PSU_Y0 + 70, PSU_Z0 + 75      # PSU fan (centre of its underside)
    cuts += hex_cutters(hex_centers(cy - 60, cy + 60, cz - 60, cz + 60, 4.5,
                                    inside=lambda u, v: math.hypot(u - cy, v - cz) < 56),
                        4.5, lambda u, v: V(-T - 1, u, v), V(T + 2, 0, 0))
    return cut_all(s, cuts)

# ---------------------------------------------------------------- foot (print 4)
def foot():
    # Ø22 × 12 cylinder, Ø7 × 8 pocket from below; M3 × 8 pan head into the floor insert.
    # Flat face (top) goes on the bed; in assembly coordinates it sits under the floor at the first foot position.
    x, y = FEET[0]
    s = cyl(FOOT_D / 2, FOOT_H, (x, y, -T - FOOT_H), (0, 0, 1))
    s = s.makeChamfer(1.0, [e for e in s.Edges if abs(e.BoundBox.ZMin - (-T - FOOT_H)) < 1e-6])
    s = s.cut(cyl(3.5, 8, (x, y, -T - FOOT_H - 0.01), (0, 0, 1)))
    s = s.cut(cyl(M3 / 2, FOOT_H + 1, (x, y, -T - FOOT_H - 0.5), (0, 0, 1)))
    return s

# ---------------------------------------------------------------- PSU support
def psu_support():
    x0, x1 = PSU_SUP_X
    xm = x0 + 12
    s = None
    for y0, y1 in PSU_SUP_COLS:
        c = box(x0, x1, y0, y1, 0, PSU_Z0)
        s = c if s is None else s.fuse(c)
    s = s.fuse(box(x0, x1, PSU_SUP_COLS[0][0], PSU_SUP_COLS[-1][1], 6, 10))   # rail, rests on the bosses
    cuts = []
    for y in PSU_SUP_SCREWS:
        cuts += countersink(xm, y, 10, (0, 0, -1), depth=4)
    return cut_all(s, cuts)

# ---------------------------------------------------------------- front panels
def front_panel(key, kind="mesh"):
    sp = PANELS[key]
    x0, x1, z0, z1 = sp["plate"]
    o = sp["open"]
    cuts = []
    def rbox(a0, a1, y0, y1, b0, b1, r):   # plate in the XZ plane with corners rounded by r
        bx = box(a0, a1, y0, y1, b0, b1)
        return bx.makeFillet(r, [e for e in bx.Edges if abs(e.Vertexes[0].Point.y - e.Vertexes[1].Point.y) > 1e-6])
    if sp.get("magnets"):
        # Steam Machine type: 6.5 mm plate sits on the outer face of the wall (Y -T-6.5..-T); 4 magnets on its back
        # protrude 4 mm (pocket 0.8 deep, magnet glued in)
        s = rbox(x0, x1, -T - 6.5, -T, z0, z1, PANEL_R)
        for x, z in sp["magnets"]:
            h = MAGNET[0] / 2 + 0.1
            cuts.append(box(x - h, x + h, -T - 0.8, -T + 1, z - h, z + h))
        yf = -T - 6.5   # outer face
    else:
        # screwed panels: outer plate Y -T..-T+1.25 (in the recess), inner step Y -T+1.25..0 (in the opening)
        s = rbox(x0 + FIT / 2, x1 - FIT / 2, -T, -T + 1.25, z0 + FIT / 2, z1 - FIT / 2, PANEL_R)
        s = s.fuse(box(o[0] + FIT / 2, o[1] - FIT / 2, -T + 1.25 - 0.01, 0, o[2] + FIT / 2, o[3] - FIT / 2))
        yf = -T
        for x, z in sp["screws"]:
            s = s.fuse(cyl(4, 2.0 - FIT / 2, (x, -T + 1.25 - 0.01, z), (0, 1, 0)))
            cuts += countersink(x, -T, z, (0, 1, 0), depth=4)
    cx, cz = (o[0] + o[1]) / 2, (o[2] + o[3]) / 2
    if kind == "mesh":
        cuts += hex_cutters(hex_centers(o[0] + 3, o[1] - 3, o[2] + 3, o[3] - 3, 4.0),
                            4.0, lambda u, v: V(u, yf - 1, v), V(0, 10, 0))
    elif kind == "screen":   # window 75 x 46 for a 3.5" IPS module (480x320)
        cuts.append(box(cx - 37.5, cx + 37.5, yf - 1, 1, cz - 23, cz + 23))
    elif kind == "fan":      # 120 mm fan: grille + 4 screw holes (fan screwed to the panel from inside)
        cuts += fan_cut(cx, cz, lambda u, v: V(u, yf - 1, v), V(0, 10, 0))
    elif kind == "controls": # control strip: 2 Cherry MX (14 x 14, 1.5 mm plate around), USB-C, 2 x USB-A
        for x, z in SWITCHES:
            cuts.append(box(x - 7.05, x + 7.05, yf - 1, 1, z - 7.05, z + 7.05))
            cuts.append(box(x - 10, x + 10, yf + 1.5, 1, z - 10, z + 10))
        cuts.append(box(USB_C[0] - 4.8, USB_C[0] + 4.8, yf - 1, 1, USB_C[1] - 1.95, USB_C[1] + 1.95))
        for x, z in USB_A:
            cuts.append(box(x - 6.8, x + 6.8, yf - 1, 1, z - 3.2, z + 3.2))
    return cut_all(s, cuts)

# ---------------------------------------------------------------- reference hardware (not printed)
def fan(cx, cy, cz, axis, size, depth, blades=7, split=False):
    # axial fan: frame − air hole + hub + blades; axis = (1,0,0)/(0,1,0)/(0,0,1) unit direction
    ax = V(*axis)
    c = V(cx, cy, cz)
    base = c - ax * (depth / 2)
    r = size / 2 - 1.5
    # build the frame relative to the axis: square prism along the axis
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
    # Hardware that is not printed; dimensions from the ATX/PCIe standards and product specs (approximate).
    pcb = box(X_BF, X_BB, Y_R - 185, Y_R, Z_B, Z_TOP)
    # I/O port block: inside the opening, 0.5 mm short of the wall
    board = pcb.fuse(box(X_BF - 14, X_BF, Y_R - 18, D - 0.5, IO[2] + 3, IO[3] - 6))
    board = board.fuse(box(X_BF - 16, X_BF, Y_R - 18, D - 0.5, IO[2] + 3, IO[2] + 17))    # PS/2 + USB
    board = board.fuse(box(X_BF - 8, X_BF, CPU_Y - 18.75, CPU_Y + 18.75, CPU_Z - 18.75, CPU_Z + 18.75))  # socket + CPU
    board = board.fuse(box(X_BF - 11, X_BF, Y_R - 99, Y_R - 10, Z_C - 4.5, Z_C + 3))           # PCIEX16
    board = board.fuse(box(X_BF - 11, X_BF, Y_R - 35, Y_R - 10, Z_C - 40.64 - 4, Z_C - 40.64 + 3))  # PCIEX1
    for dz in (58, 68.2):                                                                      # 2 × DIMM
        board = board.fuse(box(X_BF - 7, X_BF, Y_R - 168, Y_R - 35, CPU_Z - dz - 3, CPU_Z - dz + 3))
    board = board.fuse(box(X_BF - 9, X_BF, Y_R - 180, Y_R - 168, CPU_Z - 60, CPU_Z - 8))      # 24 pin
    board = board.fuse(box(X_BF - 8, X_BF, Y_R - 60, Y_R - 30, Z_TOP - 190, Z_TOP - 160))     # chipset
    for i in range(4):                                                                         # SATA
        board = board.fuse(box(X_BF - 7, X_BF, Y_R - 150 + i * 13, Y_R - 141 + i * 13, Z_B, Z_B + 16))
    # GPU: PCB + cooler shroud + fan; bracket plate + protruding tab + ports
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
        bracket = bracket.fuse(box(x0, x1, D - 1.2, D - 0.2, Z_C - 15, Z_C - 9))   # 0.2 short of the wall (ribs)
    # cooler: fin stack (24 plates along Y) + 4 heat pipes + 90 mm fan
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
    # PSU: housing + fan (left face) + socket/switch (rear) + cable bundle (front)
    psu = box(PSU_X0, PSU_X0 + 86, PSU_Y0, D, PSU_Z0, PSU_Z0 + 150)
    psu = psu.cut(Part.makeCylinder(58, 3, V(PSU_X0 - 1, PSU_Y0 + 70, PSU_Z0 + 75), V(1, 0, 0)))
    pf, psu_rotor = fan(PSU_X0 + 8, PSU_Y0 + 70, PSU_Z0 + 75, (1, 0, 0), 120, 15, split=True)
    psu = psu.fuse(pf)
    psu = psu.cut(box(PSU_X0 + 26, PSU_X0 + 76, D - 1, D + 1, PSU_Z0 + 6, PSU_Z0 + 36))
    psu = psu.fuse(box(PSU_X0 + 29, PSU_X0 + 57, D - 6, D - 1, PSU_Z0 + 10, PSU_Z0 + 32))     # C14 inlet, bottom centre
    psu = psu.fuse(box(PSU_X0 + 61, PSU_X0 + 73, D - 6, D - 1, PSU_Z0 + 12, PSU_Z0 + 30))    # switch, left of it
    psu = psu.fuse(Part.makeCylinder(12, 30, V(PSU_X0 + 43, PSU_Y0, PSU_Z0 + 22), V(0, -1, 0)))   # cables, front bottom
    ssd = box(1.5, 8.5, SSD_Y0, SSD_Y0 + 100, SSD_Z0, SSD_Z0 + 69.85)
    o = PANELS["front_lower"]["open"]; cx, cz = (o[0] + o[1]) / 2, (o[2] + o[3]) / 2
    lcd = box(cx - 42.5, cx + 42.5, 0, 5, cz - 27.5, cz + 27.5)        # 3.5" IPS module 85 x 55 x 5 behind the panel
    case_fan, top_rotor = fan(FAN_TOP[0], FAN_TOP[1], H - FAN_T / 2, (0, 0, 1), FAN_D + 2, FAN_T, split=True)     # top, exhaust
    bot_fan, bot_rotor = fan(FAN_BOTTOM[0], FAN_BOTTOM[1], FAN_T / 2, (0, 0, 1), FAN_D + 2, FAN_T, split=True)   # bottom, intake
    return dict(ref_board=(board, (0.1, 0.45, 0.2)), ref_gpu=(gpu, (0.15, 0.3, 0.75)),
                ref_bracket=(bracket, (0.75, 0.75, 0.75)), ref_cooler=(cooler, (0.3, 0.3, 0.3)),
                ref_psu=(psu, (0.2, 0.2, 0.2)), ref_ssd=(ssd, (0.6, 0.2, 0.2)),
                ref_fan_top=(case_fan, (0.25, 0.25, 0.3)), ref_fan_bottom=(bot_fan, (0.25, 0.25, 0.3)),
                rotor_top=(top_rotor, (0.45, 0.45, 0.5)), rotor_bottom=(bot_rotor, (0.45, 0.45, 0.5)),
                rotor_cpu=(cpu_rotor, (0.45, 0.45, 0.5)), rotor_gpu=(gpu_rotor, (0.45, 0.45, 0.5)),
                rotor_psu=(psu_rotor, (0.45, 0.45, 0.5)), ref_lcd=(lcd, (0.1, 0.1, 0.12)))

PRINTED = ("body_lower", "body_upper", "lid", "side_lower", "side_upper", "foot", "psu_support", "front_lower", "faceplate", "strip")

def build(doc_name="MiniPCCase"):
    doc = App.getDocument(doc_name) if doc_name in App.listDocuments() else App.newDocument(doc_name)
    for o in list(doc.Objects):
        doc.removeObject(o.Name)
    global FULL
    FULL = body()
    lower, upper = split_body(FULL)
    parts = dict(body_lower=(lower, (0.82, 0.82, 0.85)),
                 body_upper=(upper, (0.7, 0.72, 0.78)),
                 lid=(lid(), (0.55, 0.57, 0.62)),
                 side_lower=(lower_cover(), (0.9, 0.6, 0.3)),
                 side_upper=(upper_cover(), (0.9, 0.6, 0.3)),
                 foot=(foot(), (0.5, 0.5, 0.55)),
                 psu_support=(psu_support(), (0.5, 0.5, 0.55)),
                 front_lower=(front_panel("front_lower", "screen"), (0.15, 0.15, 0.17)),   # 3.5" LCD window
                 faceplate=(front_panel("faceplate", "plain"), (0.45, 0.25, 0.12)),        # plain: wood veneer / paint
                 strip=(front_panel("strip", "controls"), (0.2, 0.2, 0.22)))
    parts.update(references())
    for name, (shape, color) in parts.items():
        o = doc.addObject("Part::Feature", name)
        o.Shape = shape
        if App.GuiUp:
            o.ViewObject.ShapeColor = color
            if name.startswith("side"):
                o.ViewObject.Transparency = 60
    doc.recompute()
    for name in PRINTED:
        sh = doc.getObject(name).Shape
        bb = sh.BoundBox
        print(f"{name}: {bb.XLength:.1f} x {bb.YLength:.1f} x {bb.ZLength:.1f} mm, "
              f"{sh.Volume / 1000:.0f} cm3, valid={sh.isValid()}, solids={len(sh.Solids)}")
    # clash check: printed parts must not touch each other or the hardware
    names = list(PRINTED) + [n for n in parts if n.startswith("ref_")]   # rotors sit inside the fan frames, skipped
    clash = []
    for i, a in enumerate(names):
        for b in names[i + 1:]:
            if a.startswith("ref_") and b.startswith("ref_") and not (a.startswith("ref_fan") or b.startswith("ref_fan")):
                continue   # hardware-hardware clashes are only checked for the case fans
            sa = doc.getObject(a).Shape
            if a.startswith("body"):
                sa = sa.cut(RIBS)
            v = sa.common(doc.getObject(b).Shape).Volume
            if v > 0.5:
                clash.append((a, b, round(v)))
    print("clashes:", clash or "none")
    return doc

def test_piece(doc):
    # rear-right corner: GPU opening + bracket shelf, lower part of the I/O opening, B/C standoffs.
    # Mount the board with 2 screws to try the I/O shield and the GPU bracket.
    return FULL.common(box(X_TAB - 5, W + T, D - 22, D + T + 11, -T, 130))

def export_stl(out_dir="/Users/cobanov/Developer/mini-pc-case/stl", doc_name="MiniPCCase"):
    import os
    import MeshPart
    os.makedirs(out_dir, exist_ok=True)
    doc = App.getDocument(doc_name)
    shapes = {n: doc.getObject(n).Shape for n in PRINTED}
    shapes["test_piece"] = test_piece(doc)
    for key, kinds in (("front_lower", ("plain", "mesh")), ("faceplate", ("mesh", "screen")), ("strip", ("plain",))):
        for k in kinds:
            shapes[f"{key}_{k}"] = front_panel(key, k)
    for n, sh in shapes.items():
        sh.exportStep(os.path.join(out_dir, f"{n}.step"))      # STEP in assembly coordinates
        rot = PRINT_ORIENT.get(n, (V(1, 0, 0), 90) if n.startswith(("front_lower", "faceplate")) else None)   # STL in print orientation
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
              f"{sh.Volume / 1000:.0f} cm3, watertight={m.isSolid()}")

def check_fasteners(doc_name="MiniPCCase"):
    # For every screw: is the insert pocket empty in the receiving part with solid material around it at full depth,
    # is the mating hole empty with solid material around it, and does the head have SCREW_IN-3.8 mm of edge margin.
    # (p = surface point, d = inward direction) Catches clipped or unmatched holes.
    doc = App.getDocument(doc_name)
    sh = {o.Name: o.Shape for o in doc.Objects}
    def probe(name, pt):
        return sh[name].isInside(V(*pt), 0.01, True)
    def ring(p, d, depth, r):
        d = V(*d); u = V(0, 0, 1).cross(d) if abs(d.z) < 0.9 else V(1, 0, 0); w = d.cross(u)
        c = V(*p) + d * depth
        return [c + u * r, c - u * r, c + w * r, c - w * r]
    F = []   # (name, insert part, screw part, surface point, direction, distance to the screw part's outer face)
    for x, y in LID_SCREWS: F.append(("lid", "body_upper", "lid", (x, y, H), (0, 0, -1), T_LID))
    for y, z in LOWER_SCREWS: F.append(("lower side cover", "body_lower", "side_lower", (0, y, z), (1, 0, 0), T))
    for y, z in UPPER_SCREWS: F.append(("upper side cover", "body_upper", "side_upper", (0, y, z), (1, 0, 0), T))
    for wall, x in JOINT_SCREWS:
        if wall == "front": F.append(("body joint front", "body_lower", "body_upper", (x, FIT, JOINT_FRONT_Z), (0, 1, 0), T + FIT))
        else: F.append(("body joint rear", "body_lower", "body_upper", (x, JOINT_REAR_Y, Z_JOINT), (0, 0, -1), 6))
    for x, z in PANELS["front_lower"]["screws"]: F.append(("lower front panel", "body_lower", "front_lower", (x, 0.75, z), (0, 1, 0), T + 0.75))
    for x, z in PANELS["strip"]["screws"]: F.append(("control strip", "body_upper", "strip", (x, 0.75, z), (0, 1, 0), T + 0.75))
    for y in PSU_SUP_SCREWS: F.append(("PSU support", "body_lower", "psu_support", (PSU_SUP_X[0] + 12, y, 6), (0, 0, -1), 4))
    for x, y in FEET: F.append(("foot", "body_lower", None, (x, y, -T), (0, 0, 1), 0))
    for dy, dz in HOLES:
        z = Z_TOP - dz
        F.append(("motherboard", "body_upper" if z > Z_JOINT else "body_lower", None, (X_BB, Y_R - dy, z), (1, 0, 0), 0))
    for off in GPU_SLOT_OFF: F.append(("GPU bracket", "body_lower", None, (X_TAB, D + T + 5, Z_C - off), (1, 0, 0), 0))
    bad = 0
    for name, ins, scr, p, d, t_out in F:
        probs = []
        c1 = V(*p) + V(*d) * 2
        if probe(ins, c1): probs.append("insert pocket blocked")
        for q in ring(p, d, 2, 3.4) + ring(p, d, 5.5, 3.4):
            if not probe(ins, q): probs.append("material around insert missing (clipped)"); break
        if scr:
            c2 = V(*p) - V(*d) * 1.2
            if probe(scr, c2): probs.append("no mating hole")
            for q in ring(p, d, -1.9, 3.0):
                if not probe(scr, q): probs.append("mating hole on a part edge"); break
            for q in ring(p, d, -(t_out - 0.6), SCREW_IN - 0.5):   # just under the outer face, around the head: ≥ 2.2 mm to any edge
                if not probe(scr, q): probs.append(f"edge margin around head < {SCREW_IN - 3.8:.1f} mm"); break
        if probs:
            bad += 1
            print(f"  ✗ {name} @ ({p[0]:.1f},{p[1]:.1f},{p[2]:.1f}): {', '.join(sorted(set(probs)))}")
    print(f"fastener audit: {len(F)} screws, {bad} with problems" if bad else f"fastener audit: {len(F)} screws, all OK")

def check_print(doc_name="MiniPCCase", step=0.25):
    # Scans, in print orientation, the underside of every downward-facing (within 45°) flat face that is not on
    # the bed, along its long axis. A point is supported if there is material below the face's centre line or just
    # outside its long edges (overhang from an edge / rib). The longest unsupported run = unsupported bridge
    # length; anything over MAX_BRIDGE is listed.
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
                bad.append(dict(length=round(longest), z=round(z - bed), x=round(c.x), y=round(c.y)))
        print(f"{n}: {'no long bridges or overhangs' if not bad else bad}")

build()
