import os
import argparse

from lib.extractor import ExtractorGrabcut, ExtractorEdges
from lib.classifier import BackgroundClassifier
from lib.utils import read_image, save, show_image


def main():
    use_alt_model = {
        True: ExtractorEdges,
        False: ExtractorGrabcut,
    }

    parser = argparse.ArgumentParser(description='Foreground extraction.')
    parser.add_argument('--input', dest='input', help='Path to file.',
                        type=str, required=True)
    parser.add_argument('--output', dest='output', help='Path to output folder.',
                        type=str, required=False, default=None)
    parser.add_argument('--show', dest='show', help='Show image.',
                        type=bool, required=False, default=False)
    parser.add_argument('--alt', dest='alt', help='Is alternative model should be used.',
                        type=bool, required=False, default=False)
    parser.add_argument('--bg', dest='bg', help='Is background classifier should be used.',
                        type=bool, required=False, default=False)
    args = parser.parse_args()

    image_path = args.input
    output_path = args.output
    show = args.show
    is_alt = args.alt
    background = args.bg

    _, image_name = os.path.split(image_path)
    image = read_image(image_path)

    if background:
        bg_classifier = BackgroundClassifier()
        if bg_classifier.predict(image):
            print(
                f'''Image {image_path} has been classified as image with white background.
                If it\'s false, please, don\'t use argument "--bg=True" in your script run.'''
            )
        else:
            model = use_alt_model[is_alt]()
            image = model.extract(image)
    else:
        model = use_alt_model[is_alt]()
        image = model.extract(image)

    if output_path is not None:
        save(image, image_name, output_path)

    if show:
        show_image(image)


if __name__ == '__main__':
    main()
