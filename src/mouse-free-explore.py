from PyQt5.QtWidgets import QApplication
import sys
from MyWindow import MyWindow


if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = MyWindow(app)

    sys.exit(app.exec_())
