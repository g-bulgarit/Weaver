from Generator.builder_functions import *

# Open weave file
weave_file = "../Simulation/assets/moon_s120_500.wv"
cfg, pattern = parse_weave_file_wrapper(weave_file)
lst_pattern = pattern.split(",")
# get location of the output file
path_to_gcode = "test.gcode"
gcode_file = generate_base_gcode(path_to_gcode)

# iterate over weave pattern, generating move and weave commands
try:
    previous_move = 0
    move_ctr = 0
    while move_ctr < len(lst_pattern):
        gcode_file.write(move_from_to(cfg, "x", previous_move, int(lst_pattern[move_ctr])))
        # do weave
        gcode_file.write(weave_peg(cfg))
        previous = int(lst_pattern[move_ctr])
        move_ctr +=1
except Exception as e:
    print(e)
finally:
    gcode_file.close()
