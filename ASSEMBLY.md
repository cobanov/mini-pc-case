# Mini PC case — assembly and bill of materials

Model: `build_case.py` (v4). Outer size 176 × 204 × 265 mm (with lid; feet +12, rear GPU shelf and joint
tabs +11 mm), ~9.7 L. Body split in two at Z = 80 mm; tallest part 178 mm.

## Parts

| File | What | Height (as printed) |
|---|---|---|
| `body_lower` | floor + bottom intake fan, GPU opening + bracket shelf, B/R and C/H standoffs, foot and PSU-support bosses, lower front panel frame | 102 mm |
| `body_upper` | I/O opening, F/J standoffs, PSU screws/grille/socket, control strip frame, Steam plate magnet pockets, CPU backplate grille | 178 mm |
| `lid` | top cover, exhaust fan grille | 7 mm |
| `foot` × 4 | Ø22 × 12 mm, M3 into the floor | 12 mm |
| `psu_support` | removable PSU support: two columns + rail, 2 × M3 into floor bosses; the floor carries a 0.8 mm outline of its footprint | 24 mm (on its side) |
| `front_lower` (+ `_plain`, `_mesh`) | lower front panel 156 × 72: default 3.5" LCD window 75 × 46 (module 85 × 55 × 5 behind it), plain, mesh | 3 mm |
| `faceplate` (+ `_mesh`, `_screen`) | **Steam Machine faceplate** 156 × 126.1 × 6.5 with 4 magnets: default plain (for veneer/paint), mesh, screen. Valve's and third-party plates fit too | 6.5 mm |
| `strip` (+ `_plain`) | control strip 156 × 32 above the Steam plate: MX power in the centre, MX reset + USB-C left, 2 × USB-A right (panel-mount extensions) | 3 mm |
| `side_lower`, `side_upper` | left side covers; the lower one is closed and carries the SSD bed on its inside (4 screws, 1.5 mm spacers) | 2.2 mm |
| `test_piece` | rear-right corner: I/O opening, GPU opening + shelf, two standoffs | 133 mm |

## Fasteners

All M3, one insert type: Ø4.3 × 6 mm pocket, M3 × 5 × 4.5 brass heat-set insert.

| Where | Inserts | Screw |
|---|---|---|
| Motherboard (6) | 6 | M3 × 6 pan head (DIN 7985) |
| GPU bracket (rear shelf) | 2 | M3 × 6 pan head |
| Body joint, front (2): horizontal from outside, into blocks inside the lower body | 2 | M3 × 8 countersunk (DIN 7991) |
| Body joint, rear (2): vertical through the upper tab into the lower tab | 2 | M3 × 12 countersunk |
| Lid (3) | 3 | M3 × 10 countersunk |
| Side covers (lower 4, upper 4) | 8 | M3 × 8 countersunk |
| Feet (4), from below | 4 | M3 × 8 pan head |
| PSU support (2), from above through the rail | 2 | M3 × 8 countersunk |
| SSD, through the lower side cover into the SSD's bottom threads (4) | — | M3 × 6 countersunk |
| Panels: lower front 4, control strip 4 | 8 | M3 × 8 countersunk (plate 3.25 mm with pad) |
| Steam plate | — | 8 × K&J SB443-OUT (6.35 × 6.35 × 4.76 blocks; 4 in the case, 4 in the plate, glued) |
| PSU (4) | — | 6-32 UNC × 6 (comes with the PSU) |
| **Total** | **37 inserts** | M3×6: 8 · M3×8 pan: 4 · M3×8 countersunk: 22 · M3×10 countersunk: 3 · M3×12 countersunk: 2 |

### Screw placement standard (removable parts)

Every screw on a removable part sits **6 mm from the part's visible edge** (plate edge, cover seam, the lid's inner
chamfer line, tab edge): the Ø6.6 countersunk head ends 2.7 mm before the edge and stays clear of the corner radii
(R3 on panels, R5 on the body). On the side covers the top/bottom screws sit 12 mm from the seams so they clear the
lid inserts and the alignment pegs. The mating inserts are generated from the same constants, and `check_fasteners()`
probes every screw: insert pocket free and surrounded by material, mating hole present and not on an edge, and
≥ 2.2 mm of material around the head.

Other: 2 Cherry MX style mechanical switches + keycaps for power and reset (on the control strip; 14 × 14 plate
cutout, 1.5 mm plate; 2 wires soldered to the switch legs go to F_PANEL PWR/RESET); panel-mount USB-C and 2 × USB-A
extensions (cutouts 9.6 × 3.9 and 13.6 × 6.4; drill the flange holes to match your product) to the board's USB headers.
2 × 120 × 25 mm Molex fans (intake in the floor, exhaust in the lid: chimney layout; the fans' own screws, Ø4.5 holes,
105 mm pitch). Molex means no motherboard header is needed.

