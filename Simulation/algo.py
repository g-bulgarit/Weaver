def bresenham_line(x0, y0, x1, y1):
    steep = abs(y1 - y0) > abs(x1 - x0)
    if steep:
        x0, y0 = y0, x0
        x1, y1 = y1, x1

    switched = False
    if x0 > x1:
        switched = True
        x0, x1 = x1, x0
        y0, y1 = y1, y0

    if y0 < y1:
        y_step = 1
    else:
        y_step = -1

    delta_x = x1 - x0
    delta_y = abs(y1 - y0)
    error = -delta_x / 2
    y = y0

    line = []
    for x in range(x0, x1 + 1):
        if steep:
            line.append((y,x))
        else:
            line.append((x,y))

        error = error + delta_y
        if error > 0:
            y = y + y_step
            error = error - delta_x

    if switched:
        line.reverse()
    return line

def get_pixel_values_p2p(base_img, peg1_tuple, peg2_tuple):
    import numpy as np
    line_value = 0
    gscale_img = base_img.convert('L')
    x_0, y_0 = peg1_tuple
    x_1, y_1 = peg2_tuple
    list_of_pixels_in_line = bresenham_line(x_0, y_0, x_1, y_1)

    for pixel_coords in list_of_pixels_in_line:
        line_value += gscale_img.getpixel(pixel_coords)

    return line_value

def select_next_peg(image, list_of_pegs, starting_peg):
    # from current_peg, get values of the row of pixels between this peg
    # and all others, find out which peg results in the highest value,
    # select that peg to be the next peg.
    start_pos = list_of_pegs[starting_peg]  # get a tuple of (x, y) coords
    value_list = []

    for point in list_of_pegs:
        if point == start_pos:
            # Skip 'this' peg
            pass
        else:
            value_list.append(get_pixel_values_p2p(image, start_pos, point))

    


    next_peg = None
    return next_peg