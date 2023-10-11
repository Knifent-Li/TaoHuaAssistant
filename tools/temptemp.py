# -*- coding: utf-8 -*-
import time

import win32gui
import win32con
import win32api

win_hwnd = win32gui.FindWindow("#32770", "提示")
# thyj_win = win32gui.FindWindow('#32770', '桃花源记2更新')
thyj_win = win32gui.FindWindow('#32770', '桃花源记2')


# This function blocks or unblocks user input to the specified window
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


# Example usage: block input to a window with the title "Line App"
# set_input_blocked("桃花源记2更新", blocked=True)
# time.sleep(10)

# Example usage: unblock input to a window with the title "Line App"
# set_input_blocked("桃花源记2更新", blocked=False)

set_input_blocked("桃花源记2", blocked=True)

time.sleep(5)
win32api.SendMessage(thyj_win, win32con.WM_LBUTTONDOWN, 0, (692 << 16 | 986))
win32api.SendMessage(thyj_win, win32con.WM_LBUTTONUP, 0, (692 << 16 | 986))
time.sleep(5)
# Example usage: unblock input to a window with the title "Line App"
set_input_blocked("桃花源记2", blocked=False)
