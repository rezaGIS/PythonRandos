# Name:
# CalcMaxMinAddr.py
# ---------------------------------------------------------------------------
# Purpose:
#   Designed for TIGER streets feature class.
#   This script checks the TIGER streets address ranges on each row, usually 4 cells, min & max 
#   each for left and right sides; puts them into a list and then picks the max and min
#   and populates the max and min address cells. It does not count zeroes as a low.
#   It ignores address numbers that have non integer values.
#   NTIA wants only max & min address reange for a street segment, irregardless of left or
#   right side.
#----------------------------------------------------------------------------
# Constrainsts:
#   1. You need to manually enter the path to the file to be processed. See line 52.
#   2. Ensure FIELDLIST values match the addrress range column names in your file. See line 65.
#   3. You have added 2 new fields named 'ADDMIN' and 'ADDMAX'. The data type should be same
#         as described for the 'ROADS' feature class in the NTIAA data schema.
#
# ---------------------------------------------------------------------------
# Future Enhancements:
#   1. Add code for interactive pointing to file for processing
#   2. Add elementary event handling code.
#  3. Add code to automatically deal with short/long data type address range fields. See line 40.
#  4. Add Python built in header function
#  5. Get rid of most of gp.addmessage and port to text file. The output gets garbled if processing large datasets.
#  6. Analyze non integer addresses and see if they should be incorporated.
# ---------------------------------------------------------------------------
# author: Larry Norden 2012.01.09
# ---------------------------------------------------------------------------
# Updates:
#   2012.02.08 Larry Norden
#   1. Change string address numbers to integers for truer comparisons. In string sorting 2 is larger than 139.
#   2. Added 'isdigit' string object method to identify address numbers containing non numeric chars.
#   3. Added Open file object to capture info on address numbers that contain non numeric chars.
#   4. Added code to ignore address numbers that contain non integer values.
#
#   2012.01.31 Larry Norden:  Updated header info
# ---------------------------------------------------------------------------

# Import system modules
import sys, string, os, arcgisscripting

# Create the Geoprocessor object
gp = arcgisscripting.create(9.3)

# Load required toolboxes...
#gp.AddToolbox('C:/Program Files/ArcGIS/ArcToolbox/Toolboxes/Data Management Tools.tbx')



##myFC = 'C:/Workspace/BBPROVIDERDATA/myAgate/agate.gdb/agRds_1'        # Path of file to be processed.
myFC = 'C:/Workspace/DataDepot/DataDepot.gdb/origRoads2010Outside'

eachfield = ''
x = ''
List = []                                                                # Instantiate the array

myfile = open('C:/Workspace/myTemp.txt', 'w')

addmin = 'ADDMIN'                                                        # min address number field
addmax = 'ADDMAX'                                                        # max address number field

rows = gp.UpdateCursor(myFC)                                             # set up cursor thru each row of table

fieldlist = ['LFROMADD', 'LTOADD', 'RFROMADD', 'RTOADD']

row = rows.next()                                                        # Initialize first row for each to/from field

                                                                         ## This first section populates a python list with up to 4 addr. ranges.
while row:                                                               # Iterate thru each row
    
     rownum = row.getvalue('objectid')
     getrow = '\n' + ('Row # ' +str(rownum) + ' by objectid')
     gp.addmessage(getrow)
                       
     for eachfield in fieldlist:                                         # Iterate thru each Left/Right To/From (4) field per row
         x = row.getValue(eachfield)                                     # x = one addr. range value
         x = str(x)

         pp = (x ==  ' ')                                                # Check if x is blank, if yes then pp returns boolean TRUE
         if  pp:                                                         # if  TRUE
             gp.Addmessage(eachfield + ' is blank')
         elif not x.isdigit():                                           # if address number not all digits. ('ISDIGIT' returns false if addr. num contains non numeric char)
             myfile.write((getrow + '\n'))                               # then write offending addr num to text file
             forfile = (eachfield + ' = ' + x)
             myfile.write((forfile + '\n'))
             gp.Addmessage(forfile)
         else:
             x = int(x)                                                  # convert to integer
             gp.addmessage(x)
             List += [x]                                                 # Adds cell value to array called List
             #gp.Addmessage(eachfield + ' = ' + str(x))

                                                                         ##This section checks if list has values, if so then extracts the MAX value and then the MIN value
     if  List:                                                           # Check for empty list, returns boolean false if empty
         maxAddr = max(List)                                             # Extracts maximum address
         minAddr = min(List)                                             # Extracts minimum address
         minAddr = str(minAddr)
         maxAddr = str(maxAddr)
         gp.Addmessage('MaxAddress ' + maxAddr)                          # Debug message
         gp.Addmessage('MinAddress ' + minAddr)                          # Debug message
         List = []                                                       # clear the array
     else:
         maxAddr = 'ZZ'                                                  # Assign a value ZZ to max min address number if all 4 fields are zero
         minAddr = 'ZZ'

     row.SetValue(addmax, maxAddr)                                       ##This 'sets' (in RAM?)the MAX and MIN values in the appropriate cells; UPDATE then WRITES (to hardrive?) the value.
     row.SetValue(addmin, minAddr)

     rows.UpdateRow(row)                                                 #  Method of UpdateCursor, updates the current row with a modified row object
     row = rows.next()                                                   # Go to next row

del rows                                                                 # Delete Update cursor object
del row

myfile.close()

