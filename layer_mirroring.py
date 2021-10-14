import copy


def mirroring_layer(box_list, x, y, pallet_x, pallet_y, box_x, box_y, middle=False):

    box_list_mirrored = copy.deepcopy(box_list)

    # finding the las box coordinates in the list:
    max_index = 0
    min_index = 0
    max_coordinate = 0
    min_coordinate = box_list_mirrored[0][0] + box_list_mirrored[0][1]
    i = 0
    for box in box_list_mirrored:
        coordinate_value = box[0] + box[1]
        if max_coordinate < coordinate_value:
            max_coordinate = coordinate_value
            max_index = i
        if min_coordinate > coordinate_value:
            min_coordinate = coordinate_value
            min_index = i
        i += 1

    # Checking the last box x and y dimensions
    if box_list_mirrored[max_index][3] == 0:
        max_x = box_x
        max_y = box_y
    elif box_list_mirrored[max_index][3] == 1:
        max_x = box_y
        max_y = box_x

    # Checking the first box x and y dimensions
    if box_list_mirrored[min_index][3] == 0:
        min_x = box_x
        min_y = box_y
    elif box_list_mirrored[min_index][3] == 1:
        min_x = box_y
        min_y = box_x

    # Calculating the loading of the pallet
    load_x_max = box_list_mirrored[max_index][0] + max_x / 2
    load_y_max = box_list_mirrored[max_index][1] + max_y / 2
    load_x_min = box_list_mirrored[min_index][0] - min_x / 2
    load_y_min = box_list_mirrored[min_index][1] - min_y / 2

    # Calculating the offsets along the pallet X and Y dimensions whit centering
    middle_offset_x = 0
    middle_offset_y = 0
    if middle:
        middle_offset_x = (pallet_x - (load_x_max - load_x_min)) / 2
        middle_offset_y = (pallet_y - (load_y_max - load_y_min)) / 2

    # Mirroring all of the boxes in the output box list along the X, Y or X and Y axes
    for box in box_list_mirrored:
        if x:
            box[0] += load_x_max - 2 * box[0] + middle_offset_x
        if y:
            box[1] += load_y_max - 2 * box[1] + middle_offset_y

    return box_list_mirrored
