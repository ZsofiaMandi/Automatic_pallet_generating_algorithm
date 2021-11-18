import matplotlib.pyplot as plt
from generating_boxlists import generate_boxes_top
from z_dimension import generating_3D_output
import random

from mpl_toolkits.mplot3d import Axes3D
import numpy as np

# Input parameters
pallet_X = 100
pallet_Y = 110
pallet_Z = 50
box_X = 25
box_Y = 31
box_Z = 22
gap = 5

top_layer_1, top_layer_2 = generate_boxes_top(pallet_X, pallet_Y, box_X, box_Y, middle=True, label_side="Right", label_place="Outwards", gap=gap)

output_box_list = generating_3D_output(top_layer_1, top_layer_2, box_Z,
                                       generation_method="max_load", generation_limit=50, mass_box=2, slip_sheet=0)


def random_color():
    return np.random.uniform(0, 1, [1, 3])


def visualize_in_3D(box_list_3D, pallet_x, pallet_y, pallet_z, box_x, box_y, box_z):
    # dimension of the volume
    dimension = max(pallet_x, pallet_y, pallet_z) + 1

    # define 3D coordinate space
    x, y, z = np.indices((dimension, dimension, dimension))

    # define cubes to be plotted from box list
    cubes = []
    for box in box_list_3D:
        box_x_init = box_x
        box_y_init = box_y
        if box[3] == 0 or box[3] == 2:
            box_x_init = box_x_init
            box_y_init = box_y_init
        elif box[3] == 1 or box[3] == 3:
            box_x_init, box_y_init = box_y_init, box_x_init
        cube = (x < box[0] + box_x_init / 2) & (y < box[1] + box_y_init / 2) & (z < box[2]) & \
               (x >= box[0] - box_x_init / 2) & (y >= box[1] - box_y_init / 2) & (z >= box[2] - box_z)
        cubes.append(cube)

    voxels = cubes[0]
    colors = np.empty(voxels.shape + (3,))
    colors[cubes[0], :] = random_color()

    # define voxels and their color
    for cube in cubes[1:]:
        voxels |= cube
        colors[cube, :] = random_color()

    # plot everything
    ax = plt.figure().add_subplot(projection='3d')
    ax.voxels(voxels, facecolors=colors)

    plt.xlabel("X axis")
    plt.ylabel("Y axis")
    plt.show()


visualize_in_3D(output_box_list, pallet_X, pallet_Y, pallet_Z, box_X, box_Y, box_Z)
