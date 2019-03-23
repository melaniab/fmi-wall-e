import os
import sys
import json
import numpy as np
import time
#from PIL import Image, ImageDraw
import cv2
#from bresenham import bresenham
import skimage
import math
from PIL import Image

STORE_DIR = 'masked/'
class_names = ['BG', 'cig_butt']

# Stores the image with the mask.
# Necessary for the demo/debugging
def store_pic(img, results, image_path, visualize):
    masked_img_path = os.path.join(STORE_DIR, os.path.basename(image_path))
    image = visualize.display_instances(img, results['rois'],
                                        results['masks'], results['class_ids'], 
                                        class_names, results['scores'], plot=False)

    Image.fromarray(image.astype(np.uint8)).save(masked_img_path)


def get_mask(model, image_path, visualize):
    """Get cigarette mask in 2D."""
    img = skimage.io.imread(image_path)
    img_arr = np.array(img)
    results = model.detect([img_arr], verbose=1)[0]
    store_pic(img, results, image_path, visualize)

    h = results['masks'].shape[0]
    w = results['masks'].shape[1]
    mask = results['masks']

    num_masks = results['masks'].shape[2]
    # Empty mask
    if num_masks == 0:
        return None
    elif num_masks > 1:
        return mask.T[0]

    new_mask = mask.reshape(h, w)
    return new_mask


def calculate_center_angle(mask, draw_lines=False, image_path=None):
    mat = np.argwhere(mask)
    mat = np.array(mat).astype(np.float32)  # have to convert type for PCA
    mat[:, 0], mat[:, 1] = mat[:, 1], mat[:, 0].copy()
    # mean (e. g. the geometrical center)
    # and eigenvectors (e. g. directions of principal components)
    mean, eigenvectors = cv2.PCACompute(mat, mean=np.array([]))
    rads = np.arctan2(eigenvectors[0][1], eigenvectors[0][0])
    degrees = rads * 180 / math.pi

    # print
    if draw_lines:
        center = tuple(mean[0])
        endpoint1 = tuple(mean[0] + eigenvectors[0] * 100)
        endpoint2 = tuple(mean[0] + eigenvectors[1] * 50)

        img = cv2.imread(image_path)
        red_color = (0, 0, 255)
        cv2.circle(img, center, 5, red_color)
        cv2.line(img, center, endpoint1, red_color)
        cv2.line(img, center, endpoint2, red_color)
        cv2.imwrite("out_cigar_2.png", img)

    mean = list(mean[0])    
    return degrees, mean