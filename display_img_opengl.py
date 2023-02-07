"""
Open a Full-screen window on a Specified monitor and Display an Image
Date: 1/25/23
Contact: shnaqvi@alumni.stanford.edu
Packages: glfw, pyopengl
"""

import glfw
import PIL
import numpy as np
import time
import argparse
import sys
from monitor import Monitor


def main(args):
    # Parse Arguments ###################
    parser = argparse.ArgumentParser(
        description='Display image on a Full-screen window on a specified monitor',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--mon_ind', help='index of the monitor', default=0)
    parser.add_argument('--im_path', help='full path to the image',
                        default='/Users/salman_naqvi/Documents/Pictures/AppleLogo.jpg')
    args = parser.parse_args(args)
    print("**** {0} **** ".format(parser.description))

    # Get monitors and select required
    monitor = Monitor.select_monitor(index=args.mon_ind, width=3648, height=3144)
    my_monitor = Monitor(monitor)

    # Show image
    img = PIL.Image.open(args.im_path)

    start = time.time()
    while not glfw.window_should_close(my_monitor.get_window()) and time.time() < start + 5:
        my_monitor.show_image(img)

    my_monitor.clear_image()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main(sys.argv[1:])

