import os
import pickle

import cv2
import numpy as np
from sklearn.cluster import MiniBatchKMeans


def load_model(filename):
    model = pickle.load(open(filename, 'rb'))
    return model


def centroid_histogram(clt):
    num_labels = np.arange(0, len(np.unique(clt.labels_)) + 1)
    (hist, _) = np.histogram(clt.labels_, bins=num_labels)

    hist = hist.astype("float")
    hist /= hist.sum()

    return hist


def plot_colors(hist, centroids):
    bar = np.zeros((50, 300, 3), dtype='uint8')
    startX = 0

    for (percent, color) in zip(hist, centroids):
        endX = startX + (percent * 300)
        cv2.rectangle(bar, (int(startX), 0), (int(endX), 50),
                      color.astype('uint8').tolist(), -1)
        startX = endX

    return bar


def transform(hist, centroid):
    centroid /= 255.
    row = np.concatenate([hist.reshape((len(hist), 1)), centroid], axis=1)
    row = row.reshape((1, row.shape[0] * row.shape[1]))
    return row


class BackgroundClassifier(object):

    N_CLUSTERS = 3

    def __init__(self):
        self.model = load_model(os.path.join(os.path.dirname(__file__),
                                             'rf_background.sav'))

    @staticmethod
    def cluster_image(image, n_clusters=3):
        image = image.reshape((image.shape[0] * image.shape[1], 3))

        clt = MiniBatchKMeans(n_clusters=n_clusters)
        clt.fit(image)

        predicate = list(map(lambda x: np.average(x), clt.cluster_centers_))
        order = np.argsort(predicate)

        hist = centroid_histogram(clt)
        return hist[order], clt.cluster_centers_[order]

    def _preload_data(self, image):
        if len(image.shape) != 3:
            raise ValueError(f'Image has {len(image.shape)} channels, but 3 needed: {image.shape}')

        hist, centers = self.cluster_image(image, self.N_CLUSTERS)
        data = transform(hist, centers)
        return data

    def predict(self, image):
        '''
        Returns 0 or 1:
            0 - image has non-white background.
            1 - image has white background.
        '''

        data = self._preload_data(image)
        prediction = self.model.predict(data)
        return prediction

    def predict_proba(self, image):
        '''
        Returns probability that image has white background.
        '''

        data = self._preload_data(image)
        proba = self.model.predict_proba(data)[0][1]
        return proba
