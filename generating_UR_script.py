from generating_boxlists import generate_boxes_top
from z_dimension import generating_3D_output
import copy

# Input parameters
pallet_X = 12
pallet_Y = 9
pallet_Z = 12
box_X = 3
box_Y = 2
box_Z = 2
Pick_up_pose = [0.0, 0.0, 0.0, 1.0, 3.0, 2.0]

top_layer_1, top_layer_2 = generate_boxes_top(pallet_X, pallet_Y, box_X, box_Y,
                                              middle=True, label_side="Right", label_place="Outwards")

output_box_list = generating_3D_output(top_layer_1, top_layer_2, box_Z,
                                       generation_method="max_load", generation_limit=100, mass_box=2, slip_sheet=0)


def generating_UR_script(output_box_list_3D, pick_up_pose, speed=0.25, acc=1.2, slip_sheet_pose=None):
    with open('ur_palletizing_script.txt', 'w+') as f:
        f.write('a={}\n'.format(acc))
        f.write('v={}\n'.format(speed))
        f.write('\n')

        for box in output_box_list_3D:

            if box[3] == 0:
                rotation = 0
            elif box[3] == 1:
                rotation = 90
            elif box[3] == 2:
                rotation = 180
            elif box[3] == 3:
                rotation = 270

            box_xyz_str = ""
            box_z_approach_str = ""

            # Defining the box pick up position
            for value in box[:3]:
                box_xyz_str += str(value) + ", "
            box_full_coordinate = box_xyz_str + str(pick_up_pose[-3]) \
                                  + ", " + str(pick_up_pose[-2]) + ", " + str(pick_up_pose[-1])

            # Defining the box pick up approach position:
            box_xyz_approach = box
            box_xyz_approach[2] += 0.01
            for value in box_xyz_approach[:3]:
                box_z_approach_str += str(value) + ", "
            box_approach_full_coordinate = box_z_approach_str + str(pick_up_pose[-3]) \
                                           + ", " + str(pick_up_pose[-2]) + ", " + str(pick_up_pose[-1])

            # Defining the pick up pose approach position:
            pick_up_pose_approach = copy.deepcopy(pick_up_pose)
            pick_up_pose_approach[2] += 0.01

            f.write('movel(p{}, a, v)\n'.format(pick_up_pose_approach))         # Move to pick up approach pose
            f.write('movel(p{}, a, v)\n'.format(pick_up_pose))                  # Move to pick up pose
            f.write('grip\n')                                                   # Grip the box
            f.write('movel(p{}, a, v)\n'.format(pick_up_pose_approach))         # Move back to pick up approach pose

            f.write('movel(pose_trans(p[{}], '                                  # Move to box approach pose
                    'p[0.0, 0.0, 0.0, 0.0, 0.0, d2r({})]), a , v)\n'
                    .format(box_approach_full_coordinate, rotation))
            f.write('movel(pose_trans(p[{}], '                                  # Move to box pose
                    'p[0.0, 0.0, 0.0, 0.0, 0.0, d2r({})]), a , v)\n'
                    .format(box_full_coordinate, rotation))
            f.write('release\n')                                                # Release the box
            f.write('movel(pose_trans(p[{}], '                                  # Move back to box approach pose
                    'p[0.0, 0.0, 0.0, 0.0, 0.0, d2r({})]), a , v)\n'
                    .format(box_approach_full_coordinate, rotation))
            f.write('\n')

            # REPEAT FOR ALL BOXES


generating_UR_script(output_box_list, Pick_up_pose)
