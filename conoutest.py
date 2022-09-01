import numpy as np
import matplotlib.pyplot as plt

from skimage import measure


# Construct some test data
#x, y = np.ogrid[-np.pi:np.pi:100j, -np.pi:np.pi:100j]
#r = np.sin(np.exp((np.sin(x)**3 + np.cos(y)**2)))

r = [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,],
     [0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,],
     [0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,],
     [0,0,0,0,1,1,1,1,0,0,0,0,0,0,0,],
     [0,0,0,0,1,1,1,1,1,0,0,0,0,0,0,],
     [0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,],
     [0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,],
     [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,],
     [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,],
     [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,],
     [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,],
     [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,],
     [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,]]

constants = [c for c in np.arange(.1, 1, .1)]
# Find contours at a constant value of 0.8
contours = []
for c in constants:
    contours.append( measure.find_contours(r, c))

fig, ax = plt.subplots()
ax.imshow(r, interpolation='nearest', cmap=plt.cm.gray)

for cmap in contours:
    # Display the image and plot all contours found
    for n, contour in enumerate(cmap):
        ax.plot(contour[:, 1], contour[:, 0], linewidth=2)
    
ax.axis('image')
ax.set_xticks([])
ax.set_yticks([])
plt.show()


fig, ax = plt.subplots()
ax.imshow(r, interpolation='nearest', cmap=plt.cm.gray)

arr0 = contours[0]
print(contours[0])
for n, contour in enumerate(contours[0]):
    ax.plot(contour[:, 1], contour[:, 0], linewidth=2)

print(contours[-1])
for n, contour in enumerate(contours[-1]):
    ax.plot(contour[:, 1], contour[:, 0], linewidth=2)
    
ax.axis('image')
ax.set_xticks([])
ax.set_yticks([])
plt.show()

os.chdir(r'C:\Users\wrrog\Istituto dei Tumori\Project 1')
os.getcwd()
arr = np.load('cntrs.npy')

arr = [arr]

fig, ax = plt.subplots()
#ax.imshow(r, interpolation='nearest', cmap=plt.cm.gray)

for n, c in enumerate(arr):
    #print(c[:,1], c[:,0])
    ax.plot(c[:, 1], c[:, 0], linewidth=2)
    
ax.axis('image')
ax.set_xticks([])
ax.set_yticks([])
plt.show()

import math


def rotate(xy, theta = 7.85):
    # https://en.wikipedia.org/wiki/Rotation_matrix#In_two_dimensions
    cos_theta, sin_theta = math.cos(theta), math.sin(theta)

    return [xy[0] * cos_theta - xy[1] * sin_theta,
            xy[0] * sin_theta + xy[1] * cos_theta ]


def translate(xy, offset):
    return xy[0] + offset[0], xy[1] + offset[1]

mirror = [np.fliplr(arr[0])]

fig, ax = plt.subplots()
#ax.imshow(r, interpolation='nearest', cmap=plt.cm.gray)

for n, c in enumerate(mirror):
    #print(c[:,1], c[:,0])
    ax.plot(c[:, 1], c[:, 0], linewidth=2)
    
ax.axis('image')
ax.set_xticks([])
ax.set_yticks([])
plt.show()

newarr = []
for x in mirror[0]:
    #print(x)
    newarr.append(rotate(x, 7.85))

newarr = [np.asarray(newarr)]

fig, ax = plt.subplots()
#ax.imshow(r, interpolation='nearest', cmap=plt.cm.gray)

for n, c in enumerate(newarr):
    #print(c[:,1], c[:,0])
    ax.plot(c[:, 1], c[:, 0], linewidth=2)
    
ax.axis('image')
ax.set_xticks([])
ax.set_yticks([])
plt.show()

def fliprotate(xy):
    theta = 7.85
    cos_theta, sin_theta = math.cos(theta), math.sin(theta)
    flipped = np.fliplr(xy)

    rotated = []
    for point in flipped:
        rotated.append([point[0] * cos_theta - point[1] * sin_theta,
                        point[0] * sin_theta + point[1] * cos_theta ])
    return np.asarray(rotated)

    return flipped

newarr = [fliprotate(arr[0])]


fig, ax = plt.subplots()
#ax.imshow(r, interpolation='nearest', cmap=plt.cm.gray)

for n, c in enumerate(newarr):
    #print(c[:,1], c[:,0])
    ax.plot(c[:, 1], c[:, 0], linewidth=2)
    
ax.axis('image')
ax.set_xticks([])
ax.set_yticks([])
plt.show()


























