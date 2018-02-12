# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Name:     OIT_SpeedTierV02.py
# Purpose:  To take the featureclasses
#           BB_Service_PLSS & BB_Service_Wireless and split them into
#           residential and commercial then create a
#           seperate feature class for Satellite, Wireline,
#           Wireless(Fixed), Mobile
# Author:   seiferdb
# Created:  2016-10-13 07:11:09.00000
# Copyright:(c) seiferdb 201
# ---------------------------------------------------------------------------
import gc
gc.enable()

import arcpy
from arcpy import env
import sys
import os
import string

###------------------------------------------------------------------------------Parameters
##myFolder =  (r'C:\Working\broadBandOnly\ScriptFixing\results_speedTier')    #Rename: FolderLocation
##myGDBtext = (r"TestTwo") #+ strftime("%d_%m_%y")
##plssOIT = (r'C:\Working\broadBandOnly\ScriptFixing\CO_BB_10_2016.gdb\OIT_Colorado_Broadband\BB_Service_PLSS')
##wirelessOIT =(r'C:\Working\broadBandOnly\ScriptFixing\CO_BB_10_2016.gdb\OIT_Colorado_Broadband\BB_Service_Wireless')
#------------------------------------------------------------------------------------------Getting the variables from the user
myFolder =  arcpy.GetParameterAsText(0)    #Rename: FolderLocation
myGDBtext = arcpy.GetParameterAsText(1) #+ strftime("%d_%m_%y")
plssOIT = arcpy.GetParameterAsText(2)
wirelessOIT = arcpy.GetParameterAsText(3)
arcpy.ResetEnvironments()
#-------------------------------------------------------------------------------------------Write Message
def writeMessage(messageText):
	print messageText
	arcpy.AddMessage(messageText)

#------------------------------------------------------------------------------------------Create Workspace
COBB = '%s\%s%s' % (myFolder, myGDBtext, ".gdb")
arcpy.env.workspace = COBB

#-----------------------------------------------------------------------------------------Get count of features in OIT feature classes no real reason, does give the user an idea of the time it might take
writeMessage("Get count of features in plss feature class")
result = int(arcpy.GetCount_management(plssOIT).getOutput(0))
writeMessage (result)

writeMessage("Get count of features in Wireless feature class")
result2 = int(arcpy.GetCount_management(wirelessOIT).getOutput(0))
writeMessage (result2)

arcpy.CreateFileGDB_management(myFolder, myGDBtext, "CURRENT")
writeMessage("File Geodatabase Created")

writeMessage("Starting the Variable Queue")

#------------------------------------------------------------------------------------------------ Local variables, provided by user:

BB_Service_PLSS = plssOIT
BB_Service_Wireless = wirelessOIT

writeMessage("...Prelim data Variables Queued up...")
writeMessage("Begin Geoprocessing Operation.... ")


                       # Process: Residential PLSS seperated from biz
arcpy.Select_analysis(BB_Service_PLSS, '%s\%s' % (COBB, "wrRes"), "EndUserCat In ( '1', '5')")
wrRes = '%s\%s' % (COBB,"wrRes")
writeMessage ("Made it past the first one...")#<--------------------------------------------------------------------------------------Code Checker
arcpy.Dissolve_management(wrRes, '%s\%s' % (COBB, "SpeedTier_Wireline_Residential"), "MAXADDOWN", "", "MULTI_PART", "DISSOLVE_LINES")
arcpy.Delete_management(wrRes, "")
writeMessage ("and another one...")#<-------------------------------------------------------------------------------------------------Code Checker

                        # Process: Wireless Biz, seperated from residential
arcpy.Select_analysis(BB_Service_Wireless, '%s\%s' % (COBB, "WirelessBiz"), "EndUserCat = '2'")
WirelessBiz ='%s\%s' % (COBB, "WirelessBiz")

writeMessage ("...and here comes one more... Wireless Commercial seperated out...")#<------------------------------------------------------------Code Checker

                        # Process: Wireless Fixed Commercial
arcpy.Select_analysis(WirelessBiz, '%s\%s' % (COBB, "wlcFixed"), "TRANSTECH in ( 70, 71)")
wlcFixed = '%s\%s' % (COBB, "wlcFixed")
arcpy.Dissolve_management(wlcFixed, '%s\%s' % (COBB, "SpeedTier_Fixed_Commercial"), "MAXADDOWN", "", "MULTI_PART", "DISSOLVE_LINES")
arcpy.Delete_management(wlcFixed, "")
writeMessage("Serveral on the way now.... Just finished Fixed Commercial Wireless...")#<----------------------------------------------Code Checker


arcpy.Select_analysis(BB_Service_PLSS, '%s\%s' % (COBB, "wrBiz"), "EndUserCat = '2'")
wrBiz = '%s\%s' % (COBB, "wrBiz")
arcpy.Dissolve_management(wrBiz, '%s\%s' % (COBB, "SpeedTier_Wireline_Commercial"), "MAXADDOWN", "", "MULTI_PART", "DISSOLVE_LINES")
arcpy.Delete_management(wrBiz, "")
writeMessage("And here is the last plss feature class...")#<---------------------------------------------------------------------------Code Checker

