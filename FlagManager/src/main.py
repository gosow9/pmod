from flagmanager.data_loader.brewer_txt import Brewer
from flagmanager.qt.app import ApplicationWindow
from flagmanager.data_loader.load import load_day
from PySide6.QtWidgets import QApplication
import sys



if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = ApplicationWindow()
    #w.setFixedSize(1280, 720)
    w.resize(1280, 720)
    w.show()
    app.exec()