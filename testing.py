import math

from pattern_loadings import one_order_pattern, two_order_pattern, squared_pattern

list_packed = []
list_unpacked = []
critical_cases = []

for box_x in range(1, 8, 2):
    for box_y in range(2, 8, 2):
        for pallet_x in range(5, 50):
            for pallet_y in range(5, 50):
                if pallet_x > 2 * box_x and pallet_x > 2 * box_y and pallet_y > 2 * box_x and pallet_y > 2 * box_y:
                    if (pallet_x > pallet_y and pallet_x / pallet_y < 3) or \
                            (pallet_y > pallet_x and pallet_y / pallet_x < 3):
                        packed_boxes_oop_0 = one_order_pattern(pallet_x, pallet_y,  box_x, box_y, 0)[0]
                        packed_boxes_oop_1 = one_order_pattern(pallet_x, pallet_y,  box_x, box_y, 1)[0]

                        boxes_top_0 = two_order_pattern(pallet_x, pallet_y, box_x, box_y, 0)
                        boxes_top_1 = two_order_pattern(pallet_x, pallet_y, box_x, box_y, 1)
                        pattern_index_o1 = 0
                        pattern_index_o2 = 0
                        for i in range(len(boxes_top_0)):
                            if boxes_top_0[pattern_index_o1][4] <= boxes_top_0[i][4]:
                                pattern_index_o1 = i
                        for i in range(len(boxes_top_1)):
                            if boxes_top_1[pattern_index_o2][4] <= boxes_top_1[i][4]:
                                pattern_index_o2 = i
                        packed_boxes_top_0 = boxes_top_0[pattern_index_o1][4]
                        packed_boxes_top_1 = boxes_top_1[pattern_index_o2][4]

                        packed_boxes_sp = squared_pattern(pallet_x, pallet_y, box_x, box_y)[0]
                        packed_boxes = max(packed_boxes_oop_0, packed_boxes_oop_1,
                                           packed_boxes_top_0, packed_boxes_top_1, packed_boxes_sp)
                        unpacked_boxes = math.floor(pallet_x * pallet_y / (box_x * box_y)) - packed_boxes
                        list_packed.append(packed_boxes)
                        list_unpacked.append(unpacked_boxes)

                        if unpacked_boxes >= 5:
                            critical_cases.append([pallet_x, pallet_y, box_x, box_y])


print(list_packed)
print(list_unpacked)
print(critical_cases)
