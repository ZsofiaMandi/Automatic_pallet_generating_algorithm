import copy

# CENTERING LAYERS


def centering(output_box_list, pallet_x, pallet_y, box_x, box_y):

    box_list_centered = copy.deepcopy(output_box_list)

    max_coordinate = 0
    i = 0
    for box in box_list_centered:
        coordinate_value = box[0] + box[1]
        if max_coordinate < coordinate_value:
            max_coordinate = coordinate_value
            max_index = i
        i += 1
    # Checking the las box's x and y dimensions
    if box_list_centered[max_index][3] == 0:
        max_x = box_x
        max_y = box_y
    elif box_list_centered[max_index][3] == 1:
        max_x = box_y
        max_y = box_x
    # Calculating till where is the pallet loaded with the boxes
    load_x = box_list_centered[max_index][0] + max_x / 2
    load_y = box_list_centered[max_index][1] + max_y / 2

    x_offset = (pallet_x - load_x) / 2
    y_offset = (pallet_y - load_y) / 2

    for box in box_list_centered:
        box[0] += x_offset
        box[1] += y_offset

    return box_list_centered
