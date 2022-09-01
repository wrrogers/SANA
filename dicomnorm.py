from tools import load_scan, get_pixels_hu
import os
import matplotlib.pyplot as plt
import numpy as np
import cv2

path = r'D:\Data\LIDC-IDRI\LIDC-IDRI-0001\01-01-2000-30178\3000566-03192'
file = '000001.dcm'

slices = load_scan(path)

scan = get_pixels_hu(slices)

print(scan.shape, scan.min(), scan.max())


plt.imshow(scan[-89])

print(scan.shape, scan.min(), scan.max())

#scan = ((scan - scan.max())/(scan.max()-scan.min()) ) * -1
#scan *= 255        
#scan = scan.astype(int)

scan = cv2.normalize(scan, None, alpha = 0, beta = 255, norm_type = cv2.NORM_MINMAX, dtype = cv2.CV_32F)

scan = scan.astype(np.uint8)

print(scan.shape, scan.min(), scan.max())

plt.imshow(scan[-89])

#a = np.expand_dims(scan[70], axis = 2)
#img = np.concatenate((a, a, a), axis = 2)
#scan = np.require(img, np.uint8, 'C')

print("min max", scan[-89].min(), scan[-89].max())

scan = cv2.cvtColor(scan[-89],cv2.COLOR_GRAY2RGB)

print("min max", scan.min(), scan.max())

plt.imshow(scan)

zoomed = scan[366-20:366+20, 316-20:316+20, ]
plt.imshow(zoomed)