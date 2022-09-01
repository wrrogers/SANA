import sys
from PySide2 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication, QPushButton, QLineEdit, QAction, QSlider
from PySide2.QtWidgets import QListWidget, QTabWidget, QGraphicsView, QGraphicsScene
from PySide2.QtWidgets import QSpinBox, QWidget, QDialog, QVBoxLayout
from PySide2.QtGui import QPixmap, QImage, QMatrix, QPainter, QColor, QMouseEvent, QCursor
from PySide2.QtCore import QFile, QObject, SIGNAL

import cv2
import numpy as np
import math

class Display_Rectangles(QWidget):
    
    def __init__(self):
        QWidget.__init__(self)
        #super().__init__()
        self.initUI()
        self.img = cv2.imread('roi.jpg')
        
        
    def initUI(self):      
        self.setGeometry(100, 100, 650, 650)
        self.setWindowTitle('By Pixel')
        #self.setMouseTracking(True)
        #self.show()
        res = 40 
        self.grid = np.array([ [-1] * res  for n in range(res)]) # list comprehension
        #print(self.grid.shape)


    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self.drawRectangles(qp)
        qp.end()

        
    def drawRectangles(self, qp, w = 16):
        mode = 0
        x,y = 0,0 # starting position
        lr = 20
        hr = 35
        col = QColor(0, 0, 0)
        col.setNamedColor('#d4d4d4')
        qp.setPen(col)

        for g_row, img_row in zip(self.grid, self.img):
            for g_col, img_col in zip(g_row, img_row):
                r, g, b = (img_col[0], img_col[1], img_col[2])
                
                if g_col == 1:
                    if mode == 0:
                        r = int(math.log(r)*lr)
                        g = int(math.log(g)*hr)
                        b = int(math.log(b)*lr)
                    elif mode == 1:
                        if r+50 <= 220: r = r+50
                        if g+80 <= 255: g = g+80
                        if b+50 <= 220: b = b+50
                    else:
                        if r+70 <= 220: r = r+70
                        if g+140 <= 255: g = g+140
                        if b+70 <= 220: b = b+70
                        
                    qp.setBrush(QColor(r, g, b))
                    qp.drawRect(x, y, w, w)
                else:
                    qp.setBrush(QColor(r, g, b))
                    qp.drawRect(x, y, w, w)
                
                #qp.setBrush(QColor(200, 0, 0))
                #qp.drawRect(x, y, w, w)
                x = x + w  # move right
            y = y + w # move down
            x = 0 # rest to left edge

    def mousePressEvent(self, QMouseEvent):
        w = 16.0

        #print("MOUSE:")
        #print('(', int(QMouseEvent.x()/w), ', ', int(QMouseEvent.y()/w), ')')
        #print (QMouseEvent.pos())
        x = float(QMouseEvent.x())
        y = float(QMouseEvent.y())
        self.grid[int(y/w)][int(x/w)] = -1 * self.grid[int(y/w)][int(x/w)]
                
        #print(img[int(y/w), int(x/w), :])
             
        self.repaint()
        #self.update()
              
        
if __name__ == '__main__':
    
    app = QApplication.instance()
    if app is None: 
        app = QApplication(sys.argv)
    px = Display_Rectangles()
    px.show()
    sys.exit(app.exec_())