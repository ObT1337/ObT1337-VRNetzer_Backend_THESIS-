source = "/Users/till/Documents/Playground/alphafold_to_vrnetzer/processing_files/MAPS"
dest = "/Users/till/Documents/Playground/reduce_image_size/NEW_MAPS"
import glob
import ntpath
import os
import sys

from PIL import Image


def main(source, dest):
    ext = ["*.bmp", "*.png"]
    for e in ext:
        files = os.path.join(source, "**", e)
        print(files)
        for file in glob.glob(files, recursive=True):
            head, tail = ntpath.split(file)
            sub_dir = head.split("/")[-1]
            if "xyz" in head:
                sub_dir = os.path.join(head.split("/")[-2], sub_dir)
            image = Image.open(file)
            image = image.resize((256, 256), Image.NEAREST)
            dest_dir = os.path.join(dest, sub_dir)
            os.makedirs(dest_dir, exist_ok=True)
            file_name = os.path.join(dest_dir, tail)
            image.save(file_name)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
