from PyQt6 import QtWidgets
from views.View_Main import Ui_MainWindow
from model.grama import Grammar
from controller.Controller import Controller
import sys

class Main:
    def __init__(self):
        self.app = QtWidgets.QApplication(sys.argv)
        self.MainWindow = QtWidgets.QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.MainWindow)
        self.MainWindow.statusBar().hide()

      
        

        self.model = Grammar()
        self.controller = Controller(self.ui, self.model)

    def run(self):
        self.MainWindow.show()
        sys.exit(self.app.exec())

if __name__ == "__main__":
    main = Main()
    main.run()