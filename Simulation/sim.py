from Simulation.algo import load_configuration


def draw_point(center_tuple, point_radius, base_image):
    from PIL import ImageDraw

    center_x, center_y = center_tuple
    x1 = center_x - (point_radius/2)
    x2 = center_x + (point_radius / 2)
    y1 = center_y - (point_radius / 2)
    y2 = center_y + (point_radius / 2)
    ellipse_size = (x1, y1, x2, y2)

    draw = ImageDraw.Draw(base_image)
    draw.ellipse(ellipse_size, outline=None, fill=(255, 20, 20))


def draw_points_on_circle(center_tuple, radius, num_points, base_img):
    from math import sin, cos, radians, floor
    from PIL import Image
    center_x, center_y = center_tuple
    cfg = load_configuration()
    point_radius = int(cfg['visual']['pegs_radius'])

    point_img = Image.new('RGB', base_img.size, (0, 0, 0))
    peg_point_list = []


    for pt in range(0, num_points):
        delta = 360 / num_points
        angle = pt * delta
        # Calculate the point coordinates on the circle
        point_x = (center_x + (radius * cos(radians(angle))))
        point_y = (center_y + (radius * sin(radians(angle))))

        x_rounded = int(round(point_x, 0))
        y_rounded = int(round(point_y, 0))
        point_coords = (x_rounded, y_rounded)

        peg_point_list.append(point_coords)

        draw_point(point_coords, point_radius, point_img)

    if cfg.getboolean('debug', 'show_image_with_pegs') and __name__ == "sim":
        combined_image = Image.blend(base_img.convert('RGB'), point_img, 0.5)
        combined_image.show()

    return peg_point_list


def prepare_image(path_to_image_file):
    from PIL import Image, ImageOps
    import matplotlib
    matplotlib.use('TkAgg')
    import matplotlib.pyplot as plt
    import numpy as np
    cfg = load_configuration()

    pegs_to_draw = int(cfg['algo']['peg_number'])
    circle_diameter_px = int(cfg['algo']['circle_diameter'])
    show_algorithm_progress = cfg.getboolean('debug', 'show_algorithm_progress')

    # Calculate the ratio of the image with respect to the thread.
    thread_diameter = float(cfg['physical']['thread_diameter'])
    image_physical_diameter = float(cfg['physical']['peg_circle_diameter'])
    rescale_value = int(image_physical_diameter/thread_diameter)

    # Calculate final size in px of the peg-circle
    px_per_mm = circle_diameter_px/image_physical_diameter
    adj_thread_size = px_per_mm * thread_diameter
    px_rescale_value = 1/adj_thread_size

    circle_diameter_px *= px_rescale_value  # Resize circle
    circle_diameter_px = round(circle_diameter_px-10)

    image_file = Image.open(path_to_image_file)
    base_img = image_file.resize((rescale_value, rescale_value)).convert('L')

    base_img = ImageOps.invert(base_img)
    clean_image = Image.new('L', (rescale_value, rescale_value), color=(255))

    if show_algorithm_progress:
        plt.ion()
        plt.imshow(np.asarray(base_img), cmap='Greys')
        plt.pause(0.2)

    peg_points_list = draw_points_on_circle((rescale_value/2, rescale_value/2),
                                            circle_diameter_px/2,
                                            pegs_to_draw,
                                            base_img)
    return base_img, clean_image, peg_points_list

def post_process_image(image, begin_timestamp):
    from PIL import ImageDraw
    import datetime
    cfg = load_configuration()
    peg_number = cfg['algo']['peg_number']
    num_iterations = cfg['algo']['num_iterations']
    end_timestamp = datetime.datetime.now()
    total_time_seconds = end_timestamp - begin_timestamp
    minutes = total_time_seconds.seconds // 60 % 60
    seconds = total_time_seconds.seconds - 60 * minutes
    formatted_time = str(minutes) + ":" + str(seconds)
    image_scale = cfg['algo']['image_resize_square']
    contrast = int(cfg['algo']['contrast'])

    display_text = f"Pegs: {peg_number}\n" \
                   f"Iterations: {num_iterations}\n" \
                   f"Total time [M:S]: {formatted_time}\n" \
                   f"Image scale: {image_scale}\n" \
                   f"Contrast: {contrast}"

    ImageDraw.Draw(image).text((20, 20), display_text, fill=(0))
    return image


def simulate_weave(path_to_image):
    import datetime
    starting_time = datetime.datetime.now()

    import Simulation.algo


    cfg = load_configuration()
    starting_peg = int(cfg['algo']['starting_peg'])
    num_iterations = int(cfg['algo']['num_iterations'])

    image, clean_image, point_list = prepare_image(path_to_image)

    pattern = Simulation.algo.get_pattern(image,
                                          point_list,
                                          starting_peg,
                                          num_iterations,
                                          clean_image=clean_image)
    post_process_image(clean_image, starting_time)
    clean_image.show()

    return pattern

def compile_file(pattern, image_name):
    """
    Function that takes in a pattern and the settings in the configuration folder
    and creates a sim file containing the pattern and the required settings
    to recreate the image from scratch.
    :param pattern: A weave pattern as a list
    :return: N/A
    """

    """
    > File name:
    
    Based off of the image name, with additional parameters:
    <image_name><seed><num_iterations>.wv
    
    > File structure:
    
    1. Header with all the required settings to re-create the image
    2. The weave pattern as comma separated values
    """
    cfg = load_configuration()
    peg_number = cfg['algo']['peg_number']
    num_iterations = cfg['algo']['num_iterations']
    image_scale = cfg['algo']['image_resize_square']
    contrast = int(cfg['algo']['contrast'])
    circ_diameter = int(cfg['algo']['circle_diameter'])

    # Create header:
    header = f"Peg Numbers: {peg_number}\n" \
             f"Iterations: {num_iterations}\n" \
             f"Image Scale: {image_scale}\n" \
             f"Contrast: {contrast}\n" \
             f"Circle Diameter: {circ_diameter}\n;"

    weave_pattern = ", ".join(map(str, pattern))

    # Create file:
    stripped_img_name = str(image_name.split(".")[0])
    filename = f"{stripped_img_name}_s{peg_number}_{num_iterations}.wv"
    try:
        with open(filename, 'w+') as fp:
            fp.write(header)
            fp.write(weave_pattern)
    except IOError as error_instance:
        print(error_instance)


if __name__ == "__main__":
    path_to_image = "assets/cat.png"
    final_pattern = simulate_weave(path_to_image)
    compile_file(final_pattern, path_to_image)

    # Todo:
    # - Make contrast function to better represent color values of overlapping strings [V]
    # - Implement ignore_nearest_neighbours from the configuration file. (make 'ignore list' and
    #   check indexes) [V]
    # - Make the weave pattern into a file [V]
    # - Make a parser to read the file and create an image [V]
	# - Super-resolution for the output image by scaling factor. [V]


