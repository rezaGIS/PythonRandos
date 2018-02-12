# ---------------------------------------------------------------------------
# provNameSpeedV01.py
# Created on: 2013-05-02 07:33:59.00000
# Author: Kass Rezagholi
# Description:
# Creates Mapservice feature classes for provNameSpeed
# ---------------------------------------------------------------------------

# Import arcpy module

import arcpy
from arcpy import env
import sys
import os
import string

def writeMessage(messageText):
	print messageText
	arcpy.AddMessage(messageText)

##-------------------------------------------------------------------------------Open Parameters
myFolder = arcpy.GetParameterAsText(0)
myGDBtext = arcpy.GetParameterAsText(1) #+ strftime("%d_%m_%y")
OITplss = arcpy.GetParameterAsText(2)
OITwireless = arcpy.GetParameterAsText(3)

##-------------------------------------------------------------------------------Workspace Location
COBB = '%s\%s%s' % (myFolder, myGDBtext, ".gdb")
env.workspace = COBB



##-------------------------------------------------------------------------------Final Output feature class
provNameSpeed = '%s\%s' % (COBB, "provNameSpeed")

##-------------------------------------------------------------------------------Create Geodatabase
# Process: Create File GDB
writeMessage("Creating geodatabase")
arcpy.CreateFileGDB_management(myFolder, myGDBtext, "CURRENT")
writeMessage("File Geodatabase created")


##-------------------------------------------------------------------------------Feature classes and temporary layers
provNamePlss = '%s\%s' % (COBB, "provNamePlss")
provNameWireless = COBB + "\\provNameWireless"
provNameWireline = COBB + "\\provNameWireline"
provNameWirelineFinal = COBB + "\\provNameWirelineFinal"
provNameFixed = '%s\%s' % (COBB, "provNameFixed")
provNameSat = '%s\%s' % (COBB, "provNameSat")
provNameMob = '%s\%s' % (COBB, "provNameMob")
#
# PLSS
#
##-------------------------------------------------------------------------------Start Census Processing
writeMessage("Add OIT PLSS")
arcpy.FeatureClassToFeatureClass_conversion(OITplss, COBB, "plss", "", "", "")
writeMessage("Coverage imported")

plss = COBB + "\\plss"

writeMessage("Start OIT PLSS dissolve: PROVNAME, TRANSTECH, MAXADDOWN, and MAXADUP")
try:
    arcpy.Dissolve_management(plss, provNamePlss, ["PROVNAME","TRANSTECH","MAXADDOWN","MAXADUP"], "", "MULTI_PART", "DISSOLVE_LINES")
    writeMessage("Dissolve successful")
except Exception as e:
    print e
    writeMessage("Dissolve failed")

##-------------------------------------------------------------------------------Add and Calculate fields
writeMessage("Add and Calculate _low and _high fields")

