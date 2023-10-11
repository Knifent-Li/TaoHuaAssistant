# -*- coding: utf-8 -*-
import os
import threading
import time

import assets
from utils import win32ref
from utils.dataparser import JsonLoader

WIN_TITLE_TWOBOX = "2Box"
WIN_TITLE_THYJ = "桃花源记2"
WIN_TITLE_THYJ_UPDATE = "桃花源记2更新"
WIN_TITLE_UPDATE = "提示"
WIN_TITLE_OPEN = "打开"
WIN_CLASS_DIALOG = "#32770"
WIN_CLASS_THYJ = "TL_THYJ2_WINDOW_CLS"
UPDATE_VERIFY_BTN_ID = 2
THYJ_UPDATE_BTN_ID = 1004
THYJ_UPDATE_BTN_INDEX = 1
DLG_EDIT_CTRL_ID = 1148
DLG_EDIT_CTRL_INDEX = 3
JSON_PATH = os.path.split(os.path.realpath(__file__))[0] + r"\..\elements.json"
JSON_CENTER = "center_point"
JSON_L_POINT = "start_position"
JSON_R_POINT = "end_position"
JSON_SIZE = "size"
BUTTON_0 = "TH_0游戏界面开始"
BUTTON_1 = "TH_1进入服务器选择"
BUTTON_2 = "TH_2服务器名称填入框"
BUTTON_3 = "TH_3清空服务器名称"
BUTTON_4 = "TH_4服务器页面进入游戏"
BUTTON_5 = "TH_5账号登陆框"
BUTTON_6 = "TH_6选择角色界面进入游戏框"
EDIT_1 = "TH_33账号"
EDIT_2 = "TH_34密码"


class Assistant:
    def __init__(self, accounts, path):
        self.accounts = accounts
        self.twobox_hwnd = None
        self.client_path = path
        self.run_twobox()
        self.json_parser = JsonLoader(json_path=JSON_PATH)

    def run_twobox(self):
        os.startfile(assets.TWO_BOX_PATH)
        self.twobox_hwnd = win32ref.wait_for_window(None, WIN_TITLE_TWOBOX)

    def manage_client(self):
        pass

    def update_and_startup(self):
        menu_item_open = win32ref.get_menu_item_handle(self.twobox_hwnd)
        account_list = list(self.accounts.keys())
        handles = set()

        def open_client(dlg_hwnd, th_client_path):
            """
            Run an instance of thyj client.
            """
            edit_control_handle = win32ref.traversal_ctrl_hwnd(dlg_hwnd, DLG_EDIT_CTRL_ID, DLG_EDIT_CTRL_INDEX)

            time.sleep(1)
            win32ref.send_str(th_client_path, edit_control_handle)
            win32ref.send_enter_key(dlg_hwnd)

        for account in account_list:
            password = self.accounts[account]
            # Send a WM_COMMAND message to click the menu item
            win32ref.access_menu(self.twobox_hwnd, menu_item_open)
            twobox_dlg_hwnd = win32ref.wait_for_window(WIN_CLASS_DIALOG, WIN_TITLE_OPEN)

            open_client(twobox_dlg_hwnd, self.client_path)

            time.sleep(2)  # Todo:Delete it

            bak_client_hwnd = win32ref.wait_for_window(WIN_CLASS_DIALOG, WIN_TITLE_THYJ_UPDATE)
            enter_btn_handle = win32ref.traversal_ctrl_hwnd(bak_client_hwnd, THYJ_UPDATE_BTN_ID, THYJ_UPDATE_BTN_INDEX)

            if not win32ref.is_widget_visible(enter_btn_handle):
                update_hint_win = win32ref.wait_for_window(WIN_CLASS_DIALOG, WIN_TITLE_UPDATE, timeout=3600)
                close_btn_hwnd = win32ref.wait_dlg_item_hwnd(update_hint_win, UPDATE_VERIFY_BTN_ID)
                win32ref.send_btn_click(close_btn_hwnd)  # Todo: 确认（close）btn的出现和检测是需要等待的

            ture_client = win32ref.wait_for_window(WIN_CLASS_DIALOG, WIN_TITLE_THYJ)

            while True:
                win32ref.send_position_click(ture_client, self.json_parser.get_attribute(BUTTON_0, JSON_CENTER)[0],
                                             self.json_parser.get_attribute(BUTTON_0, JSON_CENTER)[1])
                thyj_win = win32ref.get_new_win(WIN_TITLE_THYJ, WIN_CLASS_THYJ, handles)
                if thyj_win:
                    break
            t = threading.Thread(target=self.login, args=(thyj_win, account, password))
            t.daemon = True  # Set the thread as a daemon, so it will exit when the main program exits

            win32ref.compare_screenshot_with_image(assets.GOTO_SERVER_UI, thyj_win,
                                                   self.json_parser.get_attribute(BUTTON_1, JSON_L_POINT),
                                                   self.json_parser.get_attribute(BUTTON_1, JSON_SIZE))
            win32ref.lock_unlock_win(thyj_win, blocked=True)
            win32ref.send_position_click(thyj_win, self.json_parser.get_attribute(BUTTON_1, JSON_CENTER)[0],
                                         self.json_parser.get_attribute(BUTTON_1, JSON_CENTER)[1])
            win32ref.compare_screenshot_with_image(assets.GOTO_LOGIN_UI, thyj_win,
                                                   self.json_parser.get_attribute(BUTTON_4, JSON_L_POINT),
                                                   self.json_parser.get_attribute(BUTTON_4, JSON_SIZE))
            t.start()

    def login(self, win_hwnd, spc_account, spc_password):
        win32ref.send_position_click(win_hwnd, self.json_parser.get_attribute(BUTTON_4, JSON_CENTER)[0],
                                     self.json_parser.get_attribute(BUTTON_4, JSON_CENTER)[1])
        win32ref.compare_screenshot_with_image(assets.LOGIN_BUTTON, win_hwnd,
                                               self.json_parser.get_attribute(BUTTON_5, JSON_L_POINT),
                                               self.json_parser.get_attribute(BUTTON_5, JSON_SIZE))
        win32ref.send_position_click(win_hwnd, self.json_parser.get_attribute(EDIT_1, JSON_CENTER)[0],
                                     self.json_parser.get_attribute(EDIT_1, JSON_CENTER)[1])
        win32ref.delete_elements(win_hwnd)
        win32ref.send_str(spc_account, win_hwnd)
        win32ref.send_position_click(win_hwnd, self.json_parser.get_attribute(EDIT_2, JSON_CENTER)[0],
                                     self.json_parser.get_attribute(EDIT_2, JSON_CENTER)[1])
        win32ref.send_str(spc_password, win_hwnd)
        win32ref.send_position_click(win_hwnd, self.json_parser.get_attribute(BUTTON_5, JSON_CENTER)[0],
                                     self.json_parser.get_attribute(BUTTON_5, JSON_CENTER)[1])
        win32ref.compare_screenshot_with_image(assets.ROLE_ENTER_BUTTON, win_hwnd,
                                               self.json_parser.get_attribute(BUTTON_6, JSON_L_POINT),
                                               self.json_parser.get_attribute(BUTTON_6, JSON_SIZE))
        win32ref.lock_unlock_win(win_hwnd, blocked=False)
        win32ref.send_position_click(win_hwnd, self.json_parser.get_attribute(BUTTON_6, JSON_CENTER)[0],
                                     self.json_parser.get_attribute(BUTTON_6, JSON_CENTER)[1])
        # print(f'Thread finished for window {win_hwnd}, account {spc_account}')
