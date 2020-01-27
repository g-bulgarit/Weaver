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
    from math import sin, cos, radians
    from PIL import Image
    center_x, center_y = center_tuple
    cfg = load_configuration()
    point_radius = int(cfg['visual']['pegs_radius'])

    point_img = Image.new('RGB', base_img.size, (0, 0, 0))
    peg_point_list = []

    for angle in range(0, 360, round(360/num_points)):
        # Calculate the point coordinates on the circle
        point_x = center_x + (radius * cos(radians(angle)))
        point_y = center_y + (radius * sin(radians(angle)))

        x_rounded = int(round(point_x, 0))
        y_rounded = int(round(point_y, 0))
        point_coords = (x_rounded, y_rounded)

        peg_point_list.append(point_coords)

        draw_point(point_coords, point_radius, point_img)

    if cfg.getboolean('debug', 'show_image_with_pegs'):
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
    img_size = int(cfg['algo']['image_resize_square'])
    circle_diameter = int(cfg['algo']['circle_diameter'])
    show_algorithm_progress = cfg.getboolean('debug', 'show_algorithm_progress')



    image_file = Image.open(path_to_image_file)
    base_img = image_file.resize((img_size, img_size)).convert('L')

    base_img = ImageOps.invert(base_img)
    clean_image = Image.new('L', (img_size, img_size), color=(255))

    if show_algorithm_progress:
        plt.ion()
        plt.imshow(np.asarray(base_img), cmap='Greys')
        plt.pause(0.2)

    peg_points_list = draw_points_on_circle((img_size/2, img_size/2),
                                            circle_diameter/2,
                                            pegs_to_draw,
                                            base_img)
    return base_img, clean_image, peg_points_list

def post_process_image(image, begin_timestamp):
    from PIL import ImageDraw
    import datetime
    cfg = load_configuration()
    peg_number = cfg['algo']['peg_number']
    num_iterations = cfg['algo']['num_iterations']
    frame_factor = cfg['algo']['frame_factor']
    end_timestamp = datetime.datetime.now()
    total_time_seconds = end_timestamp - begin_timestamp
    minutes = total_time_seconds.seconds // 60 % 60
    seconds = total_time_seconds.seconds - 60 * minutes
    formatted_time = str(minutes) + ":" + str(seconds)
    image_scale = cfg['algo']['image_resize_square']
    contrast = int(cfg['algo']['contrast'])

    display_text = f"Pegs: {peg_number}\n" \
                   f"Iterations: {num_iterations}\n" \
                   f"Frame factor: {frame_factor}\n" \
                   f"Total time [M:S]: {formatted_time}\n" \
                   f"Image scale: {image_scale}\n" \
                   f"Contrast: {contrast}"

    ImageDraw.Draw(image).text((20, 20), display_text, fill=(0))
    return image


def simulate_weave():
    import datetime
    starting_time = datetime.datetime.now()

    import Simulation.algo
    path_to_image = r"woman.jpg"

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


if __name__ == "__main__":
    final_pattern = simulate_weave()
    print(final_pattern)
    # Todo:
    # - Make contrast function to better represent real life color values of overlapping strings
    # - Implement ignore_nearest_neighbours from the configuration file.
    # - AVERAGE SCALING FOR THE COLOR [v]


