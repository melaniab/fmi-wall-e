import os
import sys
import json
import numpy as np
import time
from PIL import Image, ImageDraw
import cv2
from bresenham import bresenham
import skimage
import math

path = "../datasets/cig_butts/our_dataset/55656616_418734638936862_8306943736646991872_n.jpg"

def get_mask(model, image_path):
    """Get cigarette mask in 2D."""
    img = skimage.io.imread(image_path)
    img_arr = np.array(img)
    results = model.detect([img_arr], verbose=1)
    h = results[0]['masks'].shape[0]
    w = results[0]['masks'].shape[1]
    mask = results[0]['masks']
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

    center = tuple(mean[0])
    endpoint1 = tuple(mean[0] + eigenvectors[0] * 100)
    endpoint2 = tuple(mean[0] + eigenvectors[1] * 50)

    # print
    if draw_lines:
        img = cv2.imread(image_path)
        red_color = (0, 0, 255)
        cv2.circle(img, center, 5, red_color)
        cv2.line(img, center, endpoint1, red_color)
        cv2.line(img, center, endpoint2, red_color)
        cv2.imwrite("out_cigar_2.png", img)

    return degrees, list(mean[0])