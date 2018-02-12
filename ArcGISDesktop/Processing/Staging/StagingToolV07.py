# ---------------------------------------------------------------------------
# StagingToolV07.py
# Created on: 2012-10-22 15:39:10.00000
#   (generated by ArcGIS/ModelBuilder)
# Usage: Takes processed GDB's and puts them in a standard format in the Staging Area
# Description: The tool has multiple steps:
#   1. Creates a File geodatabase in appropriate workspace path
#   2. Creates new feature class with staging template and appends processed corresponding feature class
#   3. Takes new feature class and runs through a Look-Up table to populate ProvName, DBName, FRN, ProviderType, and EndUserCat where appropriate
#   4.

# Edits from version 6 - Tom McKean - Added 'if statements' for TYPICUP and TYPICDOWN to populate fields based on given values.
# ---------------------------------------------------------------------------

# Import arcpy module
import arcpy, os, string

# Set Input Datasets
FolderLocation = arcpy.GetParameterAsText(0)

myGDBtext = arcpy.GetParameterAsText(1)
censusInput = arcpy.GetParameterAsText(2)
roadsInput = arcpy.GetParameterAsText(3)
midmileInput = arcpy.GetParameterAsText(4)
wirelessInput = arcpy.GetParameterAsText(5)
addressInput = arcpy.GetParameterAsText(6)

myGDB = '%s\%s%s' % (FolderLocation, myGDBtext, ".gdb")
arcpy.env.workspace = myGDB

# Expression
analystName = arcpy.GetParameterAsText(7)
analyst1 = analystName.encode('utf-8')
analyst = '"%s"' %(analyst1)



# Lookup Table Path
lookup = r"P:\SBDDGP-ARRA Project\BroadbandProductionArea\Workspaces\BaseData\lookup.gdb\lookup"


census = '%s\%s' % (myGDB, "census")
roads = '%s\%s' % (myGDB, "roads")
wireless = '%s\%s' % (myGDB, "wireless")
midmile = '%s\%s' % (myGDB, "midmile")
address = '%s\%s' % (myGDB, "address")


# Process: Create File GDB
arcpy.CreateFileGDB_management(FolderLocation, myGDBtext, "CURRENT")
arcpy.env.overwriteOutput = True
arcpy.AddMessage("File GDB created")

