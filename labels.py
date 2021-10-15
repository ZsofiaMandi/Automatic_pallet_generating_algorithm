import copy
import math

# PUTTING LABELS ON THE BOX SIDES


def labeling(box_list_mirrored, label_side, label_place, box_x, box_y):

    box_list_mirrored = copy.deepcopy(box_list_mirrored)

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

    # Defining a starting min x and y coordinate for the boxes in orientation 0
    j = 0
    for box in box_list_mirrored:
        if box[3] == 0:
            min_coordinate_0_x = box_list_mirrored[j][0]
            min_coordinate_0_y = box_list_mirrored[j][1]
            break
        j += 1

    # Defining a starting min x and y coordinate for the boxes in orientation 1
    k = 0
    for box in box_list_mirrored:
        if box[3] == 1:
            min_coordinate_1_x = box_list_mirrored[k][0]
            min_coordinate_1_y = box_list_mirrored[k][1]
            break
        k += 1

    # Calculating the indexes for the boxes with the min and max x and y coordinate in orientation 0 and 1
    i = 0
    for box in box_list_mirrored:

        coordinate_value_x = box[0]
        coordinate_value_y = box[1]
        if box[3] == 0:
            if max_coordinate_0_x <= coordinate_value_x:
                max_coordinate_0_x = coordinate_value_x
                max_index_0_x = i
            if min_coordinate_0_x >= coordinate_value_x:
                min_coordinate_0_x = coordinate_value_x
                min_index_0_x = i
            if max_coordinate_0_y <= coordinate_value_y:
                max_coordinate_0_y = coordinate_value_y
                max_index_0_y = i
            if min_coordinate_0_y >= coordinate_value_y:
                min_coordinate_0_y = coordinate_value_y
                min_index_0_y = i
        elif box[3] == 1:
            if max_coordinate_1_x <= coordinate_value_x:
                max_coordinate_1_x = coordinate_value_x
                max_index_1_x = i
            if min_coordinate_1_x >= coordinate_value_x:
                min_coordinate_1_x = coordinate_value_x
                min_index_1_x = i
            if max_coordinate_1_y <= coordinate_value_y:
                max_coordinate_1_y = coordinate_value_y
                max_index_1_y = i
            if min_coordinate_1_y >= coordinate_value_y:
                min_coordinate_1_y = coordinate_value_y
                min_index_1_y = i
        i += 1

    # Checking if the min and max index boxes have the same starting and ending point for both orientations
    # if not, it means that the min or max from the boxes is in the middle of the pallet for one of the orientation
    # and not on the sides, in that case -1 out that index and coordinate and index,
    # so it won't match with any of the conditions at labeling
    if min_coordinate_0_x - box_x / 2 != min_coordinate_1_x - box_y / 2:
        if min_coordinate_1_x - box_y / 2 < 0:
            min_coordinate_1_x = -1
            min_index_1_x = -1
        elif min_coordinate_0_x - box_x / 2 < 0:
            min_coordinate_0_x = -1
            min_index_0_x = -1
        elif min_coordinate_0_x - box_x / 2 < min_coordinate_1_x - box_y / 2:
            min_coordinate_1_x = -1
            min_index_1_x = -1
        elif min_coordinate_0_x - box_x / 2 > min_coordinate_1_x - box_y / 2:
            min_coordinate_0_x = -1
            min_index_0_x = -1

    if min_coordinate_0_y - box_y / 2 != min_coordinate_1_y - box_x / 2:
        if min_coordinate_1_y - box_x / 2 < 0:
            min_coordinate_1_y = -1
            min_index_1_y = -1
        elif min_coordinate_0_y - box_y / 2:
            min_coordinate_0_y = -1
            min_index_0_y = -1
        elif min_coordinate_0_y - box_y / 2 < min_coordinate_1_y - box_x / 2:
            min_coordinate_1_y = -1
            min_index_1_y = -1
        elif min_coordinate_0_y - box_y / 2 > min_coordinate_1_y - box_x / 2:
            min_coordinate_0_y = -1
            min_index_0_y = -1

    if max_coordinate_0_x + box_x / 2 != max_coordinate_1_x + box_y / 2:
        if max_coordinate_0_x + box_x / 2 > max_coordinate_1_x + box_y / 2:
            max_coordinate_1_x = -1
            max_index_1_x = -1
        else:
            max_coordinate_0_x = -1
            max_index_0_x = -1

    if max_coordinate_0_y + box_y / 2 != max_coordinate_1_y + box_x / 2:
        if max_coordinate_0_y + box_y / 2 > max_coordinate_1_y + box_x / 2:
            max_coordinate_1_y = -1
            max_index_1_y = 0
        else:
            max_coordinate_0_y = -1
            max_index_0_y = -1

    # If the min and max index is equal in one orientation,
    # then finding out that on which side the box is and correcting the values
    max_coordinate_x = max(max_coordinate_0_x, max_coordinate_1_x)
    max_coordinate_y = max(max_coordinate_0_y, max_coordinate_1_y)
    min_coordinate_x = min(min_coordinate_0_x, min_coordinate_1_x)
    min_coordinate_y = min(min_coordinate_0_y, min_coordinate_1_y)
    pallet_load_x = max_coordinate_x - min_coordinate_x
    pallet_load_y = max_coordinate_y - min_coordinate_y

    if min_index_0_x == max_index_0_x:
        if box_list_mirrored[min_index_0_x][0] < pallet_load_x / 2:
            max_index_0_x = -1
        else:
            min_index_0_x = -1

    if min_index_1_x == max_index_1_x:
        if box_list_mirrored[min_index_1_x][0] < pallet_load_x / 2:
            max_index_1_x = -1
        else:
            min_index_1_x = -1

    if min_index_0_y == max_index_0_y:
        if box_list_mirrored[min_index_0_y][0] < pallet_load_y / 2:
            max_index_0_y = -1
        else:
            min_index_0_y = -1

    if min_index_1_y == max_index_1_y:
        if box_list_mirrored[min_index_1_y][0] < pallet_load_y / 2:
            max_index_1_y = -1
        else:
            min_index_1_y = -1

    # The label is on the Front side of the box in the beginning (along with x, the up side from the top view)
    if label_side == "Front":
        for box in box_list_mirrored:

            # If box orientation is 0 -> it's correct, if 1 -> all labels will be on the right side
            if label_place == "Front":
                pass

            # If box orientation is 0 -> rotate with 180° to orientation 2, if 1 -> all labels will be on the right side
            elif label_place == "Back":
                if box[3] == 0:
                    box[3] = 2

            # If box orientation is 0 -> all labels will be on the front side, if 1 -> it's correct
            elif label_place == "Right":
                pass

            # If box orientation is 1 -> rotate with 180° to orientation 3, if 0 -> all labels will be on the front side
            elif label_place == "Left":
                if box[3] == 1:
                    box[3] = 3

            elif label_place == "Outwards":
                if min_index_0_y >= 0:
                    if box[3] == 0 and box[1] == box_list_mirrored[min_index_0_y][1]:    # Front
                        pass
                if min_index_1_x >= 0:
                    if box[3] == 1 and box[0] == box_list_mirrored[min_index_1_x][0]:    # Left
                        box[3] = 3
                if max_index_0_y >= 0:
                    if box[3] == 0 and box[1] == box_list_mirrored[max_index_0_y][1]:    # Back
                        box[3] = 2
                if max_index_1_x >= 0:
                    if box[3] == 1 and box[0] == box_list_mirrored[max_index_1_x][0]:    # Right
                        pass

    # The label is on the Back side of the box in the beginning (along with x, the down side from the top view)
    elif label_side == "Back":
        for box in box_list_mirrored:

            # If box orientation is 0 -> it's correct, if 1 -> all labels will be on the left side
            if label_place == "Back":
                pass

            # If box orientation is 0 -> rotate with 180° to orientation 2, if 1 -> all labels will be on the left side
            elif label_place == "Front":
                if box[3] == 0:
                    box[3] = 2

            # If box orientation is 0 -> all labels will be on the back side, if 1 -> it's correct
            elif label_place == "Left":
                pass

            # If box orientation is 1 -> rotate with 180° to orientation 3, if 0 -> all labels will be on the left side
            elif label_place == "Right":
                if box[3] == 1:
                    box[3] = 3

            elif label_place == "Outwards":
                if min_index_0_y >= 0:
                    if box[3] == 0 and box[1] == box_list_mirrored[min_index_0_y][1]:    # Front
                        box[3] = 2
                if min_index_1_x >= 0:
                    if box[3] == 1 and box[0] == box_list_mirrored[min_index_1_x][0]:    # Left
                        pass
                if max_index_0_y >= 0:
                    if box[3] == 0 and box[1] == box_list_mirrored[max_index_0_y][1]:    # Back
                        pass
                if max_index_1_x >= 0:
                    if box[3] == 1 and box[0] == box_list_mirrored[max_index_1_x][0]:    # Right
                        box[3] = 3

    elif label_side == "Left":
        for box in box_list_mirrored:

            # If box orientation is 1 -> rotate with 180° to orientation 3, if 0 -> all labels will be on the left side
            if label_place == "Back":
                if box[3] == 1:
                    box[3] = 3

            # If box orientation is 1 -> it's correct, if 0 -> all labels will be on the left side
            elif label_place == "Front":
                pass

            # If box orientation is 1 -> all labels will be on the front side, if 0 -> it's correct
            elif label_place == "Left":
                pass

            # If box orientation is 0 -> rotate with 180° to orientation 2, if 1 -> all labels will be on the front side
            elif label_place == "Right":
                if box[3] == 0:
                    box[3] = 2

            elif label_place == "Outwards":
                if min_index_1_y >= 0:
                    if box[3] == 1 and box[1] == box_list_mirrored[min_index_1_y][1]:    # Front
                        pass
                if min_index_0_x >= 0:
                    if box[3] == 0 and box[0] == box_list_mirrored[min_index_0_x][0]:    # Left
                        pass
                if max_index_1_y >= 0:
                    if box[3] == 1 and box[1] == box_list_mirrored[max_index_1_y][1]:    # Back
                        box[3] = 3
                if max_index_0_x >= 0:
                    if box[3] == 0 and box[0] == box_list_mirrored[max_index_0_x][0]:    # Right
                        box[3] = 2

    elif label_side == "Right":
        for box in box_list_mirrored:

            # If box orientation is 1 -> rotate with 180° to orientation 3, if 0 -> all labels will be on the left side
            if label_place == "Back":
                pass

            # If box orientation is 1 -> it's correct, if 0 -> all labels will be on the left side
            elif label_place == "Front":
                if box[3] == 1:
                    box[3] = 3

            # If box orientation is 1 -> all labels will be on the front side, if 0 -> it's correct
            elif label_place == "Left":
                if box[3] == 0:
                    box[3] = 2

            # If box orientation is 0 -> rotate with 180° to orientation 2, if 1 -> all labels will be on the front side
            elif label_place == "Right":
                pass

            elif label_place == "Outwards":
                if min_index_1_y >= 0:
                    if box[3] == 1 and box[1] == box_list_mirrored[min_index_1_y][1]:    # Front
                        box[3] = 3
                if min_index_0_x >= 0:
                    if box[3] == 0 and box[0] == box_list_mirrored[min_index_0_x][0]:    # Left
                        box[3] = 2
                if max_index_1_y >= 0:
                    if box[3] == 1 and box[1] == box_list_mirrored[max_index_1_y][1]:    # Back
                        pass
                if max_index_0_x >= 0:
                    if box[3] == 0 and box[0] == box_list_mirrored[max_index_0_x][0]:    # Right
                        pass

    return box_list_mirrored
