# -*- coding: utf-8 -*-
import os
import sys
import time
from configparser import ConfigParser

import pywinauto
import win32api
import win32con
import win32gui


_TITLE = "2Box"
_CONFIG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', "config.ini")


def read_config(section, key=None):
    config = ConfigParser()
    config.read(_CONFIG_PATH, encoding='utf-8')

    if key is None:
        # Return all keys in the section as a dictionary
        return dict(config[section])
    else:
        # Return the value of the specified key in the section
        return config.get(section, key)


def find_idx_sub_handle(pHandle, winClass, index=0):
    """
    已知子窗口的窗体类名
    寻找第index号个同类型的兄弟窗口
    """
    assert type(index) == int and index >= 0
    handle = win32gui.FindWindowEx(pHandle, 0, winClass, None)
    while index > 0:
        handle = win32gui.FindWindowEx(pHandle, handle, winClass, None)
        index -= 1
    return handle


def find_sub_handle(p_handle, winClassList):
    """
    递归寻找子窗口的句柄
    pHandle是祖父窗口的句柄
    winClassList是各个子窗口的class列表，父辈的list-index小于子辈
    """
    assert type(winClassList) == list
    if len(winClassList) == 1:
        return find_idx_sub_handle(p_handle, winClassList[0][0], winClassList[0][1])
    else:
        p_handle = find_idx_sub_handle(p_handle, winClassList[0][0], winClassList[0][1])
        return find_sub_handle(p_handle, winClassList[1:])


def send_str(text, hwnd=None):
    fstr = [ord(c) for c in text]
    for item in fstr:
        win32api.PostMessage(hwnd, win32con.WM_CHAR, item, 0)


class Win:
    def __init__(self, window_name):
        self.window_name = window_name
        self.window_handle = None

    def wait_for_window(self, timeout=10):
        start_time = time.monotonic()
        while True:
            handle = win32gui.FindWindow(None, self.window_name)
            if handle != 0:
                self.window_handle = handle
                return True
            elif time.monotonic() - start_time > timeout:
                sys.exit(-1)
            time.sleep(1)

    def set_foreground(self):
        win32gui.SetForegroundWindow(self.window_handle)


class TwoBox(Win):
    def __init__(self, file_path):
        super().__init__(_TITLE)
        self.file_path = file_path
        self.execute()
        self.app = pywinauto.application.Application(backend="uia")
        self.app.connect(title=_TITLE, timeout=10)
        self.window = self.app.Dialog

    def execute(self):
        os.startfile(self.file_path)
        self.wait_for_window()
        self.set_foreground()

    def thyj_startup(self):
        self.window.menu_select("#0")
        # self.window.print_control_identifiers()
        menu_win = self.window['文件(F)Menu']
        menu_item_2 = self.window['MenuItem2']
        menu_2_text = menu_item_2.window_text()

        def two_box_init(dialog_window):

            hwdlist = []
            id_count = 0
            edit_control_handle = 0
            win32gui.EnumChildWindows(dialog_window.handle, lambda hwnd, param: param.append(hwnd), hwdlist)
            for i in hwdlist:
                ctrlid = win32gui.GetDlgCtrlID(i)
                if ctrlid == 1148:
                    id_count += 1
                if id_count == 3:
                    edit_control_handle = i
                    break

            send_str(read_config('DEFAULT', 'launch_path'), edit_control_handle)
            win32api.PostMessage(dialog_window.handle, win32con.WM_KEYDOWN, 0x0D, 0)

        if "launch.exe" in menu_2_text:
            menu_win.item_by_path("#1").select()

        else:
            menu_win.item_by_path("#0").select()
            open_dialog = self.window['打开Dialog']
            two_box_init(open_dialog)

        return True
