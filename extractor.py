import os

import cv2
import numpy as np
import matplotlib.pyplot as plt


def change_contrast(image):
    lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(2, 2))
    cl = clahe.apply(l)

    limg = cv2.merge((cl, a, b))
    final = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)
    return final


def read_image(image_path, contrast=False):
    if not os.path.exists(image_path):
        raise ValueError(f'Cannot find image: {image_path}')

    img = cv2.imread(image_path)
    image = img[:, :, ::-1]

    if contrast:
        image = change_contrast(image)

    return image


def calculate_mask(image):
    mask_init = np.zeros(image.shape[:2], np.uint8)
    backgroundModel = np.zeros((1, 65), np.float64)
    foregroundModel = np.zeros((1, 65), np.float64)
    rectangle = (5, 5, image.shape[1] - 5, image.shape[0] - 5)
    cv2.grabCut(image, mask_init, rectangle,
                backgroundModel, foregroundModel,
                6, cv2.GC_INIT_WITH_RECT)
    mask = np.where((mask_init == 2) | (mask_init == 0), 0, 1).astype('uint8')
    mask = np.logical_not(mask)
    return mask


def replace_background(image, mask, color):
    image[mask] = color
    return image


def show_image(image):
    plt.imshow(image)
    plt.show()


def save(image, name, path):
    img_name, img_ext = os.path.splitext(name)
    new_img_name = f'{img_name}_fg{img_ext}'
    cv2.imwrite(os.path.join(path, new_img_name), image[:, :, ::-1])
