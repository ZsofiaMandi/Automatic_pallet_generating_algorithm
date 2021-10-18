import math
import copy


# GENERATING THE OUTPUT BOX LISTS IN 3 DIMENSIONS FROM THE 2 LAYERS


def generating_3D_output(layer_1, layer_2, box_z, generation_method, generation_limit, slip_sheet=0):

    # The generation can be done in 3 different ways, maximizing the height, the load or the number of boxes
    """generation_method = 'max_height', 'max_load', 'number_of_boxes'"""

    if generation_method == "max_height":
        output_3D_box_list = []
        max_height = generation_limit
        num_of_layers = math.floor(max_height / (box_z + slip_sheet))

        for i in range(num_of_layers):
            layer_A = copy.deepcopy(layer_1)
            layer_B = copy.deepcopy(layer_2)
            if i % 2 == 0:
                for box_A in layer_A:
                    box_A[2] = box_z * (i + 1)
                output_3D_box_list.extend(layer_A)
            else:
                for box_B in layer_B:
                    box_B[2] = box_z * (i + 1)
                output_3D_box_list.extend(layer_B)

    print(output_3D_box_list)

    return output_3D_box_list
