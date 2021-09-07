from pattern_loadings import one_order_pattern, two_order_pattern, squared_pattern


# Getting the best results from each pattern:
def generate_boxes_oop(pallet_x, pallet_y, box_x, box_y, middle=False, label_side="None", label_place="None"):
    box_sides = [box_x, box_y]

    output_box_list = []
    output_box_list_rotated = []

    result_oop_0 = one_order_pattern(pallet_x, pallet_y, box_x, box_y, 0)
    result_oop_1 = one_order_pattern(pallet_x, pallet_y, box_x, box_y, 1)

    if result_oop_0[0] >= result_oop_1[0]:
        orientation = 0
        rotated = 1
        box_0 = box_x
        box_1 = box_y
    else:
        orientation = 1
        rotated = 0
        box_1 = box_y
        box_0 = box_x

    result_oop = one_order_pattern(pallet_x, pallet_y, box_x, box_y, orientation)
    num_x = result_oop[2]
    num_y = result_oop[3]

    for i in range(num_x):
        box_coordinate = [0, 0, 0, orientation]
        box_coordinate[0] = box_0 * i + box_0 / 2
        for j in range(num_y):
            box_coordinate = [box_coordinate[0], 0, 0, orientation]
            box_coordinate[1] = box_1 * j + box_1 / 2
            output_box_list.append(box_coordinate)

    # Making a rotated second layer

    result_oop_rotated = one_order_pattern(pallet_x, pallet_y, box_x, box_y, rotated)
    num_x = result_oop_rotated[2]
    num_y = result_oop_rotated[3]

    for i in range(num_x):
        box_coordinate_rotated = [0, 0, 0, rotated]
        box_coordinate_rotated[0] = box_1 * i + box_1 / 2
        for j in range(num_y):
            box_coordinate_rotated = [box_coordinate_rotated[0], 0, 0, rotated]
            box_coordinate_rotated[1] = box_0 * j + box_0 / 2
            output_box_list_rotated.append(box_coordinate_rotated)

    # Aligning the pattern to the middle of the pallet
    if middle and len(output_box_list) > 0:
        if output_box_list[-1][3] == 0 or output_box_list[-1][3] == 2:
            load_x = output_box_list[-1][0] + box_x / 2
            load_y = output_box_list[-1][1] + box_y / 2
        elif output_box_list[-1][3] == 1 or output_box_list[-1][3] == 3:
            load_x = output_box_list[-1][0] + box_y / 2
            load_y = output_box_list[-1][1] + box_x / 2

        x_offset = (pallet_x - load_x) / 2
        y_offset = (pallet_y - load_y) / 2

        for box in output_box_list:
            box[0] += x_offset
            box[1] += y_offset

        if output_box_list_rotated[-1][3] == 0 or output_box_list_rotated[-1][3] == 2:
            load_x_rotated = output_box_list_rotated[-1][0] + box_x / 2
            load_y_rotated = output_box_list_rotated[-1][1] + box_y / 2
        elif output_box_list_rotated[-1][3] == 1 or output_box_list_rotated[-1][3] == 3:
            load_x_rotated = output_box_list_rotated[-1][0] + box_y / 2
            load_y_rotated = output_box_list_rotated[-1][1] + box_x / 2

        x_offset_rotated = (pallet_x - load_x_rotated) / 2
        y_offset_rotated = (pallet_y - load_y_rotated) / 2

        for box in output_box_list_rotated:
            box[0] += x_offset_rotated
            box[1] += y_offset_rotated

    print("OOP output box list:             ", output_box_list)
    print("OOP rotated output box list:     ", output_box_list_rotated)

    return [output_box_list, output_box_list_rotated]


