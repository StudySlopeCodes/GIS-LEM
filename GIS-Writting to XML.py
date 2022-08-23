import xml.dom.minidom as minidom
import xml.etree.ElementTree as ET

import arcpy
import numpy as np
import os
import subprocess

# the first xml file path is needed

#dirPath =  r"C:\Users\ZhiYong\Desktop\GeoResult\xmlfile"
dirPath = arcpy.GetParameterAsText(0)

for file in os.listdir(dirPath):
    path = os.path.join(dirPath,file)

arcpy.AddMessage(path)   
tree = ET.parse(path) # Element Tree
root = tree.getroot()

VeryHard = []
Hard = []
Soft = []
VerySoft = []
Rocks = [VeryHard, Hard, Soft, VerySoft]


#---bulild the rock list------#

unit = arcpy.GetParameterAsText(1)
units = arcpy.da.SearchCursor(unit, ["VALUE"])
Gs = []

cohesion = arcpy.GetParameterAsText(2)
cohesions = arcpy.da.SearchCursor(cohesion, ["VALUE"])
Cs = []

friction = arcpy.GetParameterAsText(3)
frictions = arcpy.da.SearchCursor(friction, ["VALUE"])
Fs = []


for value in units:
    Gs.append(value[0])

for value in cohesions:
    Cs.append(value[0])
    
for value in frictions:
    Fs.append(value[0])

 

for num in range(len(Gs)):
    Rocks[num].append(Gs[num])
for num in range(len(Cs)):
    Rocks[num].append(Cs[num])
for num in range(len(Fs)):
    Rocks[num].append(Fs[num])



Orpath = arcpy.GetParameterAsText(5)

for rock in  Rocks:
    #----modify the parameter of rocks----#
    for gama in root.iter('UnitWeight'):
        gama.text = str(rock[0])

    for coh in root.iter('CohesionPrime'):
       coh.text = str(rock[1])

    for  phi in root.iter('PhiPrime'):
       phi.text = str(rock[2])

#predefine parameters

    RasterWidth = 40
    ModelWidth = 60

#zeros point is not changed
    NumPoint = ["3","4"]


#------batch to xml files------#


    for Angle in range(10,70):
        #define parameters
        ArcAngle = Angle/180 *3.1415
        Height = RasterWidth * np.tan(ArcAngle)

        # rename files
        for name in root.iter("Name"):
            name.text = "C" + str(rock[1]) + "S" + str(Angle)
            break

        # points
        for point in root.iter("Point"):
            if point.attrib["ID"]  in NumPoint and len(point.attrib) ==4:
                point .attrib["Y"] = str(Height)

        # write to xml file

        Propath = os.path.join(Orpath, str(Angle))
        NewTree = ET.ElementTree(root)
        NewTree.write(Propath + "C" + str(rock[1]) + '.xml')