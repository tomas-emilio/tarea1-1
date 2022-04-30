# coding=utf-8

import glfw
from OpenGL.GL import *
import numpy as np
import sys, os.path

class Controller(object):
    def __init__(self):
         
        self.fillPolygon = True
        self.leftClickOn = False
        self.mousePos = (0,0)

    def on_key(self, window, key, scancode, action, mods):
        if action != glfw.PRESS:
            return

        if key == glfw.KEY_SPACE:
            self.fillPolygon = not self.fillPolygon

        elif key == glfw.KEY_ESCAPE:
            glfw.set_window_should_close(window, True)

        else:
            print('Unknown key')
    
    def cursor_pos_callback(self, window, x, y):
        self.mousePos = (x, y)


    def mouse_button_callback(self, window, button, action, mods):

        """
        glfw.MOUSE_BUTTON_1: left click
        glfw.MOUSE_BUTTON_2: right click
        glfw.MOUSE_BUTTON_3: scroll click
        """

        if (action == glfw.PRESS or action == glfw.REPEAT):
            if (button == glfw.MOUSE_BUTTON_1):
                self.leftClickOn = True

        elif (action == glfw.RELEASE):
            if (button == glfw.MOUSE_BUTTON_1):
                self.leftClickOn = False