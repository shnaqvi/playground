import os
import matplotlib.pyplot as plt
from PIL import Image
import skimage as sk
import numpy as np


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    im_dir = 'path_to_imgs'
    pngs = [os.path.join(im_dir, file) for file in os.listdir(im_dir)
            if os.path.splitext(file)[1] == '.png']
    for png in pngs:
        im = sk.io.imread(png)
        im = sk.exposure.rescale_intensity(im, out_range=(0, 255)).astype(np.uint8)
        sk.io.imsave(png, im, check_contrast=False)