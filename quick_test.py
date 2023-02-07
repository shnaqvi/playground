import os
import matplotlib.pyplot as plt
from PIL import Image
import skimage as sk
import numpy as np
import cv2


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    '''
    # 1/27/23 - Salman Naqvi
    import numpy as np
    import matplotlib.image as mimg
    import matplotlib.pyplot as plt
    import os

    # Create and Save an image with center portion lit
    im = np.zeros((3144, 3648))
    pad_sz = 30
    xx, yy = np.meshgrid(range(3648), range(3144))
    r = np.sqrt((xx-(im.shape[1] / 2))**2 + (yy-(im.shape[0] / 2))**2)
    im[r < pad_sz] = 1
    
    mimg.imsave(os.path.join('data', f'im_ctr_pix.png'), im, cmap=plt.cm.gray)
    '''