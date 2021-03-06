from pattern_loadings import one_order_pattern, two_order_pattern, squared_pattern
from layer_mirroring import mirroring_layer
from labels import labeling
from centering import centering
from stretching import stretching


# GENERATING THE OUTPUT BOX LISTS IN 2 DIMENSIONS FOR THE 3 ALGORITHMS, BOTH FOR THE FIRST AND SECOND LAYER,
# BASED ON THE INFORMATION GETTING FROM THE PATTERN LOADING FUNCTIONS


# GENERATING THE OUTPUT BOX LIST FOR THE ONE-ORDER PATTERN:
def generate_boxes_oop(pallet_x, pallet_y, box_x, box_y, middle=False, stretch=False,
                       label_side="None", label_place="None", gap=0):
    output_box_list = []
    output_box_list_rotated = []

    box_x = box_x + gap / 2
    box_y = box_y + gap / 2

    # Getting the information from the pattern loading functions about how many boxes we can put on the pallet
    # for both orders
    result_oop_0 = one_order_pattern(pallet_x, pallet_y, box_x, box_y, 0)
    result_oop_1 = one_order_pattern(pallet_x, pallet_y, box_x, box_y, 1)

    # Checking which order performed better
    if result_oop_0[0] >= result_oop_1[0]:
        orientation = 0
        rotated = 1
        box_0 = box_x
        box_1 = box_y
    else:
        orientation = 1
        rotated = 0
        box_0 = box_y
        box_1 = box_x

    # ---------LAYER 1--------- #
    # Using the orientation with the MORE boxes and calculating how many boxes we can put along the X and Y dimensions
    # of the pallet
    result_oop = one_order_pattern(pallet_x, pallet_y, box_x, box_y, orientation)
    num_x = result_oop[2]
    num_y = result_oop[3]

    # Generating the output box list for the one order pattern FIRST LAYER based on the calculated values
    for i in range(num_x):
        box_coordinate = [0, 0, 0, orientation]
        box_coordinate[0] = box_0 * i + box_0 / 2
        for j in range(num_y):
            box_coordinate = [box_coordinate[0], 0, 0, orientation]
            box_coordinate[1] = box_1 * j + box_1 / 2
            output_box_list.append(box_coordinate)

    # Making a rotated second layer, which has all of the boxes in the other order

    # ---------LAYER 2--------- #
    # Using the orientation with the LESS boxes and calculating how many boxes we can put along the X and Y dimensions
    # of the pallet
    result_oop_rotated = one_order_pattern(pallet_x, pallet_y, box_x, box_y, rotated)
    num_x_rotated = result_oop_rotated[2]
    num_y_rotated = result_oop_rotated[3]

    # Generating the output box list for the one order pattern SECOND LAYER (rotated) based on the calculated values
    for i in range(num_x_rotated):
        box_coordinate_rotated = [0, 0, 0, rotated]
        box_coordinate_rotated[0] = box_1 * i + box_1 / 2
        for j in range(num_y_rotated):
            box_coordinate_rotated = [box_coordinate_rotated[0], 0, 0, rotated]
            box_coordinate_rotated[1] = box_0 * j + box_0 / 2
            output_box_list_rotated.append(box_coordinate_rotated)

    # --------- CENTERING --------- #
    # Aligning the pattern to the middle of the pallet
    # Centering the first and second layer
    if middle and len(output_box_list) > 0:
        output_box_list = centering(output_box_list, pallet_x, pallet_y, box_x, box_y)
        output_box_list_rotated = centering(output_box_list_rotated, pallet_x, pallet_y, box_x, box_y)

    # --------- LABELING --------- #
    # Labeling the first and second layer as well
    if label_side != "None" and label_place != "None":
        output_box_list = labeling(output_box_list, label_side, label_place, box_x, box_y)
        output_box_list_rotated = labeling(output_box_list_rotated, label_side, label_place, box_x, box_y)

    for box in output_box_list:
        box[0] = round(box[0], 4)
        box[1] = round(box[1], 4)
    for box in output_box_list_rotated:
        box[0] = round(box[0], 4)
        box[1] = round(box[1], 4)

    return [output_box_list, output_box_list_rotated]


