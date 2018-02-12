#-------------------------------------------------------------------------------
# Name:        Provider Data Transfer
# Purpose:     This tool will transfer broadband's previous workspace with proper folder structure and previous delivery's readme.
#
# Author:      Kass Rezagholi
#
# Created:     07/07/2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import arcpy, os, shutil

LookupTable = arcpy.GetParameterAsText(0)       #Location of lookup table
OriginFolder = arcpy.GetParameterAsText(1)      #Source folder of previous provider data
DestinationFolder = arcpy.GetParameterAsText(2)     #Destination folder where provider data folders will be stored


ProviderNameField = "PROVALIAS"

def createFolder():
    try:
        OldReadmeLocation = os.path.join(OriginFolder + "/" + row.getValue(ProviderNameField) + "/" + "README.txt")
        forTesting = shutil.copyfile(OldReadmeLocation, DestinationFolder + "/" + row.getValue(ProviderNameField) + "/" +  "README.txt")
    except:
        print "Provider" + row.getValue(ProviderNameField) + "README.txt does not exist.  Check log to explore error."
    cursor = arcpy.SearchCursor(LookupTable)
    row = cursor.next()
    while row:
        arcpy.CreateFolder_management(DestinationFolder,row.getValue(ProviderNameField))
        finalDestination = os.path.join(DestinationFolder + "/" + row.getValue(ProviderNameField))
        copyText()
        row = cursor.next()


createFolder()