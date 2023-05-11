# -*- coding: utf-8 -*-
import time

import pyautogui
import win32api
import win32con
import win32gui

from modules.two_box import send_str, find_sub_handle

_THYJ_DLG = '桃花源记2'


def create_player(account, password):
    time.sleep(2)
    thyj_win = win32gui.FindWindow('#32770', _THYJ_DLG)
    win32api.SendMessage(thyj_win, win32con.WM_LBUTTONDOWN, 0, (692 << 16 | 986))
    win32api.SendMessage(thyj_win, win32con.WM_LBUTTONUP, 0, (692 << 16 | 986))

    while True:
        is_server_activate = pyautogui.pixelMatchesColor(958, 782, (144, 236, 248))
        if is_server_activate:
            break
        else:
            time.sleep(0.1)

    player_win_hwd = win32gui.FindWindow('TL_THYJ2_WINDOW_CLS', _THYJ_DLG)
    win32api.PostMessage(player_win_hwd, win32con.WM_KEYDOWN, 0x0D, 0)

    while True:
        is_prepare_login = pyautogui.pixelMatchesColor(1172, 779, (240, 252, 248))
        if is_prepare_login:
            break
        else:
            time.sleep(0.1)

    win32api.PostMessage(player_win_hwd, win32con.WM_KEYDOWN, 0x0D, 0)
    while True:
        is_prepare_input = pyautogui.pixelMatchesColor(962, 663, (80, 132, 208))
        if is_prepare_input:
            break
        else:
            time.sleep(0.1)

    win32api.PostMessage(player_win_hwd, win32con.WM_KEYDOWN, 0x09, 0)
    win32api.PostMessage(player_win_hwd, win32con.WM_KEYUP, 0x09, 0)
    time.sleep(0.5)
    for _ in range(0, 13):
        win32api.SendMessage(player_win_hwd, win32con.WM_KEYDOWN, 0x25, 0)
        win32api.SendMessage(player_win_hwd, win32con.WM_KEYDOWN, 0x2E, 0)

    time.sleep(0.5)
    send_str(account, player_win_hwd)

    win32api.PostMessage(player_win_hwd, win32con.WM_KEYDOWN, 0x09, 0)
    win32api.PostMessage(player_win_hwd, win32con.WM_KEYUP, 0x09, 0)
    send_str(password, player_win_hwd)

    win32api.PostMessage(player_win_hwd, win32con.WM_KEYDOWN, 0x0D, 0)
    while True:
        is_login = pyautogui.pixelMatchesColor(1183, 789, (208, 244, 248))
        if is_login:
            break
        else:
            time.sleep(0.1)

    win32api.PostMessage(player_win_hwd, win32con.WM_KEYDOWN, 0x0D, 0)

    while True:
        temp_hwnd = find_sub_handle(0, [("TL_THYJ2_WINDOW_CLS", 1)])
        temp_title = win32gui.GetWindowText(temp_hwnd)[19:22]
        if len(temp_title) != 0 and "当前" not in temp_title:
            break
        else:
            time.sleep(0.1)

    return player_win_hwd
