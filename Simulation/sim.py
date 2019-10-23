def load_configuration():
    import configparser
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config

def draw_point(center_tuple, point_radius, base_image):
    from PIL import ImageDraw

    centerX, centerY = center_tuple
    x1 = centerX - (point_radius/2)
    x2 = centerX + (point_radius / 2)
    y1 = centerY - (point_radius / 2)
    y2 = centerY + (point_radius / 2)
    ellipse_size = (x1, y1, x2, y2)

    draw = ImageDraw.Draw(base_image)
    draw.ellipse(ellipse_size, outline=None, fill=(255,0,0))





def draw_points_on_circle(config, center_tuple, radius, num_points, base_img):
    from math import sin, cos, radians
    centerX, centerY = center_tuple
    point_radius = int(config['visual']['pegs_radius'])

    peg_point_list = []

    for angle in range(0, 360, round(360/num_points)):
        # Calculate the point coordinates on the circle
        pointX = centerX + (radius * cos(radians(angle)))
        pointY = centerY + (radius * sin(radians(angle)))
        point_coords = (pointX, pointY)

        peg_point_list.append(point_coords)

        draw_point(point_coords, point_radius, base_img)
    return peg_point_list



def prepare_image(path_to_image, config):
    from PIL import Image
    image = Image.open(path_to_image)
    base_img = image.resize((800,800))
    pegs_to_draw = int(config['algo']['peg_number'])
    peg_points_list = draw_points_on_circle(config, (400,400), 300, pegs_to_draw, base_img)
    base_img.show()
    return base_img, peg_points_list


if __name__ == "__main__":

    path_to_image = r"Koala.jpg"

    config = load_configuration()
    image, point_list = prepare_image(path_to_image, config)
    print(point_list)



