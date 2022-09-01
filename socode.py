import sys
import numpy as np
import cv2
from PyQt5 import QtCore, QtGui, QtWidgets

class OpenCVItem(QtWidgets.QGraphicsItem):
    def __init__(self, img, parent=None):
        super(OpenCVItem, self).__init__(parent)
        res = 40
        self.grid = -np.ones((res, res))
        self._img = img
        height, width, channel = self._img.shape
        bytesPerLine = 3 * width
        self._qimage = QtGui.QImage(self._img.data, 
            width, height, 
            bytesPerLine, 
            QtGui.QImage.Format_RGB888).rgbSwapped()

    def boundingRect(self):
        w, h, _ = self._img.shape
        return QtCore.QRectF(0, 0, w, h)

    def paint(self, painter, option, widget):
        painter.drawImage(0, 0, self._qimage)
        self.drawRectangles(painter)

    def drawRectangles(self, painter):
        mode = 0
        lr = 20
        hr = 35
        painter.save()
        painter.setPen(QtGui.QPen(QtGui.QColor("#d4d4d4")))
        w1, h1 = self.grid.shape
        fw = self.boundingRect().width()/w1 
        fh = self.boundingRect().height()/h1
        s = QtCore.QSizeF(fw, fh)
        for idx, v in np.ndenumerate(self.grid):            
            if v == 1:
                r_ = QtCore.QRectF(fw*QtCore.QPointF(*idx), s)
                r_int = r_.toRect()
                (r, g, b), _ = cv2.meanStdDev(self._img[r_int.left():r_int.right(), 
                    r_int.top():r_int.bottom()])
                if mode == 0:
                    r = np.log(r+1)*lr
                    g = np.log(g+1)*hr
                    b = np.log(b+1)*lr
                elif mode == 1:
                    if r+50 <= 220: r = r+50
                    if g+80 <= 255: g = g+80
                    if b+50 <= 220: b = b+50
                else:
                    if r+70 <= 220: r = r+70
                    if g+140 <= 255: g = g+140
                    if b+70 <= 220: b = b+70
                painter.setBrush(QtGui.QColor(*(int(x) for x in (r, g, b))))
                painter.drawRect(r_)
        painter.restore()

    def mousePressEvent(self, event):
        w1, h1 = self.grid.shape
        fw = self.boundingRect().width()/w1
        fh = self.boundingRect().height()/h1
        xi = int(event.pos().x()/fw) 
        yi = int(event.pos().y()/fh)
        self.grid[xi][yi] = -self.grid[xi][yi]
        self.update()
        super(OpenCVItem, self).mousePressEvent(event)

class Display_Pixels(QtWidgets.QGraphicsView):
    def __init__(self, parent=None):
        super(Display_Pixels, self).__init__(parent)
        scene = QtWidgets.QGraphicsScene(self)
        self.setScene(scene)
        item = OpenCVItem(cv2.imread("roi.jpg"))
        scene.addItem(item)

class Window(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(Window,self).__init__(parent=parent)
        self.setGeometry(1,31,900,900)
        self.setWindowTitle("Pre-Alignment system")

def run():
    app = QtWidgets.QApplication.instance()
    if app is None: 
        app = QtWidgets.QApplication(sys.argv)
    GUI = Window()
    view = Display_Pixels(GUI)
    GUI.setCentralWidget(view)
    GUI.show()
    sys.exit(app.exec_())

run()