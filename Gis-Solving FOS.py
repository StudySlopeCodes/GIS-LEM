#-----coding: utf-8 -------#
import arcpy
import pandas as pd
import numpy as np
import os
import time

from threading import Event
from arcpy import env
from arcpy.sa import *
arcpy.env.overwriteOutput = True


#path = r"D:\software\Geostudio\GeoE\GeoStudio 9\Bin\GeoCmd.exe"
#xmlPath =r"C:\Users\ZhiYong\Desktop\GeoResult\test"

path = arcpy.GetParameterAsText(0)
xmlPath = arcpy.GetParameterAsText(1)

Cohesion = arcpy.GetParameterAsText(2)
Cohesion = arcpy.Raster(Cohesion)

Cur = arcpy.da.SearchCursor(Cohesion, ["VALUE"])

Cohs = []
for row in Cur:
    Cohs.append(row[0])



for Coh in Cohs:
    for num in range(10, 70):  
        name= str(num) + "C" + str(Coh)
        xmlFilePath = os.path.join(xmlPath, name)
        xmlFile = xmlFilePath + ".xml"
        files = subprocess.Popen([path, xmlFile, '/solve'], shell = True)
        return_code = files.wait()
    print("finish")