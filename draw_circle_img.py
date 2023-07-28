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
import cv2
import cv2.aruco as aruco

Shape = Enum('Shapes', 'square, plus, circle, ring, aruco, charuco, checker')

class DictAttr():
    def __init__(self, my_dict):
        for key, value in my_dict.items():
            setattr(self, key, value)

def draw_shape(im, draw_params, row_id, col_id):
    shape_type, _, pos, feat_size, feat_thick, grid_size, _, _= [getattr(draw_params, attr) for attr in draw_params.__dict__.keys() 
                                                      if not callable(getattr(draw_params, attr)) 
                                                      and not attr.startswith("__")]

    if shape_type == Shape.square:
        box_rows = np.r_[np.maximum(0, pos[0] - int(feat_size/2)):pos[0] + int(feat_size/2) + 1]
        box_cols = np.r_[np.maximum(0, pos[1] - int(feat_size/2)):pos[1] + int(feat_size/2) + 1]
        im[box_rows[:, None], box_cols, 1] = 1

    elif shape_type == Shape.plus:
        im[np.maximum(0, pos[0] - int(feat_thick/2)): pos[0] + int(feat_thick/2) + 1, 
           np.maximum(0, pos[1] - int(feat_size/2)): pos[1] + int(feat_size/2) + 1, 
           1] = 1
        im[np.maximum(0, pos[0] - int(feat_size/2)): pos[0] + int(feat_size/2) + 1, 
           np.maximum(0, pos[1] - int(feat_thick/2)): pos[1] + int(feat_thick/2) + 1, 
           1] = 1
        
    elif shape_type in (Shape.circle, Shape.ring):
        xx, yy = np.meshgrid(range(im.shape[1]), range(im.shape[0]))
        r = np.sqrt((xx - pos[1])**2 + (yy - pos[0])**2)

        if shape_type == Shape.circle:
            im[r < feat_size, 1] = 1
        else:
            im[(r < feat_size) & (r > feat_size - feat_thick), 1] = 1
    
    elif shape_type == Shape.aruco:
        aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_250)
        tag_size = feat_size 

        tag_id = (grid_size*row_id)+(col_id+1)
        im_tag = aruco.generateImageMarker(aruco_dict, id=tag_id, sidePixels=tag_size, borderBits=2)
        im_tag = cv2.normalize(im_tag, None, 0, 1, cv2.NORM_MINMAX)

        im[int(pos[0]-tag_size/2)-200:int(pos[0]-tag_size/2)+tag_size+200,
           int(pos[1]-tag_size/2)-200:int(pos[1]-tag_size/2)+tag_size+200, 1] = 1
        im[int(pos[0]-tag_size/2):int(pos[0]-tag_size/2)+tag_size,
           int(pos[1]-tag_size/2):int(pos[1]-tag_size/2)+tag_size, 1] = im_tag
        
    elif shape_type == Shape.charuco:
        aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_250)
        tag_size = feat_size 

        board = aruco.CharucoBoard((2, 2), 1, .7, aruco_dict)
        im_board = board.generateImage((tag_size,tag_size), 0, 0)
        im_board = cv2.normalize(im_board, None, 0, 1, cv2.NORM_MINMAX)

        im[int(pos[0]-tag_size/2):int(pos[0]-tag_size/2)+tag_size,
           int(pos[1]-tag_size/2):int(pos[1]-tag_size/2)+tag_size, 1] = im_board
    
    elif shape_type == Shape.checker:
        im_checker = np.zeros((feat_size, feat_size))
        square_size = int(feat_size/2)
        im_checker[square_size:square_size+square_size, 0:square_size] = 1
        im_checker[0:square_size, square_size:square_size+square_size] = 1
        im[pos[0]-square_size:pos[0]-square_size+feat_size,
           pos[1]-square_size:pos[1]-square_size+feat_size, 1] = im_checker
        
    return im


