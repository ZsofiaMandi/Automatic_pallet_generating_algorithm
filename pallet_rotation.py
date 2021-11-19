from generating_boxlists import generate_boxes_top
import copy


def rotating_top_pallet(pallet_x, pallet_y, box_x, box_y, middle=False,
                        label_side="None", label_place="None", x=True, y=True, gap=0):
    top = generate_boxes_top(pallet_x, pallet_y, box_x, box_y, middle, label_side, label_place, x, y, gap)[0]

    top_rotated = generate_boxes_top(pallet_y, pallet_x, box_x, box_y, middle, label_side, label_place, x, y, gap)[0]

    output_box_list = []

    if len(top) >= len(top_rotated):
        output_box_list = copy.deepcopy(top)
    else:
        for box in top_rotated:
            box_0 = box[1]
            box_1 = pallet_y - box[0]
            box_2 = 0
            if box[3] == 0:
                box_3 = 3
            elif box[3] == 1:
                box_3 = 0
            elif box[3] == 2:
                box_3 = 1
            elif box[3] == 3:
                box_3 = 2
            output_box_list.append([box_0, box_1, box_2, box_3])

    return output_box_list
