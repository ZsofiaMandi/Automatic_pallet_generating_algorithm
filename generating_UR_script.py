from generating_boxlists import generate_boxes_sp
from z_dimension import generating_3D_output
import copy

# Input parameters
pallet_X = 530 / 1000
pallet_Y = 600 / 1000
pallet_Z = 250 / 1000
box_X = 135 / 1000
box_Y = 170 / 1000
box_Z = 110 / 1000
Pick_up_pose = [686.6 / 1000, 378.8 / 1000, 106.3 / 1000, 0.0, 3.142, 0.0]
Pallet_coordinate_system = [-298.4 / 1000, -765 / 1000, 13.8 / 1000, 0.0, 0.0, 0.0]

sp_layer_1, sp_layer_2 = generate_boxes_sp(pallet_X, pallet_Y, box_X, box_Y,
                                           middle=True, label_side="Front", label_place="Outwards")

output_box_list = generating_3D_output(sp_layer_1, sp_layer_2, box_Z,
                                       generation_method="max_height", generation_limit=pallet_Z)

print(output_box_list)


def generating_UR_script(output_box_list_3D, pick_up_pose,
                         pallet_coordinate_system, speed=0.08, acc=0.8, slip_sheet_pose=None,
                         pick_up_offset=0.15, box_down_offset=0.15, vacuum=30):
    with open('ur_palletizing_script.txt', 'w+') as f:
        f.write('a={}\n'.format(acc))
        f.write('v={}\n'.format(speed))
        f.write('\n')

        num = output_box_list_3D[-1][2] / output_box_list_3D[0][2]

        for box in output_box_list_3D:

            i = num - int(output_box_list_3D[-1][2] / box[2]) + 1
            print(num, i)
            pick_up_pose_approach = copy.deepcopy(pick_up_pose)
            pick_up_pose_approach[2] += pick_up_offset * i

            if box[3] == 0:
                rotation = 0
            elif box[3] == 1:
                rotation = -90
            elif box[3] == 2:
                rotation = 180
            elif box[3] == 3:
                rotation = 90

            box_xyz_str = ""
            box_z_approach_str = ""
            box[2] -= 0.01
            # Defining the box pick up position
            for value in box[:3]:
                box_xyz_str += str(value) + ", "
            box_full_coordinate = box_xyz_str + str(pick_up_pose[-3]) \
                                  + ", " + str(pick_up_pose[-2]) + ", " + str(pick_up_pose[-1])

            # Defining the box put down approach position:
            box_xyz_approach = box
            box_xyz_approach[2] += box_down_offset
            for value in box_xyz_approach[:3]:
                box_z_approach_str += str(value) + ", "
            box_approach_full_coordinate = box_z_approach_str + str(pick_up_pose[-3]) \
                                           + ", " + str(pick_up_pose[-2]) + ", " + str(pick_up_pose[-1])

            f.write("#Move to pick up approach pose\n")
            f.write('movel(pose_trans(p{}, p{}), a, v)\n'.format(pallet_coordinate_system, pick_up_pose_approach))

            f.write("#Move to pick up pose\n")
            f.write('movel(pose_trans(p{},p{}), a, v)\n'.format(pallet_coordinate_system, pick_up_pose))

            f.write('#Grip box\n')
            f.write('vg_grip(channel=2, vacuum={}, timeout=0.0, alert=False, tool_index=0)\n'.format(vacuum))
            f.write('sleep(1)\n')
            f.write('#Move back to pick up approach pose\n')
            f.write('movel(pose_trans(p{},p{}), a, v)\n'.format(pallet_coordinate_system, pick_up_pose_approach))

            f.write('#Move to box approach pose\n')
            f.write('movel(pose_trans(p{},pose_trans(p[{}],p[0.0, 0.0, 0.0, 0.0, 0.0, d2r({})])), a , v)\n'
                    .format(pallet_coordinate_system, box_approach_full_coordinate, rotation))

            f.write('#Move to box pose\n')
            f.write('movel(pose_trans(p{},'
                    'pose_trans(p[{}],p[0.0, 0.0, 0.0, 0.0, 0.0, d2r({})])), a , v)\n'
                    .format(pallet_coordinate_system, box_full_coordinate, rotation))

            f.write('#Release box\n')
            f.write('vg_release(channel=2, timeout=0.0, autoidle=False, tool_index=0)\n')

            f.write('#Move back to box approach pose\n')
            f.write('movel(pose_trans(p{},'
                    'pose_trans(p[{}],p[0.0, 0.0, 0.0, 0.0, 0.0, d2r({})])), a , v)\n'
                    .format(pallet_coordinate_system, box_approach_full_coordinate, rotation))
            f.write('\n')

            # REPEAT FOR ALL BOXES


generating_UR_script(output_box_list, Pick_up_pose, Pallet_coordinate_system)
