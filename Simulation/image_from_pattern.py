from Simulation.algo import bresenham_line, set_all_pixels_black
from Simulation.sim import draw_points_on_circle

def parse_file(filename):
    with open(filename, "r") as fp:
        body = fp.read()
        header, pattern = body.split(";")
        header_list = header.split("\n")
        peg_number = header_list[0].split(":")[1].strip()
        num_iterations = header_list[1].split(":")[1].strip()
        image_scale = header_list[2].split(":")[1].strip()
        contrast = header_list[3].split(":")[1].strip()
        circ_diameter = header_list[4].split(":")[1].strip()
        pattern = pattern.strip()
        return int(peg_number), \
               int(num_iterations), \
               int(image_scale), \
               int(contrast), \
               int(circ_diameter), \
               pattern

if __name__ == "__main__":
    from PIL import Image
    import numpy as np
    import matplotlib.pyplot as plt
    # Get file
    filename = "woman_s120_100.wv"
    # Get params from file
    peg_number, num_iterations, image_scale, contrast, circ_diameter, pattern = parse_file(filename)
    # Make new image with the correct size
    canvas = Image.new('L', (image_scale, image_scale), color=(255))
    # Get list of points on the circle
    point_list = draw_points_on_circle((image_scale/2, image_scale/2),
                          circ_diameter/2,
                          peg_number,
                          canvas)
    # For csv - draw each line as given
    pattern_list = pattern.split(",")
    for move in range(len(pattern_list)-1):
        set_all_pixels_black(canvas,
                             point_list[int(pattern_list[move])],
                             point_list[int(pattern_list[move+1])])

    canvas.show()