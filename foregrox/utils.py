import os

import cv2
import matplotlib.pyplot as plt


def change_contrast(image):
    lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    l_coord, a_coord, b_coord = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(2, 2))
    clahe = clahe.apply(l_coord)

    limg = cv2.merge((clahe, a_coord, b_coord))
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


def show_image(image):
    plt.imshow(image)
    plt.show()


def save(image, name, path):
    img_name, img_ext = os.path.splitext(name)
    new_img_name = f'{img_name}_fg{img_ext}'
    cv2.imwrite(os.path.join(path, new_img_name), image[:, :, ::-1])