if __name__ == '__main__':
    
    # Define Constants
    # XXX: Draw Circle at the Center by setting `grid_size` to 1
    overwrite_seq = True
    data_dir = '/Volumes/flamingo_data/_Salman/_calibration/Jan23_loft/dataset_jun23/pattern_psf' #'data'
    draw_params = {
        'shape_type': Shape.circle,
        'im_size': (3144, 3648),
        'pos': [0, 0],
        'feat_size': 4,    #1000 for ghost, 10 for psf
        'feat_thick': 100,
        'grid_size': 5,    #4 for psf
        'grid_start': 600, #1000 for ghost, 500 for psf
        'grid_only': False
    }
    draw_params = DictAttr(draw_params)

    # Evaluate distance between shapes
    pos_increm = ((np.array(draw_params.im_size) - draw_params.grid_start*2)/
                  (draw_params.grid_size-1)).astype(int)
    im_grid = np.zeros((*draw_params.im_size, 3))  

    # Detect Checker
    # import skimage as sk
    # im = cv2.imread('/Volumes/flamingo_data-1/_Salman/_calibration/Jan23_loft/dataset_apr3/raw_captures/checker.png')
    # # im[im>60] = 0
    # # im = sk.exposure.rescale_intensity(im, out_range=(0, 255)).astype(np.uint8)
    # ret, corners = cv2.findChessboardCorners(im, (4,4), None)
    # # im = cv2.drawChessboardCorners(im, (4,4), corners,ret)
    # plt.imshow(im)

    # # Detect Markers and Draw Corners
    # im = cv2.imread('/Volumes/flamingo_data-1/_Salman/_calibration/Jan23_loft/dataset_apr3/raw_captures/zn10_plus.jpeg')
    # import skimage as sk
    # # im = sk.io.imread('/Volumes/flamingo_data-1/_Salman/_calibration/Jan23_loft/dataset_apr3/raw_captures/aruco_copy.png')
    # # im[im>50] = 0
    # # im = sk.exposure.rescale_intensity(im, out_range=(0, 255)).astype(np.uint8)

    # fld = cv2.ximgproc.createFastLineDetector(length_threshold=10)  # 85
    # lines = fld.detect(im)
    # im_segs = fld.drawSegments(np.zeros_like(impr, dtype=np.uint8), lines, linethickness=5)

    # im = cv2.convertScaleAbs(im, 10, 4)
    # kernel = np.array([[0, -1, 0],
    #                [-1, 5,-1],
    #                [0, -1, 0]])
    # im = cv2.filter2D(src=im, ddepth=-1, kernel=kernel)
    # arucoDict = aruco.getPredefinedDictionary(aruco.DICT_4X4_250)
    # arucoParams = cv2.aruco.DetectorParameters()
    # (corners, ids, rejected) = cv2.aruco.detectMarkers(im, arucoDict,
    #                                                 parameters=arucoParams)
    # print(corners)
    # # cv2.aruco.drawDetectedMarkers(im, corners, ids)
    # plt.imshow(im)
    # for tags in corners:
    #     for corner in np.squeeze(tags):
    #         plt.plot(*corner, 'xr')

    #%%
    # Save an all Black image
    mimg.imsave(os.path.join(data_dir, 'black.png'), np.zeros((*draw_params.im_size, 3)))#, cmap=plt.cm.gray)

    im_names = []
    feat_loc = np.empty((0, 4), int)
    # Draw point in the center of the grid
    draw_params.pos =  (np.array(draw_params.im_size)/2).astype(int)
    im_grid = draw_shape(im_grid, draw_params, 0, 0)
    im_names.append(f'g-{draw_params.shape_type.name}{draw_params.feat_size}-0-0')
    mimg.imsave(os.path.join(data_dir, f'{im_names[-1]}.png'), im_grid)#, cmap=plt.cm.gray)
    feat_loc = np.vstack([feat_loc, [0, 0, *draw_params.pos]])

    # Loop over points in grid
    if draw_params.grid_size > 1:
        for row_id in range(draw_params.grid_size):
            for col_id in range(draw_params.grid_size):

                # Skip image at the center that was previously drawn
                if (draw_params.grid_size+1)%2==0:
                    if row_id+1==(draw_params.grid_size+1)/2 and \
                        col_id+1==(draw_params.grid_size+1)/2:
                        continue

                draw_params.pos =  [draw_params.grid_start + (row_id)*pos_increm[0], 
                                    draw_params.grid_start + (col_id)*pos_increm[1]]
                im_grid = draw_shape(im_grid, draw_params, row_id, col_id)

                # Create separate images for each point source and save
                if not draw_params.grid_only and draw_params.grid_size > 1:
                    im = np.zeros((draw_params.im_size[0], draw_params.im_size[1], 3))     
                    im = draw_shape(im, draw_params, row_id, col_id)

                    im_names.append(f'g-{draw_params.shape_type.name}{draw_params.feat_size}-{row_id+1}-{col_id+1}')
                    mimg.imsave(os.path.join(data_dir, f'{im_names[-1]}.png'), im)#, cmap=plt.cm.gray)
                    
                    feat_loc = np.vstack([feat_loc, [col_id+1, row_id+1, *draw_params.pos]])

    # plt.imshow(im_grid)

    im_names.append(f'g-{draw_params.shape_type.name}{draw_params.feat_size}-grid')
    mimg.imsave(os.path.join(data_dir, f'{im_names[-1]}.png'), im_grid)#, cmap=plt.cm.gray)

    # Write Locations of all features to JSON
    json.dump(feat_loc.tolist(), open(os.path.join(data_dir, f'{draw_params.shape_type.name}-locations.json'), 'w'),
            indent=4, separators=(',', ': '))
    
    #%%  Overwrite Sequence file with image names
    if overwrite_seq:
        seq = json.load(open(os.path.join(data_dir, 'sequence.json')))
        seq['images'] = im_names
        seq['patterns'][0] = list(range(len(im_names)))
        seq['patterns'][1] = list([len(im_names)-1])
        json.dump(seq, open(os.path.join(data_dir, 'sequence.json'), 'w'),
              indent=4, separators=(',', ': '))


    # plt.imshow(im)
    # plt.axis('off')
    

    # # Detect Markers and Draw Corners
    # im = cv2.imread('/Volumes/flamingo_data/_Salman/_calibration/Jan23_loft/dataset_apr3/pattern/g-aruco-grid.png')
    # arucoDict = aruco.getPredefinedDictionary(aruco.DICT_4X4_250)
    # arucoParams = cv2.aruco.DetectorParameters()
    # (corners, ids, rejected) = cv2.aruco.detectMarkers(im, arucoDict,
    #                                                 parameters=arucoParams)
    # # cv2.aruco.drawDetectedMarkers(im, corners, ids)
    # plt.imshow(im)
    # for tags in corners:
    #     for corner in np.squeeze(tags):
    #         plt.plot(*corner, 'xr')
