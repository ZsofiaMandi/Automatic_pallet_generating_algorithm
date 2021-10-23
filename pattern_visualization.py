from graphics import *
from generating_boxlists import generate_boxes_oop, generate_boxes_top, generate_boxes_sp
import math


# VISUALIZING THE PATTERN LAYERS IN 2 DIMENSIONS


# Defining the function what draws one layer from the output box list and from the input values
def drawing_pallet_pattern(pallet_x, pallet_y, box_dim1, box_dim2, output_box_list, pattern_name,
                           labeling=False, label_side="None", color=color_rgb(200, 200, 200)):
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

    # drawing the surrounding rectangle what represents the pallet
    pt_pallet1 = Point(b, b)
    pt_pallet2 = Point(100 + rect_x, b + rect_y)
    pallet = Rectangle(pt_pallet1, pt_pallet2)
    pallet.setOutline(color_rgb(120, 120, 120))
    pallet.setWidth(5)
    pallet.draw(win)

    # drawing the rectangles representing the boxes
    for box in output_box_list:

        if box[3] == 0 or box[3] == 2:
            box_x = box_dim1 * a  # Current box dimension along pallet X side
            box_y = box_dim2 * a  # Current box dimension along pallet Y side
        elif box[3] == 1 or box[3] == 3:
            box_x = box_dim2 * a  # Current box dimension along pallet X side
            box_y = box_dim1 * a  # Current box dimension along pallet Y side

        x = b + box[0] * a - box_x / 2  # Current box left-up corner's coordinate's x component
        y = b + box[1] * a - box_y / 2  # Current box left-up corner's coordinate's y component

        pt_box1 = Point(x, y)                   # Current box left-down corner
        pt_box2 = Point(x + box_x, y + box_y)   # Current box right-down corner

        box_draw = Rectangle(pt_box1, pt_box2)
        box_draw.setOutline(color_rgb(100, 100, 100))
        box_draw.setWidth(2)
        box_draw.setFill(color)
        box_draw.draw(win)

    # Drawing box labels
    if labeling and label_side != "None":

        for box in output_box_list:

            if box[3] == 0 or box[3] == 2:
                box_x = box_dim1 * a  # Current box dimension along pallet X side
                box_y = box_dim2 * a  # Current box dimension along pallet Y side
            elif box[3] == 1 or box[3] == 3:
                box_x = box_dim2 * a  # Current box dimension along pallet X side
                box_y = box_dim1 * a  # Current box dimension along pallet Y side

            x = b + box[0] * a - box_x / 2  # Current box left-up corner's coordinate's x component
            y = b + box[1] * a - box_y / 2  # Current box left-up corner's coordinate's y component

            if label_side == "Front":
                param_0 = 0
                param_1 = 1
                param_2 = 2
                param_3 = 3
            elif label_side == "Right":
                param_0 = 3
                param_1 = 0
                param_2 = 1
                param_3 = 2
            elif label_side == "Back":
                param_0 = 2
                param_1 = 3
                param_2 = 0
                param_3 = 1
            elif label_side == "Left":
                param_0 = 1
                param_1 = 2
                param_2 = 3
                param_3 = 0

            if box[3] == param_0:
                pt_label1 = Point(x + box_x / 10, y)
                pt_label2 = Point(x + box_x - box_x / 10, y)
            elif box[3] == param_1:
                pt_label1 = Point(x + box_x, y + box_y / 10)
                pt_label2 = Point(x + box_x, y + box_y - box_y / 10)
            elif box[3] == param_2:
                pt_label1 = Point(x + box_x / 10, y + box_y)
                pt_label2 = Point(x + box_x - box_x / 10, y + box_y)
            elif box[3] == param_3:
                pt_label1 = Point(x, y + box_y / 10)
                pt_label2 = Point(x, y + box_y - box_y / 10)

            label_line = Line(pt_label1, pt_label2)
            label_line.setOutline(color_rgb(128, 0, 64))
            label_line.setWidth(3.5)
            label_line.draw(win)

    #  Writing a label with the number of packed boxes
    packed_boxes = len(output_box_list)
    pt_label = Point(win_x / 2, b / 4)
    label = Text(pt_label, "Packed boxes: {}".format(packed_boxes))
    label.draw(win)

    #  Writing a label with the loading of the pallet
    usage = round(packed_boxes * box_x * box_y / (rect_x * rect_y) * 100, 2)
    unpacked_boxes = math.floor(rect_x * rect_y / (box_x * box_y)) - packed_boxes
    pt_usage_label = Point(win_x / 2, 3 * b / 4)
    usage_label = Text(pt_usage_label, "Pallet load: {}%".format(usage))
    usage_label.draw(win)

    #  Writing a label with the number of the unpacked boxes
    pt_unpacked_label = Point(win_x / 2, 2 * b / 4)
    unpacked_label = Text(pt_unpacked_label, "Unpacked boxes: {}".format(unpacked_boxes))
    unpacked_label.draw(win)

    win.getMouse()


# Calling the drawing for every layer and pattern to test the output
def main():
    # Input parameters
    pallet_x = 11
    pallet_y = 7
    pallet_z = 10
    box_x = 2
    box_y = 3
    box_z = 110 / 10 / 5
    color_b = color_rgb(211, 204, 236)
    color_c = color_rgb(239, 228, 176)

    # Generating the required output box lists with the box coordinates for each layer and pattern
    oop = generate_boxes_oop(pallet_x, pallet_y, box_x, box_y, middle=True,
                             label_side="Right", label_place="Outwards")
    top = generate_boxes_top(pallet_x, pallet_y, box_x, box_y, middle=True,
                             label_side="Right", label_place="Outwards")
    sp = generate_boxes_sp(pallet_x, pallet_y, box_x, box_y, middle=True,
                           label_side="Right", label_place="Outwards")

    oop_layer_1 = oop[0]
    oop_layer_2 = oop[1]
    top_layer_1 = top[0]
    top_layer_2 = top[1]
    sp_layer_1 = sp[0]
    sp_layer_2 = sp[1]

    print(top_layer_2)

    #Drawing the different layers
    drawing_pallet_pattern(pallet_x, pallet_y, box_x, box_y, oop_layer_1, "One order pattern - Layer A",
                           labeling=True, label_side="Right")
    drawing_pallet_pattern(pallet_x, pallet_y, box_x, box_y, oop_layer_2, "One order pattern - Layer B",
                           labeling=True, label_side="Right", color=color_c)
    drawing_pallet_pattern(pallet_x, pallet_y, box_x, box_y, top_layer_1, "Two order pattern - Layer A",
                           labeling=True, label_side="Right")
    drawing_pallet_pattern(pallet_x, pallet_y, box_x, box_y, top_layer_2, "Two order pattern - Layer B",
                           labeling=True, label_side="Right", color=color_b)
    drawing_pallet_pattern(pallet_x, pallet_y, box_x, box_y, sp_layer_1, "Squared pattern - Layer A",
                           labeling=True, label_side="Right")
    drawing_pallet_pattern(pallet_x, pallet_y, box_x, box_y, sp_layer_2, "Squared pattern - Layer B",
                           labeling=True, label_side="Right", color=color_b)


main()
