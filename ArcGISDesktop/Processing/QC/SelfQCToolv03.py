# ---------------------------------------------------------------------------
# SelfQCToolv1.py
# Created on: 2014-02-25 15:39:10.00000
#
# Usage: Tests GDB's for errors after running through the Staging Tool
# Description: The tool has multiple steps:
#   1. Creates a txt file for an output report
#   2. Identifies features in a feature class
#   3. Tests each possibility of error within each field of every FC present

# Edits for future versions:

# Import system modules
import sys, string, os, arcpy
from arcpy import env
import time
from datetime import date
from os import remove, close
today = date.today()

#acquire arguments
theGDB = sys.argv[1]  #theFeatureDataSet eg C:\Users\DE.gdb
analyst = sys.argv[2]

##theGDB = r"C:\GOIT\ProductionOCT2014\agate\processed\agate.gdb" ##Comment out for production use
##theOF = r"C:\Users\rezaghok\Desktop\TEST2" ##Comment out for production use
##analyst = "Testing Environment" ##Comment out for production use
#set up variables
myFlag = 0
theST = "CO"
theOF = os.path.dirname(theGDB)

#Break the GDB name and path for saving and naming the report

filename = os.path.split(theGDB)
fullname = arcpy.ParseFieldName(os.path.basename(theGDB))
nameList = fullname.split(",")
alias1 = nameList[2]
alias = alias1.strip(' ')
print alias

env.workspace = theGDB
#Create Reciept
try:
    theYear = today.year
    theMonth = today.month
    theDay = today.day

    #set up output file
    outFile = theOF + "/"+ alias +"_QC_"+ str(theYear) + "_" + str(theMonth) + "_" + str(theDay) + ".txt"
    myFile = open(outFile, 'w')
    myFile.write("" + "\n")
    myFile.write("* -----------------------------------------------------------------------------" + "\n")
    myFile.write("* Data QC Report" + "\n")
    myFile.write("* SelfQCToolv1.py" + "\n")
    myFile.write("* Created on: " + str(theMonth) + "/" + str(theDay) + "/" + str(theYear) + "\n") #
    myFile.write("* Created by: " + analyst + "\n")  ###investigate getting who out of the metadata
    myFile.write("* Colorado Broadband Data Development Program" + "\n")
    myFile.write("* -----------------------------------------------------------------------------" + "\n")
    myFile.write("" + "\n")
    myFile.write("*******************************************************************************" + "\n")
    myFile.write("*****                                                                     *****" + "\n")
    myFile.write("*****                                                                     *****" + "\n")
    myFile.write("*****                     Self QC Reciept version 2.0                     *****" + "\n")
    myFile.write("*****                     Check below for any FAILED Statements           *****" + "\n")
    myFile.write("*****                     Check below for any WARNING Statements          *****" + "\n")
    myFile.write("*****                     Raw MBPS required                               *****" + "\n")
    myFile.write("*******************************************************************************" + "\n")
    myFile.close()
    del theDay, theMonth, theYear
except:
    arcpy.AddMessage(arcpy.GetMessage(0))
    arcpy.AddMessage(arcpy.GetMessage(1))
    arcpy.AddMessage(arcpy.GetMessage(2))
    theMsg = "Something bad happened during the writing of the reciept;"
    theMsg = theMsg + "please re-run"
    arcpy.AddMessage(theMsg)
    del theMsg

#write out functions
#Function sbdd_qry creates a layer from a query and determines if the
#count is greater than 0; essentially this function looks for unexpected
#values in a source layer field
def sbdd_qry (theFL, myFL, myQry, mySeverity):
    if mySeverity == "Fail":
        myMsg = "    FAILED      " + myFL + " YOU MUST FIX THESE"
    if mySeverity == "Warn":
        myMsg = "    WARNING     " + myFL + " YOU MUST EXPLAIN THESE "
    myFlag = 0
    myCnt = 0
    arcpy.AddMessage("     Checking for unexpected values: " + myFL)
    arcpy.MakeFeatureLayer_management(theFL, myFL, myQry)
    myCnt = int(arcpy.GetCount_management(myFL).getOutput(0))
    arcpy.Delete_management(myFL)
    if myCnt > 0: #exception occurred
        myFile.write("      Field Check: " + myMsg + " " + str(myCnt) + " UNEXPECTED VALUES \n")
        myFlag = 1
    else:
        myFile.write("      Field Check:     passed      " + myFL + \
                     " values are good \n")
    del myCnt, theFL, myFL, myQry
    return (myFlag)

