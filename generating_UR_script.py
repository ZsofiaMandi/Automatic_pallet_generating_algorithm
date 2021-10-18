from generating_boxlists import generate_boxes_top
from z_dimension import generating_3D_output

# Input parameters
pallet_X = 12
pallet_Y = 9
pallet_Z = 12
box_X = 3
box_Y = 2
box_Z = 2
pick_up_pose = "p[0.0, 0.0, 0.0, 0.0, 0.0, 0.0]"

top = generate_boxes_top(pallet_X, pallet_Y, box_X, box_Y, middle=True, label_side="Right", label_place="Outwards")
top_layer_1 = top[0]
top_layer_2 = top[1]
print("layer_A", top_layer_1)
print("layer_b", top_layer_2)

output_box_list = generating_3D_output(top_layer_1, top_layer_2, box_Z,
                                       generation_method="max_load", generation_limit=100, mass_box=2, slip_sheet=0)


def generating_UR_script(output_box_list_3D, pick_up_pose, speed=0.25, acc=1.2, slip_sheet_pose=None):

    angles = "3.14, 0.0, 0.0"
    print(output_box_list_3D[0][:3])
    with open('ur_palletizing_script.txt', 'w+') as f:
        f.write('a={}\n'.format(acc))
        f.write('v={}\n'.format(speed))
        for box in output_box_list_3D:
            box_xyz_str = ""
            for value in box[:3]:
                box_xyz_str += str(value) + ", "
            f.write('movel(p[{}{}], a, v)\n'.format(box_xyz_str, angles))


generating_UR_script(output_box_list, pick_up_pose)