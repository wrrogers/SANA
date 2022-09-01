import sys

import matplotlib.pyplot as plt

from PySide2 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication, QPushButton, QLineEdit, QAction, QSlider
from PySide2.QtWidgets import QListWidget, QTabWidget, QGraphicsView, QGraphicsScene
from PySide2.QtWidgets import QSpinBox, QWidget, QDialog, QVBoxLayout, QHBoxLayout
from PySide2.QtWidgets import QFrame, QRadioButton, QCheckBox
from PySide2.QtGui import QPixmap, QImage, QMatrix, QPainter, QColor, QPen, QCursor
from PySide2.QtCore import QFile, QObject, SIGNAL

import pydicom as dicom
import SimpleITK as sitk

import os
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
#from ast import literal_eval

import cv2
from PIL import Image, ImageMath
import math

from Display_Pixels import Display_Pixels
from rectangles import Display_Rectangles
from tools import load_scan, get_pixels_hu

class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(30, 30, 300, 300)

    def paintEvent(self, event):
        painter = QPainter(self)
        pixmap = QPixmap("roi.jpg")
        painter.drawPixmap(self.rect(), pixmap)
        pen = QPen(QColor(255, 0, 0), 1)
        painter.setPen(pen)
        painter.drawLine(10, 10, self.rect().width() -10 , 10)

if __name__ == '__main__':
    print(os.getcwd())
    app = QApplication.instance()
    if app is None: 
        app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec_())