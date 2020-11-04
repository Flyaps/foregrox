import numpy as np

from foregrox.extractor import ExtractorGrabcut


def test_grabcut_mask():
    image = np.full((12, 12, 3), 255, np.uint8)
    expected_mask = np.full((12, 12), True, np.bool)
    black_points = [
        (5, 5),
        (6, 5),
        (6, 6)
    ]
    for point in black_points:
        image[point] = np.array([0, 0, 0], np.uint8)
        expected_mask[point] = False
    mask = ExtractorGrabcut.calculate_mask(image)
    assert (mask == expected_mask).all()
