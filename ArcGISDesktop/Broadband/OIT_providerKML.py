# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# OIT_providerKMLv02.py
# Created on: 2016-06-13 13:54:52.00000
#   (generated by ArcGIS/ModelBuilder)
# Usage: OIT_providerKMLv02 <plss> <wireless> <midmile> <provName> <Folder> <symbology_lyr>
# Description: Use this to quickly export provider coverages into KMLs for review.
#Future Enhancements: Work on making symbology more legible / and or kml having
# tiers listed instead.
# ---------------------------------------------------------------------------

# Import arcpy module
import arcpy

# Script arguments
plss = arcpy.GetParameterAsText(0)

wireless = arcpy.GetParameterAsText(1)

midmile = arcpy.GetParameterAsText(2)

provName = arcpy.GetParameterAsText(3)

Folder = arcpy.GetParameterAsText(4)

symbology_lyr = arcpy.GetParameterAsText(5)
if symbology_lyr == '#' or not symbology_lyr:
    symbology_lyr = "P:\\SBDDGP-ARRA Project\\BroadbandProductionArea\\Workspaces\\Tools\\Code\\Post_Processing\\OIT_providerKML\\symbology.lyr" # provide a default value if unspecified

# Local variables:
midmile_Layer = midmile
v_String__midmile_kmz = midmile_Layer
String = "%Folder%/%provName%"
wireless_Layer = wireless
wireless_symbology_lyr = wireless_Layer
v_String__wireless_kmz = wireless_symbology_lyr
plss_layer = plss
plss_symbology_lyr = plss_layer
v_String__plss_kmz = plss_symbology_lyr

# Process: Make Feature Layer
try:
	arcpy.MakeFeatureLayer_management(midmile, midmile_Layer, "", Folder, "OBJECTID OBJECTID VISIBLE NONE;SHAPE SHAPE VISIBLE NONE;PROVALIAS PROVALIAS VISIBLE NONE;PROVNAME PROVNAME VISIBLE NONE;DBANAME DBANAME VISIBLE NONE;FRN FRN VISIBLE NONE;OWNERSHIP OWNERSHIP VISIBLE NONE;BHCAPACITY BHCAPACITY VISIBLE NONE;BHTYPE BHTYPE VISIBLE NONE;LATITUDE LATITUDE VISIBLE NONE;LONGITUDE LONGITUDE VISIBLE NONE;ELEVFEET ELEVFEET VISIBLE NONE;STATEABBR STATEABBR VISIBLE NONE;CONFIDENCE CONFIDENCE HIDDEN NONE;WHO WHO HIDDEN NONE;WHEN WHEN HIDDEN NONE")
except:
    print "YOU FAIL"
try:
	# Process: Layer To KML
	arcpy.LayerToKML_conversion(midmile_Layer, v_String__midmile_kmz, "0", "false", "DEFAULT", "1024", "96", "CLAMPED_TO_GROUND")
except:
    print "YOU FAIL"
try:
	# Process: Make Feature Layer (2)
	arcpy.MakeFeatureLayer_management(wireless, wireless_Layer, "", Folder, "OBJECTID OBJECTID VISIBLE NONE;Shape Shape VISIBLE NONE;PROVALIAS PROVALIAS VISIBLE NONE;PROVNAME PROVNAME VISIBLE NONE;DBANAME DBANAME VISIBLE NONE;FRN FRN VISIBLE NONE;TRANSTECH TRANSTECH VISIBLE NONE;SPECTRUM SPECTRUM VISIBLE NONE;MAXADDOWN MAXADDOWN VISIBLE NONE;MAXADUP MAXADUP VISIBLE NONE;TYPICDOWN TYPICDOWN VISIBLE NONE;TYPICUP TYPICUP VISIBLE NONE;MAXSUBDOWN MAXSUBDOWN VISIBLE NONE;MAXSUBUP MAXSUBUP VISIBLE NONE;CONFIDENCE CONFIDENCE HIDDEN NONE;PRICE PRICE VISIBLE NONE;STATEABBR STATEABBR VISIBLE NONE;ENDUSERCAT ENDUSERCAT VISIBLE NONE;WHO WHO HIDDEN NONE;WHEN WHEN HIDDEN NONE;Shape_Length Shape_Length HIDDEN NONE;Shape_Area Shape_Area HIDDEN NONE")
except:
    print "YOU FAIL"
try:
	# Process: Apply Symbology From Layer (2)
	arcpy.ApplySymbologyFromLayer_management(wireless_Layer, symbology_lyr)
except:
    print "YOU FAIL"
try:
	# Process: Layer To KML (2)
	arcpy.LayerToKML_conversion(wireless_symbology_lyr, v_String__wireless_kmz, "0", "false", "DEFAULT", "1024", "96", "CLAMPED_TO_GROUND")
except:
    print "YOU FAIL"
try:
	# Process: Make Feature Layer (3)
	arcpy.MakeFeatureLayer_management(plss, plss_layer, "", "", "OBJECTID OBJECTID VISIBLE NONE;Shape Shape VISIBLE NONE;PROVALIAS PROVALIAS VISIBLE NONE;PROVNAME PROVNAME VISIBLE NONE;DBANAME DBANAME VISIBLE NONE;FRN FRN VISIBLE 	NONE;TRANSTECH TRANSTECH VISIBLE NONE;MAXADDOWN MAXADDOWN VISIBLE NONE;MAXADUP MAXADUP VISIBLE NONE;TYPICDOWN TYPICDOWN VISIBLE NONE;TYPICUP TYPICUP VISIBLE NONE;MAXSUBDOWN MAXSUBDOWN VISIBLE NONE;MAXSUBUP MAXSUBUP VISIBLE 	NONE;PRICE 		PRICE VISIBLE NONE;CONFIDENCE CONFIDENCE HIDDEN NONE;PROVIDER_TYPE PROVIDER_TYPE VISIBLE NONE;ENDUSERCAT ENDUSERCAT VISIBLE NONE;PLSSID PLSSID HIDDEN NONE;REFGRIDNO REFGRIDNO HIDDEN NONE;OIT_ID OIT_ID HIDDEN NONE;WHO WHO HIDDEN 		NONE;WHEN 	WHEN HIDDEN NONE;Shape_Length Shape_Length HIDDEN NONE;Shape_Area Shape_Area HIDDEN NONE")
except:
    print "YOU FAIL"
try:
	# Process: Apply Symbology From Layer
	arcpy.ApplySymbologyFromLayer_management(plss_layer, symbology_lyr)
except:
    print "YOU FAIL"
try:
	# Process: Layer To KML (3)
	arcpy.LayerToKML_conversion(plss_symbology_lyr, v_String__plss_kmz, "0", "false", "DEFAULT", "1024", "96", "CLAMPED_TO_GROUND")
except:
    print "YOU FAIL"