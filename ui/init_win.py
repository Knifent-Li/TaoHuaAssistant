from os import path

from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QDesktopWidget, \
    QMessageBox
from PyQt5.QtGui import QIcon

from assets import QICON_PATH
from modules.control import Assistant
from utils.dataparser import ConfigManager

CONFIG_PATH = path.split(path.realpath(__file__))[0] + r"\..\config.ini"


def is_absolute_path(path):
    if not path.isabs(path) or not path.exists(path):
        return None

    if path.isdir(path):
        path = path.join(path, "launch.exe")
        if not path.exists(path):
            return None
    elif path.isfile(path) and not path.basename(path) == "launch.exe":
        return None

    return path


class InitWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.edit_accounts = None
        self.launcher_path = None
        self.accounts = None
        self.edit_launcher_path = None
        self.layout = QVBoxLayout()
        self.config_handler = ConfigManager(config_path=CONFIG_PATH)
        self.init_ui()

    def init_ui(self):
        """Initialize the user interface."""
        # Set up the layout
        self.setLayout(self.layout)

        # Set up window properties
        self.setup_window()

        # Check if the config file exists and load accounts and launcher path
        config_exists = path.isfile(CONFIG_PATH)
        self.accounts = self.config_handler.get_accounts() if config_exists else None
        self.launcher_path = self.config_handler.get_launch_path() if config_exists else None

        # Update UI elements
        if self.accounts and self.launcher_path:
            self.setup_startup_ui()
        else:
            self.setup_initial_configuration_ui()

    def clear_layout(self):
        """Clear the existing widgets from the layout."""
        while self.layout.count():
            widget = self.layout.takeAt(0).widget()
            if widget is not None:
                widget.deleteLater()

    def setup_window(self):
        """Set up the window properties."""
        self.setWindowTitle("初始化")
        self.resize(300, 100)

        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

        self.setWindowIcon(QIcon(QICON_PATH))
        self.show()

    def setup_initial_configuration_ui(self):
        """Set up the UI for initial configuration."""
        label1 = QLabel("请输入桃花源记2`launch.exe`的安装位置(路径)：")
        self.edit_launcher_path = QLineEdit()
        btn_to_account_ui = QPushButton("下一步")
        btn_to_account_ui.clicked.connect(self.get_th_path)

        self.layout.addWidget(label1)
        self.layout.addWidget(self.edit_launcher_path)
        self.layout.addWidget(btn_to_account_ui)

    def get_th_path(self):
        """Handle the click event for the next button and save the launcher path."""
        self.launcher_path = is_absolute_path(self.edit_launcher_path.text())
        if not self.edit_launcher_path.text():
            QMessageBox.warning(self, "错误", "请输入路径")
            return

        if self.launcher_path:
            self.config_handler.set_launch_path(self.launcher_path)
            self.config_handler.save_config()

            self.setup_accounts_input_ui()
        else:
            QMessageBox.warning(self, "错误", "请检查路径格式，文件是否存在(示例:D:\\桃花源记2\\launch.exe)")
            return

    def setup_accounts_input_ui(self):
        """Switch to the accounts input interface."""
        # Clear the existing widgets
        self.clear_layout()

        # Add the account/password input widgets
        label2 = QLabel("请输入5个账号和密码")
        label3 = QLabel("(格式: 账号1:密码1, 账号2:密码2, ...)")
        self.edit_accounts = QLineEdit()
        btn_to_startup_ui = QPushButton("确认")
        btn_to_startup_ui.clicked.connect(self.get_accounts)

        self.layout.addWidget(label2)
        self.layout.addWidget(label3)
        self.layout.addWidget(self.edit_accounts)
        self.layout.addWidget(btn_to_startup_ui)

        self.update()

    def get_accounts(self):
        """Extract accounts from the user input and save them to config."""
        text = self.edit_accounts.text().strip()

        if not text:
            QMessageBox.warning(self, "错误", "请输入账号和密码")
            return

        try:
            self.accounts = self.parse_account_text(text)
        except ValueError:
            QMessageBox.warning(self, "错误", "输入格式错误，请输入格式为 '账号1:密码1, 账号2:密码2, ...' 的账号和密码")
            return

        self.config_handler.set_accounts(self.accounts)
        self.config_handler.save_config()
        self.setup_startup_ui()

    @staticmethod
    def parse_account_text(text):
        """Parse a string containing accounts and passwords into a dictionary."""
        accounts = {}
        for pair in text.split(","):
            account, password = pair.split(":")
            account = account.strip()
            password = password.strip()
            if not account or not password:
                raise ValueError
            accounts[account] = password
        return accounts

    def setup_startup_ui(self):
        """Set up the UI for startup."""
        self.clear_layout()
        button_start = QPushButton("启动")
        button_start.clicked.connect(self.start_up)
        self.layout.addWidget(button_start)

        self.update()

    def start_up(self):
        th_assistant = Assistant(self.accounts, self.launcher_path)
        th_assistant.update_and_startup()