Walls 2.2 mm (3 perimeters), lid 3 mm; total 788 cm³: 660 cm³ without the Steam plate ≈ 840 g PETG, plate at 20 %
infill ≈ 80 g → everything fits on one 1 kg spool (with a small margin).
For a wood look glue 0.6 mm walnut veneer onto the plain plate, or print the plate in wood-filled PLA.
PSU 150 × 86 × 140 (the user's PSU is 149.7 × 86.4 × 140); on its rear face the socket is bottom centre, the switch
left of it, the grille above; cables leave at the front bottom. Outer corners R5, top/bottom edges chamfered 1.5 mm.

## Designing your own panel

All three panels follow one rule: the outer plate is 1.25 mm thick and sits in a 1.25 mm recess in the case (flush
with the outside); the inner step in the middle is 1.25 mm thicker and enters the wall opening; Ø3.4 holes + 90°
countersinks in the 4 corners. Clearance: plate and step are 0.2 mm smaller per side. The plate may be as thick and
as proud of the surface as you like.

| Panel | Plate (outer) | Opening | Screw centres (from the plate corner) |
|---|---|---|---|
| Lower front | 156 × 72 | 128 × 48 | 6 × 6 mm inset |
| Control strip | 156 × 32 | 128 × 18 | 6 × 6 mm inset (two per end, 20 mm apart) |

**Upper front = Steam Machine faceplate** (from Valve's official `steam_machine_3d.stp`, CC BY-NC-SA):
156 × 126.1 mm, 6.5 mm thick, flat or slightly convex front; no recess, the plate sits on the outer face of the
front wall. On its back, 4 SB443-OUT magnets at (±67, ±52.5) mm from the plate centre protrude 4 mm from the plate
(glued into a 0.8 mm pocket). The case has 6.65 mm square pockets at the same positions: the plate's magnet enters
4 mm, the case's magnet sits behind it (glue them so the poles attract). Case opening 112 × 82 (6 mm from the pockets).
Valve's stock plate, the Inkterface e-ink plate and third-party Steam Machine plates fit as well.

Space behind: 8 mm on the lower front panel (GPU), 50 mm behind the Steam plate (to the cooler), 40 mm on the strip.
The front joint screws of the body sit behind the Steam plate (Z 95): reachable with the plate off, invisible with it on.
Screwed panels carry Ø8 × 2 mm pads at the screw corners for the countersunk heads; the case has matching Ø8.6 pockets.

## Mating features (clearance 0.4 mm, PETG)

- **Body joint (Z = 80):** a 2 mm lip rising 6 mm on the inner face of the lower body's front and right walls, two
  4 mm pegs on the left posts; the upper body sits on them. Front 2 + rear 2 screws. The rear tabs are 12 × 12 mm at
  x 14 and 42 (left of the GPU opening and bracket tab), the lower one with a 45° underside.
- **Side covers** sit in the slot between the front/rear walls and the floor, outer faces flush with the case; the
  two meet at Z = 80 with a plain seam, order does not matter.
- **The upper side cover's** top tongue enters the groove under the lid.
- **The lid's** 4 mm rim on the front, right and rear edges sits inside the walls.
- **The I/O shield** clips with its springs into the wall thinned to 1.2 mm around the opening.
- **PSU support:** its two columns stand on the floor inside the 0.8 mm outline, the rail rests on the two bosses;
  screw it down before the PSU goes in. Move `PSU_SUP_COLS` for a PSU of a different depth.

## Printing

| Part | Orientation (STL is already oriented) | Note |
|---|---|---|
| `body_lower` | upright, floor on the bed | 215 mm deep: fits the K1 bed with 2.5 mm to spare, mouse-ear brims at the corners instead of a brim |
| `body_upper` | upright, joint face (the Z = 80 ring) on the bed | brim; 178 mm |
| `lid` | flat face on the bed | |
| `foot` | flat face on the bed, 4 pieces | |
| `psu_support` | on its side | |
| `front_lower*`, `faceplate*` | outer face on the bed | snap off the breakaway ribs in the case's panel openings |
| `strip*` | outer face on the bed | |
| `side_lower` | outer face on the bed | |
| `side_upper` | inner face on the bed | tongue and overlap rest on the bed |
| `test_piece` | upright | **print this first** |

Settings: PETG, 0.2 mm layers, 3 perimeters, 20 % gyroid, no supports. Snap off the thin breakaway ribs in the I/O,
GPU and socket openings with pliers after printing and sand the edge.

## Assembly order

1. Seat the inserts with a soldering iron (lower body 18, upper body 11, plus 8 in the panel frames).
2. Screw the 4 feet to the floor.
3. Lower side cover: mount the SSD on the bed on its inside with 4 screws (connector towards the front). Lower body:
   mount the intake fan in the floor (air in) and screw the PSU support onto its two floor bosses.
4. Control strip: fit the MX switches and the USB extensions, press on the keycaps. Upper body: slide the PSU in and
   fix it from the rear with the 4 × 6-32 screws (the PSU's underside is flush with the joint plane; it rests on the
   PSU support once the halves are joined).
5. Seat the upper body on the lower one (lip + pegs); tighten the 2 front horizontal screws (Steam plate off) and
   the 2 rear vertical screws.
6. Clip in the I/O shield from inside; mount the board with 6 screws (upper body F/J, lower body B/R/C/H).
7. Insert the GPU and fix its bracket to the rear shelf with 2 screws.
8. Connect the cables, wire the power switch to F_PANEL. Mount the exhaust fan under the lid (air up); connect both fans to a PSU Molex.
9. Fit the lower front panel and the control strip with 4 screws each, set the Steam plate on its magnets; then the
   side covers, then the lid.

## To verify on hardware

- `GPU_TAB_H = 112.5`: board surface to the underside of the GPU bracket tab (with the test piece).
- PCIEX16 alignment (`Z_C`): from the board manual drawing; test with the GPU opening of the test piece.
- PSU socket/switch: per the standard ATX drawing; move the cutout if your PSU's rear differs.