def generate_boxes_top(pallet_x, pallet_y, box_x, box_y, middle=False, swapping=False,
                       label_side="None", label_place="None"):
    output_box_list = []

    # Selecting the pattern with the most packed boxes
    result_top_1 = two_order_pattern(pallet_x, pallet_y, box_x, box_y, 0)
    result_top_2 = two_order_pattern(pallet_x, pallet_y, box_x, box_y, 1)

    pattern_index_o1 = 0
    pattern_index_o2 = 0
    for i in range(len(result_top_1)):
        if result_top_1[pattern_index_o1][4] <= result_top_1[i][4]:
            pattern_index_o1 = i
    for i in range(len(result_top_2)):
        if result_top_2[pattern_index_o2][4] <= result_top_2[i][4]:
            pattern_index_o2 = i

    if result_top_1[pattern_index_o1][4] >= result_top_2[pattern_index_o2][4]:
        orientation_1 = 0
        orientation_2 = 1
        box_0 = box_x
        box_1 = box_y
        pattern_index = pattern_index_o1
    else:
        orientation_1 = 1
        orientation_2 = 0
        box_0 = box_y
        box_1 = box_x
        pattern_index = pattern_index_o2

    result_top = two_order_pattern(pallet_x, pallet_y, box_x, box_y, orientation_1)
    num_x_o1 = result_top[pattern_index][0]
    num_y_o1 = result_top[pattern_index][1]
    num_x_o2 = result_top[pattern_index][2]
    num_y_o2 = result_top[pattern_index][3]

    x_start = num_x_o1 * box_0

    # checking if there is remaining space at the end of the rows and columns or not and splitting them
    rem_space_y = num_y_o1 * box_1 - num_y_o2 * box_0

    o1_spacing = 0
    o2_spacing = 0
    if rem_space_y < 0:
        o1_spacing = abs(rem_space_y) / (num_y_o1 - 1)
    elif rem_space_y > 0:
        o2_spacing = rem_space_y / (num_y_o2 - 1)

    for i in range(num_x_o1):
        box_coordinate = [0, 0, 0, orientation_1]
        box_coordinate[0] = box_0 * i + box_0 / 2
        for j in range(num_y_o1):
            box_coordinate = [box_coordinate[0], 0, 0, orientation_1]
            box_coordinate[1] = o1_spacing * j + box_1 * j + box_1 / 2
            output_box_list.append(box_coordinate)

    for i in range(num_x_o2):
        box_coordinate = [0, 0, 0, orientation_2]
        box_coordinate[0] = x_start + box_1 * i + box_1 / 2
        for j in range(num_y_o2):
            box_coordinate = [box_coordinate[0], 0, 0, orientation_2]
            box_coordinate[1] = o2_spacing * j + box_0 * j + box_0 / 2
            output_box_list.append(box_coordinate)

    # swapping the columns with different orientations
    if swapping:
        swaps = min(num_x_o1, num_x_o2)
        k = 0
        for j in range(num_y_o1):
            s = 0
            for i in range(num_x_o1):
                output_box_list[k][0] += box_1 * s
                k += 1
                s += 1
                if s > swaps:
                    s = swaps

        c = 0
        for j in range(num_y_o2):
            for i in range(swaps):
                output_box_list[num_y_o1 * num_x_o1 + c][0] = box_0 * (i + 1) + box_1 * i
                c += 1

        # finding the las box coordinates in the list:

    if middle and len(output_box_list) > 0:
        max_coordinate = 0
        i = 0
        for box in output_box_list:
            coordinate_value = box[0] + box[1]
            if max_coordinate < coordinate_value:
                max_coordinate = coordinate_value
                max_index = i
            i += 1

        load_x = output_box_list[max_index][0] + output_box_list[max_index][2]
        load_y = output_box_list[max_index][1] + output_box_list[max_index][3]

        x_offset = (pallet_x - load_x) / 2
        y_offset = (pallet_y - load_y) / 2

        for box in output_box_list:
            box[0] += x_offset
            box[1] += y_offset

    print("TOP output box list:             ", output_box_list)

    return [output_box_list]


