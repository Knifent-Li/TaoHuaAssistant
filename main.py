import os
import sys
import configparser
from assets import QICON_PATH
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QDesktopWidget, \
    QMessageBox


def is_windows_absolute_path(path):
    if not os.path.isabs(path):
        return False

    if not os.path.exists(path):
        return False

    if os.path.isdir(path):
        path = os.path.join(path, "launch.exe")
        if not os.path.exists(path):
            return False
    elif os.path.isfile(path):
        if not os.path.basename(path) == "launch.exe":
            return False
    else:
        return False

    return path


class InitWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.accounts = None
        self.layout = None
        self.edit_launcher_path = None
        self.edit_accounts = None
        self.launcher_path = None
        self.init_ui()

    def init_ui(self):
        # Create the label
        label1 = QLabel("请输入桃花源记2`launch.exe`的安装位置(路径)：")

        # Create the line edit
        self.edit_launcher_path = QLineEdit()

        # Create the button
        button_next_1 = QPushButton("下一步")
        button_next_1.clicked.connect(self.button_click_for_next_1)

        # Create the layout
        self.layout = QVBoxLayout()
        self.layout.addWidget(label1)
        self.layout.addWidget(self.edit_launcher_path)
        self.layout.addWidget(button_next_1)

        # Set the layout
        self.setLayout(self.layout)

        # Set the window properties
        self.setWindowTitle("初始化")
        self.resize(300, 100)
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        self.setWindowIcon(QIcon(QICON_PATH))

        # Show the window
        self.show()

    def button_click_for_next_1(self):
        if not self.edit_launcher_path.text():
            QMessageBox.warning(self, "错误", "请输入路径")
            return

        self.launcher_path = self.edit_launcher_path.text()
        if is_windows_absolute_path(self.launcher_path):
            # Save the launcher_path value to the config file
            self.launcher_path = is_windows_absolute_path(self.launcher_path)
            config = configparser.ConfigParser()
            config['DEFAULT'] = {'launch_path': self.launcher_path}
            try:
                with open('config.ini', 'w', encoding="utf-8") as config_file:
                    config.write(config_file)
            except OSError:
                QMessageBox.warning(self, "错误", "请使用管理员模式运行此工具")

            self.switch_to_accounts_input()
        else:
            QMessageBox.warning(self, "错误", "请检查路径格式，文件是否存在(示例:D:\\桃花源记2\\launch.exe)")
            return

    def switch_to_accounts_input(self):
        # Remove the path input widgets
        while self.layout.count():
            widget = self.layout.takeAt(0).widget()
            if widget is not None:
                widget.deleteLater()

        # Add the account/password input widgets
        label2 = QLabel("请输入5个账号和密码")
        label3 = QLabel("(格式: 账号1:密码1, 账号2:密码2, ...)")
        self.edit_accounts = QLineEdit()
        button_vrf = QPushButton("确认")
        button_vrf.clicked.connect(self.get_accounts)
        self.layout.addWidget(label2)
        self.layout.addWidget(label3)
        self.layout.addWidget(self.edit_accounts)
        self.layout.addWidget(button_vrf)

        self.update()

    def get_launcher_path(self):
        # print(self.launcher_path)
        return self.launcher_path

    def get_accounts(self):
        text = self.edit_accounts.text().strip()

        if not text:
            QMessageBox.warning(self, "错误", "请输入账号和密码")
            return {}

        self.accounts = {}
        try:
            for pair in text.split(","):
                account, password = pair.split(":")
                account = account.strip()
                password = password.strip()
                if not account or not password:
                    raise ValueError
                self.accounts[account] = password
        except ValueError:
            QMessageBox.warning(self, "错误", "输入格式错误，请输入格式为 '账号1:密码1, 账号2:密码2, ...' 的账号和密码")
            return {}

        config = configparser.ConfigParser()
        config.read('config.ini', encoding='utf-8')

        # Remove all existing pairs in the ACCOUNTS section
        if config.has_section('ACCOUNTS'):
            config.remove_section('ACCOUNTS')

        # Create a new ACCOUNTS section and add the new account and password pairs
        config.add_section('ACCOUNTS')
        for account, password in self.accounts.items():
            config.set('ACCOUNTS', account, password)

        # Write the updated ConfigParser object to the config.ini file
        with open('config.ini', 'w', encoding="utf-8") as config_file:
            config.write(config_file)
        print(self.accounts)
        return self.accounts


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = InitWindow()
    app.exec_()

    path_launcher = window.get_launcher_path()
