import os
import argparse

from extractor import (
    read_image, calculate_mask,
    replace_background, save,
    show_image
)


def main():
    parser = argparse.ArgumentParser(description='Foreground extraction.')
    parser.add_argument('--input', dest='input', help='Path to file.',
                        type=str, required=True)
    parser.add_argument('--output', dest='output', help='Path to output folder.',
                        type=str, required=False, default=None)
    parser.add_argument('--show', dest='show', help='Show image.',
                        type=bool, required=False, default=False)
    args = parser.parse_args()

    image_path = args.input
    output_path = args.output
    show = args.show

    _, image_name = os.path.split(image_path)

    image = read_image(image_path)
    mask = calculate_mask(image)
    image = replace_background(image, mask, color=255)

    if output_path is not None:
        save(image, image_name, output_path)

    if show:
        show_image(image)


if __name__ == '__main__':
    main()
