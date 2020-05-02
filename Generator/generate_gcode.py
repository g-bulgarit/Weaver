from Generator.builder_functions import *

# Open weave file
weave_file = open("weave.wv", "r'")
# get location of the output file
path_to_gcode = "test.gcode"
gcode_file = generate_base_gcode(path_to_gcode)

# iterate over weave pattern, generating move and weave commands
try:
    pass
except:
    pass
finally:
    weave_file.close()
    gcode_file.close()
