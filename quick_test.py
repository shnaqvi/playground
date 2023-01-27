


# Press the green button in the gutter to run the script.
if __name__ == '__main__':


    '''
    # 1/27/23 - Salman Naqvi
    import numpy as np
    import matplotlib.pyplot as plt
    import matplotlib.image as mimg
    import os
    
    # Create and Save an image with center portion lit
    im = np.zeros((3144, 3648))
    pad_sz = 6

    im_ctr_rows = np.r_[im.shape[0] / 2 - 1 - pad_sz:im.shape[0] / 2 + 1 + pad_sz].astype(int)
    im_ctr_cols = np.r_[im.shape[1] / 2 - 1 - pad_sz:im.shape[1] / 2 + 1 + pad_sz].astype(int)
    im[im_ctr_rows[:, None], im_ctr_cols] = 100

    mimg.imsave(os.path.join('data', f'im_ctr_pix.png'), im, cmap=plt.cm.gray)
    '''