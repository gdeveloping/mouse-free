from PyQt5.QtWidgets import QApplication
import sys
from window import MainWindow


if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = MainWindow(app)

    sys.exit(app.exec_())
