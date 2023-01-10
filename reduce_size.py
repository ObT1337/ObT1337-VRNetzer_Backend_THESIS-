import glob
import ntpath
import os
import sys

import cv2
import numpy as np
from PIL import Image

# requires pillow 9.0.1+


def main(source, dest,method):
    ext = ["*.bmp", "*.png"]
    for e in ext:
        files = os.path.join(source, "**", e)
        print(files)
        for file in glob.glob(files, recursive=True):
            head, tail = ntpath.split(file)
            sub_dir = head.split(os.sep)[-1]
            if "xyz" in head:
                sub_dir = os.path.join(head.split(os.sep)[-2], sub_dir)

            # resized
            if method == "pillow":
                img = Image.open(file)
                img = img.resize((256, 256), Image.Dither.NONE)
            elif method == "opencv":
                img = cv2.imread(file)
                resized = cv2.resize(img,(256,256))
            elif method == "skip":
                img = Image.open(file)
                img = skip_every_2(img)

            dest_dir = os.path.join(dest, sub_dir)
            os.makedirs(dest_dir, exist_ok=True)
            file_name = os.path.join(dest_dir, tail)

            # save
            if method in ["pillow","skip"]:
                img.save(file_name.replace("v4","v2"))
            elif method =="opencv":
                cv2.imwrite(file_name,resized)

def skip_every_2(img):
    res = np.zeros((256,256,3), dtype=np.uint8)
    tmp =np.array(img)
    row_idx = 0
    pixel_idx = 0
    i = 0
    new_image =[]
    for row in range(0, len(tmp)):
        for pixel in range(0,len(tmp[row,:]),4):
            res[row_idx, pixel_idx] = tmp[row, pixel]
            pixel_idx += 1
            if pixel_idx > 255:
                row_idx += 1
                pixel_idx = 0
    return Image.fromarray(res)

if __name__ == "__main__":
    # main(sys.argv[1], sys.argv[2])
    # src = r"c:\Users\sebastian\Documents\Unreal Projects\VRNetzer_Backend\static\MAPS"
    # dest = r"c:\Users\sebastian\Documents\Unreal Projects\VRNetzer_Backend\static\NewMaps"
    src = "/Users/till/Documents/Playground/VRNetzer_Backend/static/maps/cartoons_ss_coloring"
    dest = "/Users/till/Documents/Playground/VRNetzer_Backend/static/maps/cartoons_ss_coloring_256"
    main(src, dest,"skip")
