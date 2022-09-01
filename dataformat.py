#import matplotlib.pyplot as plt
import pydicom as dicom
import numpy as np
import pandas as pd
import os

#Thanks to Howard Chen https://www.raddq.com/dicom-processing-segmentation-visualization-in-python/
def load_scan(path):
    print("Loading scan...")
    fdir = os.listdir(path)
    files = [f for f in fdir if '.dcm' in f]
    
    slices = [dicom.read_file(path + '/' + s) for s in files]

    slices.sort(key = lambda x: int(x.InstanceNumber))
    try:
        slice_thickness = np.abs(slices[0].ImagePositionPatient[2] - slices[1].ImagePositionPatient[2])
    except:
        slice_thickness = np.abs(slices[0].SliceLocation - slices[1].SliceLocation)
        
    for s in slices:
        s.SliceThickness = slice_thickness

    return slices

os.chdir('D:/Data/LIDC-IDRI')
path = os.path.join(os.getcwd(), 'LIDC-IDRI-0001/01-01-2000-30178/3000566-03192')
patient = load_scan(path)

print(patient)

path = os.path.join(os.getcwd(),r'D:\Data\LIDC-IDRI\LIDC-IDRI-0181\01-01-2000-CT THORAX WCONTRAST-05064\3-Recon 2 CHEST-95147')
file = '000001.dcm'
ds = dicom.read_file(os.path.join(path, file), force=True)
ds.dir()

ds

print(ds.SeriesInstanceUID)
#ds.dir('patient')
print(ds.PatientID)
print(ds.Modality)
#ds.dir('pixel')
#print(ds.PixelPaddingValue)
print(ds.PixelRepresentation)
print(ds.PixelSpacing)
print(ds.SamplesPerPixel)
print(ds.SliceLocation)
print(ds.SliceThickness)
print(ds.ImagePositionPatient)

path = os.path.join(os.getcwd(),r'LIDC-IDRI-0001\01-01-2000-35511\3000923-62357')
file = '000001.dcm'
ds = dicom.read_file(os.path.join(path, file), force=True)
print(ds.SeriesInstanceUID)
print(ds.PatientID)
print(ds.Modality)

mapping = pd.DataFrame(columns = ['Patient'])
mapping.set_index('Patient')
for root, dirs, files in os.walk('.', topdown=True):
    for name in files:
        if '000001.dcm' in name:
            path = os.path.join(os.getcwd(),root)
            ds = dicom.read_file(os.path.join(path, file), force=True)
            if ds.Modality == 'CT':
                #print(root[2:16])
                mapping.loc[ds.SeriesInstanceUID] = root[2:16]
            
print(mapping.head())

os.chdir('D:/Data/LIDC-IDRI')       
mapping.to_csv('PatientMap.csv')

annotations = pd.read_csv('annotations.csv')

annotations['patientuid'] = np.nan
cols = annotations.columns
cols

mapping = pd.read_csv('PatientMap.csv')

mapping.set_index('seriesuid')
annotations.set_index('seriesuid')

mapping.loc[mapping.seriesuid == '1.3.6.1.4.1.14519.5.2.1.6279.6001.179049373636438705059720603192']
annotations.loc['1.3.6.1.4.1.14519.5.2.1.6279.6001.179049373636438705059720603192']

for n, data in annotations.iterrows():
    patient =  mapping.loc[ mapping.seriesuid == data[0] ]
    print("Series:", patient.seriesuid, "\n")
    if(len(patient.patientuid.values)>0):
        print("Patient:", patient.patientuid.item())
        annotations.set_value(n, 'patientuid', patient.patientuid.item())
    print("---------")
    
    
annotations.to_csv('meta.csv')
