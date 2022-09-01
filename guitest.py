import sys
from PyQt5 import QtGui, QtCore
from PySide2.QtWidgets import QApplication, QPushButton, QLineEdit, QAction, QSlider
from PySide2.QtWidgets import QListWidget, QTabWidget, QGraphicsView, QGraphicsScene
from PySide2.QtWidgets import QSpinBox, QWidget, QDialog, QVBoxLayout, QHBoxLayout, QFrame
from PySide2.QtWidgets import QMainWindow, QFrame, QGraphicsRectItem

from Display_Pixels import Display_Pixels

class Window(QMainWindow):
    def __init__(self, parent=None):
        #This initializes the main window or form
        super(Window,self).__init__(parent=parent)
        self.setGeometry(1,31,900,900)
        self.setWindowTitle("Pre-Alignment system")
        
class Form(QObject):
    def __init__(self, ui_file, parent=None):
        super(Form, self).__init__(parent)
        ui_file = QFile(ui_file)
        ui_file.open(QFile.ReadOnly)
        loader = QUiLoader()       
        #self.window = loader.load(ui_file)
        
        #self.view = self.window.findChild(QGraphicsView, 'graphicsView')
        
        ui_file.close()

def run():
    app = QApplication.instance()
    if app is None: 
        app = QApplication(sys.argv)
    GUI = Window()
    #GUI = Form('guitest.ui')
    view = Display_Pixels(GUI)

    GUI.show()
    sys.exit(app.exec_())

run()