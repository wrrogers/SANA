import SimpleITK as sitk
import sys, os
import numpy as np


def getMeta(path, file):
    reader = sitk.ImageFileReader()
    reader.SetFileName(os.path.join(path, file))
    reader.LoadPrivateTagsOn();
    
    reader.ReadImageInformation()
    
    #print(reader.GetFileName())
    
    taglib = {}
    for k in reader.GetMetaDataKeys():
        v = reader.GetMetaData(k)
        #print("({0}) == \"{1}\"".format(k,v))
        if k == "0020|000d": taglib['Study Instance UID'] = v
        if k == "0020|000e": taglib['Series Instance UID'] = v
        if k == "0020|0052": taglib['Frame of Reference UID'] = v
        if k == "0040|a124": taglib['UID'] = v
    
    return taglib


for x in range(1, 7):
    path = "D:/Data/LIDC-IDRI/LIDC-IDRI-0001/01-01-2000-30178/3000566-03192"
    file = '00000{}.dcm'.format(x)
    taglib = getMeta(path, file)
    
    #print("\nImage Size: {0}".format(reader.GetSize()));
    #print("Image PixelType: {0}".format(sitk.GetPixelIDValueAsString(reader.GetPixelID())));
        
    print('\nTags:')
    for t in taglib.items():
        print("{0}\t\t\t{1}".format(t[0],t[1]))