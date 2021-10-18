import matplotlib.pyplot as plt
from generating_boxlists import generate_boxes_top
from z_dimension import generating_3D_output
import random

from mpl_toolkits.mplot3d import Axes3D
import numpy as np

# Input parameters
pallet_X = 12
pallet_Y = 9
pallet_Z = 12
box_X = 3
box_Y = 2
box_Z = 2

top_layer_1, top_layer_2 = generate_boxes_top(pallet_X, pallet_Y, box_X, box_Y, middle=True, label_side="Right", label_place="Outwards")

output_box_list = generating_3D_output(top_layer_1, top_layer_2, box_Z,
                                       generation_method="max_load", generation_limit=100, mass_box=2, slip_sheet=0)


def random_color():
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    rand_color = (r, g, b)
    return rand_color

color1 = random_color()


def visualize_in_3D(box_list_3D, pallet_x, pallet_y, pallet_z, box_x, box_y, box_z):
    dimension = max(pallet_x, pallet_y, pallet_z) + 1
    # prepare some coordinates
    x, y, z = np.indices((dimension, dimension, dimension))

    cubes = []
    for box in box_list_3D:
        if box[3] == 0 or box[3] == 2:
            pass
        elif box[3] == 1 or box[3] == 3:
            box_x, box_y = box_y, box_x
        cube = (x <= box[0] + box_x / 2) & (y <= box[1] + box_y / 2) & (z <= box[2]) & \
               (x >= box[0] - box_x / 2) & (y >= box[1] - box_y / 2) & (z >= box[2] - box_z)
        cubes.append(cube)

    voxels = cubes[0]
    for cube in cubes[1:]:
        voxels |= cube
    # set the colors of each object
    colors = np.empty(voxels.shape, dtype=object)
    # colors[cube1] = 'blue'
    # colors[cube2] = 'red'
    # colors[cube3] = 'green'

    # and plot everything
    ax = plt.figure().add_subplot(projection='3d')
    ax.voxels(voxels, facecolors="red")

    plt.show()


visualize_in_3D(output_box_list, pallet_X, pallet_Y, pallet_Z, box_X, box_Y, box_Z)
