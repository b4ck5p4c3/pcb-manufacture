from appPreProcessor import *
import json

class Debug(PreProc):
    include_header = False
    coordinate_format = "%.*f"
    feedrate_format = '%.*f'

    def start_code(self, p):
        return f"start"

    def startz_code(self, p):
        return f"startz"

    def lift_code(self, p):
        return f"lift"

    def down_code(self, p):
        return f"down"

    def toolchange_code(self, p):
        return f"toolchange"

    def up_to_zero_code(self, p):
        return f"up_to_zero"

    def rapid_code(self, p):
        return f"rapid {p.x} {p.y}"

    def linear_code(self, p):
        return f"linear {p.x} {p.y}"

    def end_code(self, p):
        return f"end"

    def feedrate_code(self, p):
        return f"feedrate"

    def z_feedrate_code(self, p):
        return f"z_feedrate"

    def spindle_code(self, p):
        return f"spindle"

    def dwell_code(self, p):
        return f"dwell"

    def spindle_stop_code(self, p):
        return f"spindle_stop"
