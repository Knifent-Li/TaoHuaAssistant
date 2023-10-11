# -*- coding: utf-8 -*-
import ctypes
import time

import win32con
import win32api
import win32gui

# Target window title
target_window_title = "桃花源记2"

target_window = win32gui.FindWindow(None, target_window_title)

# Get the dimensions of the target window
window_rect = win32gui.GetWindowRect(target_window)

# Get the current coordinates of the mouse cursor


def set_input_blocked(window_title, blocked=True):
    # Find the window handle
    hwnd = win32gui.FindWindow(None, window_title)
    if hwnd == 0:
        print(f"Error: Could not find window with title '{window_title}'")
        return

    # Modify the window style to disable or enable user input
    style = win32api.GetWindowLong(hwnd, win32con.GWL_STYLE)
    if blocked:
        style |= win32con.WS_DISABLED
        print(f"Blocked user input to window with title '{window_title}'")
    else:
        style &= ~win32con.WS_DISABLED
        print(f"Restored user input to window with title '{window_title}'")
    win32api.SetWindowLong(hwnd, win32con.GWL_STYLE, style)


def compare_pixel_color(window_handle, x, y):
    hdc_window = ctypes.windll.user32.GetDC(window_handle)
    pixel_color = ctypes.windll.gdi32.GetPixel(hdc_window, x, y)
    r = pixel_color & 0xFF
    g = (pixel_color >> 8) & 0xFF
    b = (pixel_color >> 16) & 0xFF
    ctypes.windll.user32.ReleaseDC(window_handle, hdc_window)
    # set_input_blocked("桃花源记2", blocked=False)

    return r, g, b


# Convert screen coordinates to client coordinates (relative to the window)
# set_input_blocked("桃花源记2", blocked=False)
# set_input_blocked("桃花源记2", blocked=True)
while True:
    cursor_x, cursor_y = win32gui.GetCursorPos()
    window_rect = win32gui.GetWindowRect(target_window)
    relative_x = cursor_x - window_rect[0]
    relative_y = cursor_y - window_rect[1]
    dr, dg, db = compare_pixel_color(target_window, relative_x, relative_y)
    print(f"Relative coordinates: ({relative_x}, {relative_y})")
    print(f"{dr},{dg},{db}")
    time.sleep(2)

