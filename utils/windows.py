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
        return (width, height)

    def send_key(self, key):
        virtual_key = win32api.MapVirtualKey(ord(key), win32con.MAPVK_VK_TO_VSC)
        win32api.PostMessage(self.handle, win32con.WM_KEYDOWN, virtual_key, 0)
        win32api.PostMessage(self.handle, win32con.WM_KEYUP, virtual_key, 0)

    def send_click(self, x, y):
        lParam = win32api.MAKELONG(x, y)
        win32api.PostMessage(self.handle, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lParam)
        win32api.PostMessage(self.handle, win32con.WM_LBUTTONUP, 0, lParam)
