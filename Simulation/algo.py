def load_configuration():
    import configparser
    config_reader = configparser.ConfigParser()
    config_reader.read('config.ini')
    return config_reader


def bresenham_line(x0, y0, x1, y1):
    """
    Return all pixels between (x0, y0) and (x1, y1) as a list.

    :param x0: Self explanatory.
    :param y0: Self explanatory.
    :param x1: Self explanatory.
    :param y1: Self explanatory.
    :return: List of pixel coordinate tuples.
    """

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
    error = - delta_x / 2
    y = y0

    line = []
    for x in range(x0, x1 + 1):
        if steep:
            line.append((y, x))
        else:
            line.append((x, y))

        error = error + delta_y
        if error > 0:
            y = y + y_step
            error = error - delta_x

    if switched:
        line.reverse()
    return line


def get_pixel_values_p2p(base_img, peg1_tuple, peg2_tuple):
    """
    Function that calculates the value of a line, in terms of pixel intensity.
    :param base_img: Image to calculate from.
    :param peg1_tuple: (x, y) of point 1.
    :param peg2_tuple: (x, y) of point 2.
    :return: Integer value of the line.
    """
    import numpy as np
    x_0, y_0 = peg1_tuple
    x_1, y_1 = peg2_tuple
    list_of_pixels_in_line = bresenham_line(x_0, y_0, x_1, y_1)
    list_of_intensities = [base_img.getpixel(loc) for loc in list_of_pixels_in_line]
    line_length = len(list_of_pixels_in_line)
    line_value = np.sum(list_of_intensities)/255/line_length

    return line_value


def set_all_pixels_black(input_image, pos1, pos2, override_contrast=None):
    """
    Function that sets all pixels between two points black.
    :param input_image: Image to draw on.
    :param pos1: (x, y) of point 1.
    :param pos2: (x, y) of point 2.
    :param override_contrast: boolean - used for the generate image from pattern utility.
    :return: The newly drawn on image.
    """
    from PIL import ImageDraw
    cfg = load_configuration()
    if override_contrast is not None:
        contrast_val = override_contrast
    else:
        contrast_val = int(cfg['algo']['contrast'])
    x_0, y_0 = pos1
    x_1, y_1 = pos2
    list_of_pixels_in_line = bresenham_line(x_0, y_0, x_1, y_1)
    draw_image = ImageDraw.Draw(input_image)
    for pixel in list_of_pixels_in_line:
        color = input_image.getpixel(pixel)
        draw_image.point(pixel, fill=max(0,color-contrast_val))  # CONTRAST VALUE

    return input_image


def generate_skip_list(current_index):
    """
    Bare bones, patch version of a function to skip the n-nearest symmetric neighbors.
    This can save calculation time, but will limit the overall 'clarity' of the image.
    :param current_index: Takes in the index in which the simulation is currently at.
    :return: A list that is a mask of which values to skip (marked with 1)
    """
    # Load configuration parameters
    cfg = load_configuration()
    peg_amt = int(cfg['algo']['peg_number'])
    skip_amount = int(cfg['algo']['skip_nearest_neighbours'])

    # Create variables and the mask skeleton
    output_list = [0 for _ in range(peg_amt)]
    top_overflow = 0
    bottom_overflow = 0

    # Check if the list will overflow
    if current_index + skip_amount > peg_amt:
        top_overflow = (current_index + skip_amount - peg_amt)
    if current_index -skip_amount < 0:
        bottom_overflow = abs(current_index - skip_amount)

    # Build the mask, filling in 1's where needed
    for index in range(peg_amt):
        # if overflow:
        if index < top_overflow:
            output_list[index] = 1
        if index > (peg_amt - bottom_overflow):
            output_list[index] = 1
        # if between the requested scope:
        if current_index - skip_amount < index < current_index + skip_amount:
            output_list[index] = 1

    return output_list


def select_next_peg(image, list_of_pegs, starting_peg, clean_image=None):
    """
    Function that decides which peg will be jumped to next using the color values of the pixels.
    :param image: Input image to work on.
    :param list_of_pegs: List of the locations of all pegs.
    :param starting_peg: Which peg to start on (from config...)
    :param clean_image: Optional - if a blank image is passed, an "as-is" output image will also be shown.
    :return: The next peg, as integer.
    """

    start_pos = list_of_pegs[starting_peg]  # get a tuple of (x, y) coords
    value_list = []
    skip_list = generate_skip_list(starting_peg)

    for index, point in enumerate(list_of_pegs):
        if (point == start_pos) or (skip_list[index] == 1):
            # Skip 'this' peg
            value_list.append(0)
        else:
            value = get_pixel_values_p2p(image, start_pos, point)
            value_list.append(value)

    next_peg = value_list.index(max(value_list))

    # set the pixels in the image between these two lines to be full black...
    new_image = set_all_pixels_black(image,
                                     list_of_pegs[starting_peg],
                                     list_of_pegs[next_peg])

    if clean_image is not None:
        clean_image = set_all_pixels_black(clean_image,
                                           list_of_pegs[starting_peg],
                                           list_of_pegs[next_peg])
    return new_image, next_peg, clean_image


def get_pattern(image, list_of_pegs, starting_peg, num_iterations, clean_image=None):
    """
    Function that gets a move-list to create the yarn portrait, peg by peg.
    :param image: Image to work on.
    :param list_of_pegs: List of the locations of all pegs.
    :param starting_peg: Which peg to start on (from config...)
    :param num_iterations: How many moves to do.
    :param clean_image: Optional - if a blank image is passed, an "as-is" output image will also be shown.

    :return: A list of pegs, in order, following which - the output image can be achieved.
    """
    import numpy as np
    import matplotlib.pyplot as plt

    next_peg = starting_peg
    next_img = image
    move_list = []
    cfg = load_configuration()
    do_plot = cfg.getboolean('debug', 'show_algorithm_progress')

    for iteration in range(num_iterations):
        next_img, next_peg, clean_image = select_next_peg(next_img, list_of_pegs, next_peg, clean_image=clean_image)
        move_list.append(next_peg)
        if do_plot:
            plt.clf()
            plt.imshow(np.asarray(clean_image), cmap='gray')
            plt.pause(0.01)

    return move_list