# Process: Check for Speed Tiers
# a Speed tier is where a provider is listing more than 1 record for a
#technology in a given block; like 'Mikes Net providing DSL at MaxAd Down/Up
#of 5/3 and 3/1 in Block 001


#sbdd_qryDef writes out the definitions for the queries,
#since these are used multiple times
def sbdd_qryDef (myField):
    if myField == "WiredTRANSTECH":
        theQry = "TRANSTECH IS NULL OR (TRANSTECH <> 10 AND TRANSTECH <> 11 AND TRANSTECH <> 12 AND TRANSTECH <> 20 AND "
        theQry = theQry + "TRANSTECH <> 30 AND TRANSTECH <> 40 AND TRANSTECH "
        theQry = theQry + "<> 41 AND TRANSTECH <> 50 AND TRANSTECH <> 90)"
    if myField == "WireLessTRANSTECH":
        theQry = "TRANSTECH IS NULL OR (TRANSTECH <> 70 AND TRANSTECH <> 71 AND "
        theQry = theQry + "TRANSTECH <> 80 AND TRANSTECH <> 60)"
    if myField == "MaxAdDown":
        theQry = "MAXADDOWN IS NULL OR (MAXADDOWN < .0 AND MAXADDOWN <> -9999)"
    if myField == "MaxAdUp":
        theQry = "MAXADUP > MaxAdDown OR (MAXADUP < .0 AND MAXADUP <> -9999) OR MaxAdUp IS NULL"
    if myField == "PROVALIAS":
        theQry = "PROVALIAS Is NULL OR PROVALIAS = '' OR PROVALIAS = ' '"
    if myField == "Flag_TT10_MAD":
        theQry = "TRANSTECH = 10 AND (MAXADDOWN < .768 OR MAXADDOWN > 100)"
    if myField == "Flag_TT10_MAU":
        theQry = "TRANSTECH = 10 AND (MAXADUP < .200 OR MAXADUP > 100 OR MAXADUP > MAXADDOWN)"
    if myField == "Flag_TT11_MAD":
        theQry = "TRANSTECH = 11 AND (MAXADDOWN < .768 OR MAXADDOWN > 100)"
    if myField == "Flag_TT11_MAU":
        theQry = "TRANSTECH = 11 AND (MAXADUP < .200 OR MAXADUP > 100 OR MAXADUP > MAXADDOWN)"
    if myField == "Flag_TT12_MAD":
        theQry = "TRANSTECH = 12 AND (MAXADDOWN < .768 OR MAXADDOWN > 100)"
    if myField == "Flag_TT12_MAU":
        theQry = "TRANSTECH = 12 AND (MAXADUP < .200 OR MAXADUP > 100 OR MAXADUP > MAXADDOWN)"
    if myField == "Flag_TT20_MAD":
        theQry = "TRANSTECH = 20 AND (MAXADDOWN < .768 OR MAXADDOWN > 100)"
    if myField == "Flag_TT20_MAU":
        theQry = "TRANSTECH = 20 AND (MAXADUP < .200 OR MAXADUP > 100 OR MAXADUP > MAXADDOWN)"
    if myField == "Flag_TT30_MAD":
        theQry = "TRANSTECH = 30 AND (MAXADDOWN < .768 OR MAXADDOWN > 1000)"
    if myField == "Flag_TT30_MAU":
        theQry = "TRANSTECH = 30 AND (MAXADUP < .200 OR MAXADUP > 1000 OR MAXADUP > MAXADDOWN)"
    if myField == "Flag_TT40_MAD":
        theQry = "TRANSTECH = 40 AND (MAXADDOWN < .768 OR MAXADDOWN > 1000)"
    if myField == "Flag_TT40_MAU":
        theQry = "TRANSTECH = 40 AND (MAXADUP < .200 OR MAXADUP > 25 OR MAXADUP > MAXADDOWN)"
    if myField == "Flag_TT41_MAD":
        theQry = "TRANSTECH = 41 AND (MAXADDOWN < .768 OR MAXADDOWN > 25)"
    if myField == "Flag_TT41_MAU":
        theQry = "TRANSTECH = 41 AND (MAXADUP < .200 OR MAXADUP > 25 OR MAXADUP > MAXADDOWN)"
    if myField == "Flag_TT50_MAD":
        theQry = "TRANSTECH = 50 AND (MAXADDOWN < .768 OR MAXADDOWN > 1000)"
    if myField == "Flag_TT50_MAU":
        theQry = "TRANSTECH = 50 AND (MAXADUP < .200 OR MAXADUP > 1000 OR MAXADUP > MAXADDOWN)"
    if myField == "Flag_TT60_MAD":
        theQry = "TRANSTECH = 60 AND (MAXADDOWN < .768 OR MAXADDOWN > 25)"
    if myField == "Flag_TT60_MAU":
        theQry = "TRANSTECH = 60 AND (MAXADUP < .200 OR MAXADUP > 6 OR MAXADUP > MAXADDOWN)"
    if myField == "Flag_TT70_MAD":
        theQry = "TRANSTECH = 70 AND (MAXADDOWN < .768 OR MAXADDOWN > 25)"
    if myField == "Flag_TT70_MAU":
        theQry = "TRANSTECH = 70 AND (MAXADUP < .200 OR MAXADUP > 25 OR MAXADUP > MAXADDOWN)"
    if myField == "Flag_TT71_MAD":
        theQry = "TRANSTECH = 71 AND (MAXADDOWN <.768 OR MAXADDOWN > 25)"
    if myField == "Flag_TT71_MAU":
        theQry = "TRANSTECH = 71 AND (MAXADUP < .200 OR MAXADUP > 25 OR MAXADUP > MAXADDOWN)"
    if myField == "Flag_TT80_MAD":
        theQry = "TRANSTECH = 80 AND (MAXADDOWN <.768 OR MAXADDOWN > 25)"
    if myField == "Flag_TT80_MAU":
        theQry = "TRANSTECH = 80 AND (MAXADUP < .200 OR MAXADUP > 25 OR MAXADUP > MAXADDOWN)"
    if myField == "PROVNAME":
        theQry = "PROVNAME Is Null OR PROVNAME = '' OR PROVNAME = ' ' OR PROVNAME = 'no match'"
    if myField == "DBANAME":
        theQry = "DBANAME Is Null OR DBANAME = '' OR DBANAME = ' '"
    if myField == "FRN":
        theQry = "FRN Is Null OR FRN = '' OR (CHAR_LENGTH(FRN) < 10 AND FRN <> '9999')"
    if myField == "OWNERSHIP":
        theQry ="OWNERSHIP Is Null OR (OWNERSHIP < 0 OR OWNERSHIP > 1)"
    if myField == "BHCAPACITY":
        theQry = "BHCAPACITY < 0 OR BHCAPACITY > 9"
    if myField == "BHTYPE":
        theQry = "BHTYPE < 0 OR BHTYPE > 4"
    if myField == "LATITUDE":
        theQry = "LATITUDE Is Null OR LATITUDE < 0"
    if myField == "LONGITUDE":
        theQry = "LONGITUDE Is Null OR (LONGITUDE < -170 OR LONGITUDE > -60)"
    if myField == "ELEVFEET":
        theQry = "ELEVFEET IS NULL OR ELEVFEET < -9999 OR (ELEVFEET BETWEEN -9998 AND -1) "
        theQry = theQry + "OR ELEVFEET > 400"
    if myField == "STATEABBR":
        theQry = "STATEABBR Is Null or STATEABBR <> '" + theST + "'"
    if myField == "ANCHORNAME":
        theQry = "ANCHORNAME IS NULL OR ANCHORNAME = '' OR ANCHORNAME = ' '"
    if myField == "ADDRESS":
        theQry = "ADDRESS IS NULL OR ADDRESS = '' OR ADDRESS = ' '"
    if myField == "BLDGNBR":
        theQry = "BLDGNBR IS NULL OR BLDGNBR = '' OR BLDGNBR = ' '"
    if myField == "STREETNAME":
        theQry = "STREETNAME IS NULL OR STREETNAME = '' OR STREETNAME = ' '"
    if myField == "CITY":
        theQry = "CITY IS NULL OR CITY = '' OR CITY = ' ' OR CITY = 'CITY'"
    if myField == "STATECODE":
        theQry = "STATECODE IS NULL OR STATECODE <> '" + theST + "'"
    if myField == "ZIP5":
        theQry = "ZIP5 IS NULL OR ZIP5 = '' OR ZIP5 = ' ' OR ZIP5 = '0'"
    if myField == "CAICAT":
        theQry = "CAICAT IS NULL OR (CAICAT < '1' OR CAICAT > '7')"
    if myField == "ENDUSERCAT":
        theQry = "ENDUSERCAT IS NULL OR (ENDUSERCAT < '1' OR ENDUSERCAT > '5')"
    if myField =="ENDUSERCAT_CENRD":
        theQry = "ENDUSERCAT IS NULL OR (ENDUSERCAT < '1' OR ENDUSERCAT > '5')"
    if myField == "ENDUSERCAT_WIRE":
        theQry = "ENDUSERCAT IS NULL OR ENDUSERCAT NOT IN ('1','2','5')"
    if myField == "ENDUSERCAT_ADD":
        theQry = "ENDUSERCAT IS NULL OR ENDUSERCAT NOT IN ('1','2')"
    if myField == "BBSERVICE":
        theQry = "BBSERVICE IS NULL OR BBSERVICE = '' OR BBSERVICE = ' ' OR "
        theQry = theQry + " (BBSERVICE <> 'N' AND BBSERVICE <> 'Y' AND "
        theQry = theQry + " BBSERVICE <> 'U')"
    if myField == "PROVIDER_TYPE":
        theQry = "PROVIDER_TYPE IS NULL OR PROVIDER_TYPE NOT IN ('1','2','3')"
    if myField == "PROVIDER_TYPE_CENRD":
        theQry = "PROVIDER_TYPE IS NULL OR (PROVIDER_TYPE <> 1 AND "
        theQry = theQry + "PROVIDER_TYPE <> 2 AND PROVIDER_TYPE <> 3 )"
    if myField == "STATEFIPS":
        theQry = "STATEFIPS IS NULL OR STATEFIPS = '' OR STATEFIPS = ' ' "
        theQry = theQry + "OR STATEFIPS <> '" + stFIPS + "'"
    if myField == "COUNTYFIPS":
        theQry = "COUNTYFIPS IS NULL OR COUNTYFIPS = '' OR COUNTYFIPS = ' ' "
        theQry = theQry + " OR (CHAR_LENGTH(COUNTYFIPS) <> 3) "
    if myField == "TRACT":
        theQry = "TRACT IS NULL OR TRACT = '' OR TRACT = ' ' OR "
        theQry = theQry + "(CHAR_LENGTH(TRACT) <> 6)"
    if myField == "BLOCKID":
        theQry = "BLOCKID IS NULL OR BLOCKID = '' OR BLOCKID = ' ' OR "
        theQry = theQry + " (CHAR_LENGTH(BLOCKID) <> 4)"
    if myField == "BLOCKSUBGROUP":
        theQry = "BLOCKSUBGROUP = '' OR BLOCKSUBGROUP = ' ' OR "
        theQry = theQry + " (CHAR_LENGTH(BLOCKSUBGROUP) <> 1)"
    if myField == "GEOUNITTYPE":
        theQry = "GEOUNITTYPE IS NULL OR (GEOUNITTYPE <> 'CO')"
    if myField == "STATECOUNTYFIPS":
        theQry = "STATECOUNTYFIPS IS NULL OR (STATECOUNTYFIPS NOT LIKE '"
        theQry = theQry + stFIPS + "%') OR (CHAR_LENGTH(STATECOUNTYFIPS) <> 5)"
    if myField == "ADDMIN":
        theQry = "(ADDMIN = '' OR ADDMIN = ' ')"
    if myField == "ADDMAX":
        theQry = "(ADDMAX = '' OR ADDMAX = ' ')"
    if myField == "STATE":
        theQry = "STATE IS NULL OR (STATE <> '" + theST + "')"
    if myField == "SPECTRUM":
        theQry = "SPECTRUM IS NULL OR (SPECTRUM < 1 OR SPECTRUM > 10)"
    if myField == "OneSpeedAndNotTheOther":  #speed needs to be consistently populated
        theQry = "(MAXADDOWN IS NOT NULL  AND MAXADUP = '') OR "
        theQry = theQry + " (MAXADDOWN = ''  AND MAXADUP IS NOT NULL)"
    if myField =="TYPICDOWN":
        theQry = "TYPICDOWN > MAXADDOWN OR (TYPICDOWN < 0 AND TYPICDOWN <> -9999) OR TYPICDOWN IS NULL"
    if myField =="TYPICUP":
        theQry = "TYPICUP > MAXADUP OR (TYPICUP < .0 AND TYPICUP <> -9999) OR TYPICUP IS NULL"
    if myField == "STREETNAME":
        theQry = "STREETNAME IS NULL OR STREETNAME ='' OR STREETNAME = ' '"
    if myField =="MAXSUBDOWN":
        theQry = "MAXSUBDOWN > MAXADDOWN OR (MAXSUBDOWN < .0 AND MAXSUBDOWN <> -9999) OR MAXSUBDOWN IS NULL"
    if myField =="MAXSUBUP":
        theQry = "MAXSUBUP > MAXSUBDOWN OR (MAXSUBUP < .0 AND MAXSUBUP <> -9999) OR MAXSUBUP IS NULL"
    return(theQry)

