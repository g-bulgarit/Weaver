# File to hold all functions to generate motion based on the weave pattern.

import numpy as np

# Get constants
peg_diameter = 455
num_pegs = 120
peg_to_degree_ratio = 360/num_pegs
motor_max_travel = peg_diameter * np.pi  # Full revolution of the frame.

def generate_base_gcode(file_path):
    # generate the gcode file with some boilerplate.
    gcode_file = open(file_path, "w+")
    gcode_file.write("G91\n")
    # add more boilerplate here
    return gcode_file

def move_from_to(motor, from_pos, to_pos):

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
    if delta_pegs > num_pegs / 2:
        direction = -1
        distance_to_move = np.abs(delta_pegs - num_pegs/2)

    # find the center angle
    center_angle = delta_pegs * peg_to_degree_ratio
    linear_distance = center_angle * (np.pi/180) * peg_diameter
    # Create gcode string
    return f"G0 {motor}{linear_distance:.2f}"

def weave_peg():
    pass



if __name__ == "__main__":
    print(move_from_to("x",40,30))