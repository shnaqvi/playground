import glfw
from OpenGL.GL import *
import numpy as np


class Monitor:
    def __init__(self, monitor):
        self.monitor = monitor
        self.name = glfw.get_monitor_name(monitor)
        panel_mode = glfw.get_video_mode(monitor)
        self.width, self.height = panel_mode.size
        self.ref_rate = panel_mode.refresh_rate

        print(f'Running on {self.name}, {self.width} x {self.height} @ {self.ref_rate} Hz monitor')

        self.__setup_window()

    def get_resolution(self):
        return self.width, self.height

    def get_name(self):
        return self.name

    def get_window(self):
        return self.window

    @staticmethod
    def select_monitor(index=None, width=0, height=0):
        # Initialize GLFW
        if not glfw.init():
            raise Exception('glfw failed init')

        monitors = glfw.get_monitors()

        if index is not None:
            return monitors[index]
        else:
            selected_monitor = []
            for monitor in monitors:
                mode = glfw.get_video_mode(monitor)
                if mode.size.width != width and mode.size.height != height:
                    continue
                else:
                    selected_monitor.append(monitor)
            if len(selected_monitor) > 1:
                raise Exception('more than 1 monitor matching required resolution detected')
            if not len(selected_monitor):
                raise Exception('monitor not found matching required resolution')

            return selected_monitor[0]

    @staticmethod
    def __key_input_clb(window, key, scancode, action, mode):
        if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
            glfw.set_window_should_close(window, True)

    def __setup_window(self):
        # Create window
        glfw.default_window_hints()
        glfw.window_hint(glfw.DECORATED, glfw.FALSE)
        glfw.window_hint(glfw.AUTO_ICONIFY, glfw.FALSE)  # IMP: Ensures window doesn't disappear if scope is lost

        self.window = glfw.create_window(self.width, self.height, "Panel Pattern", self.monitor, None)
        self.x0, self.y0, self.x1, self.y1 = 0, 0, self.width, self.height

        if not self.window:
            raise Exception("glfw_create_window(...) failed!");
        glfw.make_context_current(self.window)

        # Clear Display to Black
        glClear(GL_COLOR_BUFFER_BIT)
        glfw.swap_buffers(self.window)
        glfw.poll_events()

        # Load Projection Matrix
        glLoadIdentity()
        glOrtho(0, self.width, self.height, 0, -1, +1)

        # Generate & Bind Texture and Set Options
        self.tex = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.tex)
        glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glEnable(GL_TEXTURE_2D)

        # Set Keyboard input callback
        glfw.set_key_callback(self.window, self.__key_input_clb)

        # Get the mouse off the panel window
        glfw.set_input_mode(self.window, glfw.CURSOR, glfw.CURSOR_HIDDEN)

    def show_image(self, img):
        # img_data = np.array(list(img.getdata()), np.uint8) #with PIL

        # Draw the image
        glfw.poll_events()
        glfw.make_context_current(self.window)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, img.shape[1], img.shape[0], 0, GL_RGB, GL_UNSIGNED_BYTE, img) #with PIL: img_data, img.size[0], img.size[1]
        glClear(GL_COLOR_BUFFER_BIT)
        glBegin(GL_QUADS)
        glTexCoord2f(0, 0); glVertex2i(self.x0, self.y0)
        glTexCoord2f(0, 1); glVertex2i(self.x0, self.y1)
        glTexCoord2f(1, 1); glVertex2i(self.x1, self.y1)
        glTexCoord2f(1, 0); glVertex2i(self.x1, self.y0)
        glEnd()
        glfw.swap_buffers(self.window)


    def clear_image(self):
        # Clear the screen
        glClear(GL_COLOR_BUFFER_BIT)
        glfw.swap_buffers(self.window)
        glfw.poll_events()
        if glfw.window_should_close(self.window):
            raise Exception("program terminated by user")


    def close_window(self):
        glfw.set_window_should_close(self.window, True)
        glfw.terminate()