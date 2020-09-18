# File to hold all functions to generate motion based on the weave pattern.
from Simulation.image_from_pattern import parse_file
from configparser import ConfigParser


def parse_weave_file_wrapper(file_path):
    """
    Function to fetch weave parameters from the saved output file of the main algo.
    This information is then used to calculate the motion paths for the motors.
    :param file_path: Path to the .wv file
    :return:
                -cfg: a python dictionary that contains the parameters listed below
                -pattern: the final weave-pattern [list]
    """
    num_pegs, _, _, _, peg_diameter, pattern = parse_file(file_path)

    wv_cfg = ConfigParser()
    wv_cfg.read(r"generator_config.ini")

    cfg = dict()
    cfg["num_pegs"] = num_pegs
    cfg["peg_radius"] = peg_diameter/2
    cfg["steps_per_peg"] = wv_cfg["Steps"]["steps_per_peg"]
    lst_pattern = pattern.split(",")

    return cfg, wv_cfg, lst_pattern


def generate_base_gcode(file_path, cfg_parser):
    """
    Function to generate the header for the gCode file.
    TODO: change functionality with the config file (for other motor drivers...?)
    :param file_path: path where to create the new gcode file in.
    :return: an **OPEN** file handler, ready for writing.
    """
    gcode_file = open(file_path, "w+")
    gcode_file.write(";START: Boilerplate code from the gcode generator\n")

    # Behaviour per motor driver:
    motor_driver = str(cfg_parser["Motors"]["motor_driver"])
    if motor_driver == "TMC":
        # Set motor current to 595mA to prevent overheating and damage.
        gcode_file.write("M906 X595 Y595\n")

    gcode_file.write("G4 P1000 ;Wait 1Sec.\n")
    gcode_file.write("M201 X25.0 ;Set x axis acceleration to 25.\n")
    gcode_file.write("G4 P1000 ;Wait 1Sec.\n")
    gcode_file.write("G91 ;Set all axis to relative motion.\n")
    gcode_file.write("G4 P1000 ;Wait 1Sec.\n")
    gcode_file.write(";END: Boilerplate code from the gcode generator\n")

    return gcode_file


def move_weavehead(direction):
    if direction == 1:
        return "G0 Y-10.00\nG4 P500\n"
    else:
        return "G0 Y10.00\nG4 P500\n"


def weave_peg_anti_backlash(cfg=None, debug=False):
    if cfg is not None:
        one_pin_distance = float(cfg["steps_per_peg"])
    else:
        raise Exception("Missing configuration file")

    # Text container:
    output_block = ""

    if debug:
        output_block += ";WEAVE[ANTIBACKLASH]: start\n"
    output_block += move_weavehead(1)
    output_block += rotate_frame(one_pin_distance)
    output_block += "G4 P500\n"
    output_block += move_weavehead(0)
    output_block += "G4 P500\n"
    if debug:
        output_block += ";WEAVE[ANTIBACKLASH]: end\n"

    return output_block


def move_p2p_one_dir(previous_pt, next_pt, first=False, cfg=None):
    if cfg is not None:
        # Take values from config
        one_pin_distance = float(cfg["steps_per_peg"])
        num_pegs = cfg["num_pegs"]
    else:
        raise Exception("Missing configuration file.")

    if int(next_pt) < int(previous_pt):
        delta = (num_pegs - int(previous_pt)) + int(next_pt)
    else:
        delta = int(next_pt) - int(previous_pt)

    distance_to_move = round(one_pin_distance * delta, 3)
    if first:
        distance_to_move -= one_pin_distance/2

    return f"G0 X{str(distance_to_move)}\n"


def rotate_frame(amount):
    outstr = f"G0 X{round(amount,3)}\n"
    return outstr


def generate_antibacklash_gcode(gcode_file, pattern, cfg):
    current_move = pattern[0]
    gcode_file.write(move_p2p_one_dir(0, current_move, cfg=cfg, first=True))
    gcode_file.write(weave_peg_anti_backlash(cfg))

    for next_move in pattern[1:]:
        gcode_file.write(move_p2p_one_dir(current_move, next_move, cfg=cfg))
        gcode_file.write(weave_peg_anti_backlash(cfg=cfg))
        current_move = next_move


if __name__ == "__main__":
    # Do nothing
    pass