# GENERATING THE OUTPUT BOX LIST FOR THE TWO-ORDER PATTERN:
def generate_boxes_top(pallet_x, pallet_y, box_x, box_y, middle=False,
                       label_side="None", label_place="None", x=True, y=True, gap=0):
    output_box_list = []

    box_x = box_x + gap / 2
    box_y = box_y + gap / 2

    # Getting the two-order pattern results for both starting orientations
    result_top_1 = two_order_pattern(pallet_x, pallet_y, box_x, box_y, 0)
    result_top_2 = two_order_pattern(pallet_x, pallet_y, box_x, box_y, 1)

    # Selecting the best two-order patterns for the two orientations
    # If more patterns give the same number of boxes then choose the one with the most mixed orientation combination
    # for more stable second layer if we want to mirror it
    pattern_index_o1 = 0
    pattern_index_o2 = 0
    for i in range(len(result_top_1)):
        if result_top_1[pattern_index_o1][4] <= result_top_1[i][4]:
            pattern_index_o1 = i
    for i in range(len(result_top_2)):
        if result_top_2[pattern_index_o2][4] <= result_top_2[i][4]:
            pattern_index_o2 = i

    # Selecting the better from the 2 two-order pattern solution
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

    # Finalizing the selected two-order pattern and having the information about how much boxes we can put along
    # the X and Y dimensions of the pallet in both orders
    result_top = two_order_pattern(pallet_x, pallet_y, box_x, box_y, orientation_1)
    num_x_o1 = result_top[pattern_index][0]
    num_y_o1 = result_top[pattern_index][1]
    num_x_o2 = result_top[pattern_index][2]
    num_y_o2 = result_top[pattern_index][3]

    x_start = num_x_o1 * box_0  # Starting x coordinate for the 2. order (offsetting with the width of the 1. order)

    # --------- ALIGNING THE TWO ORDERS --------- #
    # checking if there is remaining space at the end of the columns or not and splitting them if there is
    rem_space_y = num_y_o1 * box_1 - num_y_o2 * box_0  # Calculating the remaining space along the pallet Y dimension

    # Checking if the first or second order hangs beyond the Y dimension relative to the other and calculating the
    # spacing for it
    o1_spacing = 0
    o2_spacing = 0
    if rem_space_y < 0:
        if num_y_o1 - 1 != 0:
            o1_spacing = abs(rem_space_y / (num_y_o1 - 1))
    elif rem_space_y > 0:
        if num_y_o2 - 1 != 0:
            o2_spacing = rem_space_y / (num_y_o2 - 1)

    # --------- FIRST LAYER --------- #

    # Making the output box list for the first layer for the first order (including the aligning)
    for i in range(num_x_o1):
        box_coordinate = [0, 0, 0, orientation_1]
        box_coordinate[0] = box_0 * i + box_0 / 2
        for j in range(num_y_o1):
            box_coordinate = [box_coordinate[0], 0, 0, orientation_1]
            box_coordinate[1] = o1_spacing * j + box_1 * j + box_1 / 2
            output_box_list.append(box_coordinate)

    # Extending the output box list for the first layer with the second order (including the aligning)
    for i in range(num_x_o2):
        box_coordinate = [0, 0, 0, orientation_2]
        box_coordinate[0] = x_start + box_1 * i + box_1 / 2
        for j in range(num_y_o2):
            box_coordinate = [box_coordinate[0], 0, 0, orientation_2]
            box_coordinate[1] = o2_spacing * j + box_0 * j + box_0 / 2
            output_box_list.append(box_coordinate)

    # --------- CENTERING --------- #

    if middle and len(output_box_list) > 0:
        output_box_list = centering(output_box_list, pallet_x, pallet_y, box_x, box_y)

    # --------- SECOND LAYER --------- #
    # Making a second layer from the first layer by mirroring it
    output_box_list_mirrored = mirroring_layer(output_box_list, x, y, pallet_x, pallet_y, box_x, box_y, middle)

    # --------- LABELING --------- #
    # Rotating the boxes in the first and second layer to put the labels in the desired directions
    if label_side != "None" and label_place != "None":
        output_box_list = labeling(output_box_list, label_side, label_place, box_x, box_y)
        output_box_list_mirrored = labeling(output_box_list_mirrored, label_side, label_place, box_x, box_y)

    for box in output_box_list:
        box[0] = round(box[0], 4)
        box[1] = round(box[1], 4)
    for box in output_box_list_mirrored:
        box[0] = round(box[0], 4)
        box[1] = round(box[1], 4)

    return [output_box_list, output_box_list_mirrored]


