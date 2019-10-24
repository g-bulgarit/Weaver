def load_configuration():
    import configparser
    config_reader = configparser.ConfigParser()
    config_reader.read('config.ini')
    return config_reader


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


def draw_points_on_circle(config_obj, center_tuple, radius, num_points, base_img):
    from math import sin, cos, radians
    from PIL import Image
    center_x, center_y = center_tuple
    point_radius = int(config_obj['visual']['pegs_radius'])

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

    if config_obj.getboolean('debug', 'show_image_with_pegs'):
        combined_image = Image.blend(base_img, point_img, 0.5)
        combined_image.show()
    return peg_point_list


def prepare_image(path_to_image_file, config_obj):
    from PIL import Image, ImageDraw

    pegs_to_draw = int(config_obj['algo']['peg_number'])
    img_size = int(config_obj['algo']['image_resize_square'])
    circle_diameter = int(config_obj['algo']['circle_diameter'])

    image_file = Image.open(path_to_image_file)
    base_img = image_file.resize((img_size, img_size))

    peg_points_list = draw_points_on_circle(config,
                                            (img_size/2, img_size/2),
                                            circle_diameter/2,
                                            pegs_to_draw,
                                            base_img)
    return base_img, peg_points_list


if __name__ == "__main__":
    from Simulation.algo import *
    from PIL import Image, ImageOps
    import numpy as np

    path_to_image = r"Marilyn.jpg"

    config = load_configuration()
    starting_peg = int(config['algo']['starting_peg'])
    num_iterations = int(config['algo']['num_iterations'])

    image, point_list = prepare_image(path_to_image, config)
    clean_image = Image.new('RGB', (1600, 1600), color=(255, 255, 255))

    print(point_list)
    pattern = get_pattern(image, point_list, starting_peg, num_iterations, clean_image=clean_image)

    old_image = Image.open(path_to_image).resize((1600, 1600))
    old_image_buf = np.asarray(old_image)
    image_buf = np.asarray(image)

    diff = image_buf - old_image_buf

    final_image = Image.fromarray(diff)
    final_image = ImageOps.invert(final_image)

    final_image.show()
    clean_image.show()

    print(pattern)

