import sys

from PyQt5.QtWidgets import QApplication
from ui.init_win import InitWindow


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = InitWindow()
    app.exec_()
