# -*- coding: utf-8 -*-

import numpy as np
import scipy.ndimage
from PIL import Image

def no_error_dilate(input_image, ground_truth_image, output_image, dilation_radius, foreground_label = 255, background_label = 128):
    '''
    Dilates the foreground and background labels in a label image to a given 
    radius (which excludes the pixel in question, so a radius of 1 would result
    in an extra pixel in each direction being flipped to that label). Avoids
    introducing errors by not performing any dilation on a pixel outside of its
    'place' (foreground pixels won't be dilated if they're in the background
    and vice versa).
    
    All non-zero labels will be dilated.
    
    input_image: The label image to dilate.
    ground_truth_image: The binary ground truth image.
    output_image: Where to save the result.
    dilation_radius: Radius of dilation to perform.
    '''
    image = scipy.ndimage.imread(input_image)
    output = np.zeros(image.shape, dtype=np.uint8)
    ground_truth = np.greater(scipy.ndimage.imread(ground_truth_image), 0)
    
    x, y = np.ogrid[-dilation_radius : dilation_radius + 1, -dilation_radius : dilation_radius + 1]
    circle_mask = x**2 + y**2 <= dilation_radius**2
    
    # Iterate over all pixels for dilation
    it = np.nditer(image, flags=['multi_index'])
    while not it.finished:
        pixel = int(it[0])

        # Figure out the mask sizes only for the label pixels
        if pixel == foreground_label or pixel == background_label:
            is_true_foreground = ground_truth[it.multi_index]
            image_min_row = max(it.multi_index[0] - dilation_radius, 0)
            image_min_col = max(it.multi_index[1] - dilation_radius, 0)
            image_max_row = min(it.multi_index[0] + dilation_radius + 1, image.shape[0])
            image_max_col = min(it.multi_index[1] + dilation_radius + 1, image.shape[1])
            
            mask_min_row = max(dilation_radius - it.multi_index[0], 0)
            mask_min_col = max(dilation_radius - it.multi_index[1], 0)
            mask_max_row = min(image.shape[0] - it.multi_index[0] + dilation_radius, circle_mask.shape[0])
            mask_max_col = min(image.shape[1] - it.multi_index[1] + dilation_radius, circle_mask.shape[1])

        if pixel == foreground_label:
            output[it.multi_index] = foreground_label

            # We only dilate (and hence apply the mask) if this is a foreground
            # pixel on true foreground or a background pixel on true background
            if is_true_foreground:
                temp_mask = circle_mask[mask_min_row:mask_max_row, mask_min_col:mask_max_col]
                output[image_min_row:image_max_row, image_min_col:image_max_col][temp_mask] = foreground_label
        elif pixel == background_label:
            output[it.multi_index] = background_label

            if not is_true_foreground:
                temp_mask = circle_mask[mask_min_row:mask_max_row, mask_min_col:mask_max_col]
                output[image_min_row:image_max_row, image_min_col:image_max_col][temp_mask] = background_label
        
        it.iternext()
    
    Image.fromarray(output).save(output_image)
    
def textbook_dilation(input_image, output_image, dilation_radius):
    '''
    Dilates all pixels a given radius (which excludes the pixel in question, so
    a radius of 1 would result in an extra pixel in each direction being flipped
    to that label).
    
    All non-zero labels will be dilated.
    
    input_image: The label image to dilate.
    output_image: Where to save the result.
    dilation_radius: Radius of dilation to perform.
    '''
    image = scipy.ndimage.imread(input_image)
    
    x, y = np.ogrid[-dilation_radius : dilation_radius + 1, -dilation_radius : dilation_radius + 1]
    circle_mask = x**2 + y**2 <= dilation_radius**2
    dilated_image = scipy.ndimage.morphology.grey_dilation(image, footprint=circle_mask)
    
    Image.fromarray(dilated_image).save(output_image)
