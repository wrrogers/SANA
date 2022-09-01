import sys
from PySide2 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication, QPushButton, QLineEdit, QAction, QSlider
from PySide2.QtWidgets import QListWidget, QTabWidget, QGraphicsView, QGraphicsScene
from PySide2.QtWidgets import QSpinBox, QWidget, QDialog
from PySide2.QtGui import QPixmap, QImage, QMatrix
from PySide2.QtCore import QFile, QObject, SIGNAL

def window():
   win = QDialog()
   if win.isVisible():
        # uncomment below, if you like symmetry :)
        # self.setMinimumSize(630, 150)
        win.resize(400,400)
   else:
        win.setMinimumSize(400,400)
        win.resize(400, 400)
   b1 = QPushButton(win)
   b1.setText("Button1")
   b1.move(50,20)
   b1.clicked.connect(b1_clicked)

   b2 = QPushButton(win)
   b2.setText("Button2")
   b2.move(50,50)
   QObject.connect(b2,SIGNAL("clicked()"),b2_clicked)
   
   grview = QGraphicsView(win)
   grview.move(50, 100)

   win.setWindowTitle("Pixel Display")
   win.show()

   sys.exit(app.exec_())
    
def b1_clicked():
   print ("Button 1 clicked")

def b2_clicked():
   print ("Button 2 clicked")
   
def draw():
    
    x,y = 0,0 # starting position

    for row in grid:
        for col in row:
          if col == 1:
              fill(250,0,0)
          else:
              fill(255)
          rect(x, y, w, w)
          x = x + w  # move right
        y = y + w # move down
        x = 0 # rest to left edge

if __name__ == '__main__':
    app = QApplication.instance()
    if app is None: 
        app = QApplication(sys.argv)
    w = window()
    
