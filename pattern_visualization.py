from graphics import *
from generating_boxlists import generate_boxes_oop, generate_boxes_top, generate_boxes_sp
import math

# VISUALIZING THE PATTERN LAYERS IN 2 DIMENSIONS


# Defining the function what draws one layer from the output box list and from the input values
def drawing_pallet_pattern(pallet_x, pallet_y, box_dim1, box_dim2, output_box_list, pattern_name,
                           color=color_rgb(200, 200, 200), coloring_directions="None"):

    if (pallet_x < box_dim1 and pallet_x < box_dim2) or (pallet_y < box_dim1 and pallet_y < box_dim2):
        raise ValueError('Invalid pallet - box combination, please make a pallet size at minimum as big as one box')

    # Calculating the window size
    a = 50  # ratios for making the same size of dimensions from the output_box_list
    b = 100

    rect_x = pallet_x * a
    rect_y = pallet_y * a

    win_x = rect_x + 2 * b
    win_y = rect_y + 2 * b

    win = GraphWin(pattern_name, win_x, win_y)

    offset_x = 0
    offset_y = 0

    # drawing the surrounding rectangle what represents the pallet
    pt_pallet1 = Point(b, b)
    pt_pallet2 = Point(100 + rect_x, b + rect_y)
    pallet = Rectangle(pt_pallet1, pt_pallet2)
    pallet.setOutline(color_rgb(120, 120, 120))
    pallet.setWidth(5)
    pallet.draw(win)

    # drawing the rectangles representing the boxes
    for box in output_box_list:

        if box[3] == 0:
            box_x = box_dim1 * a
            box_y = box_dim2 * a
        elif box[3] == 1:
            box_x = box_dim2 * a
            box_y = box_dim1 * a

        x = b + box[0] * a + offset_x - box_x / 2
        y = b + box[1] * a + offset_y - box_y / 2

        pt_box1 = Point(x, y)
        pt_box2 = Point(x + box_x, y + box_y)

        box = Rectangle(pt_box1, pt_box2)
        box.setOutline(color_rgb(100, 100, 100))
        box.setWidth(2)
        box.setFill(color)
        box.draw(win)

    #  Writing a label with the number of packed boxes
    packed_boxes = len(output_box_list)
    pt_label = Point(win_x / 2, b / 4)
    label = Text(pt_label, "Packed boxes: {}".format(packed_boxes))
    label.draw(win)

    #  Writing a label with the loading of the pallet
    usage = round(packed_boxes * box_x * box_y / (rect_x * rect_y) * 100, 2)
    """
    "  Put below line in the unpacked boxes section below? For consistency, like above in the packed boxes section.
    """
    unpacked_boxes = math.floor(rect_x * rect_y / (box_x * box_y)) - packed_boxes

    pt_usage_label = Point(win_x / 2, 3 * b / 4)
    usage_label = Text(pt_usage_label, "Pallet load: {}%".format(usage))
    usage_label.draw(win)

    """
    "  Wrong comment.
    """
    #  Writing a label with the number of the packed boxes
    pt_unpacked_label = Point(win_x / 2, 2 * b / 4)
    unpacked_label = Text(pt_unpacked_label, "Unpacked boxes: {}".format(unpacked_boxes))
    unpacked_label.draw(win)

    win.getMouse()


# Calling the drawing for every layer and pattern to test the output
def main():
    # Input parameters
    pallet_x = 11
    pallet_y = 9
    box_x = 2
    box_y = 3
    color_b = color_rgb(211, 204, 236)
    color_c = color_rgb(239, 228, 176)

    # Generating the required output box lists with the box coordinates for each layer and pattern
    oop = generate_boxes_oop(pallet_x, pallet_y, box_x, box_y, middle=True)
    top = generate_boxes_top(pallet_x, pallet_y, box_x, box_y, middle=True)
    sp = generate_boxes_sp(pallet_x, pallet_y, box_x, box_y, middle=True)

    oop_layer_1 = oop[0]
    oop_layer_2 = oop[1]
    top_layer_1 = top[0]
    top_layer_2 = top[1]
    sp_layer_1 = sp[0]
    sp_layer_2 = sp[1]

    # Drawing the different layers
    drawing_pallet_pattern(pallet_x, pallet_y, box_x, box_y, oop_layer_1, "One order pattern - Layer A")
    drawing_pallet_pattern(pallet_x, pallet_y, box_x, box_y, oop_layer_2, "One order pattern - Layer B", color_c)
    drawing_pallet_pattern(pallet_x, pallet_y, box_x, box_y, top_layer_1, "Two order pattern - Layer A")
    drawing_pallet_pattern(pallet_x, pallet_y, box_x, box_y, top_layer_2, "Two order pattern - Layer B", color_b)
    drawing_pallet_pattern(pallet_x, pallet_y, box_x, box_y, sp_layer_1, "Squared pattern - Layer A")
    drawing_pallet_pattern(pallet_x, pallet_y, box_x, box_y, sp_layer_2, "Squared pattern - Layer B", color_b)


main()