try:
    arcpy.AddField_management(provNamePlss, "down_low", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
    arcpy.AddField_management(provNamePlss, "down_high", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
    arcpy.AddField_management(provNamePlss, "up_low", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
    arcpy.AddField_management(provNamePlss, "up_high", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
    writeMessage("Fields Added")
except:
    writeMessage("Fields Not Added")

try:
    arcpy.CalculateField_management(provNamePlss, "down_low", "X", "VB", "IF [MAXADDOWN] = 3 THEN\\nX = 0.75\\nEND IF\\nIF [MAXADDOWN] = 4 THEN\\nX = 1.5\\nEND IF\\nIF [MAXADDOWN] = 5 THEN\\nX = 3 \\nEND IF\\nIF [MAXADDOWN] = 6 THEN\\nX = 6\\nEND IF\\nIF [MAXADDOWN] = 7 THEN\\nX = 10\\nEND IF\\nIF [MAXADDOWN] = 8 THEN\\nX = 25\\nEND IF\\nIF [MAXADDOWN] = 9 THEN\\nX = 50\\nEND IF\\nIF [MAXADDOWN] = 10 THEN\\nX = 100\\nEND IF\\nIF [MAXADDOWN] = 11 THEN\\nX = 1000\\nEND IF")
    arcpy.CalculateField_management(provNamePlss, "down_high", "X", "VB", "IF [MAXADDOWN] = 3 THEN\\nX = 1.5\\nEND IF\\nIF [MAXADDOWN] = 4 THEN\\nX = 3\\nEND IF\\nIF [MAXADDOWN] = 5 THEN\\nX = 6\\nEND IF\\nIF [MAXADDOWN] = 6 THEN\\nX = 10\\nEND IF\\nIF [MAXADDOWN] = 7 THEN\\nX = 25\\nEND IF\\nIF [MAXADDOWN] = 8 THEN\\nX = 50\\nEND IF\\nIF [MAXADDOWN] = 9 THEN\\nX = 100\\nEND IF\\nIF [MAXADDOWN] = 10 THEN\\nX = 999\\nEND IF\\nIF [MAXADDOWN] = 11 THEN\\nX = 1000\\nEND IF")
    arcpy.CalculateField_management(provNamePlss, "up_low", "X", "VB", "IF [MAXADUP] = 2 THEN\\nX = 0.2\\nEND IF\\nIF [MAXADUP] = 3 THEN\\nX = 0.75\\nEND IF\\nIF [MAXADUP] = 4 THEN\\nX = 1.5\\nEND IF\\nIF [MAXADUP] = 5 THEN\\nX = 3 \\nEND IF\\nIF [MAXADUP] = 6 THEN\\nX = 6\\nEND IF\\nIF [MAXADUP] = 7 THEN\\nX = 10\\nEND IF\\nIF [MAXADUP] = 8 THEN\\nX = 25\\nEND IF\\nIF [MAXADUP] = 9 THEN\\nX = 50\\nEND IF\\nIF [MAXADUP] = 10 THEN\\nX = 100\\nEND IF\\nIF [MAXADUP] = 11 THEN\\nX = 1000\\nEND IF")
    arcpy.CalculateField_management(provNamePlss, "up_high", "X", "VB", "IF [MAXADUP] = 2 THEN\\nX = 0.75\\nEND IF\\nIF [MAXADUP] = 3 THEN\\nX = 1.5\\nEND IF\\nIF [MAXADUP] = 4 THEN\\nX = 3\\nEND IF\\nIF [MAXADUP] = 5 THEN\\nX = 6\\nEND IF\\nIF [MAXADUP] = 6 THEN\\nX = 10\\nEND IF\\nIF [MAXADUP] = 7 THEN\\nX = 25\\nEND IF\\nIF [MAXADUP] = 8 THEN\\nX = 50\\nEND IF\\nIF [MAXADUP] = 9 THEN\\nX = 100\\nEND IF\\nIF [MAXADUP] = 10 THEN\\nX = 999\\nEND IF\\nIF [MAXADUP] = 11 THEN\\nX = 1000\\nEND IF")
    writeMessage("Fields Calculated")
except:
    writeMessage("Field Calculations failed")

##-------------------------------------------------------------------------------Wireline feature class creation
provNameSpeed_Wireline = COBB + "\\provNameSpeed_Wireline"
try:
    arcpy.CopyFeatures_management(provNamePlss, provNameSpeed_Wireline, "", "0", "0", "0")
    writeMessage("Final PLSS output created: provNameSpeed_Wireline")

except:
    writeMessage("Final PLSS feature class not created")

writeMessage("PLSS Processing complete; Moving on to wireless....")

##-------------------------------------------------------------------------------Start wireless processing
#
# WIRELESS
#
writeMessage("Add OIT Wireless Coverage")
wireless = COBB + "\\wireless"
arcpy.FeatureClassToFeatureClass_conversion(OITwireless, COBB, "wireless", "", "", "")
writeMessage("Coverage imported")
writeMessage("Start OIT PLSS dissolve: PROVNAME, TRANSTECH, MAXADDOWN, and MAXADUP")
try:
    arcpy.Dissolve_management(wireless, provNameWireless, ["PROVNAME","TRANSTECH","MAXADDOWN","MAXADUP"], "", "MULTI_PART", "DISSOLVE_LINES")
    writeMessage("Wireless dissolve complete ")
except Exception as e:
    print e
    writeMessage("Dissolve Failed")

##-------------------------------------------------------------------------------Add and calculate fields
writeMessage("Add _low and _high fields")
try:
    arcpy.AddField_management(provNameWireless, "down_low", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
    arcpy.AddField_management(provNameWireless, "down_high", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
    arcpy.AddField_management(provNameWireless, "up_low", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
    arcpy.AddField_management(provNameWireless, "up_high", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
    writeMessage("Fields added")
except:
    writeMessage("Fields could not be added")

writeMessage("Calculate fields")
try:
    arcpy.CalculateField_management(provNameWireless, "down_low", "X", "VB", "IF [MAXADDOWN] = 3 THEN\\nX = 0.75\\nEND IF\\nIF [MAXADDOWN] = 4 THEN\\nX = 1.5\\nEND IF\\nIF [MAXADDOWN] = 5 THEN\\nX = 3 \\nEND IF\\nIF [MAXADDOWN] = 6 THEN\\nX = 6\\nEND IF\\nIF [MAXADDOWN] = 7 THEN\\nX = 10\\nEND IF\\nIF [MAXADDOWN] = 8 THEN\\nX = 25\\nEND IF\\nIF [MAXADDOWN] = 9 THEN\\nX = 50\\nEND IF\\nIF [MAXADDOWN] = 10 THEN\\nX = 100\\nEND IF\\nIF [MAXADDOWN] = 11 THEN\\nX = 1000\\nEND IF")
    arcpy.CalculateField_management(provNameWireless, "down_high", "X", "VB", "IF [MAXADDOWN] = 3 THEN\\nX = 1.5\\nEND IF\\nIF [MAXADDOWN] = 4 THEN\\nX = 3\\nEND IF\\nIF [MAXADDOWN] = 5 THEN\\nX = 6\\nEND IF\\nIF [MAXADDOWN] = 6 THEN\\nX = 10\\nEND IF\\nIF [MAXADDOWN] = 7 THEN\\nX = 25\\nEND IF\\nIF [MAXADDOWN] = 8 THEN\\nX = 50\\nEND IF\\nIF [MAXADDOWN] = 9 THEN\\nX = 100\\nEND IF\\nIF [MAXADDOWN] = 10 THEN\\nX = 999\\nEND IF\\nIF [MAXADDOWN] = 11 THEN\\nX = 1000\\nEND IF")
    arcpy.CalculateField_management(provNameWireless, "up_low", "X", "VB", "IF [MAXADUP] = 2 THEN\\nX = 0.2\\nEND IF\\nIF [MAXADUP] = 3 THEN\\nX = 0.75\\nEND IF\\nIF [MAXADUP] = 4 THEN\\nX = 1.5\\nEND IF\\nIF [MAXADUP] = 5 THEN\\nX = 3 \\nEND IF\\nIF [MAXADUP] = 6 THEN\\nX = 6\\nEND IF\\nIF [MAXADUP] = 7 THEN\\nX = 10\\nEND IF\\nIF [MAXADUP] = 8 THEN\\nX = 25\\nEND IF\\nIF [MAXADUP] = 9 THEN\\nX = 50\\nEND IF\\nIF [MAXADUP] = 10 THEN\\nX = 100\\nEND IF\\nIF [MAXADUP] = 11 THEN\\nX = 1000\\nEND IF")
    arcpy.CalculateField_management(provNameWireless, "up_high", "X", "VB", "IF [MAXADUP] = 2 THEN\\nX = 0.75\\nEND IF\\nIF [MAXADUP] = 3 THEN\\nX = 1.5\\nEND IF\\nIF [MAXADUP] = 4 THEN\\nX = 3\\nEND IF\\nIF [MAXADUP] = 5 THEN\\nX = 6\\nEND IF\\nIF [MAXADUP] = 6 THEN\\nX = 10\\nEND IF\\nIF [MAXADUP] = 7 THEN\\nX = 25\\nEND IF\\nIF [MAXADUP] = 8 THEN\\nX = 50\\nEND IF\\nIF [MAXADUP] = 9 THEN\\nX = 100\\nEND IF\\nIF [MAXADUP] = 10 THEN\\nX = 999\\nEND IF\\nIF [MAXADUP] = 11 THEN\\nX = 1000\\nEND IF")
    writeMessage("Fields calculated successfully")
except:
    writeMessage("Could not calculate fields")

##-------------------------------------------------------------------------------Making Fixed, Satellite, and Mobile Layers and feature classes
writeMessage("Make Fixed, Satellite, and Mobile Layers")
arcpy.MakeFeatureLayer_management(provNameWireless, provNameFixed, "\"TRANSTECH\" IN(70, 71)", COBB)
writeMessage("Fixed Layer Created")
arcpy.MakeFeatureLayer_management(provNameWireless, provNameSat, "\"TRANSTECH\" = 60", COBB)
writeMessage("Satellite Layer Created")
arcpy.MakeFeatureLayer_management(provNameWireless, provNameMob, "\"TRANSTECH\" = 80", COBB)
writeMessage("Mobile Layer Created")

writeMessage("Creating final outputs")

provNameSpeed_Satellite = COBB + "\\provNameSpeed_Satellite"
provNameSpeed_Fixed = COBB + "\\provNameSpeed_Fixed"
provNameSpeed_Mobile = COBB + "\\provNameSpeed_Mobile"

arcpy.CopyFeatures_management(provNameSat, provNameSpeed_Satellite, "", "0", "0", "0")
writeMessage("Satellite complete")
arcpy.CopyFeatures_management(provNameFixed, provNameSpeed_Fixed, "", "0", "0", "0")
writeMessage("Fixed Wireless Complete")
arcpy.CopyFeatures_management(provNameMob, provNameSpeed_Mobile, "", "0", "0", "0")
writeMessage("Mobile complete")

writeMessage("Final Outputs created")
writeMessage("Append final provNameSpeed feature class")

##-------------------------------------------------------------------------------Final Append and outputs
#
# FINAL provNameSpeed APPEND
#

try:
    arcpy.CopyFeatures_management(provNameWirelineFinal, provNameSpeed, "", "0", "0", "0")
    arcpy.Append_management([provNameFixed, provNameMob, provNameSat], provNameSpeed, "TEST", "", "")
    writeMessage("Append complete")
except:
    writeMessage("Append Failed")
##-------------------------------------------------------------------------------Merge all into one for provNameSpeed_ALL
try:
    arcpy.Merge_management([provNameSpeed_Wireline, provNameSpeed_Fixed, provNameSpeed_Mobile, provNameSpeed_Satellite], "provNameSpeed_ALL")
except:
    writeMessage("Merge to create 'provNameSpeed_ALL' failed")

##-------------------------------------------------------------------------------Delete temporary im_memory files
# Delete Temporary files
arcpy.Delete_management(plss, "")
arcpy.Delete_management(provNamePlss, "")
arcpy.Delete_management(wireless, "")
arcpy.Delete_management(provNameWireless, "")
arcpy.Delete_management(provNameWirelineFinal, "")