# GENERATING THE OUTPUT BOX LIST FOR THE SQUARED PATTERN:
def generate_boxes_sp(pallet_x, pallet_y, box_x, box_y, middle=False, stretch=False,
                      label_side="None", label_place="None", x=True, y=True, gap=0):
    output_box_list = []

    box_x = box_x + gap / 2
    box_y = box_y + gap / 2

    # Getting the squared pattern results
    result_sp = squared_pattern(pallet_x, pallet_y, box_x, box_y)

    # Getting how many squares we can put in a row (pallet X dim) and in a col (pallet Y dim)
    num_squares_row = result_sp[2]
    num_squares_col = result_sp[3]

    # Checking the remaining space besides the squares with boxes
    rem_space_x_1 = result_sp[4]
    rem_space_y_1 = result_sp[5]
    rem_space_x_2 = result_sp[6]
    rem_space_y_2 = result_sp[7]

    splitting = result_sp[8]  # The split remaining space is bigger along the x dim or the y dim

    # Filling the remaining spaces with the oop function
    filling_1 = generate_boxes_oop(rem_space_x_1, rem_space_y_1, box_x, box_y)[0]
    filling_2 = generate_boxes_oop(rem_space_x_2, rem_space_y_2, box_x, box_y)[0]

    num_box_x_filling1 = 0
    num_box_y_filling1 = 0
    num_box_x_filling2 = 0
    num_box_y_filling2 = 0

    # Checking the orientation of the boxes in filling 1
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

    # Checking the orientation of the boxes in filling 2
    if len(filling_2) != 0:
        if filling_2[0][0] == box_x / 2:
            orientation_filling2 = 0
            not_box_side_split_2 = box_y
        else:
            orientation_filling2 = 1
            not_box_side_split_2 = box_x

    # Offsetting the fillings with the width and height of the square block
    for box in filling_1:
        box[1] += num_squares_col * (box_x + box_y)

    for box in filling_2:
        box[0] += num_squares_row * (box_x + box_y)

    # checking if there is remaining space at the end of the rows and columns or not and splitting them
    # (comparing the square block to the oop fillings)

    # Calculating the number of boxes in a row in the two fillings
    num_box_in_row_filling1 = 0
    num_box_in_row_filling2 = 0
    for box in filling_1:
        if box[1] == filling_1[0][1]:
            num_box_in_row_filling1 += 1
    for box in filling_2:
        if box[1] == filling_2[0][1]:
            num_box_in_row_filling2 += 1

    # Calculating the number of boxes in a column in the two fillings
    num_box_in_col_filling_1 = 0
    num_box_in_col_filling_2 = 0
    for box in filling_1:
        if box[0] == filling_1[0][0]:
            num_box_in_col_filling_1 += 1
    for box in filling_2:
        if box[0] == filling_2[0][0]:
            num_box_in_col_filling_2 += 1

    # Calculating the number of rows in the filling 1
    num_rows = 0
    for box in filling_1:
        if box[0] - box_side_split_1 / 2 == 0:
            num_rows += 1
    # Calculating the number of columns in the filling 2
    num_cols = 0
    for box in filling_2:
        if box[1] - not_box_side_split_2 / 2 == 0:
            num_cols += 1

    # Defining the box dimensions in filling 1 along the pallet X and Y dimensions
    if len(filling_1) != 0:
        if filling_1[0][3] == 0:
            box_f1_x = box_x
            box_f1_y = box_y
        elif filling_1[0][3] == 1:
            box_f1_x = box_y
            box_f1_y = box_x
    else:
        box_f1_x = 0
        box_f1_y = 0

    # Defining the box dimensions in filling 2 along the pallet X and Y dimensions
    if len(filling_2) != 0:
        if filling_2[0][3] == 0:
            box_f2_x = box_x
            box_f2_y = box_y
        elif filling_2[0][3] == 1:
            box_f2_x = box_y
            box_f2_y = box_x
    else:
        box_f2_x = 0
        box_f2_y = 0

    # Calculating the remaining space along the X and Y dimensions of the pallet based on which splitting part
    # is bigger, the one along the X dimension (splitting 1) or the other along the Y dimension (splitting 2)
    if splitting == "x":
        remaining_space_x = num_squares_row * (box_x + box_y) + num_cols * box_f2_x - num_box_in_row_filling1 * box_f1_x
        remaining_space_y = num_squares_col * (box_x + box_y) - num_box_in_col_filling_2 * box_f2_y
    elif splitting == "y":
        remaining_space_x = num_squares_row * (box_x + box_y) - num_box_in_row_filling1 * box_f1_x
        remaining_space_y = num_squares_col * (
                box_x + box_y) + num_rows * box_f1_y - num_box_in_col_filling_2 * box_f2_y

    # --------- SPACING --------- #
    # Calculating the spacings along X dimension of the pallet
    square_and_row_spacing_x = 0  # The spacing for the squares and rows (splitting 1) along the X dimension
    row_spacing_f1_x = 0  # The spacing
    col_spacing_f2_x = 0
    if remaining_space_x < 0:
        if num_squares_row + num_cols - 1 != 0: # When the filling 1 is wider than the squares and cols together
            square_and_row_spacing_x = abs(remaining_space_x) / (num_squares_row + num_cols - 1)
            col_spacing_f2_x = abs(remaining_space_x) / (num_squares_row + num_cols - 1)
    elif remaining_space_x > 0:  # When the squares and cols together is wider than the filling 1
        if num_box_in_row_filling1 - 1 != 0:
            row_spacing_f1_x = remaining_space_x / (num_box_in_row_filling1 - 1)

    # Calculating the spacing along the Y dimension of the pallet
    square_spacing_y = 0
    col_spacing_f2_y = 0
    row_spacing_f1_y = 0
    if remaining_space_y < 0:
        if num_squares_col + num_rows - 1 != 0:
            square_spacing_y = abs(remaining_space_y / (num_squares_col + num_rows - 1))
            row_spacing_f1_y = abs(remaining_space_y / (num_squares_col + num_rows - 1))
    elif remaining_space_y > 0:
        if num_box_in_col_filling_2 - 1 != 0:
            col_spacing_f2_y = remaining_space_y / (num_box_in_col_filling_2 - 1)

    # --------- SQUARES --------- #
    # Making the box coordinates for the first of four elements of the box squares
    for i in range(num_squares_row):
        box_coordinate = [0, 0, 0, 0]
        box_coordinate[0] = box_x * i + box_y * i + square_and_row_spacing_x * i + box_x / 2
        for j in range(num_squares_col):
            box_coordinate = [box_coordinate[0], 0, 0, 0]
            box_coordinate[1] = box_x * j + box_y * j + square_spacing_y * j + box_y / 2
            output_box_list.append(box_coordinate)

    # Making the box coordinates for the second of four elements of the box squares
    for i in range(num_squares_row):
        box_coordinate = [box_x, 0, 0, 1]
        box_coordinate[0] = box_x + box_x * i + box_y * i + square_and_row_spacing_x * i + box_y / 2
        for j in range(num_squares_col):
            box_coordinate = [box_coordinate[0], box_y, 0, 1]
            box_coordinate[1] = box_x * j + box_y * j + square_spacing_y * j + box_x / 2
            output_box_list.append(box_coordinate)

    # Making the box coordinates for the third of four elements of the box squares
    for i in range(num_squares_row):
        box_coordinate = [0, box_y, 0, 1]
        box_coordinate[0] = box_x * i + box_y * i + square_and_row_spacing_x * i + box_y / 2
        for j in range(num_squares_col):
            box_coordinate = [box_coordinate[0], box_y, 0, 1]
            box_coordinate[1] = box_y + box_x * j + box_y * j + square_spacing_y * j + box_x / 2
            output_box_list.append(box_coordinate)

    # Making the box coordinates for the first element of the box squares
    for i in range(num_squares_row):
        box_coordinate = [box_y, box_x, 0, 0]
        box_coordinate[0] = box_y + box_x * i + box_y * i + square_and_row_spacing_x * i + box_x / 2
        for j in range(num_squares_col):
            box_coordinate = [box_coordinate[0], box_x, 0, 0]
            box_coordinate[1] = box_x + box_x * j + box_y * j + square_spacing_y * j + box_y / 2
            output_box_list.append(box_coordinate)

    # --------- FILLINGS --------- #
    # Making the box coordinates for the filling1
    i = 0
    k = 0
    for x_i in range(num_box_in_row_filling1):
        for y_i in range(num_box_in_col_filling_1):
            filling_1[i][1] += row_spacing_f1_y * (y_i + num_squares_col - 1 + 1)
            filling_1[i][0] += row_spacing_f1_x * k
            i += 1
        k += 1

    # Making the box coordinates for the filling2
    j = 0
    for x_j in range(num_box_in_row_filling2):
        m = 0
        for y_j in range(num_box_in_col_filling_2):
            filling_2[j][0] += col_spacing_f2_x * (x_j + num_squares_row - 1 + 1)
            filling_2[j][1] += col_spacing_f2_y * m
            j += 1
            m += 1

    # Adding filling1 and filling2 boxes to the output box list
    output_box_list.extend(filling_1)
    output_box_list.extend(filling_2)

    # --------- CENTERING --------- #
    if middle and len(output_box_list) > 0:
        output_box_list = centering(output_box_list, pallet_x, pallet_y, box_x, box_y)

    # --------- SECOND LAYER --------- #
    # Making a second layer from the first layer by mirroring it
    output_box_list_mirrored = mirroring_layer(output_box_list, x, y, pallet_x, pallet_y, box_x, box_y, middle)

    # --------- LABELING --------- #
    # Rotating the boxes in the first and second layer to put the labels in the desired directions
    if label_side != "None" and label_place != "None":
        output_box_list = labeling(output_box_list, label_side, label_place, box_x, box_y)
        output_box_list_mirrored = labeling(output_box_list_mirrored, label_side, label_place, box_x, box_y)

    for box in output_box_list:
        box[0] = round(box[0], 4)
        box[1] = round(box[1], 4)
    for box in output_box_list_mirrored:
        box[0] = round(box[0], 4)
        box[1] = round(box[1], 4)

    return [output_box_list, output_box_list_mirrored]
