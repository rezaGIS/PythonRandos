# Name:
# CalcStreetName.py
# ---------------------------------------------------------------------------
# Purpose:
#   Designed to modify TIGER streets feature class.
#   Concatenate parsed street address fields 'PRETYPABRV', 'NAME' into new field 'STREETNAME'.
#   Because TIGER parsed street addresses into 6 components and NTIA parses
#   street addresses into 4 components.
#----------------------------------------------------------------------------
# Constrainsts:
#   1. You need to manually enter the path to the file to be processed.
#   2. Varible FIELDNAME needs to match the new field name, here 'STREETNAME'
#
#   NEED TO ADD ONE MORE COMPONENT TO SCRIPT: PREQUALABR
#   BUT THE algorithm WILL NEED TO REDONE SINCE IT IS SET UP TO CONCATANATE
#   2 FIELDS, NOT 3.
#
#   FOR NOW PREQUALABR CAN BE CONCATENATED MANUALLY.
#
#---------------------------------------------------------------------------
# Future Enhancements:
#   1. Add code for interactive pointing to file for processing
#   2. Add elementary event handling code.
#   3. Add Python built in header function (docstring)
#   4. ADD PREQUALABR.
#.  5. Remove space from between I- 70 etc.
#---------------------------------------------------------------------------
# Author: Larry Norden 2012.01.09
# ---------------------------------------------------------------------------
# Updates:
#   2012.02.09 Larry Norden:  Added info about PREQUALABR.
#   2012.01.31 Larry Norden:  Updated header info
# ---------------------------------------------------------------------------


# Import system modules
import sys, string, os, arcgisscripting

# Create the Geoprocessor object
gp = arcgisscripting.create(9.3)

# Load required toolboxes...
#gp.AddToolbox('C:/Program Files/ArcGIS/Desktop10.0/ArcToolbox/Toolboxes/Data Management Tools.tbx')

myFC = 'C:/Workspace/DataDepot/DataDepot.gdb/strTest20'


fieldname = 'STREETNAME'
name = ' '
rows = gp.UpdateCursor(myFC)                                # set up cursor thru each row of table

fieldlist = ['PRETYPABRV', 'NAME']

row = rows.next()                                                       # Initialize first row for each to/from field

while row:                                                                    # Iterate thru each row
     pp = 0
     gp.Addmessage('pp is ' + str(pp))
     List = []  
     for eachfield in fieldlist:
         x = row.getValue(eachfield)
         #if x:
         gp.Addmessage('x = ' + str(x))
         List.append(x)
         pp = len(List)
         gp.Addmessage('len(List) is ' + str(len(List)) )
         if pp == 2:
            name = ' '.join(List)
            
         name = str(name)
         name = name.strip()

     row.SetValue(fieldname, name)
     rows.UpdateRow(row) 
     row = rows.next()
             
 
del rows                                                                       # Delete Update cursor object
del row
'''
elif pp == 1:
                 name = List.pop()
                 name = str(name)
                 name = name.strip()
                 gp.Addmessage('Single name is ' + name)
                 row.SetValue(fieldname, name)
gp.CalculateField_management (myFC, 'PREDIR', ['PREDIRABRV'] )

     gp.Addmessage('MaxAddress ' + maxAddr)         # Debug message
     gp.Addmessage('MinAddress ' + minAddr)           # Debug message
     List = []                                                                   # clear the array
'''

