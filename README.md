# pcb-manufacture

Homebrew PCB manufacturing solution using laser etching on painted raw copper-plated PCB

It uses FlatCAM for generating pre-GCode and Klipper for CNC control

The process is simple in steps:
1. Create PCB manufacture files (`.gcode`, `.drl`) in any PCB software (KiCad for example)
2. Convert `.gcode` and `.drl` to pre-GCode files using custom preprocessors
3. Convert pre-GCode to GCode using `convert.py`
4. Apply your GCode to CNC and raw PCB material
5. Etch PCB
6. Remove paint using any solvent (we use IPA and ... for this)
7. Use your PCB!

# FlatCAM

For generating pre-GCode files, you need:
- Add [flatcam/bksp_drill.py](bksp_drill.py) and [flatcam/bksp_engrave.py](bksp_engrave.py) to `lib/preprocessors` directory in your FlatCAM installation
- Use them to create drill and engraving pre-GCode files

# Converting to GCode

Use `convert.py` to convert resuling files to GCode

For our CNC installation use this command line parameters:
```shell
python3 convert.py \
    --laser-power 255 \
    --spindle-power 127 \
    --default-speed 2400 \
    --laser-z 71.6 \
    --laser-feedrate 300 \
    --spindle-z-home 115 \
    --spindle-z-pre-drill 92 \
    --spindle-z-drill 88.5 \
    --spindle-feedrate 60 \
    -l engrave.nc -d drill.nc -o output.gcode
```