# ---------------------------------------------------------------------------
# myTest.py
# Created on: 2012-08-01
#         by: Larry Norden
#
# Description:
# Recieved a table of addresses from Secretary of State. The entire address
# was concatenated into one cell. To geocode one needs distinct instances
# of house address, city, state and zip code
# 
# This script parses out the full address located in a single cell into 4
# seperate fields: house address, city, state and zip code. 
# 
# It strips out the 'suite', 'apartment' etc. identifiers since those
# strings confounds the geocoder.
#
# Output: 4 seperate fields: house address, city, state and zip code.
#
# ---------------------------------------------------------------------------

"""Parse a full address string into 4 components.



"""


# Import arcpy module
import arcpy
import sys
import string

# Location of GDB containing address table.
arcpy.env.workspace = (r'C:\Workspace\geocodeNathen\vtrRolls.gdb')

# Text file that will record anomalies, i.e. incomplete addresses.
myfile = open('C:/Workspace/geocodeNathen/myTemp.txt', 'w')

# Local variables:
#csvfile = 'generalTEST'
#csvfile = 'voterTest2011'

# Address table where one field contains entire address. For geocoding
# the number and street, city, state and zip all need to be in seperate fields.
# If the address references something like 'Apt#' that is not brought over.
csvfile = 'IFTV2010General'

# Address field to parse. It is 'bad' because the entire address,
# house number to zip code is one string. Also contains 'Apt#' 
# which is not helpful for geocoding.
badfield = 'RESIDENTIAL_ADDRESS'

# New address fields that will be added to the end of the address table
# that will contain the parsed address values.
addr1field = 'ADDR1'
cityfield = 'CITY1'
zipfield = 'ZIP1'
stfield = 'STATE1'

# List of new address fields
addrfldlist = [addr1field, cityfield, zipfield, stfield]

try:
    try:
        if arcpy.Exists(csvfile):
            print 'Starting with ' + csvfile
    except:
        msg1 = 'table does not exist'
        print msg1
        arcpy.AddMessage(msg1)
    
    
    row, rows = None, None
    # Make list of user added fields.
    tablefields = [f.name for f in arcpy.ListFields(csvfile, '*1')]

    # Check if new address fields have been added
    for addrfield in addrfldlist:
        # if user added fields not in table
        if addrfield not in tablefields:
            # Add Field
            arcpy.AddField_management(csvfile, addrfield, "TEXT", "", "",
                                      50, "", "NULLABLE", "NON_REQUIRED", "")

    # Function to remove apt numbers starting from key works below.
    def stripunits(houseaddr):
        global no_apt
        # List of subunits that are attached to the end of the address strings.
        # If found then that string and everything to the right is removed.
        unitlist = ['LOT', 'APT', '#', 'UNIT', 'TRLR', 'STE', 'SPACE']
        for unit in unitlist:
            # Split the string at the last occurance of (unit). Return 3-tuple
            # containing the part before the separator, separator itself and
            # part after separator.  If separator not found, return a 3-tuple
            # containing 2 empty strings, followed by string itself.
            mytemp = houseaddr.rpartition(unit)
            no_apt = mytemp[0]

            # If 1st tuple is NOT empty returns address string
            if  no_apt != '':
                #print no_apt
                return no_apt
        return  


    # Instantiate UpdateCursor object.
    rows = arcpy.UpdateCursor(csvfile)

    for row in rows:
        # x is 'RESIDENTIAL_ADDRESS' value.
        x = row.getValue(badfield)

        # Just for fun print out objectid
        objID = row.getValue('OBJECTID')
        print objID
        
        # Luckily each part of the full address is comma seperated.
        # Parse address by comma into list.
        newlist = string.split(x,',')

        # Check for not fully formed addresses
        if len(newlist) == 3 and (newlist[0] != '' or newlist[1] != ''
                                  or newlist[2] != ''):
            # Remove extra whitespace from inside house address.
            newaddr = ' '.join(newlist[0].split())

            # Function to remove apt numbers.
            stripunits(newaddr)

            # If apt info was stripped out, use new address
            if no_apt != '':
                row.setValue(addr1field, no_apt)
            else:
                row.setValue(addr1field,newaddr)
                
            # Add city.
            row.setValue(cityfield, newlist[1])

            # Parse STATE ZIP into list from 3rd item in 'newlist'.
            statezip = string.split(newlist[2])

            #Check if there are 2 elements: zip, state abbr.
            if len(statezip) == 2:
                # Add zipcode
                row.setValue(zipfield, statezip[1])

                # Add state abbreviation.
                row.setValue(stfield, statezip[0])
            else:
                myfile.write('OBJECTID = ' + (str(objID) + '\n'))
                myfile.write('Problem with zip or state' + '\n')
                myfile.write((x + '\n'))
                myfile.write((row.getValue('COUNTY') + ' County' + '\n\n'))

        else:
            myfile.write('OBJECTID = ' + (str(objID) + '\n'))
            myfile.write((x + '\n'))
            myfile.write((row.getValue('COUNTY') + ' County' + '\n\n'))
            #forfile = (x)
            #myfile.write((forfile + '\n'))

        rows.updateRow(row)
            
except:
    if not arcpy.GetMessages() == "":
        arcpy.AddMessage(arcpy.GetMessages(2))
        print arcpy.GetMessages(2)
        print 'bailing out'

finally:
    # Regardless of whether the script succeeds or not, delete 
    #  the row and cursor
    #
    myfile.close()
    print 'done'
    if row:
        del row
    if rows:
        del rows   



    
    
    

