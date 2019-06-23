__version__ = '0.1.0'

from .extractor import ExtractorGrabcut, ExtractorEdges
from .classifier import BackgroundClassifier, centroid_histogram, transform, load_model, plot_colors