#set the stFIPS
stFIPS = "0"
stFIPS = '08'

#CHECK GEOMETRY
# The workspace in which the feature classes will be checked
outTable = theGDB + "/checkGeometryResult"
if arcpy.Exists(outTable):
    arcpy.Delete_management(outTable)

# A variable that will hold the list of all the feature classes
# inside the geodatabase
fcs = []

# List all standalone feature classes
fcs = arcpy.ListFeatureClasses()

print "Running the check geometry tool on %i feature classes" % len(fcs)
arcpy.CheckGeometry_management(fcs, outTable)

if (str(arcpy.GetCount_management(outTable))) <> '0':
    print (str(arcpy.GetCount_management(outTable)) + " geometry problems were found.")
    arcpy.AddMessage(str(arcpy.GetCount_management(outTable)) + " geometry problems were found.")
    arcpy.RepairGeometry_management(fcs)
    arcpy.Delete_management(outTable)
else:
    print(str(arcpy.GetCount_management(outTable)) + " geometry problems were found. - - Deleting Table")
    arcpy.AddMessage(str(arcpy.GetCount_management(outTable)) + " geometry problems were found. - - Deleting Table")
    arcpy.Delete_management(outTable)

#Start Census Block checks
fc = "plss"
if arcpy.Exists(fc):
    #check for BB_Service_CensusBlock
    arcpy.AddMessage("Begining checks on Feature Class: " + fc)

    fcCnt = int(arcpy.GetCount_management(fc).getOutput(0))

    myFile = open(outFile, 'a')
    myFile.write("" + "\n")
    myFile.write("      Initial Feature Count: " + str(fcCnt) + " features \n")
    myFile.write("*Check Layer: " + fc + "\n")
    myChecks = ["WiredTRANSTECH", "MaxAdDown", "MaxAdUp", "PROVALIAS",
                "ENDUSERCAT_CENRD", "TYPICDOWN", "TYPICUP", "MAXSUBDOWN", "MAXSUBUP"] #Fail queries
    for myCheck in myChecks:
            myFlag = myFlag + sbdd_qry (theGDB + "/" + fc, fc + "_" +
                                        myCheck, sbdd_qryDef(myCheck), "Fail")
    myChecks = ["Flag_TT10_MAD","Flag_TT10_MAU","Flag_TT11_MAD", "Flag_TT11_MAU", "Flag_TT12_MAD",
                "Flag_TT12_MAU", "Flag_TT20_MAD","Flag_TT20_MAU",
                "Flag_TT30_MAD","Flag_TT30_MAU","Flag_TT40_MAD","Flag_TT40_MAU",
                "Flag_TT41_MAD","Flag_TT41_MAU","Flag_TT50_MAD","Flag_TT50_MAU"] #Warn queries
    for myCheck in myChecks:
            myFlag = myFlag + sbdd_qry (theGDB + "/" + fc, fc + "_" +
                                        myCheck, sbdd_qryDef(myCheck), "Warn")
    myChecks = ["PROVNAME", "DBANAME", "PROVIDER_TYPE_CENRD", "FRN"]
    for myCheck in myChecks:
        myFlag = myFlag + sbdd_qry (theGDB + "/" + fc, fc + "_" +
                                    myCheck, sbdd_qryDef(myCheck), "Fail")



