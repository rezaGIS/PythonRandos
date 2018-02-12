#==================================================================================================================
# OIT_ConfidenceInterval.py
# Created on: 12/05/2016
# Usage: Converts OIT final template feature classes to mapservice ready confidence GDB
# Description: The tool has multiple steps:
#==================================================================================================================

# Import arcpy module
#import arcpy, os, string

import arcpy
from arcpy import env
import string
import sys
import os
import pickle
import glob

def writeMessage(messageText):
	print (messageText)
	arcpy.AddMessage(messageText)

#Set Input Datasets================================================================================================
DestinationFolder = arcpy.GetParameterAsText(0)
LandlineInput = arcpy.GetParameterAsText(1)
WirelessInput = arcpy.GetParameterAsText(2)
Term = arcpy.GetParameterAsText(3)

myGDBtext = "confidenceInterval_"+Term



myGDB = '%s\%s%s' % (DestinationFolder, myGDBtext, ".gdb")
arcpy.env.workspace = myGDB


arcpy.env.overwriteOutput = True
if arcpy.Exists(myGDB):
    arcpy.AddMessage("File GDB already exists")
else:
    arcpy.CreateFileGDB_management(DestinationFolder, myGDBtext, "CURRENT")
    arcpy.AddMessage("File GDB created")

#LANDLINE==========================================================================================================

LandlineOutputLayer = '%s\%s' % (myGDB, "LandlineOutputLayer")
LandlineFinalLayer = '%s\%s' % (myGDB, "LandlineFinalLayer")
LandlineOutput = '%s\%s' % (myGDB, "landlinetemp")
LandlineFinal = '%s\%s' % (myGDB, "landline")


arcpy.MakeFeatureLayer_management(LandlineInput, LandlineOutputLayer)
arcpy.CopyFeatures_management(LandlineOutputLayer, LandlineOutput)



arcpy.MakeFeatureLayer_management(LandlineOutput, LandlineFinalLayer)
arcpy.Dissolve_management(LandlineFinalLayer, LandlineFinal, ["PROVNAME", "CONFIDENCE"], "", "", "")
arcpy.Delete_management(LandlineOutput, "")



#WIRELESS==========================================================================================================

WirelessOutputLayer = '%s\%s' % (myGDB, "WirelessOutputLayer")
WirelessFinalLayer = '%s\%s' % (myGDB, "WirelessFinalLayer")
WirelessOutput = '%s\%s' % (myGDB, "wirelesstemp")
WirelessFinal = '%s\%s' % (myGDB, "wireless")

TT60 = 60
TT60String = str(TT60)
TT80 = 80
TT80String = str(TT80)

arcpy.MakeFeatureLayer_management(WirelessInput, WirelessOutputLayer)
arcpy.SelectLayerByAttribute_management(WirelessOutputLayer, "NEW_SELECTION", "TRANSTECH = "+TT60String)
arcpy.SelectLayerByAttribute_management(WirelessOutputLayer, "ADD_TO_SELECTION", "TRANSTECH = "+TT80String)
arcpy.SelectLayerByAttribute_management(WirelessOutputLayer, "SWITCH_SELECTION")
arcpy.CopyFeatures_management(WirelessOutputLayer, WirelessOutput)



arcpy.MakeFeatureLayer_management(WirelessOutput, WirelessFinalLayer)
arcpy.Dissolve_management(WirelessFinalLayer, WirelessFinal, ["PROVNAME", "CONFIDENCE"], "", "", "")
arcpy.Delete_management(WirelessOutput, "")


























#DumpFields = ["PROVALIAS", "PROVNAME", "DBANAME", "FRN", "TRANSTECH", "MAXADDOWN", "MAXADUP", "TYPICDOWN", "TYPICUP", "MAXSUBDOWN",
              #"MAXSUBUP", "PRICE", "PRICE", "PROVIDER_TYPE", "ENDUSERCAT", "PLSSID", "REFGRIDNO", "OIT_ID", "WHO", "WHEN"]

#arcpy.DeleteField_management(LandlineOutputLayer, DumpFields)

#arcpy.Dissolve_management("taxlots", "C:/output/output.gdb/taxlots_dissolved",
                          #["LANDUSE", "TAXCODE"], "", "SINGLE_PART",
                          #"DISSOLVE_LINES")


#arcpy.CopyFeatures_management(LandlineOutputLayer, LandlineOutput)
#confidenceInterval_October2016.gdb