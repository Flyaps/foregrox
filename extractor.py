import os

import cv2
import numpy as np
import matplotlib.pyplot as plt


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


def change_contrast(image):
    lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(2, 2))
    cl = clahe.apply(l)

    limg = cv2.merge((cl, a, b))
    final = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)
    return final


class ExtractorGrabcut(object):

    @staticmethod
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

    def extract(self, image, color=255):
        mask = self.calculate_mask(image)
        image[mask] = color
        return image


class ExtractorEdges(object):

    @staticmethod
    def detect_edge(channel):
        scharrX = cv2.Scharr(channel, cv2.CV_16S, 1, 0)
        scharrY = cv2.Scharr(channel, cv2.CV_16S, 0, 1)
        scharr = np.hypot(scharrX, scharrY)

        scharr[scharr > 255] = 255
        return scharr

    @staticmethod
    def find_significant_contours(edge_img):
        image, contours, hierarchy = cv2.findContours(edge_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        level1 = []
        for i, tupl in enumerate(hierarchy[0]):
            # Each array is in format (Next, Prev, First child, Parent)
            # Filter the ones without parent
            if tupl[3] == -1:
                tupl = np.insert(tupl, 0, [i])
                level1.append(tupl)

        significant = []
        too_small = edge_img.size * 5 / 100
        for tupl in level1:
            contour = contours[tupl[0]]
            area = cv2.contourArea(contour)
            if area > too_small:
                significant.append([contour, area])

        significant.sort(key=lambda x: x[1])
        return [x[0] for x in significant]

    def extract(self, image, color=255):
        img = image.copy()
        image = change_contrast(image)
        image = cv2.bilateralFilter(image, 40, 80, 20)
        image = cv2.GaussianBlur(image, (3, 3), 0)

        edge_img = np.max(
            np.array([self.detect_edge(image[:, :, 0]),
                      self.detect_edge(image[:, :, 1]),
                      self.detect_edge(image[:, :, 2])]),
            axis=0
        )

        median = np.median(edge_img)
        edge_img[edge_img <= median] = 0
        edge_img_8u = np.asarray(edge_img, np.uint8)
        significant = self.find_significant_contours(edge_img_8u)

        mask = edge_img.copy()
        mask[mask > 0] = 0
        cv2.fillPoly(mask, significant, color)

        mask = np.logical_not(mask)
        img[mask] = color
        return img
