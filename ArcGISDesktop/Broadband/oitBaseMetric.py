
# ---------------------------------------------------------------------------
# OITBaseMetricv01.py
# Created on: 2015-10-05 by: Kass Rezagholi
#
#
# Description: Use this script to create a base metric feature class that will
# be used in a variety of future scripts.  This will essentially take census
# block household data and apply it into PLSS QQ's gathered by OIT.  Only areas
# where there is known infrastructure will be in the result.
#
# ---------------------------------------------------------------------------


import arcpy

# Script arguments
workspace = arcpy.GetParameterAsText(0) #Pre-created gdb to put results
censusid = arcpy.GetParameterAsText(1) #censusid from metrics on local
plss = arcpy.GetParameterAsText(2) #OITFinalTemplate plss featureclass
OIT_PLSS_QQ = arcpy.GetParameterAsText(3) #OIT_PLSS_QQ base template
ColoradoAddresses = arcpy.GetParameterAsText(4) #Current Address data set

#Workspace
arcpy.env.workspace = workspace
arcpy.env.overwriteOutput = True

# Local variables:
addressPointsOutside = "addressPointsOutside"
addressPLSSSJ = "addressPLSSSJ"
plssMerge = "plssMerge"
plssMerge_Dissolve =  "plssMerge_Dissolve"
baseMetrics = "baseMetrics"
baseMetricsCount = "baseMetricsCount"

# Process: Erase

arcpy.AddMessage("Starting OIT PLSS Metrics script.")
arcpy.Erase_analysis(ColoradoAddresses, plss, "addressPointsOutside", "")
print "Erase complete."
arcpy.AddMessage("Erase complete.")
#Process: Spatial Join

arcpy.SpatialJoin_analysis(OIT_PLSS_QQ, addressPointsOutside, "addressPLSSSJ", "JOIN_ONE_TO_ONE", "KEEP_COMMON")
print "Spatial join complete."
arcpy.AddMessage("Spatial join complete.")

#Process: Merge
arcpy.Merge_management([plss, addressPLSSSJ], "plssMerge")
print "Merge Complete."
arcpy.AddMessage("Merge Complete.")

# Process: Dissolve

arcpy.Dissolve_management(plssMerge, "plssMerge_Dissolve", "OIT_ID", "", "MULTI_PART", "DISSOLVE_LINES")
arcpy.AddMessage("Dissolve complete.")

# Process: Intersect

arcpy.Intersect_analysis([plssMerge_Dissolve, censusid], "baseMetrics", "ALL", "", "INPUT")
arcpy.AddMessage("Intersect complete.")

# Format baseMetrics and calculate adjusted households field

arcpy.AddField_management(baseMetrics, "Adjusted_HseHolds", "DOUBLE")
arcpy.Frequency_analysis(baseMetrics, baseMetricsCount, "GEOID10", )
arcpy.JoinField_management(baseMetrics, "GEOID10", baseMetricsCount, "GEOID10", "FREQUENCY")
arcpy.CalculateField_management(baseMetrics, "Adjusted_HseHolds", "[HseHolds] / [Frequency]", "VB")
arcpy.AddMessage("Adjusted_HseHolds added.")

# Delete temp files not needed
arcpy.Delete_management(addressPLSSSJ)
arcpy.Delete_management(addressPointsOutside)
arcpy.Delete_management(plssMerge)
arcpy.Delete_management(baseMetricsCount)
arcpy.Delete_management(plssMerge_Dissolve)
arcpy.AddMessage("Temp files deleted.")
