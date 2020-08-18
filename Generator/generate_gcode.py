from Generator.builder_functions import *

# Open weave file
# weave_file = "../Simulation/assets/moon_s120_500.wv"
weave_file = "w_s50_250.wv"
cfg, pattern = parse_weave_file_wrapper(weave_file)
lst_pattern = pattern.split(",")

# create the output file
path_to_gcode = "w_250itr.gcode"
gcode_file = generate_base_gcode(path_to_gcode)



# iterate over weave pattern, generating move and weave commands
generate_antibacklash_gcode(gcode_file, lst_pattern)
# generate_absolute_gcode(gcode_file, lst_pattern)

gcode_file.write("M117 100%\n")

