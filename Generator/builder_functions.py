# File to hold all functions to generate motion based on the weave pattern.
import numpy as np
from Simulation.image_from_pattern import parse_file

cfg = {
        "num_pegs" : 0,
        "peg_radius" : 0,
        "peg_to_degree_ratio" : 0,
        "motor_max_travel" : 0,
      }

def parse_weave_file_wrapper(file_path):
    num_pegs, _, _, _, peg_diameter, pattern = parse_file(file_path)
    cfg["num_pegs"] = num_pegs
    cfg["peg_radius"] = peg_diameter/2
    cfg["peg_to_degree_ratio"] = 360/num_pegs
    cfg["motor_max_travel"] = peg_diameter * np.pi  # Full revolution of the frame.
    return cfg, pattern

def generate_base_gcode(file_path):
    # generate the gcode file with some boilerplate.
    # returns file handler for the open file!

    gcode_file = open(file_path, "w+")
    gcode_file.write(";START: Boilerplate code from the gcode generator\n")
    gcode_file.write("G4 P1000 ;Wait 1Sec.\n")
    gcode_file.write("M201 X25.0 ;Set x axis acceleration to 25.\n")
    # gcode_file.write("G0 x3.00 ;Move to 3mm.\n")
    # gcode_file.write("G4 P1500 ;Wait 1Sec.\n")
    # gcode_file.write("G0 x0.00 ;Move to 0mm.\n")
    gcode_file.write("G4 P1000 ;Wait 1Sec.\n")
    gcode_file.write("G91 ;Set all axis to relative motion, as it is easier to work with.\n")
    gcode_file.write("G4 P1000 ;Wait 1Sec.\n")
    gcode_file.write(";END: Boilerplate code from the gcode generator\n")
    return gcode_file


def generate_abs_base_gcode(file_path):
    # generate the gcode file with some boilerplate.
    # returns file handler for the open file!

    gcode_file = open(file_path, "w+")
    gcode_file.write(";START: Boilerplate code from the gcode generator\n")
    gcode_file.write("M201 x50.0 ;Set x axis acceleration to 50.\n")
    gcode_file.write("G90 ;Set all axis to absolute motion.\n")
    gcode_file.write("G4 P1000 ;Wait 1Sec.\n")
    gcode_file.write(";END: Boilerplate code from the gcode generator\n")
    return gcode_file

def move_from_to(motor, from_pos, to_pos, debug=False, status=None):
    # Takes in <from> and <to> peg numbers, decides on best way to go,
    # calculates the conversion from radial distance to linear distance
    # generates and returns gcode line.

    direction = 1  # Generally.
    outstr = ""
    one_peg_distance = 3.21
    delta_pegs = to_pos - from_pos
    if abs(delta_pegs) >= 25:
        delta_pegs = (50-abs(delta_pegs))

    linear_distance_after_gear = delta_pegs * one_peg_distance

    if status: outstr+= f"M117 {status}\n"
    if debug: outstr+= f";START: Move to peg {to_pos}\n"
    outstr += f"G0 {motor.upper()}{linear_distance_after_gear:.3f}\n"
    if debug: outstr += f";END: Move to peg {to_pos}\n"
    return outstr

def move_weavehead(dir):
    if dir == 1:
        return "G0 Y-10.00\nG4 P500\n"
    else:
        return "G0 Y10.00\nG4 P500\n"

def move_weavehead_abs(dir):
    if dir == 1:
        return "G0 Y-5.00\nG4 P500\n"
    else:
        return "G0 Y5.00\nG4 P500\n"

def weave_peg(debug=False):
    # Calls the weave sequence:
    #   1. rotate frame <x> degrees to + dir
    #   2. half turn on the weave motor
    #   3. rotate frame <2x> degrees to - dir
    #   4. half turn on the weave motor
    #   5. rotate frame <x> degree to + dir

    # center_angle = 0.5 * cfg["peg_to_degree_ratio"]
    # circum = 2 * np.pi * cfg["peg_radius"]
    # linear_distance = circum / center_angle
    # half_step = linear_distance / 2
    # half_step = center_angle * (np.pi/180) * cfg["peg_radius"]

    one_peg_distance = 3.21
    half_step = one_peg_distance*0.45

    output_block = ""
    if debug: output_block += ";WEAVE: start\n"
    output_block += rotate_frame(-half_step)
    output_block += "G4 P500\n"
    output_block += move_weavehead(1)
    output_block += rotate_frame(2* half_step)
    output_block += "G4 P500\n"
    output_block += move_weavehead(0)
    output_block += rotate_frame(-half_step*1.25)
    output_block += "G4 P500\n"
    if debug: output_block += ";WEAVE: end\n"
    return output_block

