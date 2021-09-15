from pattern_loadings import one_order_pattern
from generating_boxlists import generate_boxes_oop, generate_boxes_top, generate_boxes_sp

pallet_X = 9
pallet_Y = 10
box_X = 2
box_Y = 3


result_OOP = generate_boxes_oop(pallet_X, pallet_Y,  box_X, box_Y)[0]
result_TOP = generate_boxes_top(pallet_X, pallet_Y, box_X, box_Y)
result_SP = generate_boxes_sp(pallet_X, pallet_Y, box_X, box_Y)

print("FINAL RESULT OOP", result_OOP)
print("FINAL RESULT TOP", result_TOP)
print("FINAL RESULT SP", result_SP)


