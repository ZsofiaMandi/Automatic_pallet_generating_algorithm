import copy


def stretching(output_box_list, pallet_x, pallet_y, box_x, box_y, num_x, num_y):

    box_list_mirrored = copy.deepcopy(output_box_list)

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
    if box_list_mirrored[max_index][3] == 0 or box_list_mirrored[max_index][3] == 2:
        max_x = box_x
        max_y = box_y
    elif box_list_mirrored[max_index][3] == 1 or box_list_mirrored[max_index][3] == 3:
        max_x = box_y
        max_y = box_x

    # Checking the first box x and y dimensions
    if box_list_mirrored[min_index][3] == 0 or box_list_mirrored[max_index][3] == 2:
        min_x = box_x
        min_y = box_y
    elif box_list_mirrored[min_index][3] == 1 or box_list_mirrored[max_index][3] == 3:
        min_x = box_y
        min_y = box_x

    pallet_load_x = pallet_x - (box_list_mirrored[max_index][0] + max_x / 2
                                - box_list_mirrored[min_index][0] - min_x / 2)

    pallet_load_y = pallet_y - (box_list_mirrored[max_index][1] + max_y / 2
                                - box_list_mirrored[min_index][1] - min_y / 2)

    half_of_pallet_x = pallet_load_x / 2
    half_of_pallet_y = pallet_load_y / 2

    offset_x = (pallet_x - pallet_load_x) / (num_x - 1)

    return box_list_mirrored
