import sys

import matplotlib.pyplot as plt

from PySide2.QtCore import Qt
from PySide2 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication, QPushButton, QLineEdit, QAction
from PySide2.QtWidgets import QListWidget, QTabWidget, QGraphicsView, QSlider
from PySide2.QtWidgets import QSpinBox, QWidget, QDialog, QVBoxLayout, QFrame
from PySide2.QtWidgets import QRadioButton, QCheckBox, QMessageBox
from PySide2.QtWidgets import QListWidgetItem, QHBoxLayout, QGraphicsScene
from PySide2.QtGui import QPixmap, QImage, QMatrix, QPainter, QColor, QPen
from PySide2.QtGui import QCursor, QIcon
from PySide2.QtCore import QFile, QObject, SIGNAL

import pydicom as dicom
import SimpleITK as sitk

import os
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from skimage import measure
#from ast import literal_eval

import cv2
from PIL import Image, ImageMath
import math

from Display_Pixels import Display_Pixels
from rectangles import Display_Rectangles
#from tools import load_scan, get_pixels_hu

class Form(QObject):

    def __init__(self, ui_file, parent=None):
        super(Form, self).__init__(parent)
        ui_file = QFile(ui_file)
        ui_file.open(QFile.ReadOnly)
 
        loader = QUiLoader()
        
        self.left_adjust = 8
        self.convert_coords = False
        
        self.base_dir = 'C:/Users/wrrog/Istituto dei Tumori/Project 1/'
        
        self.window = loader.load(ui_file)
        ui_file.close()
    
        #self.setWindowTitle('Segmentr')
        #self.setMouseTracking(True)
        
        self.isGrown = False
        self.OPPACITY = 200
        self.r = 0
        self.g = 0
        self.b = 204
        self.adjust = -700

        self.cb_mask = self.window.findChild(QCheckBox, 'Mask_CheckBox')
        self.cb_mask.setChecked(True)
        self.cb_mask.toggled.connect(self.display_edit_l)
        
        self.cb_contour = self.window.findChild(QCheckBox, 'Contours_CheckBox')
        self.cb_contour.setChecked(True)
        self.cb_contour.toggled.connect(self.display_edit_l)
        
        self.rb_draw = self.window.findChild(QRadioButton, 'RB_Draw')
        self.rb_draw.setChecked(True)
        self.rb_draw.toggled.connect(lambda:self.changeEraseMode(self.rb_draw))
        
        self.rb_erase = self.window.findChild(QRadioButton, 'RB_Erase')
        self.rb_erase.toggled.connect(lambda:self.changeEraseMode(self.rb_erase))
        
        self.fill_button = self.window.findChild(QPushButton, 'Fill_Button')
        self.fill_button.clicked.connect(self.fill_edit)
        
        self.edit_button = self.window.findChild(QPushButton, 'Edit_Button')
        self.edit_button.clicked.connect(self.start_edit)
        
        self.seed_button = self.window.findChild(QPushButton, 'Seed_Button')
        self.seed_button.clicked.connect(self.load_segment)
        
        self.load_button = self.window.findChild(QPushButton, 'Load_Button')
        self.load_button.clicked.connect(self.load_saved_segment)

        self.edit_sli = self.window.findChild(QSlider, 'Edit_Slider')
        self.edit_sli.valueChanged.connect(self.update_edit)

        self.brush_sli = self.window.findChild(QSlider, 'Brush_Slider')
        self.brush_sli.setMinimum(0)
        self.brush_sli.setMaximum(4)
        self.brush_sli.setValue(0)
        self.brush_sli.valueChanged.connect(self.changeBrushSize)
        
        self.growth_sli = self.window.findChild(QSlider, 'Growth_Slider')
        self.growth_sli.setMinimum(-2000)
        self.growth_sli.setMaximum(1000)
        self.growth_sli.setValue(0)
        self.growth_sli.valueChanged.connect(self.update_segment)
        
        self.rg_zoom_sli = self.window.findChild(QSlider, 'RG_Zoom_Slider')
        self.rg_zoom_sli.setMinimum(5)
        self.rg_zoom_sli.setMaximum(100)
        self.rg_zoom_sli.valueChanged.connect(self.update_roi)
        
        self.rg_slice_sli = self.window.findChild(QSlider, 'RG_Slice_Slider')
        self.rg_slice_sli.valueChanged.connect(self.update_roi)
        
        self.rg_slice_sli2 = self.window.findChild(QSlider, 'RG_Slice_Slider_2')
        self.rg_slice_sli2.setMaximum(1000)
        self.rg_slice_sli2.setMinimum(-1000)
        self.rg_slice_sli2.valueChanged.connect(self.update_segment)

        self.rg_slice_sb_d = self.window.findChild(QSpinBox, 'RG_Slice_Spin_Down')   
        self.rg_slice_sb_d.valueChanged.connect(self.update_roi)

        self.rg_slice_sb_u = self.window.findChild(QSpinBox, 'RG_Slice_Spin_Up')   
        self.rg_slice_sb_u.valueChanged.connect(self.update_roi)
        #self.rg_slice_sb_last = self.rg_slice_sb_u.value()

        self.grview = self.window.findChild(QGraphicsView, 'RGgraphicsView')
        self.grview2 = self.window.findChild(QGraphicsView, 'RGgraphicsView2')
        self.edit_l = self.window.findChild(QGraphicsView, 'Edit_GraphicsView')

        self.edit_layout = self.window.findChild(QHBoxLayout, 'Editor_Layout')
        self.view = Display_Pixels()
        self.view.installEventFilter(self)
        self.edit_layout.addWidget(self.view)
        self.view.getSignal.connect(self.update_edit_event)
        self.edit_layout.setAlignment(self.view, Qt.AlignCenter)

        #self.view.show()
        
        self.scan_tabs    = self.window.findChild(QTabWidget, 'Scan_Tabs')
        self.scan_tabs.setCurrentIndex(0) 
        
        self.tabs    = self.window.findChild(QTabWidget, 'tabWidget')
        self.tabs.setCurrentIndex(0) 
        
        self.scan_list   = self.window.findChild(QListWidget, 'Scan_List')
        self.scan_list.itemClicked.connect(self.set_nodules)
        
        self.nodule_list = self.window.findChild(QListWidget, 'Nodule_List')
        self.nodule_list.itemClicked.connect(self.load_roi)
        
        self.set_base    = self.window.findChild(QAction, 'actionSet_Base_Directory')
        self.set_base.setShortcut('Ctrl+B')
        self.set_base.triggered.connect(self.set_base_handler)
        
        self.act_save    = self.window.findChild(QAction, 'Action_Save')
        self.act_save.setShortcut('Ctrl+S')
        self.act_save.triggered.connect(self.save_segment)

        self.but_save = self.window.findChild(QPushButton, 'PushButton_Save')
        self.but_save.clicked.connect(self.save_segment)

        self.defaultValues()

        self.window.show()
        
    def defaultValues(self):
        self.rg_zoom_sli.setValue(20)
        
        self.rg_slice_sli.setMinimum(-2)
        self.rg_slice_sli.setMaximum(2)
        self.rg_slice_sli.setValue(0)
        
        self.rg_slice_sb_d.setValue(2)
        
        self.rg_slice_sb_u.setValue(2)
 
    def set_base_handler(self):
        path = os.getcwd()
        self.dname = QFileDialog.getExistingDirectory()
        os.chdir(os.path.join(path,self.dname))
        self.meta = pd.read_csv('meta.csv')
        self.pop_scans()
                        
    def pop_scans(self):
        cont = os.listdir(self.dname)
        #cont = [c[9:] for c in cont]
        #print("All contents:")
        #print(cont)
        cont.sort()
        self.scan_list.clear()
        for c in cont:
            #print(c)
            path = os.path.join(self.dname+"/"+c)
            if not os.path.isfile(path): 
                #print(path, c[self.left_adjust:])
                nods = self.meta.loc[self.meta.patientuid == c[self.left_adjust:]]
                #print("Length:", len(nods))
                is_complete = len(nods) == self.countFiles(path, '.npy')
                is_empty = len(nods) == 0
                #print(c, len(nods), "COMP:",is_complete, "EMPTY:",is_empty, "Count:",self.countFiles(path, '.npy'))
                if is_empty:
                    #print("Empty")
                    comp = QListWidgetItem()
                    comp.setText(str(c))
                    comp.setTextColor(QColor(0,0,0,100))
                    comp.setIcon(QIcon(self.base_dir + "neutral.png"))
                    self.scan_list.addItem(comp)
                else:            
                    #print("Not empty")
                    if is_complete:
                        #print("Completed")
                        comp = QListWidgetItem()
                        comp.setText(str(c))
                        comp.setTextColor(QColor(self.r, self.g, self.b, self.OPPACITY))
                        nods = self.meta[self.meta.patientuid == c]
                        #print(nods)
                        chks = nods[nods.confirmed == 'PySide2.QtCore.Qt.CheckState.Checked']
                        #print(c, "Cheks:", len(nods), len(chks))
                        #print()
                        if len(nods) == len(chks):
                            comp.setIcon(QIcon(self.base_dir + "checked.png"))
                        else:
                            comp.setIcon(QIcon(self.base_dir + "unchecked.png"))
                        self.scan_list.addItem(comp)
                    else:
                        #print("Not completed, add", str(c))
                        comp = QListWidgetItem()
                        comp.setText(str(c))
                        comp.setTextColor(QColor(0,0,0,255))
                        comp.setIcon(QIcon(self.base_dir + "unchecked.png"))
                        self.scan_list.addItem(comp)
        
    def set_nodules(self, item):
        self.patient = item.text()
        self.pop_nodules()
        
    def pop_nodules(self):
        #print("Populating nodules...")
        
        nodules = self.meta.loc[self.meta['patientuid'] == self.patient[self.left_adjust:]]
        self.nodule_list.clear()
        patient_path = os.path.join(self.dname, self.patient)
        hassegmentations = "segmentations" in os.listdir(patient_path)
        if hassegmentations:
            segmented = os.listdir(os.path.join(patient_path, "segmentations"))
        else:
            segmented = []
        
        #print("Has segmentations:", hassegmentations, segmented)
        for n, data in nodules.iterrows():
            #print(str(n),'\n', data)
            if str(n) in segmented:
                #print("Is in the segmented:", str(n) in segmented)
                comp = QListWidgetItem()
                comp.setText(str(n))
                comp.setTextColor(QColor(self.r, self.g, self.b, self.OPPACITY))
                comp.setFlags(comp.flags() | QtCore.Qt.ItemIsUserCheckable)

                #print(self.meta.loc[self.meta.noduleuid == n, 'confirmed'].item())

                if self.meta.loc[self.meta.noduleuid == n, 'confirmed'].item() == 'PySide2.QtCore.Qt.CheckState.Checked':
                    comp.setCheckState(QtCore.Qt.Checked)
                else:
                    comp.setCheckState(QtCore.Qt.Unchecked)
                self.nodule_list.addItem(comp)
            else:
                comp = QListWidgetItem()
                comp.setText(str(n))
                comp.setTextColor(QColor(0,0,0,255))
                comp.setFlags(comp.flags() | QtCore.Qt.ItemIsUserCheckable)
                comp.setCheckState(QtCore.Qt.Unchecked)
                self.nodule_list.addItem(comp)
                
    def update_nodules(self):
        nodule_items = self.nodule_list.selectedItems()
        for item in nodule_items:
            item.setTextColor(QColor(self.r, self.g, self.b, self.OPPACITY))
            
    def update_scans(self):
        ppath = os.path.join(self.dname, self.patient)
        spath = os.path.join(ppath, "segmentations")
        npath = os.path.join(spath, self.nodule)
        
        num_saved = self.countFiles(spath, '.npy')
        nods      = self.meta.loc[self.meta.noduleuid == int(self.nodule)]
        num_nods  = len(nods)
        chked     = nods.loc[nods.confirmed == 'PySide2.QtCore.Qt.CheckState.Checked']
        #print(nods)
        #print(chked)
        num_chked = len(chked)
        #print(num_saved, num_chked)
        if num_chked == num_saved:
            print("Yay")
        

    def load_roi(self, item, zoom = 20, segd = 2, segu = 2, seg = 0):
        #print("Loading ROI...")
        self.confirm_segment()
        self.defaultValues()
        self.nodule = item.text()
        self.scene = QGraphicsScene()
        self.scene2 = QGraphicsScene()
        scanPath = self.genNextScan(os.path.join(self.dname, self.patient))
        scan_path = next(scanPath)
        
        self.sitk_ct_scan, self.origin, self.spacing = self.imageReader(scan_path)

        reader = sitk.ImageFileReader()
        filepath = os.path.join(scan_path, "IM-0001-0001-0001.dcm")
        reader.SetFileName(filepath)
        reader.LoadPrivateTagsOn();
        
        reader.ReadImageInformation()
        
        #print(reader.GetFileName())
        
        self.taglib = {}
        for k in reader.GetMetaDataKeys():
            v = reader.GetMetaData(k)
            #print("({0}) == \"{1}\"".format(k,v))
            if k == "0020|000d": self.taglib['Study Instance UID'] = v
            if k == "0020|000e": self.taglib['Series Instance UID'] = v
            if k == "0020|0052": self.taglib['Frame of Reference UID'] = v
            if k == "0040|a124": self.taglib['UID'] = v

        self.ct_scan = sitk.GetArrayFromImage(self.sitk_ct_scan)
        #print("The shape is:", self.ct_scan.shape)
        
        # Will use this to add the roi back to for the WHOLE mask not just the ROI
        self.shell = np.zeros(self.ct_scan.shape)
        
        # Lose contrast when doing from the source, since it already contains the full spectrum of colors
        # self.ct_scan = cv2.normalize(self.ct_scan, None, alpha = 0, beta = 255, norm_type = cv2.NORM_MINMAX, dtype = cv2.CV_32F)
        # self.ct_scan = self.ct_scan.astype(np.uint8)
        
        x = float(self.meta.loc[int(self.nodule)].coordX)
        y = float(self.meta.loc[int(self.nodule)].coordY)
        z = float(self.meta.loc[int(self.nodule)].coordZ)

        coords = [z, y, x]
        
        #print("Actual corrdinates", coords)
        
        if self.convert_coords:
            vcoords = self.getVoxelCoord(coords, self.origin, self.spacing)
            self.x = int(vcoords[2])
            self.y = int(vcoords[1])
            self.z = int(vcoords[0])
        else:
            self.x = int(x)
            self.y = int(y)
            self.z = int(z)

        #print(self.x, self.y, self.z)

        self.display_roi()
        
        #print("ROI Loaded")
                
    def display_roi(self, zoom = 20, segd = 2, segu = 2, z = 0):

        #print("Display ROI...")
        self.zb = self.z+(segd*-1)
        self.ze = self.z+segu+1
        
        self.yb = self.y-zoom
        self.ye = self.y+zoom

        self.xb = self.x-zoom
        self.xe = self.x+zoom

        self.imgs = self.ct_scan[self.zb:self.ze, self.yb:self.ye, self.xb:self.xe]
        
        print("The shape is:", self.imgs.shape)
        
        # CONTRAST, middle ground, "more" consistent amongst slices but loses some contrast
        self.imgs = cv2.normalize(self.imgs, None, alpha = 0, beta = 255, norm_type = cv2.NORM_MINMAX, dtype = cv2.CV_32F)
        self.imgs = self.imgs.astype(np.uint8)
        
        img = self.imgs[z, :, :]
        
        # Convert to RGB
        img = cv2.cvtColor(img,cv2.COLOR_GRAY2RGB)

        width, height, channel = img.shape     
        bytesPerLine = 3 * width
        
        imgQT = QImage(img, height, width, bytesPerLine, QImage.Format_RGB888).rgbSwapped()
        imgQP = QPixmap.fromImage(imgQT)
        imgQPrs = imgQP.scaled(768, 768)
        self.scene.addPixmap(imgQPrs)
        self.grview.setScene(self.scene)
        
    def load_segment(self):       
        self.sitk_ct_scan2 = sitk.GetImageFromArray(self.imgs)
        #print("got image")
        
        self.ct_scan_255 = sitk.Cast(sitk.RescaleIntensity(self.sitk_ct_scan2), sitk.sitkUInt8)
        otsu_filter = sitk.OtsuThresholdImageFilter()
        otsu_filter.SetInsideValue(0)
        otsu_filter.SetOutsideValue(1)
        thresh = int(otsu_filter.GetThreshold())
        #print("otsu finished", thresh)

        self.growth_sli.setValue(thresh)
        self.display_segment()
        
    def load_saved_segment(self):
        ldir = os.path.join(self.dname, self.patient)
        ldir = os.path.join(ldir, "segmentations")
        ldir = os.path.join(ldir, self.nodule)
        loaded = np.load(os.path.join(ldir, "segment.npy"))
        self.seg_arr = loaded
        self.update_edit_draw(load=True)
        self.start_edit()
        
    def display_segment(self, z = 0):
        numslices = int(self.rg_slice_sb_u.value() - (self.rg_slice_sb_d.value()*-1))
        #print(numslices)
        self.rg_slice_sli2.setMaximum(numslices)
        self.rg_slice_sli2.setMinimum(0)
        thresh = self.growth_sli.value()
        seed = (self.rg_zoom_sli.value(),
                 self.rg_zoom_sli.value(),
                 self.rg_slice_sli.value())

        self.seg = sitk.ConnectedThreshold(self.sitk_ct_scan2, 
                                          seedList=[seed], 
                                          lower=thresh+self.adjust, 
                                          upper=1000)
        
        self.seg_arr = sitk.GetArrayFromImage(self.seg)
        #print("Completed connected threshold")

        self.sitk_overlay = sitk.LabelOverlay(self.ct_scan_255, self.seg)
        self.overlay = sitk.GetArrayFromImage(self.sitk_overlay).astype(float)
        
        #print(z)
        img = self.overlay[z, :, :]
            
        # Convert hu into grayscale image pixels
        #img = ( (img - img.max())/(img.max()-img.min()) ) * -1
        #img *= 255
        #img = img.astype(int)
        #img = (255 - img)
        
        # save and read image file until I figure how to get Qt to read it
        #params=[cv2.IMWRITE_JPEG_QUALITY, 100]
        #a = np.expand_dims(img, axis = 2)
        #img = np.concatenate((a, a, a), axis = 2)
        img = np.require(img, np.uint8, 'C')

        width, height, channel = img.shape     
        bytesPerLine = 3 * width
        
        imgQT = QImage(img, height, width, bytesPerLine, QImage.Format_RGB888).rgbSwapped()
        imgQP = QPixmap.fromImage(imgQT)
        imgQPrs = imgQP.scaled(768, 768)
        self.scene2.addPixmap(imgQPrs)
        self.grview2.setScene(self.scene2)
        
    def genNextScan(self, path):
        os.chdir(os.path.join(path))
        for root, dirs, files in os.walk(".", topdown=False):
            newpath = os.path.join(path, root)
            for name in files:
                ds = dicom.read_file(os.path.join(newpath, name), force=True)
                if hasattr(ds, 'Modality'):
                    if ds.Modality == 'CT':
                        yield os.path.join(root)#, origin, spacing
                    else:
                        pass
    
    def imageReader(self, path):
        reader = sitk.ImageSeriesReader()
        dicom_names = reader.GetGDCMSeriesFileNames(path)
        reader.SetFileNames(dicom_names)
        image = reader.Execute()
        origin = np.array(list(reversed(image.GetOrigin())))
        spacing = np.array(list(reversed(image.GetSpacing())))
        return image, origin, spacing

    def getVoxelCoord(self, Coord, origin, spacing):
        stretchedVoxelCoord = np.absolute(Coord - origin)
        voxelCoord = stretchedVoxelCoord / spacing
        return voxelCoord

    def update_roi(self):
        nzoom = self.rg_zoom_sli.value()
        sli = self.rg_slice_sli.value()
        segu = self.rg_slice_sb_u.value()
        segd = self.rg_slice_sb_d.value() 
        self.rg_slice_sli.setMaximum(segu-(segd*-1))
        self.rg_slice_sli.setMinimum(0)
        self.display_roi(zoom=nzoom, 
                             segu=segu,
                             segd=segd,
                             z=sli)
        
    def update_segment(self):
        sli = self.rg_slice_sli2.value()
        self.display_segment(z=sli)
        
    def start_edit(self):
        self.tabs.setCurrentIndex(1)
        #np.save('segment_edit.np', self.seg)
        #np.save('roi_edit.np', self.imgs)
        self.scene_edit = QGraphicsScene()

        self.update_edit_draw()

        self.edit_sli.setMinimum(0)
        self.edit_sli.setMaximum(self.imgs_seg.shape[0]-1)
        self.display_edit_l()

    def update_edit_draw(self, z = 0, load = False):
        #print("Types:", type(self.imgs), type(self.seg))
        #print("SHAPE of the imgs:", self.imgs.shape)
        #print("SHAPE of the seg:", self.seg.shape)
        #print(self.imgs.)
        
        if load:
            self.rg_slice_sb_d.setValue(self.meta.loc[int(self.nodule), 'zl'])
            self.rg_slice_sb_u.setValue(self.meta.loc[int(self.nodule), 'zu'])
            self.rg_zoom_sli.setValue(self.meta.loc[int(self.nodule), 'zoom'])
        
        self.imgs_seg = self.imgs * self.seg_arr
        
        #imgs_xyz = self.reshapeImage(self.imgs)
        #img_xyz = imgs_xyz[:,:,0]
        img_xyz = self.imgs[z,:,:]
        #img = img_xyz.astype(int)
        # Convert hu into grayscale image pixels
        #img = ( (img_xyz - img_xyz.max())/(img_xyz.max()-img_xyz.min()) ) * -1
        #img *= 255        
        #
        #img = (255 - img)
        
        a = np.expand_dims(img_xyz, axis = 2)
        img = np.concatenate((a, a, a), axis = 2)
        img = np.require(img, np.uint8, 'C')
        
        #print(seg_arr.max(), seg_arr.min(), np.percentile(seg_arr, [0,100]))
        
        self.view.setImage(img, self.seg_arr[z])
        self.view.updateAll()
        
    def display_edit_l(self, z = 0):
        
        if self.cb_mask.isChecked():
            img = self.imgs_seg[self.edit_sli.value(), :, :]
        else:
            img = self.imgs[self.edit_sli.value(),:,:]

        # Convert hu into grayscale image pixels
        #img = ( (img - img.max())/(img.max()-img.min()) ) * -1
        #img *= 255        
        #img = img.astype(int)
        #img = (255 - img)
        

        
        # save and read image file until I figure how to get Qt to read it        
        a = np.expand_dims(img, axis = 2)
        img = np.concatenate((a, a, a), axis = 2)
        img = np.require(img, np.uint8, 'C')
        
        width, height, channel = img.shape     
        bytesPerLine = 3 * width
        
        imgQT = QImage(img, height, width, bytesPerLine, QImage.Format_RGB888).rgbSwapped()
        self.imgQP = QPixmap.fromImage(imgQT)
        imgQPrs = self.imgQP.scaled(768, 768)
        self.scene_edit.addPixmap(imgQPrs)
        self.edit_l.setScene(self.scene_edit)
        
        if self.cb_contour.isChecked():
            contours = np.asarray(measure.find_contours(self.seg_arr[self.edit_sli.value(),:,:], .001))
            pen = QtGui.QPen(QColor(0,255,0, 100),2)
            
            coords = []
            for l in contours:
                for c in l:
                    coords.append(c)
            
            try:
                coords = np.fliplr(np.asarray(coords))
            except:
                pass
            
            for n, c in enumerate(coords):
                if n < len(coords)-1:
                    l = len(self.imgs[self.edit_sli.value(), :, :])
                    s = .5
                    start = c
                    end   = coords[n+1]
                    #print(start[0], start[1])
                    #print(end[0], end[1])
                    r = QtCore.QLineF(QtCore.QPointF((start[0]+s)*(768/l), (start[1]+s)*(768/l)), 
                                      QtCore.QPointF((  end[0]+s)*(768/l), (  end[1]+s)*(768/l)))
                    self.scene_edit.addLine(r, pen)
        
    def fill_edit(self):
        print("Filling...")
        
    def changeEraseMode(self, b):
      if b.text() == "Draw":
         if b.isChecked() == True:
            self.view.eraseMode(True)
				
      if b.text() == "Erase":
         if b.isChecked() == True:
            self.view.eraseMode(False)
            
    def changeBrushSize(self):
        self.view.brushMode(self.brush_sli.value())

    def update_edit(self):
        self.display_edit_l(z=self.edit_sli.value())
        self.update_edit_draw(z=self.edit_sli.value())
        
    def update_edit_event(self, grid):
        self.seg_arr[self.edit_sli.value()] = grid
        self.update_edit_draw(z=self.edit_sli.value())
        self.display_edit_l(z=self.edit_sli.value())

    def save_segment(self):
        # We need to remember the position for loading
        self.meta.loc[int(self.nodule), 'zl'] = self.rg_slice_sb_d.value()
        self.meta.loc[int(self.nodule), 'zu'] = self.rg_slice_sb_u.value()
        self.meta.loc[int(self.nodule), 'zoom'] = self.rg_zoom_sli.value()
        
        self.meta.to_csv(os.path.join(self.dname,"meta.csv"), index = None)
        
        
        w = QWidget()
        
        ppath = os.path.join(self.dname, self.patient)
        spath = os.path.join(ppath, "segmentations")
        npath = os.path.join(spath, self.nodule)
        
        if hasattr(self, 'seg_arr'):
            if hasattr(self.seg_arr, 'shape'):
                result = QMessageBox.question(w, 'Save', 
                                              "Would you like to save the segmentation?", 
                                              QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                
                if result == QMessageBox.Yes:
                    contents = os.listdir()
                    if "segmentations" in contents:
                        os.chdir(spath)
                        contents = os.listdir()
                        if self.nodule in contents:
                            self.shell[self.zb:self.ze, self.yb:self.ye, self.xb:self.xe] = self.seg_arr
                            np.save(npath+"/"+"segment", self.seg_arr)
                        else:
                            os.chdir(spath)
                            os.mkdir(self.nodule)
                            
                            self.shell[self.zb:self.ze, self.yb:self.ye, self.xb:self.xe] = self.seg_arr
                            np.save(npath+"/"+"segment", self.seg_arr)
                        
                    else:
                        os.chdir(ppath)
                        os.mkdir("segmentations")
                        os.chdir(spath)
                        os.mkdir("{}".format(self.nodule))
                        
                        self.shell[self.zb:self.ze, self.yb:self.ye, self.xb:self.xe] = self.seg_arr
                        np.save(npath+"/"+"segment", self.seg_arr)
                        
            else:
                msg = QMessageBox(w)
                msg.setWindowTitle("Nothing to save")
                msg.setText("You first need to generate a mask!")
                msg.exec_()
        else:
            msg = QMessageBox(w)
            msg.setWindowTitle("Nothing to save")
            msg.setText("You first need to generate a mask!")
            msg.exec_()
            
        self.update_nodules()
        self.update_scans()

        
    def confirm_segment(self):
        self.meta.set_value(int(self.nodule_list.currentItem().text()), 
                            'confirmed', 
                            self.nodule_list.currentItem().checkState())
        
        self.meta.to_csv(os.path.join(self.dname,"meta.csv"), index=False)

    def countFiles(self, path, ext):
        count = 0
        for root, dirs, files in os.walk(path):
            for file in files:
                if file.endswith(ext):
                     count += 1
        return count

if __name__ == '__main__':
    app = QApplication.instance()
    if app is None: 
        app = QApplication(sys.argv)
    form = Form('Segmentr.ui')
    sys.exit(app.exec_())
