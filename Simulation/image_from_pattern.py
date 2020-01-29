from Simulation.algo import set_all_pixels_black, load_configuration
from Simulation.sim import draw_points_on_circle
from gooey import GooeyParser, Gooey

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


def draw_from_pattern(pattern, point_list, canvas, override_contrast=None, trim_amt=None):
    cfg = load_configuration()
    trim_factor = int(cfg['parser']['pattern_trim'])
    if trim_amt != None:
        trim_factor = trim_amt
    else:
        if trim_factor > 100 or trim_factor <= 0:
            raise Exception("Trim factor is not between 0 and 100")

    pattern_list = pattern.split(",")
    pattern_list = pattern_list[0:int(len(pattern_list) * trim_factor/100)]
    for move in range(len(pattern_list) - 1):
        set_all_pixels_black(canvas,
                             point_list[int(pattern_list[move])],
                             point_list[int(pattern_list[move + 1])],
                             override_contrast)


@Gooey(program_name="Weaver: Pattern to Image")
def main():
    from PIL import Image
    parser = GooeyParser(description="Supply .wv file to get the image.")
    parser.add_argument('Filename', widget="FileChooser")
    parser.add_argument('--Contrast',
                        help="Number from 1-100%, defines how dark each line is.",
                        default=None,
                        gooey_options={
                            'validator': {
                                'test': '1<=int(user_input)<= 100',
                                'message': 'Contrast must be in the specified range!'
                            }
                        }
                        )
    parser.add_argument('--Trim',
                        help="Number from 1-100%, defines how much of the generated pattern to use.\n"
                             "Could be beneficial if there are too many windings.",
                        default=None,
                        gooey_options={
                            'validator': {
                                'test': '1<=int(user_input)<= 100',
                                'message': 'Pattern trim must be in the specified range!'
                            }
                        }
                        )
    args = parser.parse_args()

    peg_number, num_iterations, image_scale, contrast, circ_diameter, pattern = parse_file(args.Filename)
    if args.Contrast != None:
        contrast = int(args.Contrast)*255//100
        print(contrast)
    if args.Trim != None:
        trim = int(args.Trim)*255//100
    # Make new image with the correct size
    canvas = Image.new('L', (image_scale, image_scale), color=(255))
    # Get list of points on the circle
    point_list = draw_points_on_circle((image_scale / 2, image_scale / 2),
                                       circ_diameter / 2,
                                       peg_number,
                                       canvas)
    draw_from_pattern(pattern, point_list, canvas, override_contrast=contrast, trim_amt=trim)
    canvas.show()

if __name__ == "__main__":
    main()