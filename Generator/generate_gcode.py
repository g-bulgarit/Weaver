from Generator.builder_functions import *

# Load files and parse data
weave_file = r"G:\Code\Weaver\Simulation\assets\cat_s180_10000.wv"
cfg, pattern = parse_weave_file_wrapper(weave_file)
lst_pattern = pattern.split(",")

# create the output file
path_to_gcode = "out.gcode"
gcode_file = generate_base_gcode(path_to_gcode)

# iterate over weave pattern, generating move and weave commands
generate_antibacklash_gcode(gcode_file, lst_pattern, cfg)

gcode_file.write("M117 100%\n")

