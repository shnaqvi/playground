'''
Create and Save an image with center portion lit
Date: 1/25/23
Contact: shnaqvi@alumni.stanford.edu
'''

import numpy as np
import matplotlib.image as mimg
import matplotlib.pyplot as plt
import os


if __name__ == '__main__':
    im = np.zeros((3144, 3648))
    pad_sz = 30
    shape_type = 'circle'

    if shape_type == 'square':
        im_ctr_rows = np.r_[im.shape[0] / 2 - 1 - pad_sz:im.shape[0] / 2 + 1 + pad_sz].astype(int)
        im_ctr_cols = np.r_[im.shape[1] / 2 - 1 - pad_sz:im.shape[1] / 2 + 1 + pad_sz].astype(int)
        im[im_ctr_rows[:, None], im_ctr_cols] = 1
    elif shape_type == 'circle':
        xx, yy = np.meshgrid(range(3648), range(3144))
        r = np.sqrt((xx - (im.shape[1] / 2))**2 + (yy - (im.shape[0] / 2))**2)
        im[r < pad_sz] = 1

    mimg.imsave(os.path.join('data', f'im_ctr_pix.png'), im, cmap=plt.cm.gray)
