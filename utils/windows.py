#!/usr/bin/env python

import win32api
import win32con
import win32gui


class Window:
    def __init__(self, title):
        self.handle = win32gui.FindWindow(None, title)

    def get_size(self):
        rect = win32gui.GetWindowRect(self.handle)
        width = rect[2] - rect[0]
        height = rect[3] - rect[1]
        return width, height

    def send_key(self, key):
        pass

    def send_click(self, x, y):
        pass

    def get_menu(self):
        pass
