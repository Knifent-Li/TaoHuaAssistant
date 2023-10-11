# -*- coding: utf-8 -*-
import time

import cv2
import win32api
import win32con
import win32gui
import win32ui
import numpy as np
from skimage.metrics import structural_similarity as ssim
# WM_MOUSEMOVE = 0x0200
# WM_LBUTTONDOWN = 0x0201
# WM_LBUTTONUP = 0x0202


def wait_for_window(win_class, win_title, timeout=10):
    start_time = time.time()
    while True:
        if win32gui.FindWindow(win_class, win_title):
            return win32gui.FindWindow(win_class, win_title)
        elapsed_time = time.time() - start_time
        if elapsed_time >= timeout:
            return False
        time.sleep(0.1)


def get_menu_item_handle(win_hwnd, submenu_index=0, menu_item_index=0):
    menu_handle = win32gui.GetMenu(win_hwnd)
    submenu_handle = win32gui.GetSubMenu(menu_handle, submenu_index)
    menu_item_handle = win32gui.GetMenuItemID(submenu_handle, menu_item_index)
    return menu_item_handle


def send_str(text, widget_hwnd):
    fstr = [ord(c) for c in text]
    for item in fstr:
        win32api.PostMessage(widget_hwnd, win32con.WM_CHAR, item, 0)


def send_enter_key(win_hwnd):
    win32api.PostMessage(win_hwnd, win32con.WM_KEYDOWN, 0x0D, 0)


def access_menu(win_hwnd, menu_item_hwnd):
    win32api.PostMessage(win_hwnd, win32con.WM_COMMAND, menu_item_hwnd, 0)


def traversal_ctrl_hwnd(win_hwnd, ctrl_id, ctrl_index):
    hwdlist = []
    id_count = 0
    win32gui.EnumChildWindows(win_hwnd, lambda hwnd, param: param.append(hwnd), hwdlist)
    for i in hwdlist:
        now_id = win32gui.GetDlgCtrlID(i)
        if now_id == ctrl_id:
            id_count += 1
        if id_count == ctrl_index:
            control_handle = i
            return control_handle


def lock_unlock_win(win_hwnd, blocked=True):
    # Find the window handle
    # hwnd = win32gui.FindWindow(None, win_title)
    # if hwnd == 0:
    #     return

    # Modify the window style to disable or enable user input
    style = win32api.GetWindowLong(win_hwnd, win32con.GWL_STYLE)
    if blocked:
        style |= win32con.WS_DISABLED
    else:
        style &= ~win32con.WS_DISABLED
    win32api.SetWindowLong(win_hwnd, win32con.GWL_STYLE, style)


def send_position_click(hwnd, x, y, delay=0.1):
    # Simulate mouse movement
    def simulate_mouse_move(inter_hwnd, x, y):
        lParam = win32api.MAKELONG(x, y)
        win32gui.SendMessage(inter_hwnd, win32con.WM_MOUSEMOVE, 0, lParam)

    # Simulate left mouse button down
    def simulate_left_button_down(inter_hwnd, x, y):
        lParam = win32api.MAKELONG(x, y)
        win32gui.SendMessage(inter_hwnd, win32con.WM_LBUTTONDOWN, 1, lParam)

    # Simulate left mouse button up
    def simulate_left_button_up(inter_hwnd, x, y):
        lParam = win32api.MAKELONG(x, y)
        win32gui.SendMessage(inter_hwnd, win32con.WM_LBUTTONUP, 0, lParam)
    # Simulate mouse movement to the target window
    simulate_mouse_move(hwnd, x, y)

    # Pause for a brief moment to allow the mouse movement to take effect
    time.sleep(delay)

    # Simulate left mouse button down on the target window
    simulate_left_button_down(hwnd, x, y)

    # Pause for a brief moment to simulate holding the left button down
    time.sleep(delay)

    # Simulate left mouse button up on the target window
    simulate_left_button_up(hwnd, x, y)


def is_widget_visible(hwnd, timeout=10):
    """
    Check if a widget is visible, waiting until it becomes visible or until the timeout is reached.

    :param hwnd: The handle of the widget.
    :param timeout: The maximum time to wait for the widget to become visible, in seconds. Default is 10.
    :return: True if the widget becomes visible within the timeout, otherwise False.
    """
    start_time = time.time()

    # Continue looping until the timeout is reached
    while time.time() - start_time < timeout:
        # Check if the widget is enabled
        if win32gui.IsWindowEnabled(hwnd) == 1:
            return True
        time.sleep(0.1)

    return False


