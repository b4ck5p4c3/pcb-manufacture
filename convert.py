import argparse

parser = argparse.ArgumentParser(
                    prog='converter',
                    description='FlatCAM to gcode converter')

parser.add_argument('-l', '--laser-file', help='Path to laser gcode file')
parser.add_argument('-d', '--drill-file', help='Path to drill gcode file')

parser.add_argument('-lp', '--laser-power', help='Laser power (0-255)', type=float, required=True)
parser.add_argument('-sp', '--spindle-power', help='Spindle power (0-255)', type=float, required=True)

parser.add_argument('-ds', '--default-speed', help='Default X-Y movement speed (while not working)', type=float, required=True)
parser.add_argument('-lz', '--laser-z', help='Laser Z offset', type=float, required=True)
parser.add_argument('-lf', '--laser-feedrate', help='Laser feedrate (mm/min)', type=float, required=True)
parser.add_argument('-szh', '--spindle-z-home', help='Initial spindle Z offset', type=float, required=True)
parser.add_argument('-szpd', '--spindle-z-pre-drill', help='Spindle pre-drill Z offset', type=float, required=True)
parser.add_argument('-szd', '--spindle-z-drill', help='Spindle drill Z offset', type=float, required=True)
parser.add_argument('-sf', '--spindle-feedrate', help='Spindle feedrate (mm/min)', type=float, required=True)

parser.add_argument('-o', '--output-file', help='Path to output gcode file', required=True)

args = parser.parse_args()

def is_gcode_comment_or_none(line):
    return len(line) == 0 or line[0] == '#' or line[0] == '(' or line[0] == ';'

with open(args.output_file, 'w') as output:
    output.write('; init printer\n')
    output.write('G28\n')
    output.write('G21\n')
    output.write('G90\n')
    output.write('\n')
    if args.laser_file:
        output.write('; start lasering\n')
        output.write('USE_LASER\n')
        output.write('G0 Z%.4f F%.4f\n' % (args.laser_z, args.default_speed))
        with open(args.laser_file, 'r') as laser_input:
            while True:
                input_line = laser_input.readline()
                if len(input_line) == 0:
                    break
                line = input_line.strip()
                if is_gcode_comment_or_none(line):
                    continue
                command_data = line.split('\t')
                command = command_data[0]
                params = command_data[1:]
                if command == 'stop':
                    output.write('LASER_OFF\n')
                elif command == 'start':
                    output.write('LASER_SET S=%.4f\n' % (args.laser_power))
                elif command == 'move':
                    x = float(params[0])
                    y = float(params[1])
                    output.write('G1 X%.4f Y%.4f F%.4f\n' % (x, y, args.laser_feedrate))
                elif command == 'move_fast':
                    x = float(params[0])
                    y = float(params[1])
                    output.write('G1 X%.4f Y%.4f F%.4f\n' % (x, y, args.default_speed))
                else:
                    raise ValueError(f'unsupported laser command "{command}"')
        output.write('LASER_OFF\n')
        output.write('G28\n')
        output.write('\n')
    if args.drill_file:
        output.write('; start drilling\n')
        output.write('USE_SPINDLE\n')
        output.write('G0 Z%.4f F%.4f\n' % (args.spindle_z_home, args.default_speed))
        output.write('SPINDLE_SET S=%.4f\n' % (args.spindle_power / 2))
        output.write('G4 P5000\n')
        output.write('SPINDLE_SET S=%.4f\n' % (args.spindle_power))
        with open(args.drill_file, 'r') as drill_input:
            while True:
                input_line = drill_input.readline()
                if len(input_line) == 0:
                    break
                line = input_line.strip()
                if is_gcode_comment_or_none(line):
                    continue
                command_data = line.split('\t')
                command = command_data[0]
                params = command_data[1:]
                if command == 'up':
                    output.write('G1 Z%.4f F%.4f\n' % (args.spindle_z_pre_drill, args.spindle_feedrate))
                    output.write('G1 Z%.4f F%.4f\n' % (args.spindle_z_home, args.default_speed))
                elif command == 'down':
                    output.write('G1 Z%.4f F%.4f\n' % (args.spindle_z_pre_drill, args.default_speed))
                    output.write('G1 Z%.4f F%.4f\n' % (args.spindle_z_drill, args.spindle_feedrate))
                elif command == 'move_fast':
                    x = float(params[0])
                    y = float(params[1])
                    output.write('G0 X%.4f Y%.4f F%.4f\n' % (x, y, args.default_speed))
                else:
                    raise ValueError(f'unsupported spindle command "{command}"')
        output.write('SPINDLE_OFF\n')
        output.write('G28\n')
    output.write('\n')