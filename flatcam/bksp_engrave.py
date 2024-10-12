from appPreProcessor import *

"""
Engraving preprocessor for B4CKSP4CE Laser CNC
"""

class BKSPEngrave(PreProc):
    include_header = False
    coordinate_format = "%.*f"
    feedrate_format = '%.*f'

    def start_code(self, p):
        return "# start"

    def startz_code(self, p):
        return "# startz"

    def lift_code(self, p):
        return "stop"

    def down_code(self, p):
        return "start"

    def toolchange_code(self, p):
        return "# toolchange"

    def up_to_zero_code(self, p):
        return "# up to zero"

    def rapid_code(self, p):
        return f"move_fast\t{p.x:.4f}\t{p.y:.4f}"

    def linear_code(self, p):
        return f"move\t{p.x:.4f}\t{p.y:.4f}"

    def end_code(self, p):
        return "# end"

    def feedrate_code(self, p):
        return "# feedrate"

    def z_feedrate_code(self, p):
        return "# z feedrate"

    def spindle_code(self, p):
        return "# spindle"

    def dwell_code(self, p):
        return "# dwell"

    def spindle_stop_code(self, p):
        return "# spindle stop"
