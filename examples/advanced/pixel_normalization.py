def min_max_scaler(image_array, min_value, max_value):
    image_array_scaled = (image_array - min_value) / (max_value - min_value) * 255
    return image_array_scaled


def normalization_marktackedata_2_0(image_array):
    return image_array


def normalization_markfuktighet_slu_2_0_kat(image_array):
    image_array = image_array[:,:,1] # only select second channel which contains categorical values
    return image_array


def normalization_markfuktighet_slu_2_0_kon(image_array):
    image_array = image_array[:,:,0] # only select first channel which contains values on continuous scale
    min_value = 0
    max_value = 101
    new_image_array = min_max_scaler(image_array,min_value,max_value)
    return new_image_array


def normalization_sentinel_2_2_0(image_array):
    return image_array
