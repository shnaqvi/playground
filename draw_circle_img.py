'''
Create and Save an image with center portion lit
Date: 1/25/23
Contact: shnaqvi@alumni.stanford.edu
'''
#%%
import numpy as np
import matplotlib.image as mimg
import matplotlib.pyplot as plt
import os
from enum import Enum
import json

Shape = Enum('Shapes', 'square, plus, circle, ring')

class DictAttr():
    def __init__(self, my_dict):
        for key, value in my_dict.items():
            setattr(self, key, value)

def draw_shape(im, draw_params):
    shape_type, pos, feat_size, feat_thick, _, _= [getattr(draw_params, attr) for attr in draw_params.__dict__.keys() 
                                                 if not callable(getattr(draw_params, attr)) 
                                                 and not attr.startswith("__")]

    if shape_type == Shape.square:
        box_rows = np.r_[pos[0] - 1 - feat_size:pos[0] + 1 + feat_size]
        box_cols = np.r_[pos[1] - 1 - feat_size:pos[1] + 1 + feat_size]
        im[box_rows[:, None], box_cols, 1] = 1

    elif shape_type == Shape.plus:
        im[pos[0] - 1 - feat_thick: pos[0] + feat_thick, pos[1] - 1 - feat_size: pos[1] + 1 + feat_size, 1] = 1
        im[pos[0] - 1 - feat_size: pos[0] + 1 + feat_size, pos[1] - 1 - feat_thick: pos[1] + feat_thick, 1] = 1
        
    elif shape_type in (Shape.circle, Shape.ring):
        xx, yy = np.meshgrid(range(im.shape[1]), range(im.shape[0]))
        r = np.sqrt((xx - pos[1])**2 + (yy - pos[0])**2)

        if shape_type == Shape.circle:
            im[r < feat_size, 1] = 1
        else:
            im[(r < feat_size) & (r > feat_size - feat_thick), 1] = 1

    return im


if __name__ == '__main__':
    
    # Define Constants
    # XXX: Draw Circle at the Center by setting `grid_size` to 1
    im_res = np.array((3144, 3648))
    overwrite_seq = True
    data_dir = '/Volumes/flamingo_data-1/_Salman/_calibration/Jan23_loft/dataset_apr3/pattern' #'data'
    draw_params = {
        'shape_type': Shape.plus,
        'pos': [0, 0],
        'feat_size': 20,
        'feat_thick': 5,
        'grid_size': 3, 
        'grid_only': False
    }
    draw_params = DictAttr(draw_params)

    pos_increm = (im_res/(draw_params.grid_size+1)).astype(int)
    im_grid = np.zeros((im_res[0], im_res[1], 3))  

    # Loop over points in grid
    # XXX: for condensed grid, define another parameter, `grid_start`
    im_names = []
    for row_id in range(draw_params.grid_size):
        for col_id in range(draw_params.grid_size):

            draw_params.pos =  [0 + (row_id+1)*pos_increm[0], 
                                0 + (col_id+1)*pos_increm[1]]
            im_grid = draw_shape(im_grid, draw_params)

            # Create separate images for each point source and save
            if not draw_params.grid_only and draw_params.grid_size > 1:
                im = np.zeros((im_res[0], im_res[1], 3))     
                im = draw_shape(im, draw_params)

                im_names.append(f'g-{draw_params.shape_type.name}-{row_id+1}-{col_id+1}')
                mimg.imsave(os.path.join(data_dir, f'{im_names[-1]}.png'), im)#, cmap=plt.cm.gray)

    im_names.append(f'g-{draw_params.shape_type.name}-grid')
    mimg.imsave(os.path.join(data_dir, f'{im_names[-1]}.png'), im_grid)#, cmap=plt.cm.gray)

    
    #%%  Overwrite Sequence file with image names
    if overwrite_seq:
        seq = json.load(open(os.path.join(data_dir, 'sequence.json')))
        seq['images'] = im_names
        seq['patterns'][0] = list(range(len(im_names)))
        seq['patterns'][1] = list(len(im_names)-1)
        json.dump(seq, open(os.path.join(data_dir, 'sequence.json'), 'w'),
              indent=4, separators=(',', ': '))


    # plt.imshow(im)
    # plt.axis('off')
    
