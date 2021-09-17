import math

# DEFINING 3 FUNCTIONS FOR THE 3 ALGORITHMS AND CHECKING HOW MANY BOXES WE CAN PUT ON THE PALLET WITH THOSE
# PATTERNS AND CALCULATING SOME INFORMATION FOR THE BOX GENERATING ALGORITHMS


# Defining the algorithm that allows only one rotation of the boxes in one pallet
def one_order_pattern(pallet_x, pallet_y, box_x, box_y, box_orientation):
    # returning the results in the required orientation

    # Checking the number of boxes we can put along the X dimension
    if box_orientation == 0:
        num_x = int(pallet_x / box_x)
    elif box_orientation == 1:
        num_x = int(pallet_x / box_y)

    # Checking the number of boxes we can put along the Y dimension
    if box_orientation == 0:
        num_y = int(pallet_y / box_y)
    elif box_orientation == 1:
        num_y = int(pallet_y / box_x)
    else:
        raise ValueError("box orientation must be 1 or 0")

    packed_boxes = num_x * num_y

    if pallet_x * pallet_y != 0:
        pallet_percentage = (box_x * box_y * packed_boxes) / (pallet_x * pallet_y)
    else:
        pallet_percentage = 1

    cost_of_packing = [packed_boxes, pallet_percentage, num_x, num_y]

    return cost_of_packing


# Defining the algorithm that allows two orientation of the boxes in one pallet, firstly fills up the pallet with one,
# then starts to rotate the boxes column by column till the half of the pallet,
# then repeats it along the other pallet dimension
def two_order_pattern(pallet_x, pallet_y, box_x, box_y, orientation):
    # Checking the number of boxes we can put along the X dimension of the pallet

    # Reducing the box columns with orientation 0 boxes one by one, till the half of the pallet,
    # then trying to fill up the remaining space with the boxes in orientation 1
    # returning all of the pattern combinations

    if orientation == 0:
        box_0 = box_x
        box_1 = box_y
    elif orientation == 1:
        box_0 = box_y
        box_1 = box_x

    # getting the number of cols and rows we can pack with one orientation from the OOP algorithm
    result_oop = one_order_pattern(pallet_x, pallet_y, box_x, box_y, orientation)

    num_of_cols = result_oop[2]
    num_of_rows = result_oop[3]

    cost_of_patterns = []

    half_of_pallet = math.ceil(num_of_cols / 2)

    # reducing the rows one by one (first with 0 to check the already remaining space), then filling
    # the spaces left
    for i in range(0, half_of_pallet + 1):
        pattern = []

        num_of_cols_new = num_of_cols - i
        filled_pallet_x = num_of_cols_new * box_0
        remaining_x = pallet_x - filled_pallet_x

        num_new_boxes_x = int(remaining_x / box_1)
        num_new_boxes_y = int(pallet_y / box_0)
        num_boxes = num_of_cols_new * num_of_rows + num_new_boxes_x * num_new_boxes_y

        pallet_percentage = (num_boxes * box_x * box_y) / (pallet_x * pallet_y)

        pattern = [num_of_cols_new, num_of_rows, num_new_boxes_x, num_new_boxes_y, num_boxes, pallet_percentage]

        cost_of_patterns.append(pattern)

    return cost_of_patterns


# Defining the algorithm that makes square shapes from 4 boxes,
# then tries to fill the space with the squares
def squared_pattern(pallet_x, pallet_y, box_x, box_y):
    # Calculating the square size
    square_size_xy = box_x + box_y
    packed_squares = one_order_pattern(pallet_x, pallet_y, square_size_xy, square_size_xy, 1)

    packed_boxes = packed_squares[0] * 4
    usage_percentage = (packed_boxes * box_x * box_y) / (pallet_x * pallet_y)
    num_squares_row = packed_squares[2]
    num_squares_col = packed_squares[3]

    # checking how many boxes we can put in the remaining space, splitting the space in two ways
    # more space along X:
    rem_space_xx_1 = pallet_x
    rem_space_xy_1 = pallet_y - num_squares_col * square_size_xy
    rem_space_xx_2 = pallet_x - num_squares_row * square_size_xy
    rem_space_xy_2 = num_squares_col * square_size_xy
    filling_xo1_1 = one_order_pattern(rem_space_xx_1, rem_space_xy_1, box_x, box_y, 1)
    filling_xo2_1 = one_order_pattern(rem_space_xx_1, rem_space_xy_1, box_x, box_y, 0)
    filling_xo1_2 = one_order_pattern(rem_space_xx_2, rem_space_xy_2, box_x, box_y, 1)
    filling_xo2_2 = one_order_pattern(rem_space_xx_2, rem_space_xy_2, box_x, box_y, 0)

    # more space along Y:
    rem_space_yx_1 = num_squares_row * square_size_xy
    rem_space_yy_1 = pallet_y - num_squares_col * square_size_xy
    rem_space_yx_2 = pallet_x - num_squares_row * square_size_xy
    rem_space_yy_2 = pallet_y
    filling_yo1_1 = one_order_pattern(rem_space_yx_1, rem_space_yy_1, box_x, box_y, 1)
    filling_yo2_1 = one_order_pattern(rem_space_yx_1, rem_space_yy_1, box_x, box_y, 0)
    filling_yo1_2 = one_order_pattern(rem_space_yx_2, rem_space_yy_2, box_x, box_y, 1)
    filling_yo2_2 = one_order_pattern(rem_space_yx_2, rem_space_yy_2, box_x, box_y, 0)

    # Deciding the best combination for filling the remaining space, checking the number of boxes
    # we can put in both directions in the remaining two spaces split in both ways

    if filling_xo1_1[0] >= filling_xo2_1[0]:
        filling_x_1 = filling_xo1_1
    else:
        filling_x_1 = filling_xo2_1

    if filling_xo1_2[0] >= filling_xo2_2[0]:
        filling_x_2 = filling_xo1_2
    else:
        filling_x_2 = filling_xo2_2

    if filling_yo1_1[0] >= filling_yo2_1[0]:
        filling_y_1 = filling_yo1_1
    else:
        filling_y_1 = filling_yo2_1

    if filling_yo1_2[0] >= filling_yo2_2[0]:
        filling_y_2 = filling_yo1_2
    else:
        filling_y_2 = filling_yo2_2

    if (filling_x_1[0] + filling_x_2[0]) >= (filling_y_1[0] + filling_y_2[0]):
        rem_space_x_1 = pallet_x
        rem_space_y_1 = pallet_y - num_squares_col * square_size_xy
        rem_space_x_2 = pallet_x - num_squares_row * square_size_xy
        rem_space_y_2 = num_squares_col * square_size_xy
        splitting = "x"
    else:
        rem_space_x_1 = num_squares_row * square_size_xy
        rem_space_y_1 = pallet_y - num_squares_col * square_size_xy
        rem_space_x_2 = pallet_x - num_squares_row * square_size_xy
        rem_space_y_2 = pallet_y
        splitting = "y"

    # Returning the cost of the packing, along with some information about the remaining space dimensions
    # for further calculations

    cost_of_packing = [packed_boxes, usage_percentage, num_squares_row, num_squares_col, rem_space_x_1,
                       rem_space_y_1, rem_space_x_2, rem_space_y_2, splitting]

    return cost_of_packing
