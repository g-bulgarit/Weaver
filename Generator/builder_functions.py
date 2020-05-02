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
    gcode_file.write("G91 ;Set all axis to relative motion, as it is easier to work with.\n")
    gcode_file.write(";END: Boilerplate code from the gcode generator\n")
    return gcode_file

def move_from_to(cfg, motor, from_pos, to_pos):

    # Call G91 first!
    #
    #
    # Takes in <from> and <to> peg numbers, decides on best way to go,
    # calculates the conversion from radial distance to linear distance
    # generates and returns gcode line.

    direction = 1  # Generally.

    delta_pegs = to_pos - from_pos
    if delta_pegs < 0:
        direction = -1
    # check if it's better to go backwards
    if delta_pegs > cfg["num_pegs"] / 2:
        direction = -1
        distance_to_move = np.abs(delta_pegs - cfg["num_pegs"]/2)

    # find the center angle
    center_angle = delta_pegs * cfg["peg_to_degree_ratio"]
    linear_distance = center_angle * (np.pi/180) * cfg["peg_radius"]
    # Create gcode string
    return f"G0 {motor.upper()}{linear_distance:.3f}\n"

def weave_peg():
    pass



if __name__ == "__main__":
    movelist = [30,60,30,120, 80, 60, 20, 0]
    previous = 0
    for move in movelist:
        print(move_from_to("x", previous, move))
        previous = move