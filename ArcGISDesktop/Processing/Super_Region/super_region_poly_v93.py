# Name: super_region_poly_v93.py
#
# Description
# -----------
# This script will take a polygon featureclass that contains overlapping polygons and build a
# planarized feature class (with no overlapping polygons) and a one-to-many look up table. This
# is useful for including polygon feature classes with overlapping features in a spatial overlay
# operation such as a union. Optionally you can calculate a MIN, MAX, SUM, or MEAN statistic for any
# numeric field in the inputFC and propogate it to the output featureclass (for example, the MIN
# "YEAR" value of the overlapping features).  
#
# Written By: Chris Snyder, WA DNR, 03/09/2008, chris.snyder(at)wadnr.gov
#
# Written For: Python 2.5.1 and ArcGIS v9.3.1 SP0
#
# UPDATES:
# 20091207 - Added an error check preventing the planarizedFC and lookupTbl from having the same name
#            if planarizedFC is a shapefile and lookupTbl and they are in the same workspace.
# 20091203 - The gp object now uses the v9.3 creation parameter (and made the neccessary changes)  
# 20091203 - The "," symbol for decimal places (European) should now be supported
# 20091102 - Added the SUM option as a summary statistic
# 20090603 - The polyIdDic dictionary is now keyed by a 3 item tuple instead of 1 big text string
# 20090415 - NULL values are now ignored in the statistic calculation
# 20090315 - Added the ability to generate a summary statistic 
#
# Notes on input parameters (for the toolbox):
# VARIABLE             PAREMETER_INDEX     PARAMETER_DATA_TYPE
# -------------------------------------------------------------------
# inputFC              0                   Feature Layer (the input FL)
# planarizedFC         1                   Feature Class (the output FC)
# lookupTbl            2                   Table (the output look up table)
# xyTolerance          3                   Linear Unit (the tolerace used to break the linework of the inputFC)
# polyIdFieldName      4                   String (the name of the new polyId field
# ovlpCountFieldName   5                   String (the name of the new ovlpCount field)
# statField            6                   String (a nummeric field in the inputFC)
# statType             7                   String (SUM, MAX, MEAN, or MIN statistic)
# decimalTolerance     8                   Short Integer (the decimal precision used when looking for overlapping polygons)