fc = "wireless"
if arcpy.Exists(fc):
    #check for BB_Service_Wireless
    arcpy.AddMessage("Begining checks on Feature Class: " + fc)
    fcCnt = int(arcpy.GetCount_management(fc).getOutput(0))
    myFile = open(outFile, 'a')
    myFile.write("" + "\n")
    myFile.write("      Initial Feature Count: " + str(fcCnt) + " features \n")
    myFile.write("*Check Layer: " + fc + "\n")
    myChecks = ["WireLessTRANSTECH", "MaxAdDown", "MaxAdUp","PROVALIAS",
                "ENDUSERCAT_WIRE","TYPICDOWN", "TYPICUP", "MAXSUBDOWN", "MAXSUBUP" ] #Fail queries
    for myCheck in myChecks:
            myFlag = myFlag + sbdd_qry (theGDB + "/" + fc, fc + "_" +
                                        myCheck, sbdd_qryDef(myCheck), "Fail")
    myChecks = ["Flag_TT60_MAD","Flag_TT60_MAU","Flag_TT70_MAD","Flag_TT70_MAU",
                "Flag_TT71_MAD","Flag_TT71_MAU","Flag_TT80_MAD","Flag_TT80_MAU"]
    for myCheck in myChecks:
            myFlag = myFlag + sbdd_qry (theGDB + "/" + fc, fc + "_" +
                                        myCheck, sbdd_qryDef(myCheck), "Warn")
    myChecks = ["PROVNAME", "DBANAME", "FRN", "STATEABBR", "SPECTRUM"]
    for myCheck in myChecks:
        myFlag = myFlag + sbdd_qry (theGDB + "/" + fc, fc + "_" +
                                    myCheck, sbdd_qryDef(myCheck), "Fail")
    myFile.close()

