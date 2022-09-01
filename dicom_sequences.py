from pydicom.sequence import Sequence
from pydicom.dataset import Dataset

# create to toy datasets
block_ds1 = Dataset()
block_ds1.BlockType = "APERTURElala"
block_ds1.BlockName = "Block1"

block_ds2 = Dataset()
block_ds2.BlockType = "APERTURElala"
block_ds2.BlockName = "Block2"

beam = Dataset()
# note that you should add beam data elements like BeamName, etc; these are
# skipped in this example
plan_ds = Dataset()
# starting from scratch since we did not read a file
plan_ds.BeamSequence = Sequence([beam])
plan_ds.BeamSequence[0].BlockSequence = Sequence([block_ds1, block_ds2])
plan_ds.BeamSequence[0].NumberOfBlocks = 2

beam0 = plan_ds.BeamSequence[0]
print('Number of blocks: \n{}'.format(plan_ds))

# create a new data set
block_ds3 = Dataset()
# add data elements to it as above and don't forget to update Number of Blocks
# data element
beam0.BlockSequence.append(block_ds3)
del plan_ds.BeamSequence[0].BlockSequence[1]


cntrs = {1:[1,2,3,4,5], 2:[1,2,3,4,5,6,7]}

cntr1 = Dataset()
cntr1.BlockType = "Contour"
cntr1.BlockName = "Contour 1"
cntr1.ContourGeometricType = 'Planar'
cntr1.NumberOfContourPoints = len(cntrs[1])
cntr1.ContourData = cntrs[1]


cntr2 = Dataset()
cntr2.BlockType = "Contour"
cntr2.BlockName = "Contour 2"
cntr2.ContourGeometricType = 'Planar'
cntr2.NumberOfContourPoints = len(cntrs[2])
cntr2.ContourData = cntrs[2]

ds = Dataset()
Contours = Dataset()

ds.ROIContourSequence = Sequence([Contours])
ds.ROIContourSequence[0].ContourSequence = Sequence([cntr1, cntr2])
ds.ROIContourSequence[0].NumberOfBlocks = 2

print('Number of blocks: \n{}'.format(ds))