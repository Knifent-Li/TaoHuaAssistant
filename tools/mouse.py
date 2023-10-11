import ctypes
import time
from ctypes import wintypes

# Constants for mouse input
WM_MOUSEMOVE = 0x0200
WM_LBUTTONDOWN = 0x0201
WM_LBUTTONUP = 0x0202

# Target window title
target_window_title = "桃花源记2"

# Find the handle of the target window
target_window = ctypes.windll.user32.FindWindowW(None, target_window_title)


class POINT(ctypes.Structure):
    _fields_ = [("x", ctypes.c_long),
                ("y", ctypes.c_long)]


# Convert screen coordinates to window-relative coordinates
def screen_to_window(hwnd, screen_x, screen_y):
    point = POINT(screen_x, screen_y)
    ctypes.windll.user32.ScreenToClient(hwnd, ctypes.byref(point))
    return point.x, point.y


# Simulate mouse movement
def simulate_mouse_move(hwnd, x, y):
    lParam = y << 16 | x
    ctypes.windll.user32.SendMessageW(hwnd, WM_MOUSEMOVE, 0, lParam)


# Simulate left mouse button down
def simulate_left_button_down(hwnd, x, y):
    lParam = y << 16 | x
    ctypes.windll.user32.SendMessageW(hwnd, WM_LBUTTONDOWN, 1, lParam)


# Simulate left mouse button up
def simulate_left_button_up(hwnd, x, y):
    lParam = y << 16 | x
    ctypes.windll.user32.SendMessageW(hwnd, WM_LBUTTONUP, 0, lParam)


# Get the coordinates where you want to simulate the click
# x, y坐标需要减去title bar 的 20个 pixel
x = 401
y = 538
# dx, dy = screen_to_window(target_window_title, x, y)
dx, dy = x, y

# Simulate mouse movement to the target window
simulate_mouse_move(target_window, dx, dy)

# Pause for a brief moment to allow the mouse movement to take effect
time.sleep(0.1)

# Simulate left mouse button down on the target window
simulate_left_button_down(target_window, dx, dy)

# Pause for a brief moment to simulate holding the left button down
time.sleep(0.1)

# Simulate left mouse button up on the target window
simulate_left_button_up(target_window, dx, dy)