fc = "midmile"
if arcpy.Exists(fc):
    #check for BB_ConnectionPoint_MiddleMile
    arcpy.AddMessage("Begining checks on Feature Class: " + fc)
    fcCnt = int(arcpy.GetCount_management(fc).getOutput(0))
    myFile = open(outFile, 'a')
    myFile.write("" + "\n")
    myFile.write("      Initial Feature Count: " + str(fcCnt) + " features \n")
    myFile.write("*Check Layer: " + fc + "\n")
    myChecks = ["PROVALIAS", "PROVNAME", "DBANAME", "FRN", "OWNERSHIP",
                "BHCAPACITY","ELEVFEET", "BHTYPE", "LATITUDE", "LONGITUDE",
                "STATEABBR"]
    for myCheck in myChecks:
        myFlag = myFlag + sbdd_qry (theGDB + "/" + fc, fc + "_" +
                                    myCheck, sbdd_qryDef(myCheck), "Fail")
    myFile.close()


if myFlag > 0:
    arcpy.AddMessage("*********************************************")
    arcpy.AddMessage("*********************WARNING*****************")
    arcpy.AddMessage("It appears you have some data inegrity issues")
    arcpy.AddMessage("1) Check the reciept file for a complete list")
    arcpy.AddMessage("2) take appropriate corrective action"        )
    arcpy.AddMessage("3) and rerun the QC Tool                     ")
    arcpy.AddMessage("*********************WARNING*****************")
    arcpy.AddMessage("*********************************************")
if myFlag == 0:
    arcpy.AddMessage("*****************************************************")
    arcpy.AddMessage("*********************CONGRATULATIONS*****************")
    arcpy.AddMessage("      It appears you have NO data inegrity issues")
    arcpy.AddMessage("        this file is ready to submit into QC")
    arcpy.AddMessage("*********************CONGRATULATIONS*****************")
    arcpy.AddMessage("*****************************************************")
del myFile, outFile, myFlag