arcpy.Select_analysis(BB_Service_Wireless, '%s\%s' % (COBB, "wirelessRes"), "ENDUSERCAT IN( '1' , '5' )")
wirelessRes = '%s\%s' % (COBB, "wirelessRes")


#--------------------------------------------------------------------------------------------------------------------------------------Wireless fixed
arcpy.Select_analysis(wirelessRes, '%s\%s' % (COBB, "wlFixed"), "TRANSTECH in ( 70, 71)")
wlFixed = '%s\%s' % (COBB, "wlFixed")
arcpy.Dissolve_management(wlFixed, '%s\%s' % (COBB, "SpeedTier_Fixed_Residential"), "MAXADDOWN", "", "MULTI_PART", "DISSOLVE_LINES")
arcpy.Delete_management(wlFixed, "")

#--------------------------------------------------------------------------------------------------------------------------------------Wireless satellite Commercial
arcpy.Select_analysis(WirelessBiz, '%s\%s' % (COBB, "wlcSat"), "TRANSTECH = 60")
wlcSat = '%s\%s' % (COBB, "wlcSat")
arcpy.Dissolve_management(wlcSat, '%s\%s' % (COBB, "SpeedTier_Satellite_Commercial"), "MAXADDOWN", "", "MULTI_PART", "DISSOLVE_LINES")
arcpy.Delete_management(wlcSat, "")

#--------------------------------------------------------------------------------------------------------------------------------------Wireless satellite residential
arcpy.Select_analysis(wirelessRes, '%s\%s' % (COBB, "wlSat"), "TRANSTECH = 60")
wlSat = '%s\%s' % (COBB, "wlSat")
arcpy.Dissolve_management(wlSat, '%s\%s' % (COBB, "SpeedTier_Satellite_Residential"), "MAXADDOWN", "", "MULTI_PART", "DISSOLVE_LINES")
arcpy.Delete_management(wlSat, "")

#--------------------------------------------------------------------------------------------------------------------------------------Wireless Mobile - only one no commercial mobile
arcpy.Select_analysis(wirelessRes, '%s\%s' % (COBB, "wlMobile"), "TRANSTECH = 80")
wlMobile = '%s\%s' % (COBB, "wlMobile")
arcpy.Dissolve_management(wlMobile, '%s\%s' % (COBB, "SpeedTier_Mobile_Residential"), "MAXADDOWN", "", "MULTI_PART", "DISSOLVE_LINES")

#------------------------------------------------------------------------------------------------------------------------------------------ Adding the last field -'DownSpeedTier' - the integers - for all feature classes
writeMessage("The DownSpeedTier field is being added to all feature classes....Please standby....")

arcpy.env.workspace = COBB
arcpy.AddField_management("SpeedTier_Fixed_Commercial", "DownSpeedTier", "SHORT" )
arcpy.CalculateField_management("SpeedTier_Fixed_Commercial", "DownSpeedTier","[MAXADDOWN]")

arcpy.env.workspace = COBB
arcpy.AddField_management("SpeedTier_Fixed_Residential", "DownSpeedTier", "SHORT" )
arcpy.CalculateField_management("SpeedTier_Fixed_Residential", "DownSpeedTier", "[MAXADDOWN]")

arcpy.env.workspace = COBB
arcpy.AddField_management("SpeedTier_Mobile_Residential", "DownSpeedTier", "SHORT" )
arcpy.CalculateField_management("SpeedTier_Mobile_Residential", "DownSpeedTier", "[MAXADDOWN]")

arcpy.env.workspace = COBB
arcpy.AddField_management("SpeedTier_Satellite_Commercial", "DownSpeedTier", "SHORT" )
arcpy.CalculateField_management("SpeedTier_Satellite_Commercial", "DownSpeedTier", "[MAXADDOWN]")

arcpy.env.workspace = COBB
arcpy.AddField_management("SpeedTier_Satellite_Residential", "DownSpeedTier", "SHORT" )
arcpy.CalculateField_management("SpeedTier_Satellite_Residential", "DownSpeedTier", "[MAXADDOWN]")

arcpy.env.workspace = COBB
arcpy.AddField_management("SpeedTier_Wireline_Commercial", "DownSpeedTier", "SHORT" )
arcpy.CalculateField_management("SpeedTier_Wireline_Commercial", "DownSpeedTier", "[MAXADDOWN]")

arcpy.env.workspace = COBB
arcpy.AddField_management("SpeedTier_Wireline_Residential", "DownSpeedTier", "SHORT" )
arcpy.CalculateField_management("SpeedTier_Wireline_Residential", "DownSpeedTier", "[MAXADDOWN]")

writeMessage("Almost done... Tidying the place up ....")#<---------------------------------------------------------------------------Code Checker
arcpy.Delete_management(wlMobile, "")
arcpy.Delete_management(WirelessBiz, "")
arcpy.Delete_management(wirelessRes, "")
writeMessage("Ha! Done . . .")
