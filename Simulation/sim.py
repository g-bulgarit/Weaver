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
    draw.ellipse(ellipse_size, outline=None, fill=(255, 0, 0))


def draw_points_on_circle(config_obj, center_tuple, radius, num_points, base_img):
    from math import sin, cos, radians
    center_x, center_y = center_tuple
    point_radius = int(config_obj['visual']['pegs_radius'])

    peg_point_list = []

    for angle in range(0, 360, round(360/num_points)):
        # Calculate the point coordinates on the circle
        point_x = center_x + (radius * cos(radians(angle)))
        point_y = center_y + (radius * sin(radians(angle)))
        point_coords = (point_x, point_y)

        peg_point_list.append(point_coords)

        draw_point(point_coords, point_radius, base_img)
    return peg_point_list


def prepare_image(path_to_image_file, config_obj):
    from PIL import Image
    image_file = Image.open(path_to_image_file)
    base_img = image_file.resize((800, 800))
    pegs_to_draw = int(config_obj['algo']['peg_number'])
    peg_points_list = draw_points_on_circle(config, (400, 400), 300, pegs_to_draw, base_img)
    base_img.show()
    return base_img, peg_points_list


if __name__ == "__main__":

    path_to_image = r"Koala.jpg"

    config = load_configuration()
    image, point_list = prepare_image(path_to_image, config)
    print(point_list)
