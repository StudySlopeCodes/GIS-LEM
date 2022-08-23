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


#Path = r"C:\Users\ZhiYong\Desktop\GeoResult\test"

##------obtain the filepath of the geostuido calculating results ----##
Path = arcpy.GetParameterAsText(0)

#change the current path to the set path
os.chdir(Path)

filePaths = []
for file in os.listdir(Path):
    if os.path.isdir(file):
        filePaths.append(file)


NextPaths = []
for Num in range(len(filePaths)):
    NextPaths.append(os.path.join(Path,filePaths[Num]))


##----obtain the safety of factors calculating by geostuido
ResultPaths = []
fileNames = []
for NextPath in NextPaths: 
        fileNames.append(NextPath.split("\\")[-1])
        for file in os.listdir(NextPath):  
            file = os.path.join(NextPath, file) 
            if os.path.isdir(file):  
                ResultPaths.append(file) 

#the name of results files is defiend "slip_surface.csv" 
fileName = "slip_surface.csv"

#the Dict type is used to store the calculation results
FactorDict = {} 
for path in ResultPaths:
    temp = [] 
    factorFile = os.path.join(path, fileName)
    allFactor = pd.read_csv(factorFile)  

    if np.min(allFactor["SlipFOS"]) == 994 :
        minFactor = 0.5
    else:
        minFactor = np.min(allFactor["SlipFOS"])  

   
    splitName = factorFile.split("\\")[-3]
    FactorDict[splitName] = minFactor


#slope and Cohesion are inputted
slope = arcpy.GetParameterAsText(1)
slope = arcpy.Raster(slope)
slope = Int(slope)

Cohesion = arcpy.GetParameterAsText(2)
Cur = arcpy.da.SearchCursor(Cohesion, ["VALUE"])

Cohs = []
for row in Cur:
    Cohs.append(row[0])

#change to raster
Cohesion = arcpy.Raster(Cohesion)
factor = slope
Mark = 0
for angle in range(10,90):
    for value in Cohs:
        Name = "C" + str(value) + "S" + str(angle)
        if  Name in fileNames:
            factor = Con(BooleanAnd(factor == angle, Cohesion == value), FactorDict.get(Name), factor)
            print(factor)
        if angle > 69:
            factor = Con(BooleanAnd(factor == angle, Cohesion == value), 0.5, factor)
            print(factor)

        Mark += 1
        print(Mark, Name)


Output = arcpy.GetParameterAsText(3)

factor.save(Output)