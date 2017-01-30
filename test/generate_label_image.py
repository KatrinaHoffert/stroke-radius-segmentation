# -*- coding: utf-8 -*-

import numpy as np
from PIL import Image

foreground_label = 255
background_label = 128

# Ground truth is a big box from (100, 100) to (199, 199)
ground_truth = np.zeros((256, 256), np.uint8)
ground_truth[100:200, 100:200] = foreground_label
Image.fromarray(ground_truth).save("ground_truth.png")

label_image = np.zeros((256, 256), np.uint8)

# Legit foreground line
label_image[150:175, 150] = foreground_label

# Foreground line that goes into background
label_image[190:210, 125] = foreground_label

# Legit background line
label_image[50:100, 50] = background_label

# Background line that goes into foreground
label_image[125, 90:110] = background_label

# Background point just to demonstrate points
label_image[75, 75] = background_label

# Foreground line that stradles the edge of the ground truth
label_image[100, 125:150] = foreground_label

Image.fromarray(label_image).save("label_image.png")
