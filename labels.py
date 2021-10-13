import copy
import math

# PUTTING LABELS ON THE BOX SIDES


def labeling(input_box_list, label_side, label_place):

    box_list_labeled = copy.deepcopy(input_box_list)

    # Finding the first and last box in the list for both orientations
    # Max and min for boxes with orientation 0
    max_index_0_x = 0
    min_index_0_x = 0
    max_index_0_y = 0
    min_index_0_y = 0
    min_coordinate_0_x = 0
    min_coordinate_0_y = 0
    max_coordinate_0_x = 0
    max_coordinate_0_y = 0

    # Max and min for boxes with orientation 1
    max_index_1_x = 0
    min_index_1_x = 0
    max_index_1_y = 0
    min_index_1_y = 0
    min_coordinate_1_x = 0
    min_coordinate_1_y = 0
    max_coordinate_1_x = 0
    max_coordinate_1_y = 0

    j = 0
    for box in box_list_labeled:
        if box[3] == 0:
            min_coordinate_0_x = box_list_labeled[j][0]
            min_coordinate_0_y = box_list_labeled[j][1]
            break
        j += 1

    k = 0
    for box in box_list_labeled:
        if box[3] == 1:
            min_coordinate_1_x = box_list_labeled[k][0]
            min_coordinate_1_y = box_list_labeled[k][1]
            break
        k += 1

    i = 0
    for box in box_list_labeled:

        coordinate_value_x = box[0]
        coordinate_value_y = box[1]

        if box[3] == 0:
            if max_coordinate_0_x <= coordinate_value_x:
                max_coordinate_0_x = coordinate_value_x
                max_index_0_x = i
            if min_coordinate_0_x > coordinate_value_x:
                min_coordinate_0_x = coordinate_value_x
                min_index_0_x = i
            if max_coordinate_0_y <= coordinate_value_y:
                max_coordinate_0_y = coordinate_value_y
                max_index_0_y = i
            if min_coordinate_0_y > coordinate_value_y:
                min_coordinate_0_y = coordinate_value_y
                min_index_0_y = i
        elif box[3] == 1:
            if max_coordinate_1_x <= coordinate_value_x:
                max_coordinate_1_x = coordinate_value_x
                max_index_1_x = i
            if min_coordinate_1_x > coordinate_value_x:
                min_coordinate_1_x = coordinate_value_x
                min_index_1_x = i
            if max_coordinate_1_y <= coordinate_value_y:
                max_coordinate_1_y = coordinate_value_y
                max_index_1_y = i
            if min_coordinate_1_y > coordinate_value_y:
                min_coordinate_1_y = coordinate_value_y
                min_index_1_y = i
        i += 1

    # The label is on the front side of the box in the beginning (along with x, the up side from the top view)
    if label_side == "Front":
        for box in box_list_labeled:

            # If box orientation is 0 -> it's correct, if 1 -> all labels will be on the right side
            if label_place == "Front":
                pass

            # If box orientation is 0 -> rotate with 180° to orientation 3, if 1 -> all labels will be on the right side
            elif label_place == "Back":
                if box[3] == 0:
                    box[3] = 3

            # If box orientation is 0 -> all labels will be on the front side, if 1 -> it's correct
            elif label_place == "Right":
                pass

            # If box orientation is 0 -> rotate with 180° to orientation 3, if 1 -> all labels will be on the right side
            elif label_place == "Left":
                if box[3] == 1:
                    box[3] = 2

            elif label_place == "Outwards":

                if box[3] == 0 and box[1] == input_box_list[min_index_0_y][1]:      # Front
                    pass
                elif box[3] == 1 and box[0] == input_box_list[min_index_1_x][0]:    # Left
                    box[3] = 2
                elif box[3] == 0 and box[1] == input_box_list[max_index_0_y][1]:    # Back
                    box[3] = 3
                elif box[3] == 1 and box[0] == input_box_list[max_index_1_x][0]:    # Right
                    pass

    return box_list_labeled
