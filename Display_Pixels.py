import sys
from PySide2 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication, QPushButton, QLineEdit, QAction, QSlider
from PySide2.QtWidgets import QListWidget, QTabWidget, QGraphicsView, QGraphicsScene
from PySide2.QtWidgets import QSpinBox, QWidget, QDialog, QVBoxLayout
from PySide2.QtGui import QPixmap, QImage, QMatrix, QPainter, QColor
from PySide2.QtGui import QMouseEvent, QCursor, QPaintEvent, QPen
from PySide2.QtCore import QFile, QObject, SIGNAL, Signal

import cv2
import numpy as np
import math
import matplotlib.pyplot as plt
from skimage import measure

class Display_Pixels(QGraphicsView):
    getSignal = Signal(object)
    
    def __init__(self, parent=None):
        QGraphicsView.__init__(self, parent=parent)
        #super().__init__()
        self.initUI()
        self.img = np.ones((40,40, 3)) *-1
        self.draw = True
        self.w = 20
        self.size = 0
        self.setSceneRect( 0, 0, 800, 800 )
        self.setFixedSize(800, 800)
        
    def initUI(self):   
        #self.setGeometry(100, 100, 450, 450)
        #self.setWindowTitle('By Pixel')
        #self.setMouseTracking(True)
        #self.show()
        res = 40
        self.grid = np.array([ [0] * res  for n in range(res)]) # list comprehension
        #print(self.grid.shape)


    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self.viewport())
        self.drawRectangles(qp)
        qp.end()
        
    def drawRectangles(self, qp):
        mode = 0
        x,y = 0, 0
        adj = 0 # Distance from the edges
        lr = 20
        hr = 35
        col = QColor(255, 0, 0)
        col.setNamedColor('#d4d4d4')
        qp.setPen(QPen(col,-1 ))

        for g_row, img_row in zip(self.grid, self.img):
            for g_col, img_col in zip(g_row, img_row):
                r, g, b = (img_col[0], img_col[1], img_col[2])
                
                if g_col == 1:
                    if mode == 0:
                        r = int(math.log(r+1)*lr)
                        g = int(math.log(g+1)*hr)
                        b = int(math.log(b+1)*lr)
                    elif mode == 1:
                        if r+50 <= 220: r = r+50
                        if g+80 <= 255: g = g+80
                        if b+50 <= 220: b = b+50
                    else:
                        if r+70 <= 220: r = r+70
                        if g+140 <= 255: g = g+140
                        if b+70 <= 220: b = b+70
                        
                    qp.setBrush(QColor(r, g, b))
                    qp.drawRect(x + adj, y + adj, self.w, self.w)
                else:
                    qp.setBrush(QColor(r, g, b))
                    qp.drawRect(x + adj, y + adj, self.w, self.w)
                
                #qp.setBrush(QColor(200, 0, 0))
                #qp.drawRect(x, y, w, w)
                x = x + self.w  # move right
            y = y + self.w # move down
            x = 0 # rest to left edge
            
    def mouseReleaseEvent(self, event):
        self.getSignal.emit(self.grid)
        super(Display_Pixels, self).mouseReleaseEvent(event)

    def mousePressEvent(self, event):
        y = int(event.x()*1.0/self.w)
        x = int(event.y()*1.0/self.w)
        s1, s2 = self.grid.shape
        if self.draw:
            stroke = 1
        else:
            stroke = 0
        # verify
        if 0 <= y < s1 and 0 <= x < s2:
            self.grid[x][y] = stroke
            self.grid[x-self.size:x+self.size+1, y-self.size:y+self.size+1] = stroke
            self.viewport().update()
            
    def mouseMoveEvent(self, event):
        y = int(event.x()*1.0/self.w)
        x = int(event.y()*1.0/self.w)
        s1, s2 = self.grid.shape
        if self.draw:
            stroke = 1
        else:
            stroke = 0
        # verify
        if 0 <= y < s1 and 0 <= x < s2:
            self.grid[x][y] = stroke
            self.grid[x-self.size:x+self.size+1, y-self.size:y+self.size+1] = stroke
            self.viewport().update()
            
    def eraseMode(self, state):
        self.draw = state
        
    def brushMode(self, state):
        self.size = state
        
    def getSegment(self):
        return(self.grid)
        
    def setImage(self, img, seg):
        self.img = img
        self.grid = seg
        #self.w = round((800/self.img.shape[1]),1)
        self.w = round((768/self.img.shape[1]), 0)
        
    def updateAll(self):
        self.viewport().update()
        
if __name__ == '__main__':
    app = QApplication.instance()
    if app is None: 
        app = QApplication(sys.argv)
    px = Display_Pixels()
    px.show()
    sys.exit(app.exec_())