# Mini PC case — dimension references

## Parts
- Motherboard: ASUS PRIME H310M-K (to be verified), mATX 226 (rear edge) × 185 (depth) mm
- CPU: i3-8100 65 W; cooler PCCOOLER RC400, 53 mm, 90 mm fan
- GPU: ASUS Phoenix GTX 1050 Ti (PH-GTX1050TI-4G) 192 × 111 × 37 mm, 2 slots, no extra power
- PSU: standard ATX 150 × 86 × 140 mm, 400 W
- Printer: Creality K1, bed 220 × 220 × 250, PETG

## ATX 2.2 (atx2_2.pdf, Fig. 3–4) — inches, datum = hole A
X: along the rear edge towards the I/O (+), Y: from the rear edge towards the front (+). In the case X = up.
- Board rear edge Y = -0.400; ATX board left edge X = -0.650, right (top) edge X = 11.350
- Holes Ø0.156: A(0,0) B(3.1,0) C(4.9,0) F(11.1,0.9) G(0,6.1) H(4.9,6.1) J(11.1,6.1) K(0,8.95) L(4.9,8.95) M(11.1,8.95); mATX extra: R, S (Y=6.1, near B — measure on the board)
- H310M-K (226 mm): left/bottom edge X = 11.35 - 8.90 = 2.45 → likely holes B, C, F, H, J, R/S (depth 185 → front edge Y = 6.88)
- I/O opening 6.250 × 1.750 (158.75 × 44.45 mm), X = 5.196 … 11.446; bottom edge 3.81 mm below the board's top surface; 2.5 mm keepout
- Rear panel at Y = -0.483 from the datum (12.27 mm), panel thickness 0.94–1.32 mm for the I/O shield
- Slot pitch 0.800 (20.32 mm); AGP/x16 pin 1 ≈ X 5.0; H310M-K has 3 slots (≈ 5.0, 4.2, 3.4) — which one is the x16 to be verified from a photo

## Layout (v4, `build_case.py`)
Motherboard upright, fixed to the right wall (X = W); GPU directly in the slot, its bracket on the shelf outside the
rear wall. PSU on its side opposite the cooler, its fan facing the grille in the left side cover. SSD on the inside
of the lower side cover. Outer size 176 × 204 × 265 mm, ~9.7 L. Body in two parts from Z = 80 (GPU opening ≤ 78.2
below, I/O ≥ 81.4 and PSU above); joined by lip + pegs + 4 screws. Tallest part 178 mm.
Fasteners, screw list, printing and assembly: `ASSEMBLY.md`.
Checks (`build()`, `check_fasteners()`, `check_print()`): every part a single valid solid, no clash with the reference
hardware, every screw with its insert, mating hole and edge margin, no unsupported bridge over 18 mm in print orientation.
