from pattern_loadings import one_order_pattern
from generating_boxlists import generate_boxes_oop, generate_boxes_top, generate_boxes_sp

pallet_X = 9
pallet_Y = 10
box_X = 2
box_Y = 3


generate_boxes_oop(pallet_X, pallet_Y,  box_X, box_Y, middle=True)
generate_boxes_top(pallet_X, pallet_Y, box_X, box_Y)
generate_boxes_sp(pallet_X, pallet_Y, box_X, box_Y)