if censusInput <>"":
    #
    #   Census
    #

    arcpy.AddMessage("Start Census Processing")
    arcpy.CreateFeatureclass_management(myGDB, "census", "POLYGON", "P:\\SBDDGP-ARRA Project\\BroadbandProductionArea\\Workspaces\\BaseData\\StagingTemplate.gdb\\census", "DISABLED", "DISABLED", "GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]];-400 -400 1000000000;-100000 10000;-100000 10000;8.98315284119521E-09;0.001;0.001;IsHighPrecision", "", "0", "0", "0")
    arcpy.AddMessage("Feature Class Created")

    arcpy.Append_management(censusInput, census, "NO_TEST", "", "")
    arcpy.AddMessage("Census Append Complete")

    # Process: Calculate Fields
    arcpy.CalculateField_management(census, "STATEFIPS", "\"08\"", "VB", "")
    arcpy.CalculateField_management(census, "COUNTYFIPS", "mid ( [FULLFIPSID],3,3 )", "VB", "")
    arcpy.CalculateField_management(census, "TRACT", "mid ( [FULLFIPSID],6,6)", "VB", "")
    arcpy.CalculateField_management(census, "BLOCKID", "right ( [FULLFIPSID],4)", "VB", "")
    arcpy.AddMessage("Calculation FIPS complete")
    arcpy.AddField_management(census, "WHO", "TEXT", "", "", "10", "", "NULLABLE", "NON_REQUIRED", "")
    arcpy.AddMessage("Add Field WHO")
    arcpy.CalculateField_management(census, "WHO", analyst, "VB", "")
    arcpy.AddMessage("Add field WHEN")
    arcpy.AddField_management(census, "WHEN", "DATE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
    arcpy.CalculateField_management(census, "WHEN", "Date (  )", "VB", "")


    # Create list of ProvAlias found in Provider data
    provListRows = arcpy.UpdateCursor(census, "", "", "PROVALIAS; PROVNAME; DBNAME; FRN", "")
    provListRow = provListRows.next()
    provaliasList = []

    arcpy.AddMessage("checking PROVALIAS,TYPICUP,TYPICDOWN")
    for provListRow in provListRows:
        #print "provalias: %s, provname: %s, dbaname: %s, frn: %s, typicup: %s, typicdown: %s" % \
        #    (provListRow.PROVALIAS, provListRow.PROVNAME, provListRow.DBNAME, provListRow.FRN,provListRow.TYPICUP, provListRow.TYPICDOWN)
        if provListRow.PROVALIAS not in provaliasList:
            provaliasList.append(provListRow.PROVALIAS)
            print provListRow.PROVALIAS," added to provaliasList"
        if provListRow.TYPICUP not in provaliasList:
            provaliasList.append(provListRow.TYPICUP)
            print provListRow.TYPICUP, " added to provaliasList"
        if provListRow.TYPICDOWN not in provaliasList:
            provaliasList.append(provListRow.TYPICDOWN)
    rows = arcpy.UpdateCursor(census, "", "", "PROVALIAS; PROVNAME; DBNAME; FRN; ENDUSERCAT; PROVIDER_TYPE; TYPICUP; TYPICDOWN", "")
    row = rows.next()
    arcpy.AddMessage("Populating Census data")
    while row:
        if row.getValue('TYPICUP') in provaliasList:
            tempTYUP = row.getValue('TYPICUP')
            if tempTYUP is None:
                #print "temTYUP is Null"
                row.setValue('TYPICUP', "ZZ")
                #print "Set TYPICUP value to ZZ"
            elif tempTYUP == "ZZ":
                print "TYPICUP value already set to ZZ"
            else:
                print "TYPICUP value: " + tempTYUP
        else:
            print "Error with TYPICUP"

        if row.getValue('TYPICDOWN') in provaliasList:
            tempTYDO = row.getValue('TYPICDOWN')
            if tempTYDO is None:
                #print "temTYUP is Null"
                row.setValue('TYPICDOWN', "ZZ")
                #print "Set TYPICDOWN value to ZZ"
            elif tempTYDO == "ZZ":
                print "TYPICDOWN value already set to ZZ"
            else:
                print "TYPICDOWN value: " + tempTYDO
        else:
            print "Error with TYPICDOWN"

        if row.getValue('PROVALIAS') in provaliasList:
            tempProv = row.getValue('PROVALIAS')
            #print "tempProv=" + tempProv
            dataEndUser = row.getValue('ENDUSERCAT')
            dataProvType = row.getValue('PROVIDER_TYPE')

            lookupRows = arcpy.UpdateCursor(lookup, "", "", "PROVALIAS; PROVNAME; DBNAME; FRN; ENDUSERCAT; PROVIDER_TYPE", "")
            lookupRow = lookupRows.next()
            while lookupRow:
                lookupProv = lookupRow.getValue('PROVALIAS')
                if lookupProv == tempProv:
                    #print "match", lookupProv
                    lName = lookupRow.getValue('PROVNAME')
                    #print "ProvName: ", lName
                    lDBA = lookupRow.getValue('DBNAME')
                    #print "DBA Name: ", lDBA
                    lFRN = lookupRow.getValue('FRN')
                    #print "FRN: ", lFRN
                    row.setValue('PROVNAME', lName)
                    row.setValue('DBNAME', lDBA)
                    row.setValue('FRN', lFRN)
                    lEndUser = lookupRow.getValue('ENDUSERCAT')
                    #print "ENDUSERCAT: ", lEndUser
                    lType = lookupRow.getValue('PROVIDER_TYPE')
                    #print "PROVIDER_TYPE: ", lType
                    if dataEndUser is None:
                        row.setValue('ENDUSERCAT', lEndUser)
                        print "enduser populated"
                    else:
                        print "enduser already exists: ", dataEndUser
                    if dataProvType is None:
                        row.setValue('PROVIDER_TYPE', lType)
                        print "type populated"
                    else:
                        print "type already exists: ", dataProvType

                lookupRows.updateRow(lookupRow)
                lookupRow = lookupRows.next()
            del lookupRow, lookupRows
        else:
            #print "error"
            row.setValue('PROVNAME', "no match")
        rows.updateRow(row)
        row = rows.next()

    # Delete Fields
    del row, rows
    print "finished"
    arcpy.AddMessage("Census Finished")

if roadsInput <> "":

    #
    #   ROADS TO STAGING PROCESS
    #
    arcpy.AddMessage("Starting Roads Processing")
    #print "Starting Roads Processing"
    arcpy.CreateFeatureclass_management(myGDB, "roads", "POLYLINE", "P:\\SBDDGP-ARRA Project\\BroadbandProductionArea\\Workspaces\\BaseData\\StagingTemplate.gdb\\roads", "DISABLED", "DISABLED", "GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]];-400 -400 1000000000;-100000 10000;-100000 10000;8.98315284119521E-09;0.001;0.001;IsHighPrecision", "", "0", "0", "0")
    arcpy.AddMessage("Feature Class Created")

    # Process: Append (2)
    arcpy.Append_management(roadsInput, roads, "NO_TEST", "", "")
    print "Roads Appended"

    # Process: Calculate Field
    arcpy.CalculateField_management(roads, "STATECODE", "\"CO\"", "VB", "")
    arcpy.AddField_management(roads, "WHO", "TEXT", "", "", "10", "", "NULLABLE", "NON_REQUIRED", "")
    arcpy.CalculateField_management(roads, "WHO", analyst, "VB", "")
    print "WHO Field Added"
    arcpy.AddField_management(roads, "WHEN", "DATE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
    arcpy.CalculateField_management(roads, "WHEN", "Date (  )", "VB", "")
    print "WHEN field added"

    # Create list of ProvAlias found in Provider data
    provListRows = arcpy.UpdateCursor(roads, "", "", "PROVALIAS; PROVNAME; DBNAME; FRN", "")
    provListRow = provListRows.next()
    provaliasList = []

    for provListRow in provListRows:
        print "provalias: %s, provname: %s, dbaname: %s, frn: %s, typicup: %s, typicdown: %s" % \
            (provListRow.PROVALIAS, provListRow.PROVNAME, provListRow.DBNAME, provListRow.FRN, provListRow.TYPICUP, provListRow.TYPICDOWN)
        if provListRow.PROVALIAS not in provaliasList:
            provaliasList.append(provListRow.PROVALIAS)
        if provListRow.TYPICUP not in provaliasList:
            provaliasList.append(provListRow.TYPICUP)
            print provListRow.TYPICUP, " added to provaliasList"
        if provListRow.TYPICDOWN not in provaliasList:
            provaliasList.append(provListRow.TYPICDOWN)
            print provListRow.PROVALIAS," added to provaliasList"
    rows = arcpy.UpdateCursor(roads, "", "", "PROVALIAS; PROVNAME; DBNAME; FRN; ENDUSERCAT; PROVIDER_TYPE; TYPICUP; TYPICDOWN", "")
    row = rows.next()
    while row:
        if row.getValue('TYPICUP') in provaliasList:
            tempTYUP = row.getValue('TYPICUP')
            if tempTYUP is None:
                print "temTYUP is Null"
                row.setValue('TYPICUP', "ZZ")
                print "Set TYPICUP value to ZZ"
            elif tempTYUP == "ZZ":
                print "TYPICUP value already set to ZZ"
            else:

                print "TYPICUP value: " + tempTYUP
        else:
            print "Error with TYPICUP"

        if row.getValue('TYPICDOWN') in provaliasList:
            tempTYDO = row.getValue('TYPICDOWN')
            if tempTYDO is None:
                print "temTYUP is Null"
                row.setValue('TYPICDOWN', "ZZ")
                print "Set TYPICDOWN value to ZZ"
            elif tempTYDO == "ZZ":
                print "TYPICDOWN value already set to ZZ"
            else:
                print "TYPICDOWN value: " + tempTYDO
        else:
            print "Error with TYPICDOWN"
        if row.getValue('PROVALIAS') in provaliasList:
            tempProv = row.getValue('PROVALIAS')
            print "tempProv=" + tempProv
            dataEndUser = row.getValue('ENDUSERCAT')
            dataProvType = row.getValue('PROVIDER_TYPE')

            lookupRows = arcpy.UpdateCursor(lookup, "", "", "PROVALIAS; PROVNAME; DBNAME; FRN; ENDUSERCAT; PROVIDER_TYPE", "")
            lookupRow = lookupRows.next()
            while lookupRow:
                lookupProv = lookupRow.getValue('PROVALIAS')
                if lookupProv == tempProv:
                    print "match", lookupProv
                    lName = lookupRow.getValue('PROVNAME')
                    print "ProvName: ", lName
                    lDBA = lookupRow.getValue('DBNAME')
                    print "DBA Name: ", lDBA
                    lFRN = lookupRow.getValue('FRN')
                    print "FRN: ", lFRN
                    row.setValue('PROVNAME', lName)
                    row.setValue('DBNAME', lDBA)
                    row.setValue('FRN', lFRN)
                    lEndUser = lookupRow.getValue('ENDUSERCAT')
                    print "ENDUSERCAT: ", lEndUser
                    lType = lookupRow.getValue('PROVIDER_TYPE')
                    print "PROVIDER_TYPE: ", lType
                    if dataEndUser is None:
                        row.setValue('ENDUSERCAT', lEndUser)
                        print "enduser populated"
                    else:
                        print "enduser already exists: ", dataEndUser
                    if dataProvType is None:
                        row.setValue('PROVIDER_TYPE', lType)
                        print "type populated"
                    else:
                        print "type already exists: ", dataProvType

                lookupRows.updateRow(lookupRow)
                lookupRow = lookupRows.next()
            del lookupRow, lookupRows
        else:
            print "error"
            row.setValue('PROVNAME', "no match")
        rows.updateRow(row)
        row = rows.next()

    # Delete Fields
    del row, rows
    print "finished"
    arcpy.AddMessage("Roads Finished")

if midmileInput <>"":

    #
    #   MIDMILE PROCESSING
    #
    arcpy.AddMessage("Start Midmile Processing")
    print "Start Midmile Processing"
    # Process: Create Feature Class (3)
    arcpy.CreateFeatureclass_management(myGDB, "midmile", "POINT", "P:\\SBDDGP-ARRA Project\\BroadbandProductionArea\\Workspaces\\BaseData\\StagingTemplate.gdb\\midmile", "DISABLED", "DISABLED", "GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]];-400 -400 1000000000;-100000 10000;-100000 10000;8.98315284119521E-09;0.001;0.001;IsHighPrecision", "", "0", "0", "0")

    # Process: Append (3)
    arcpy.Append_management(midmileInput, midmile, "NO_TEST", "", "")
    print "Midmile appended"

    arcpy.CalculateField_management(midmile, "STATEABBR", "\"CO\"", "VB", "")
    print "Calculate STATEABBR"
    arcpy.AddField_management(midmile, "WHO", "TEXT", "", "", "10", "", "NULLABLE", "NON_REQUIRED", "")
    arcpy.CalculateField_management(midmile, "WHO", analyst, "VB", "")
    print "WHO field added"
    arcpy.AddField_management(midmile, "WHEN", "DATE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
    arcpy.CalculateField_management(midmile, "WHEN", "Date (  )", "VB", "")
    print "WHEN field added"

    # Create list of ProvAlias found in Provider data
    provListRows = arcpy.UpdateCursor(midmile, "", "", "PROVALIAS; PROVNAME; DBNAME; FRN", "")
    provListRow = provListRows.next()
    provaliasList = []

    for provListRow in provListRows:
        print "provalias: %s, provname: %s, dbaname: %s, frn: %s" % \
            (provListRow.PROVALIAS, provListRow.PROVNAME, provListRow.DBNAME, provListRow.FRN)
        if provListRow.PROVALIAS not in provaliasList:
            provaliasList.append(provListRow.PROVALIAS)
            print provListRow.PROVALIAS," added to provaliasList"
    rows = arcpy.UpdateCursor(midmile, "", "", "PROVALIAS; PROVNAME; DBNAME; FRN", "")
    row = rows.next()
    while row:
        if row.getValue('PROVALIAS') in provaliasList:
            tempProv = row.getValue('PROVALIAS')
            print "tempProv=" + tempProv

            lookupRows = arcpy.UpdateCursor(lookup, "", "", "PROVALIAS; PROVNAME; DBNAME; FRN", "")
            lookupRow = lookupRows.next()
            while lookupRow:
                lookupProv = lookupRow.getValue('PROVALIAS')
                if lookupProv == tempProv:
                    print "match", lookupProv
                    lName = lookupRow.getValue('PROVNAME')
                    print "ProvName: ", lName
                    lDBA = lookupRow.getValue('DBNAME')
                    print "DBA Name: ", lDBA
                    lFRN = lookupRow.getValue('FRN')
                    print "FRN: ", lFRN
                    row.setValue('PROVNAME', lName)
                    row.setValue('DBNAME', lDBA)
                    row.setValue('FRN', lFRN)

                lookupRows.updateRow(lookupRow)
                lookupRow = lookupRows.next()
            del lookupRow, lookupRows
        else:
            print "error"
            row.setValue('PROVNAME', "no match")
        rows.updateRow(row)
        row = rows.next()

    # Delete Fields
    del row, rows
    print "finished"
    arcpy.AddMessage("Midmile Finished")

if wirelessInput <>"":

    #
    #   WIRELESS
    #
    arcpy.AddMessage("Start Wireless Processing")
    print "Start Wireless Processing"
    arcpy.CreateFeatureclass_management(myGDB, "wireless", "POLYGON", "P:\\SBDDGP-ARRA Project\\BroadbandProductionArea\\Workspaces\\BaseData\\StagingTemplate.gdb\\wireless", "DISABLED", "DISABLED", "GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]];-400 -400 1000000000;-100000 10000;-100000 10000;8.98315284119521E-09;0.001;0.001;IsHighPrecision", "", "0", "0", "0")

    # Process: Append (4)
    arcpy.Append_management(wirelessInput, wireless, "NO_TEST", "", "")
    print "Wireless Append Finished"

    arcpy.CalculateField_management(wireless, "STATEABBR", "\"CO\"", "VB", "")
    print "Calculated STATEABBR"
    arcpy.AddField_management(wireless, "WHO", "TEXT", "", "", "10", "", "NULLABLE", "NON_REQUIRED", "")
    arcpy.CalculateField_management(wireless, "WHO", analyst, "VB", "")
    print "WHO field added"
    arcpy.AddField_management(wireless, "WHEN", "DATE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
    arcpy.CalculateField_management(wireless, "WHEN", "Date (  )", "VB", "")
    print "WHEN field added"

    # Create list of ProvAlias found in Provider data
    provListRows = arcpy.UpdateCursor(wireless, "", "", "PROVALIAS; PROVNAME; DBNAME; FRN; TYPICUP; TYPICDOWN", "")
    #provListRow = provListRows.next()
    provaliasList = []

    #for the current row in "wireless", print values
    for provListRow in provListRows:
        print "provalias: %s, provname: %s, dbaname: %s, frn: %s, typicup: %s, typicdown: %s" % \
            (provListRow.PROVALIAS, provListRow.PROVNAME, provListRow.DBNAME, provListRow.FRN,provListRow.TYPICUP, provListRow.TYPICDOWN)
        if provListRow.PROVALIAS not in provaliasList:
            provaliasList.append(provListRow.PROVALIAS)
            print provListRow.PROVALIAS," added to provaliasList"
        if provListRow.TYPICUP not in provaliasList:
            provaliasList.append(provListRow.TYPICUP)
            print provListRow.TYPICUP, " added to provaliasList"
        if provListRow.TYPICDOWN not in provaliasList:
            provaliasList.append(provListRow.TYPICDOWN)
    rows = arcpy.UpdateCursor(wireless, "", "", "PROVALIAS; PROVNAME; DBNAME; FRN; TYPICUP; TYPICDOWN", "")
    row = rows.next()
    while row:

        if row.getValue('TYPICUP') in provaliasList:
            tempTYUP = row.getValue('TYPICUP')
            if tempTYUP is None:
                print "temTYUP is Null"
                row.setValue('TYPICUP', "ZZ")
                print "Set TYPICUP value to ZZ"
            elif tempTYUP == "ZZ":
                print "TYPICUP value already set to ZZ"
            else:
                print "TYPICUP value: " + tempTYUP
        else:
            print "Error with TYPICUP"

        if row.getValue('TYPICDOWN') in provaliasList:
            tempTYDO = row.getValue('TYPICDOWN')
            if tempTYDO is None:
                print "temTYUP is Null"
                row.setValue('TYPICDOWN', "ZZ")
                print "Set TYPICDOWN value to ZZ"
            elif tempTYDO == "ZZ":
                print "TYPICDOWN value already set to ZZ"
            else:
                print "TYPICDOWN value: " + tempTYDO
        else:
            print "Error with TYPICDOWN"

        if row.getValue('PROVALIAS') in provaliasList:
            tempProv = row.getValue('PROVALIAS')
            print "tempProv=" + tempProv

            lookupRows = arcpy.UpdateCursor(lookup, "", "", "PROVALIAS; PROVNAME; DBNAME; FRN", "")
            lookupRow = lookupRows.next()
            while lookupRow:
                lookupProv = lookupRow.getValue('PROVALIAS')
                if lookupProv == tempProv:
                    print "match", lookupProv
                    lName = lookupRow.getValue('PROVNAME')
                    print "ProvName: ", lName
                    lDBA = lookupRow.getValue('DBNAME')
                    print "DBA Name: ", lDBA
                    lFRN = lookupRow.getValue('FRN')
                    print "FRN: ", lFRN
                    row.setValue('PROVNAME', lName)
                    row.setValue('DBNAME', lDBA)
                    row.setValue('FRN', lFRN)

                lookupRows.updateRow(lookupRow)
                lookupRow = lookupRows.next()
            del lookupRow, lookupRows
        rows.updateRow(row)
        row = rows.next()
    # Delete Fields
    del row, rows
    print "finished"
    arcpy.AddMessage("Wireless Finished")

if addressInput <>"":
    arcpy.AddMessage("Unable to process Address Points")

    #
    #   ADDRESS POINTS
    #
#    arcpy.AddMessage("Start Address Point Processing")
#    print "Start Address Points Processing"
#    arcpy.CreateFeatureclass_management(myGDB, "address", "POINT", "'P:\\SBDDGP-ARRA Project\\BroadbandProductionArea\\Workspaces\\BaseData\\StagingTemplate.gdb\\address'", "DISABLED", "DISABLED", "GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]];-400 -400 1000000000;-100000 10000;-100000 10000;8.98315284119521E-09;0.001;0.001;IsHighPrecision", "", "0", "0", "0")

    # Process: Append (5)
#    arcpy.Append_management(addressInput, "address", "NO_TEST", "", "")
#    print "Address Points Append Finished"

#    arcpy.CalculateField_management(address, "STATECODE", "\"CO\"", "VB", "")
#    print "Calculated STATECODE"
#    arcpy.AddField_management(address, "WHO", "TEXT", "", "", "10", "", "NULLABLE", "NON_REQUIRED", "")
#    arcpy.CalculateField_management("address", "WHO", analyst, "VB", "")
#    print "WHO field added"
#    arcpy.AddField_management(address, "WHEN", "DATE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
#    arcpy.CalculateField_management(address, "WHEN", "Date (  )", "VB", "")
#    print "WHEN field added"

#    arcpy.AddMessage("Address Points Finished")

print "Staging Complete"
arcpy.AddMessage("Staging complete for" + myGDB)