def weave_peg_absolute(current_loc, debug=False):
    # Calls the weave sequence:
    #   1. rotate frame <x> degrees to + dir
    #   2. half turn on the weave motor
    #   3. rotate frame <2x> degrees to - dir
    #   4. half turn on the weave motor
    #   5. rotate frame <x> degree to + dir

    # center_angle = 0.5 * cfg["peg_to_degree_ratio"]
    # circum = 2 * np.pi * cfg["peg_radius"]
    # linear_distance = circum / center_angle
    # half_step = linear_distance / 2
    # half_step = center_angle * (np.pi/180) * cfg["peg_radius"]

    one_peg_distance = 3.21
    half_step = one_peg_distance*0.35

    output_block = ""
    if debug: output_block += ";WEAVE: start\n"
    output_block += f"G0 X{str(round(current_loc - half_step,3))}\n"
    output_block += "G4 P500\n"
    output_block += move_weavehead_abs(1)
    output_block += f"G0 X{str(round(current_loc + 2*half_step,3))}\n"
    output_block += "G4 P500\n"
    output_block += move_weavehead_abs(0)
    output_block += f"G0 X{str(round(current_loc - half_step,3))}\n"
    output_block += "G4 P500\n"
    if debug: output_block += ";WEAVE: end\n"
    return output_block

def weave_peg_anti_backlash(debug=False):
    one_peg_distance = 3.21
    output_block = ""

    if debug: output_block += ";WEAVE: start\n"
    output_block += move_weavehead(1)
    output_block += rotate_frame(one_peg_distance)
    output_block += "G4 P500\n"
    output_block += move_weavehead(0)
    output_block += "G4 P500\n"
    if debug: output_block += ";WEAVE: end\n"

    return output_block


def generate_absolute_gcode(gcode_file, pattern):
    num_pegs = 50
    distance_p2p = 3.21
    pos_dict = {}
    for i in range(num_pegs-1):
        pos_dict[i] = i*distance_p2p

    for move in pattern:
        gcode_file.write(f"G0 X{str(round(pos_dict[int(move)],3))}\n")
        gcode_file.write(weave_peg_absolute(pos_dict[int(move)]))


def move_p2p_one_dir(previous, next, first=False):
    num_pegs = 50
    delta = None
    one_pin_distance = 3.21

    if int(next) < int(previous):
        delta = (num_pegs - int(previous)) + int(next)
    else:
        delta = int(next) - int(previous)

    distance_to_move = round(one_pin_distance * delta ,3)
    if first:
        distance_to_move -= one_pin_distance/2

    return f"G0 X{str(distance_to_move)}\n"

def rotate_frame(amount):
    outstr = f"G0 X{round(amount,3)}\n"
    return outstr

def generate_relative_gcode(gcode_file, pattern):
    current_move = 0

    for next_move in pattern:
        gcode_file.write(move_p2p_one_dir(current_move, next_move))
        gcode_file.write(weave_peg())
        current_move = next_move


def generate_antibacklash_gcode(gcode_file, pattern):
    current_move = pattern[0]
    gcode_file.write(move_p2p_one_dir(0, current_move, first=True))
    gcode_file.write(weave_peg_anti_backlash())

    for next_move in pattern[1:]:
        gcode_file.write(move_p2p_one_dir(current_move, next_move))
        gcode_file.write(weave_peg_anti_backlash())
        current_move = next_move





if __name__ == "__main__":
    # some test lines

    cfg = {
        "num_pegs": 49,
        "peg_radius": 82,
        "peg_to_degree_ratio": 7.2,
    }

    movelist = [5,10,5,10, 0, 24, 0, 5]
    previous = 0
    for move in movelist:
        print(f"Moving to {move}")
        print(move_from_to(cfg, "x", previous, move))
        previous = move