def generate_boxes_sp(pallet_x, pallet_y, box_x, box_y, middle=False, label_side="None", label_place="None"):
    output_box_list = []

    result_sp = squared_pattern(pallet_x, pallet_y, box_x, box_y)

    num_squares_row = result_sp[2]
    num_squares_col = result_sp[3]

    # Filling the remaining space with boxes

    rem_space_x_1 = result_sp[4]
    rem_space_y_1 = result_sp[5]
    rem_space_x_2 = result_sp[6]
    rem_space_y_2 = result_sp[7]

    splitting = result_sp[8]

    print(num_squares_row, num_squares_col, rem_space_x_1, rem_space_y_1, rem_space_x_2, rem_space_y_2, splitting)

    filling_1 = generate_boxes_oop(rem_space_x_1, rem_space_y_1, box_x, box_y)[0]
    filling_2 = generate_boxes_oop(rem_space_x_2, rem_space_y_2, box_x, box_y)[0]

    print("filling 1", filling_1)
    print("filling 2", filling_2)

    num_box_x_filling1 = 0
    num_box_y_filling1 = 0
    num_box_x_filling2 = 0
    num_box_y_filling2 = 0

    if len(filling_1) != 0:
        if filling_1[0][0] == box_x / 2:
            orientation_filling1 = 0
            box_side_split_1 = box_x
        else:
            orientation_filling1 = 1
            box_side_split_1 = box_y
        filling1_oop = one_order_pattern(rem_space_x_1, rem_space_y_1, box_x, box_y, orientation_filling1)
        num_box_x_filling1 = filling1_oop[2]
        num_box_y_filling1 = filling1_oop[3]

    if len(filling_2) != 0:
        if filling_2[0][0] == box_x / 2:
            orientation_filling2 = 0
            box_side_split_2 = box_x
        else:
            orientation_filling2 = 1
            box_side_split_2 = box_y
        filling2_oop = one_order_pattern(rem_space_x_2, rem_space_y_2, box_x, box_y, orientation_filling2)
        num_box_x_filling2 = filling2_oop[2]
        num_box_y_filling2 = filling2_oop[3]

    for box in filling_1:
        box[1] = box[1] + num_squares_col * (box_x + box_y)

    for box in filling_2:
        box[0] = box[0] + num_squares_row * (box_x + box_y)

    print("filling_1 for ", filling_1)
    print("filling_2 for ", filling_2)

    # checking if there is remaining space at the end of the rows and columns or not and splitting them

    num_box_in_row_filling1 = 0
    num_box_in_row_filling2 = 0
    for box in filling_1:
        if box[1] == filling_1[0][1]:
            num_box_in_row_filling1 += 1
    for box in filling_2:
        if box[1] == filling_2[0][1]:
            num_box_in_row_filling2 += 1

    num_box_in_col_filling_1 = 0
    num_box_in_col_filling_2 = 0
    for box in filling_1:
        if box[0] == filling_1[0][0]:
            num_box_in_col_filling_1 += 1
    for box in filling_2:
        if box[0] == filling_2[0][0]:
            num_box_in_col_filling_2 += 1

    num_rows = 0
    for box in filling_1:
        if box[0] - box_side_split_1 == 0:
            num_rows += 1
    num_cols = 0
    for box in filling_2:
        if box[1] - box_side_split_2 == 0:
            num_cols += 1

    if len(filling_1) != 0:
        box_0_x = filling_1[0][3]
        box_1_x = filling_1[0][2]
    else:
        box_0_x = 0
        box_1_x = 0
    if len(filling_2) != 0:
        box_0_y = filling_2[0][3]
        box_1_y = filling_2[0][2]
    else:
        box_0_y = 0
        box_1_y = 0

    print("check", splitting, num_squares_row, num_squares_col, box_x, box_y, num_cols, num_rows,
          num_box_in_row_filling1, num_box_in_row_filling2, num_box_in_col_filling_1, num_box_in_col_filling_2)

    if splitting == "x":
        remaining_space_x = num_squares_row * (box_x + box_y) + num_cols * box_1_y - num_box_in_row_filling1 * box_1_x
        remaining_space_y = num_squares_col * (box_x + box_y) - num_box_in_col_filling_2 * box_0_y
    elif splitting == "y":
        remaining_space_x = num_squares_row * (box_x + box_y) - num_box_in_row_filling1 * box_1_x
        remaining_space_y = num_squares_col * (box_x + box_y) + num_rows * box_0_x - num_box_in_col_filling_2 * box_0_y

    print("remaining space x", remaining_space_x)
    print("remaining space y", remaining_space_y)

    square_and_row_spacing_x = 0
    row_spacing = 0

    if remaining_space_x < 0:
        square_and_row_spacing_x = abs(remaining_space_x) / (num_squares_row + num_cols - 1)
    elif remaining_space_x > 0:
        if num_box_in_row_filling1 - 1 != 0:
            row_spacing = remaining_space_x / (num_box_in_row_filling1 - 1)

    square_spacing_y = 0
    col_spacing = 0

    if remaining_space_y < 0:
        square_spacing_y = abs(remaining_space_y) / (num_squares_col - 1)
    elif remaining_space_y > 0:
        if num_box_in_col_filling_2 - 1 != 0:
            col_spacing = remaining_space_y / (num_box_in_col_filling_2 - 1)

    # Making the squares

    for i in range(num_squares_row):
        box_coordinate = [0, 0, 0, 0]
        box_coordinate[0] = box_x * i + box_y * i + square_and_row_spacing_x * i + box_x / 2
        for j in range(num_squares_col):
            box_coordinate = [box_coordinate[0], 0, 0, 0]
            box_coordinate[1] = box_x * j + box_y * j + square_spacing_y * j + box_y / 2
            output_box_list.append(box_coordinate)

    for i in range(num_squares_row):
        box_coordinate = [box_x, 0, 0, 1]
        box_coordinate[0] = box_x + box_x * i + box_y * i + square_and_row_spacing_x * i + box_y / 2
        for j in range(num_squares_col):
            box_coordinate = [box_coordinate[0], box_y, 0, 1]
            box_coordinate[1] = box_x * j + box_y * j + square_spacing_y * j + box_x / 2
            output_box_list.append(box_coordinate)

    for i in range(num_squares_row):
        box_coordinate = [0, box_y, 0, 1]
        box_coordinate[0] = box_x * i + box_y * i + square_and_row_spacing_x * i + box_y / 2
        for j in range(num_squares_col):
            box_coordinate = [box_coordinate[0], box_y, 0, 1]
            box_coordinate[1] = box_y + box_x * j + box_y * j + square_spacing_y * j + box_x / 2
            output_box_list.append(box_coordinate)

    for i in range(num_squares_row):
        box_coordinate = [box_y, box_x, 0, 0]
        box_coordinate[0] = box_y + box_x * i + box_y * i + square_and_row_spacing_x * i + box_x / 2
        for j in range(num_squares_col):
            box_coordinate = [box_coordinate[0], box_x, 0, 0]
            box_coordinate[1] = box_x + box_x * j + box_y * j + square_spacing_y * j + box_y / 2
            output_box_list.append(box_coordinate)

    # Splitting the space between the filled boxes
    print("row spacing", row_spacing)
    print("col spacing", col_spacing)

    i = 0
    k = 0
    for x_i in range(num_box_in_row_filling1):
        for y_i in range(num_box_in_col_filling_1):
            filling_1[i][0] += row_spacing * k
            i += 1
        k += 1

    j = 0
    for x_j in range(num_box_in_row_filling2):
        m = 0
        for y_j in range(num_box_in_col_filling_2):
            filling_2[j][1] += col_spacing * m
            j += 1
            m += 1

    print("filling 1 splitted", filling_1)
    print("filling 2 splitted", filling_2)

    output_box_list.extend(filling_1)
    output_box_list.extend(filling_2)

    if middle and len(output_box_list) > 0:
        max_coordinate = 0
        i = 0
        for box in output_box_list:
            coordinate_value = box[0] + box[1]
            if max_coordinate < coordinate_value:
                max_coordinate = coordinate_value
                max_index = i
            i += 1
        load_x = output_box_list[max_index][0] + output_box_list[max_index][2]
        load_y = output_box_list[max_index][1] + output_box_list[max_index][3]

        x_offset = (pallet_x - load_x) / 2
        y_offset = (pallet_y - load_y) / 2

        for box in output_box_list:
            box[0] += x_offset
            box[1] += y_offset

    print("SP output box list:             ", output_box_list)

    return [output_box_list]
