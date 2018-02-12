# ----------------------------------------------------------------------------
# Name: NTIAFinalFormat.py
# Created: Tues Jun 26 2012
# Updated: Fri Oct 26 2012
# Author: Kass Rezagholi
# ----------------------------------------------------------------------------
# Purpose:
#   This script reads through the Staging Area and appends data from each
#   feature class into a single geodatabase.  The resulting geodatabase contains
#   all provider data for delivery to the NTIA.  Use this final gdb to load data
#   into the NTIA data submission template.
#   Inputs:
#   	1. Staging Area Folder - path to folder that contains individual
#		provider geodatabases.  All gdbs must have the exact same data
#		schema.
#   	2. Final GDB Template - template of the exact same schema as the
#		provider gdbs. This gdb should have 5 feature classes:
#		"plss"
#		"wireless"
#		"midmile"
#   	3. Log File Location - Choose a folder location to store the log file.
#		This file contains important information regarding what data
#		was loaded and, more importantly, what data was not loaded.
#   Outputs:
#   	Final GDB Template - this will contain all of the provider data that
#   		was successfully appended, as recorded in the log file.
#-----------------------------------------------------------------------------
# Assumptions:
#   1. Working in ArcGIS 10.0 +
#   2. Each gdb (provider data and template gdb) has EXACT same data schema.
# ----------------------------------------------------------------------------

import sys, string, os, arcpy
##---------------------------------------------------------------------------Set Workspace
arcpy.env.workspace = arcpy.GetParameterAsText(0)
template_gdb = arcpy.GetParameterAsText(1)
logLocation = arcpy.GetParameterAsText(2)

plss_template = '%s\%s' % (template_gdb, "plss")
wireless_template = '%s\%s' % (template_gdb, "wireless")
midmile_template = '%s\%s' % (template_gdb, "midmile")


##---------------------------------------------------------------------------Create and Open log file

logPath = '%s\%s' % (logLocation,"log.txt")
logFile = open(logPath, 'w')

log_msg = '%s%s%s' % ("Log file location: ",logPath, logFile.name)
arcpy.AddMessage(log_msg)

def addWriteMessage(messageText):
	print messageText
	arcpy.AddMessage(messageText)
	logFile.write(messageText)
	logFile.write("\n")

##---------------------------------------------------------------------------Create list of all feature classes within all GDBs in workspace

masterList = []

workspaces = arcpy.ListWorkspaces("*", "FileGDB")

ws = ',\n'.join(workspaces)

ws_msg = '%s%s' % (len(workspaces)," gdbs in selected folder (Staging Area)")
addWriteMessage(ws_msg)
addWriteMessage(ws)

for item in workspaces:
	arcpy.env.workspace = item
	fcs = arcpy.ListFeatureClasses()
	for fc in fcs:
		fcStr = str(fc)
		outputL = '%s\%s' % (str(item), fcStr)
		masterList.append(outputL)

s = ',\n'.join(masterList)
mL_msg = '%s%s%s' % ("masterList has ",len(masterList)," feature classes")
addWriteMessage(mL_msg)

##---------------------------------------------------------------------------Create plss, wireless, and midmile lists from 'masterList'

plssList = []
wirelessList = []
midmileList = []
problemList = []

for object in masterList:
    if "plss" in object:
        plssPath = str(object)
        c_msg = '%s%s' % ("1 fc added to plssList: ",plssPath)
        addWriteMessage(c_msg)
        plssList.append(plssPath)

    elif "wireless" in object:
        wirelessPath = str(object)
        w_msg = '%s%s' % ("1 fc added to wirelessList: ",wirelessPath)
        addWriteMessage(w_msg)
        wirelessList.append(wirelessPath)
    elif "midmile" in object:
        midmilePath = str(object)
        m_msg = '%s%s' % ("1 fc added to midmileList: ",midmilePath)
        addWriteMessage(m_msg)
        midmileList.append(midmilePath)
    else:
        fail_msg = '%s%s' % ("NOT PROCESSED: ", object)
        featurePath = str(object)
        addWriteMessage(fail_msg)
        problemList.append(featurePath)

##---------------------------------------------------------------------------Append fcs from each list to its respective template fc

## Append features FUNCTION
def appendFeatures(featureList,featureTemplate,name):
	list = ','.join(featureList)
	listMsg = '%s%s%s%s' % (name,"List: ",len(featureList)," feature classes")
	addWriteMessage(listMsg)
	for fc in featureList:
		try:
			arcpy.Append_management(fc, featureTemplate, "TEST", "", "")
			result = arcpy.GetCount_management(fc)
			count = int(result.getOutput(0))
			toPrint = '%s%s%s%s%s' % (count," features loaded into ",name," from ",fc)
			addWriteMessage(toPrint)
		except:
			loadError = '%s%s%s' % (name," FEATURES DID NOT LOAD from ",fc)
			addWriteMessage(loadError)
			problemList.append(fc)
	featureResult = arcpy.GetCount_management(featureTemplate)
	featureCount = int(featureResult.getOutput(0))
	featureTotal = '%s%s%s' % (name," total: ",featureCount)
	addWriteMessage(featureTotal)


appendFeatures(plssList,plss_template,"plss")
appendFeatures(wirelessList,wireless_template,"wireless")
appendFeatures(midmileList,midmile_template,"midmile")


problems = ',\n'.join(problemList)
if len(problemList) > 0:
	probMsg = '%s%s' % ("Features not loaded: ",problems)
	addWriteMessage(probMsg)
else:
	addWriteMessage("All features were successfully loaded")

logFile.close()