def wait_dlg_item_hwnd(win_hwnd, ctrl_id, timeout=10):
    """
    Get the handle of a dialog item, waiting until it appears or until the timeout is reached.

    :param win_hwnd: The window handle of the dialog.
    :param ctrl_id: The control ID of the item.
    :param timeout: The maximum time to wait for the item to appear, in seconds. Default is 10.
    :return: The handle of the dialog item if it appears within the timeout, otherwise None.
    """
    start_time = time.time()

    while time.time() - start_time < timeout:
        # Try to get the item
        item_hwnd = win32gui.GetDlgItem(win_hwnd, ctrl_id)
        if item_hwnd != 0:
            return item_hwnd
        time.sleep(0.1)

    return None


def send_btn_click(win_hwnd):
    win32gui.SendMessage(win_hwnd, win32con.BM_CLICK, 0, 0)


def compare_screenshot_with_image(image_path, win_hwnd, a_upper_left, a_size):

    def _screenshot(hwnd, upper_left, size):
        w, h = size

        # Convert screen coordinates to window coordinates
        upper_left_window = (upper_left[0], upper_left[1])

        # Get window's device context
        hwnd_dc = win32gui.GetWindowDC(hwnd)

        # Create a new device context based on the existing one
        mfc_dc = win32ui.CreateDCFromHandle(hwnd_dc)

        # Create a memory device context
        save_dc = mfc_dc.CreateCompatibleDC()

        # Create a bitmap object
        save_bitmap = win32ui.CreateBitmap()
        save_bitmap.CreateCompatibleBitmap(mfc_dc, w, h)

        # Select the bitmap object into our saved memory device context
        save_dc.SelectObject(save_bitmap)

        # BitBlt the bitmap from the window's device context to our memory device context
        save_dc.BitBlt((0, 0), (w, h), mfc_dc, upper_left_window, win32con.SRCCOPY)

        # Save screenshot to file
        temp_screenshot_path = 'temp_screenshot.bmp'
        save_bitmap.SaveBitmapFile(save_dc, temp_screenshot_path)

        # Clean up
        win32gui.DeleteObject(save_bitmap.GetHandle())
        save_dc.DeleteDC()
        mfc_dc.DeleteDC()
        win32gui.ReleaseDC(hwnd, hwnd_dc)

        return temp_screenshot_path

    def is_similar(image_a, image_b):
        # Convert the images to grayscale
        image_a = cv2.cvtColor(image_a, cv2.COLOR_BGR2GRAY)
        image_b = cv2.cvtColor(image_b, cv2.COLOR_BGR2GRAY)

        # Compute SSIM between two images
        return ssim(image_a, image_b) > 0.95  # You can adjust the threshold

    # Get the screenshot as an image file path
    screenshot_file_path = _screenshot(win_hwnd, a_upper_left, a_size)

    # Load the screenshot and the existing image
    screenshot_image = cv2.imread(screenshot_file_path)
    # Open the file as bytes
    with open(image_path, 'rb') as f:
        image_bytes = np.asarray(bytearray(f.read()), dtype=np.uint8)

    # Decode the image bytes
    existing_image = cv2.imdecode(image_bytes, cv2.IMREAD_COLOR)

    # Compare the two images
    while not is_similar(screenshot_image, existing_image):
        time.sleep(1.5)  # you can adjust sleep time
        screenshot_file_path = _screenshot(win_hwnd, a_upper_left, a_size)
        screenshot_image = cv2.imread(screenshot_file_path)

    # At this point, the images are considered to be similar
    return True


def get_new_win(win_title, win_class, known_handles):

    def enum_windows_callback(hwnd, params):
        window_name, window_class = params
        window_text = win32gui.GetWindowText(hwnd)
        class_name = win32gui.GetClassName(hwnd)
        if window_name in window_text and class_name == window_class:
            known_handles.add(hwnd)
        return True

    # Store the current handles
    previous_handles = known_handles.copy()

    # Update the current handles
    known_handles.clear()
    win32gui.EnumWindows(enum_windows_callback, (win_title, win_class))

    # Get the new handles
    new_handles = known_handles - previous_handles

    # Return only one handle or None if there are no new windows
    return next(iter(new_handles), None)


def delete_elements(win_hwnd, count=20):
    """
    Delete a specific number of elements by simulating the left arrow and delete key presses.

    :param win_hwnd: The handle of the window to send the key presses to.
    :param count: The number of elements to delete. Default is 20.
    """
    VK_LEFT = 0x25
    VK_DELETE = 0x2E

    for _ in range(count):
        # Simulate pressing the left arrow key
        win32api.SendMessage(win_hwnd, win32con.WM_KEYDOWN, VK_LEFT, 0)
        # Simulate pressing the delete key
        win32api.SendMessage(win_hwnd, win32con.WM_KEYDOWN, VK_DELETE, 0)
