#!/bin/bash
# Slice the printed parts for a Creality K1 into gcode/ (gitignored). ./slice_k1.sh [number ...], e.g. ./slice_k1.sh 06 07
# Profiles in gcode/profiles/ are complete (inherits resolved): the CLI fills settings it can't resolve with its own
# defaults (a system PLA profile came out at 200 °C and 20 % fan), so every G-code is checked against its profiles.
H=$(cd "$(dirname "$0")" && pwd)
P=/Applications/OrcaSlicer.app/Contents/Resources/profiles/Creality
O=/Applications/OrcaSlicer.app/Contents/MacOS/OrcaSlicer
G=$H/gcode/profiles
SEL=" $* "
val() { python3 -c "import json,sys; v=json.load(open(sys.argv[1]))[sys.argv[2]]; print(v[0] if isinstance(v, list) else v)" "$1" "$2"; }
run() {   # out process filament stl...
  out=$1 proc=$2 fil=$3; shift 3
  [ "$SEL" = "  " ] || [[ "$SEL" == *" ${out%%_*} "* ]] || return 0
  t=$(mktemp -d)
  (cd "$t" && "$O" --load-settings "$P/machine/Creality K1 (0.4 nozzle).json;$G/$proc" --load-filaments "$G/$fil" \
       --arrange 1 --slice 0 --outputdir "$t" $(printf "$H/stl/%s.stl " "$@") > "$t/log.txt" 2>&1)   # cd: the CLI drops a 00000.log in the working directory
  [ -f "$t/plate_1.gcode" ] || { echo "$out FAILED"; tail -3 "$t/log.txt"; return 1; }
  f=$H/gcode/$out; mv "$t/plate_1.gcode" "$f"
  for k in nozzle_temperature fan_min_speed additional_cooling_fan_speed filament_flow_ratio filament_density cool_plate_temp cool_plate_temp_initial_layer; do
    grep -q "^; $k = $(val "$G/$fil" $k)\$" "$f" || { echo "$out: $k is not $(val "$G/$fil" $k)"; return 1; }
  done
  for k in brim_type brim_width brim_object_gap elefant_foot_compensation wall_loops sparse_infill_density; do
    grep -q "^; $k = $(val "$G/$proc" $k)\$" "$f" || { echo "$out: $k is not $(val "$G/$proc" $k)"; return 1; }
  done
  echo "$out | $(grep -m1 'estimated printing time (normal mode)' "$f" | sed 's/.*= //') | $(grep -m1 '^; filament used \[g\]' "$f" | sed 's/.*= //') g"
}
run 01_foot_x4_PETG.gcode case_process_big.json case_petg.json foot foot foot foot
run 02_side_lower_PETG.gcode case_process.json case_petg.json side_lower
run 03_test_piece_PETG.gcode case_process_brim.json case_petg.json test_piece
run 04_psu_support_PETG.gcode case_process.json case_petg.json psu_support
run 05_body_lower_PETG.gcode case_process_big.json case_petg.json body_lower
run 06_body_upper_PETG.gcode case_process_brim.json case_petg.json body_upper   # 17 cm2 of wall on the bed: brim in and out
run 07_lid_PETG.gcode case_process_lid.json case_petg.json lid
run 08_side_upper_PETG.gcode case_process.json case_petg.json side_upper
run 09_strip_PLA.gcode case_process.json case_pla.json strip
run 10_front_lower_PLA.gcode case_process.json case_pla.json front_lower
run 11_faceplate_PLA.gcode case_process.json case_pla.json faceplate
