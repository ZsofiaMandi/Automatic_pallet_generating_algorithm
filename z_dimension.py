import math
import copy


# GENERATING THE OUTPUT BOX LISTS IN 3 DIMENSIONS FROM THE 2 LAYERS


def generating_3D_output(layer_1, layer_2, box_z, generation_method, generation_limit, mass_box=0, slip_sheet=0):

    # The generation can be done in 3 different ways, maximizing the height, the load or the number of boxes
    """generation_method = 'max_height', 'max_load', 'number_of_boxes'"""
    output_3D_box_list = []

    # Calculating the number of layers on top of each other with the limitation of the whole structure's height
    if generation_method == "max_height":

        max_height = generation_limit       # the max height of all of the layers and slip sheets together in mm
        num_of_layers = math.floor(max_height / (box_z + slip_sheet))

    # Calculating the number of layers on top of each other with the limitation of the whole structure's mass
    elif generation_method == "max_load":

        max_load = generation_limit     # the max load of all of the layers together in kg
        num_boxes_layer_A = len(layer_1)
        num_boxes_layer_B = len(layer_2)
        num_boxes_layers_mean = (num_boxes_layer_A + num_boxes_layer_B) / 2
        num_of_layers = math.floor(max_load / num_boxes_layers_mean)

        total_mass = 0
        for i in range(num_of_layers):
            if i % 2 == 0:
                total_mass += num_boxes_layer_A * mass_box
            else:
                total_mass += num_boxes_layer_B * mass_box

        if total_mass > max_load:
            num_of_layers -= 1
            total_mass = 0
            for i in range(num_of_layers):
                if i % 2 == 0:
                    total_mass += num_boxes_layer_A * mass_box
                else:
                    total_mass += num_boxes_layer_B * mass_box

    elif generation_method == "number_of_boxes":
        exact_number = generation_limit     # the exact number of boxes for the whole pallet
        num_boxes_layer_A = len(layer_1)
        num_boxes_layer_B = len(layer_2)
        # TODO

    # Generating the 3D output based on the number of layers
    for i in range(num_of_layers):
        layer_A = copy.deepcopy(layer_1)
        layer_B = copy.deepcopy(layer_2)
        if i % 2 == 0:
            for box_A in layer_A:
                box_A[2] = box_z * (i + 1) + slip_sheet * i
            output_3D_box_list.extend(layer_A)
        else:
            for box_B in layer_B:
                box_B[2] = box_z * (i + 1) + slip_sheet * i
            output_3D_box_list.extend(layer_B)

    return output_3D_box_list
