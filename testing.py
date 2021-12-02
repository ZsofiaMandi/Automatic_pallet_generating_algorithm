import math
import xlsxwriter

from pattern_loadings import one_order_pattern, two_order_pattern, squared_pattern


def prime_number(num):
    if num > 1:
        prime = True
        for i in range(2, num):
            if (num % i) == 0:
                prime = False
                break
    return prime


list_packed = []
list_unpacked = []
critical_cases = []
squared_best = 0
oop_best = 0
top_best = 0
oop_found = 0
top_found = 0
sp_found = 0
squared_best_cases = []
case_number = 0
for box_x in range(1, 7, 1):
    for box_y in range(box_x + 1, 8, 1):
        for pallet_x in range(5, 50):
            for pallet_y in range(pallet_x, 50):
                if pallet_x >= 2 * box_x and pallet_x >= 2 * box_y \
                        and pallet_y >= 2 * box_x and pallet_y >= 2 * box_y:
                    if (pallet_x >= pallet_y and pallet_x / pallet_y <= 3) or \
                            (pallet_y >= pallet_x and pallet_y / pallet_x <= 3):
                        packed_boxes_oop_0 = one_order_pattern(pallet_x, pallet_y, box_x, box_y, 0)[0]
                        packed_boxes_oop_1 = one_order_pattern(pallet_x, pallet_y, box_x, box_y, 1)[0]

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

                        boxes_top_2 = two_order_pattern(pallet_y, pallet_x, box_x, box_y, 0)
                        boxes_top_3 = two_order_pattern(pallet_y, pallet_x, box_x, box_y, 1)
                        pattern_index_o1 = 0
                        pattern_index_o2 = 0
                        for i in range(len(boxes_top_2)):
                            if boxes_top_2[pattern_index_o1][4] <= boxes_top_2[i][4]:
                                pattern_index_o1 = i
                        for i in range(len(boxes_top_3)):
                            if boxes_top_3[pattern_index_o2][4] <= boxes_top_3[i][4]:
                                pattern_index_o2 = i
                        packed_boxes_top_2 = boxes_top_2[pattern_index_o1][4]
                        packed_boxes_top_3 = boxes_top_3[pattern_index_o2][4]

                        packed_boxes_sp = squared_pattern(pallet_x, pallet_y, box_x, box_y)[0]
                        packed_boxes = max(packed_boxes_oop_0, packed_boxes_oop_1,
                                           packed_boxes_top_0, packed_boxes_top_1,
                                           packed_boxes_top_2, packed_boxes_top_3, packed_boxes_sp)

                        unpackable_boxes = 0
                        if box_x % 2 == 0 and box_y % 2 == 0 and (pallet_x % 2 != 0 or pallet_y % 2 != 0):
                            unpacked_boxes = math.floor((pallet_x * pallet_y - pallet_y * (pallet_x % 2) - pallet_x
                                                         * (pallet_y % 2) + (pallet_x % 2) * (pallet_y % 2)) / (
                                                                    box_x * box_y)) - packed_boxes
                        elif box_x % 3 == 0 and box_y % 3 == 0 and (pallet_x % 3 != 0 or pallet_y % 3 != 0):
                            unpacked_boxes = math.floor((pallet_x * pallet_y - pallet_y * (pallet_x % 3) - pallet_x
                                                         * (pallet_y % 3) + (pallet_x % 3) * (pallet_y % 3)) / (
                                                                    box_x * box_y)) - packed_boxes
                        else:
                            unpacked_boxes = math.floor(pallet_x * pallet_y / (box_x * box_y)) - packed_boxes

                        list_packed.append(packed_boxes)
                        list_unpacked.append(unpacked_boxes)

                        sp_compare = max(packed_boxes_oop_0, packed_boxes_oop_1,
                                         packed_boxes_top_0, packed_boxes_top_1,
                                         packed_boxes_top_2, packed_boxes_top_3)

                        tp_compare = max(packed_boxes_oop_0, packed_boxes_oop_1, packed_boxes_sp)

                        oop_compare = max(packed_boxes_top_0, packed_boxes_top_1,
                                          packed_boxes_top_2, packed_boxes_top_3, packed_boxes_sp)

                        if packed_boxes_sp > sp_compare:
                            squared_best += 1
                            squared_best_cases.append([pallet_x, pallet_y, box_x, box_y])
                        elif tp_compare < packed_boxes_top_0 or \
                                tp_compare < packed_boxes_top_1 or \
                                tp_compare < packed_boxes_top_2 or \
                                tp_compare < packed_boxes_top_3:
                            top_best += 1
                        elif oop_compare < packed_boxes_oop_0 or oop_compare < packed_boxes_oop_1:
                            oop_best += 1

                        if packed_boxes_oop_0 == packed_boxes or packed_boxes_oop_1 == packed_boxes:
                            oop_found += 1
                        if packed_boxes_sp == packed_boxes:
                            sp_found += 1
                        if packed_boxes_top_0 == packed_boxes or packed_boxes_top_1 == packed_boxes or \
                                packed_boxes_top_2 == packed_boxes or packed_boxes_top_3 == packed_boxes:
                            top_found += 1

                        if unpacked_boxes >= 5:
                            critical_cases.append([pallet_x, pallet_y, box_x, box_y])
                        case_number += 1

# Create a workbook and add a worksheet.
workbook = xlsxwriter.Workbook('pattern_tests.xlsx')
worksheet = workbook.add_worksheet()

print("squared_best_cases", squared_best_cases)
print("oop_found", oop_found)
print("oop_best", oop_best)
print("top_found", top_found)
print("top_best", top_best)
print("sp_found", sp_found)
print("sp_best", squared_best)


# print("critical_cases", critical_cases)

col = 0
for item in list_packed:
    worksheet.write(0, col, item)
    col += 1

col = 0
for item in list_unpacked:
    worksheet.write(1, col, item)
    col += 1

col = 0
for items in critical_cases:
    str1 = ""
    for item in items:
        str1 += str(item) + ", "
    str1 = str1.rstrip()
    worksheet.write(2, col, str1)
    col += 1

workbook.close()
