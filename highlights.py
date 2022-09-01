from PySide2.QtCore import Qt
from PySide2 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication, QPushButton, QLineEdit, QAction, QSlider, QLabel
from PySide2.QtWidgets import QListWidget, QTabWidget, QGraphicsView, QGraphicsScene, QListWidgetItem
from PySide2.QtWidgets import QSpinBox, QWidget, QDialog, QVBoxLayout, QHBoxLayout, QLayout
from PySide2.QtWidgets import QFrame, QRadioButton, QCheckBox, QMessageBox, QMainWindow
from PySide2.QtGui import QPixmap, QImage, QMatrix, QPainter, QColor, QPen, QCursor
from PySide2.QtCore import QFile, QObject, SIGNAL
import sys

import sys

class Main(QMainWindow):
    def __init__(self, parent = None):
        QMainWindow.__init__(self,parent)
        self.initUI()

    def initUI(self):
        mylist = QListWidget(self)
        mylist.setMinimumSize(QtCore.QSize(800, 800))
        for i in range(5):
            widgitItem = QListWidgetItem() 
            widget = QWidget()
            widgetText =  QLabel('test<span style="color:#ff0000;">test %s</span>' % (i + 1))
            widgetLayout = QHBoxLayout()
            widgetLayout.addWidget(widgetText)
            widgetLayout.setSizeConstraint(QLayout.SetFixedSize)
            widget.setLayout(widgetLayout)      
            mylist.addItem(widgitItem)
            widgitItem.setSizeHint(widget.sizeHint()) 
            mylist.setItemWidget(widgitItem, widget)


def main():
    app = QApplication.instance()
    if app is None: 
        app = QApplication(sys.argv)
    main = Main()
    main.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()