#Process: Import system modules and creates the Geoprocessor object
try:
    #Import system modules and create the Geoprocessor object the v9.3 way
    import sys, string, os, time, traceback, arcgisscripting 
    gp = arcgisscripting.create(9.3)
       
    #Defines some functions used for getting messages to the log file and ArcToolbox GUI
    def showGpMessage():
        gp.AddMessage(gp.GetMessages())
        print >> open(logFile, 'a'), gp.GetMessages()
        print gp.GetMessages()
    def showGpWarning():
        gp.AddWarning(gp.GetMessages())
        print >> open(logFile, 'a'), gp.GetMessages()
        print gp.GetMessages()
    def showGpError():
        gp.AddError(gp.GetMessages())
        print >> open(logFile, 'a'), gp.GetMessages()
        print gp.GetMessages()
    def showPyMessage():
        gp.AddMessage(str(time.ctime()) + " - " + message)
        print >> open(logFile, 'a'), str(time.ctime()) + " - " + message
        print str(time.ctime()) + " - " + message
    def showPyWarning():
        gp.AddWarning(str(time.ctime()) + " - " + message)
        print >> open(logFile, 'a'), str(time.ctime()) + " - " + message
        print str(time.ctime()) + " - " + message
    def showPyError():
        gp.AddError(str(time.ctime()) + " - " + message)
        print >> open(logFile, 'a'), str(time.ctime()) + " - " + message
        print str(time.ctime()) + " - " + message

    #Specifies the root directory variable, defines the logFile variable, and does some minor error checking...
    dateTimeString = str(time.strftime('%Y%m%d%H%M%S'))
    scriptName = os.path.split(sys.argv[0])[-1].split(".")[0]
    userName = string.lower(os.environ.get("USERNAME")).replace(" ","_").replace(".","_")
    tempPathDir = os.environ["TEMP"]
    logFileDirectory = r"\\snarf\am\div_lm\ds\gis\tools\log_files"
    if os.path.exists(logFileDirectory) == True:
        logFile = os.path.join(logFileDirectory, scriptName + "_" + userName + "_" + dateTimeString + ".txt")
        try:
            print >> open(logFile, 'a'), "Write test successfull!"
        except:
            logFile = os.path.join(tempPathDir, scriptName + "_" + userName + "_" + dateTimeString + ".txt")  
    else:
        logFile = os.path.join(tempPathDir, scriptName + "_" + userName + "_" + dateTimeString + ".txt")
    if os.path.exists(logFile)== True:
        os.remove(logFile)
        message = "Created log file " + logFile; showPyMessage()
    message = "Running " + sys.argv[0]; showPyMessage()
    
    #Process: Attempts to check out the lowest grade license available...
    try:
        if gp.CheckProduct("ArcView") == "Available":
            gp.SetProduct("ArcView")
        elif gp.CheckProduct("ArcEditor") == "Available":
            gp.SetProduct("ArcEditor")
        elif gp.CheckProduct("ArcInfo") == "Available":
            gp.SetProduct("ArcInfo")
    except:
        message = "ERROR: Could not select an ArcGIS license level! Exiting script..."; showPyError(); sys.exit()
    message =  "Selected an " + gp.ProductInfo() + " license"; showPyMessage()

    #Process: Make sure we can overwrite outputs
    gp.overwriteoutput = True
    message = "Overwrite Output: Enabled..."; showPyMessage()
    
    message = "Starting geoprocessing routine..." + "\n"; showPyMessage()
    #*****************GEOPROCESSING STUFF GOES HERE******************************

    #Process: Defines the input parameters 
    inputFC = gp.GetParameterAsText(0)
    planarizedFC = gp.GetParameterAsText(1)
    lookupTbl = gp.GetParameterAsText(2)
    xyTolerance = gp.GetParameterAsText(3)
    polyIdFieldName = gp.GetParameterAsText(4)
    ovlpCountFieldName = gp.GetParameterAsText(5)
    statFieldName = gp.GetParameterAsText(6)
    statType = gp.GetParameterAsText(7)
    decimalTolerance = gp.GetParameterAsText(8)

    #Process: Print out the input parameters
    message = "INPUT PARAMETERS"; showPyMessage()
    message = "----------------"; showPyMessage()
    message = "Input Layer              = " + inputFC; showPyMessage()
    message = "Output Featureclass      = " + planarizedFC; showPyMessage()
    message = "Output Lookup Table      = " + lookupTbl; showPyMessage()
    message = "XY Tolerance             = " + xyTolerance; showPyMessage()
    message = "Polygon ID Field Name    = " + polyIdFieldName; showPyMessage()
    message = "Overlap Count Field Name = " + ovlpCountFieldName; showPyMessage()
    message = "Statistic Field Name     = " + statFieldName; showPyMessage()
    message = "Statistic Type           = " + statType; showPyMessage()
    message = "Decimal Tolerance        = " + decimalTolerance + "\n"; showPyMessage()

    message = "Running error checks..."; showPyMessage()    

    #Process: Makes sure inputFC exists
    if gp.exists(inputFC) == False:
        message = "ERROR: " + inputFC + " does not exist! Exiting script..."; showPyError(); sys.exit()

    #Process: Makes sure inputFC is a polygon layer
    dsc = gp.describe(inputFC)
    if dsc.shapetype != "Polygon":
        message = "ERROR: " + inputFC + " must be a polygon layer! Exiting script..."; showPyError(); sys.exit()
        
    #Process: Makes sure the 'polyIdFieldName' and 'ovlpCountFieldName' fields don't already exist in inputFC
    if gp.listfields(inputFC, polyIdFieldName) != [] and gp.listfields(inputFC, ovlpCountFieldName) != []:
        message = "ERROR: " + inputFC + " already contains a " + polyIdFieldName + " and/or " + ovlpCountFieldName + " field - Delete these fields and try again! Exiting script..."; showPyError(); sys.exit()

    #Process: Makes sure planarizedFC and lookupTbl are not named the same thing
    if planarizedFC == lookupTbl:
        message = "ERROR: " + planarizedFC + " and " + lookupTbl + " can't have the same file path - Give one of them a different name!  Exiting script..."; showPyError(); sys.exit()

    #Process: Makes sure the statType is valid
    if statType not in ("","#","MAX","MIN","MEAN","SUM"):
        message = "ERROR: Specified statistic type " + str(statType) + " is invalid!  Exiting script..."; showPyError(); sys.exit()

    #Process: Makes sure both the statType and statField are specified (if only one of them is, then error)
    if statType in ("MAX","MIN","MEAN","SUM") and statFieldName in ("","#"):
        message = "ERROR: You must also specify a statistic field! Exiting script..."; showPyError(); sys.exit()
    if statType in ("","#") and statFieldName not in ("","#"):
        message = "ERROR: You must also specify a statistic type! Exiting script..."; showPyError(); sys.exit()

    #Process: Makes sure statField is a numeric field
    if statFieldName not in ("","#"):
        fieldList = gp.listfields(inputFC, statFieldName)
        statFieldType = fieldList[0].type        
        if statFieldType not in ["Integer","SmallInteger","Double","Single","OID"]:
            message = "ERROR: Specified statistic field (" + str(statFieldName) + " - " + str(statFieldType) + ") is not a numeric field!  Exiting script..."; showPyError(); sys.exit()

    #Process: Makes sure decimalTolerance is an acceptable value
    if decimalTolerance not in ("","#") and int(decimalTolerance) not in range(0,17):
            message = "ERROR: Invalid decimal tolerance (must be in range 0 - 16)! Exiting script..."; showPyError(); sys.exit()

    #Process: Makes sure planarizedFC and lookupTbl don't have the same name if planarizedFC
    #is a shapefile and lookupTbl is a .dbf and they are in the same workspace
    if planarizedFC.endswith(".shp") and lookupTbl.endswith(".dbf") and planarizedFC.partition(".shp")[0] == lookupTbl.partition(".dbf")[0]:
        message = "ERROR: Shapefile " + str(planarizedFC) + " and .dbf table " + str(lookupTbl) + " must have different file names if they are to be stored in the same workspace! Exiting script..."; showPyError(); sys.exit()

    message = "Error checks complete!"; showPyMessage()

    #Process: Makes sure the optional parameters get set to their default values if not specified
    if xyTolerance in ["","#"]:
        xyTolerance = ""
    if polyIdFieldName in ["","#"]:
        polyIdFieldName = "POLY_ID"
    if ovlpCountFieldName in ["","#"]:
        ovlpCountFieldName = "OVLP_COUNT"
    if statFieldName in ["","#"]:
        stateFieldName = ""
    if statType in ["","#"]:
        statType = ""
    if decimalTolerance in ["","#"]:
        decimalTolerance = 16

    #Process: Defines the names of some processing layers and other variables
    shatteredFC = "in_memory\\shattered"
    singlePartFC = "in_memory\\single_part"
    statFieldNameTemp = "XOXOXOXOXO"

    #Process: Makes a feature layer out inputFC (ensures the union won't bomb on account of the inputFC name having spaces and what not...
    gp.MakeFeatureLayer_management(inputFC, "fl", "")

    #Process: Union "fl" with itself
    message = "Shattering " + inputFC + "..."; showPyMessage()
    gp.Union_analysis("fl", shatteredFC, "ALL", xyTolerance, "GAPS")
    
    #Process: Adds 'polyIdFieldName' and 'ovlpCountFieldName' to shatteredFC
    gp.AddField_management(shatteredFC, polyIdFieldName, "LONG")
    gp.AddField_management(shatteredFC, ovlpCountFieldName, "LONG")
    if statType != "":
        if statType == "MEAN":
            gp.AddField_management(shatteredFC, statFieldNameTemp, "DOUBLE")
        elif statType in ("MAX","MIN","SUM") and statFieldType in ("Integer","SmallInteger","OID"):
            gp.AddField_management(shatteredFC, statFieldNameTemp, "LONG")
        elif statType in ("MAX","MIN","SUM") and statFieldType in ("Single","Double"):
            gp.AddField_management(shatteredFC, statFieldNameTemp, "DOUBLE")
        else:
            message = "ERROR: Can't establish field type of " + str(statFieldName) + "! Exiting script..."; showPyError(); sys.exit()
            
    #Process: Breaks shatteredFC into single part features
    message = "Breaking into singlepart shapes..."; showPyMessage()
    try:
        gp.MultipartToSinglepart_management(shatteredFC, singlePartFC)
    except:
        message = "ERROR: Unable to break into singlepart shapes (see gp error message below)! Exiting script..."; showPyError(); sys.exit()

    #Process: Delete in_memory\\shattered
    gp.Delete_management(shatteredFC, "FeatureClass")        
    
    #Process: Populates 'polyIdFieldName' and 'ovlpCountFieldName' and 'statFieldName'
    message = "Searching for overlapping features..."; showPyMessage()
    shapeFieldName = gp.describe(singlePartFC).shapefieldname
    polyIdDict = {}
    polyIdValue = 1
    ovlpCount = 1
    searchRows = gp.searchcursor(singlePartFC)
    searchRow = searchRows.next()
    while searchRow:
        shapeFieldValue = searchRow.getvalue(shapeFieldName)
        xCentroidValue = round(float(str(shapeFieldValue.centroid.x).replace(",",".")), int(decimalTolerance)) #comma replacement is for our European friends
        yCentroidValue = round(float(str(shapeFieldValue.centroid.y).replace(",",".")), int(decimalTolerance))
        areaValue = round(float(str(shapeFieldValue.area).replace(",",".")), int(decimalTolerance))
        axyValue = (xCentroidValue,yCentroidValue,areaValue)
        if statFieldName != "":
            statFieldValue = searchRow.getvalue(statFieldName)
        if axyValue in polyIdDict:
            polyIdDict[axyValue][1] = polyIdDict[axyValue][1] + 1
            if statFieldName != "" and statFieldValue != None:
                polyIdDict[axyValue][2].append(statFieldValue)
        else:
            if statFieldName != "" and statFieldValue == None:
                polyIdDict[axyValue] = [polyIdValue,ovlpCount,[]]
            elif statFieldName != "" and statFieldValue != None:
                polyIdDict[axyValue] = [polyIdValue,ovlpCount,[statFieldValue]]
            else:
                polyIdDict[axyValue] = [polyIdValue,ovlpCount]
            polyIdValue = polyIdValue + 1    
        searchRow = searchRows.next()
    del searchRow
    del searchRows
    message = "Populating summary fields..."; showPyMessage()
    updateRows = gp.updatecursor(singlePartFC)
    updateRow = updateRows.next()
    while updateRow:
        shapeFieldValue = updateRow.getvalue(shapeFieldName)
        xCentroidValue = round(float(str(shapeFieldValue.centroid.x).replace(",",".")), int(decimalTolerance)) #comma replacement is for our European friends
        yCentroidValue = round(float(str(shapeFieldValue.centroid.y).replace(",",".")), int(decimalTolerance))
        areaValue = round(float(str(shapeFieldValue.area).replace(",",".")), int(decimalTolerance))
        axyValue = (xCentroidValue,yCentroidValue,areaValue)
        updateRow.SetValue(polyIdFieldName, polyIdDict[axyValue][0])
        updateRow.SetValue(ovlpCountFieldName, polyIdDict[axyValue][1])
        if statFieldName != "":
            if len(polyIdDict[axyValue][2]) == 0: #If there are no values to summarize (e.g. they were all NULL values)
                pass #don't do anything
            else:
                if statType == "MAX":
                    polyIdDict[axyValue][2].sort(None,None,True)
                    updateRow.SetValue(statFieldNameTemp, polyIdDict[axyValue][2][0])
                elif statType == "MIN":
                    polyIdDict[axyValue][2].sort()
                    updateRow.SetValue(statFieldNameTemp, polyIdDict[axyValue][2][0])
                elif statType == "SUM":
                    itemSum = 0
                    for item in polyIdDict[axyValue][2]:
                        itemSum = itemSum + item
                    updateRow.SetValue(statFieldNameTemp, itemSum)
                elif statType == "MEAN":
                    itemCount = len(polyIdDict[axyValue][2])
                    itemSum = 0
                    for item in polyIdDict[axyValue][2]:
                        itemSum = itemSum + item
                    updateRow.SetValue(statFieldNameTemp, itemSum / float(itemCount))
        updateRows.UpdateRow(updateRow)
        updateRow = updateRows.next()
    del updateRow
    del updateRows
    del polyIdDict
    
    #Process: Dissolves singlePartFC
    message = "Creating planarized output..."; showPyMessage()
    if statFieldName == "":
        gp.Dissolve_management(singlePartFC, planarizedFC, polyIdFieldName + ";" + ovlpCountFieldName, "", "SINGLE_PART")
    else:
        gp.Dissolve_management(singlePartFC, planarizedFC, polyIdFieldName + ";" + ovlpCountFieldName + ";" + statFieldNameTemp, "", "SINGLE_PART")
        if statType != "":
            if statType == "MEAN":
                gp.AddField_management(planarizedFC, statFieldName, "DOUBLE") #who needs single precision float fields anyway?
            elif statType in ["MAX","MIN","SUM"] and statFieldType in ["Integer","SmallInteger","OID"]:
                gp.AddField_management(planarizedFC, statFieldName, "LONG")
            elif statType in ["MAX","MIN","SUM"] and statFieldType not in ["Integer","SmallInteger","OID"]:
                gp.AddField_management(planarizedFC, statFieldName, "DOUBLE")
            else:
                message = "ERROR: Can't establish field type of " + str(statFieldName) + " field! Exiting script..."; showPyError(); sys.exit()
        #This cursor is needed to preserve the NULL values, a normal calc converts them to 0s for some reason.
        updateRows = gp.updatecursor(planarizedFC)
        updateRow = updateRows.next()
        while updateRow:
            stateFieldNameTempValue = updateRow.getvalue(statFieldNameTemp)
            if stateFieldNameTempValue == None:
                pass
            else:
                updateRow.setvalue(statFieldName, stateFieldNameTempValue)
                updateRows.UpdateRow(updateRow)
            updateRow = updateRows.next()
        del updateRow
        del updateRows
        gp.DeleteField_management(planarizedFC, statFieldNameTemp) 

    #Process: Creates lookupTbl
    message = "Creating lookup table..."; showPyMessage() 
    gp.CopyRows_management(singlePartFC, lookupTbl, "")
    
    #Process: Deletes in_memory\\single_part
    gp.Delete_management(singlePartFC, "FeatureClass")

    #Process: Figures out how many areas of overlapping features there are
    gp.MakeFeatureLayer_management(planarizedFC, "fl", ovlpCountFieldName + " > 1")
    dupCount = int(gp.GetCount_management("fl").getoutput(0))

    #Process: Gives a final report
    message = "REGION POLY REPORT:"; showPyWarning()
    message = "-------------------"; showPyWarning()
    message = "Detected " + str(dupCount) + " areas of overlapping features."; showPyWarning()
    message = "Planarized output: " + planarizedFC; showPyWarning()
    message = "Lookup table: " + lookupTbl +"\n"; showPyWarning()
        
    #*****************GEOPROCESSING STUFF ENDS HERE******************************
    message = "Ending geoprocessing routine..."; showPyMessage()

    #Indicates that the script is complete
    message = str(sys.argv[0]) + " is all done!"; showPyMessage()

except:
    message = "\n*** LAST GEOPROCESSOR MESSAGE (may not be source of the error)***"; showPyError()
    showGpMessage()
    message = "PYTHON TRACEBACK INFO: " + traceback.format_tb(sys.exc_info()[2])[0]; showPyError()
    message = "PYTHON ERROR INFO: " +  str(sys.exc_type)+ ": " + str(sys.exc_value) + "\n"; showPyError()
message = "\n*** PYTHON LOCAL VARIABLE LIST ***"; print >> open(logFile, 'a'), str(time.ctime()) + " - " + message #don't print this mess to ArcToolbox (just the logFile)!
variableCounter = 0                      
while variableCounter < len(locals()):
    message =  str(list(locals())[variableCounter]) + " = " + str(locals()[list(locals())[variableCounter]]); print >> open(logFile, 'a'), str(time.ctime()) + " - " + message #don't print this mess to ArcToolbox (just the logFile)!
    variableCounter = variableCounter + 1
