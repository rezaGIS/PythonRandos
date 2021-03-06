
# ---------------------------------------------------------------------------
# terrifixmax_4_1v01.py
# Created on: 2015-10-15 by Kassrah Rezagholi
#   (generated by ArcGIS/ModelBuilder)
# Usage: terrifixmaxv01 <baseMetrics> <OIT_PLSS_QQ> <plss> <workspace> <wireless>
# Description: Use this script after running OITbaseMetrics.
# Use local data to improve efficiency, running over network could cause
# script to crash due to network connectivity issues.  Script will seperate
# maximum advertised speeds meeting FCC minimum standards and are residential
# services and apply to OITBaseMetrics.
# ---------------------------------------------------------------------------

# Import arcpy module
import arcpy

# Script arguments
baseMetrics = arcpy.GetParameterAsText(1) #r"C:\Users\rezaghok\Desktop\SCRATCH\metricsForMegan\southwestColorado\base.gdb\baseMetricsw" #arcpy.GetParameterAsText(1)

OIT_PLSS_QQ = arcpy.GetParameterAsText(2) #r"C:\GOIT\BaseData\base_data.gdb\OIT_PLSS_QQ" #arcpy.GetParameterAsText(2)
plss = arcpy.GetParameterAsText(3) #r"C:\GOIT\Production_OCT2015\OITFinal\OITFinalTemplate.gdb\plss" #arcpy.GetParameterAsText(2)
workspace = arcpy.GetParameterAsText(0) #r"C:\Users\rezaghok\Desktop\SCRATCH\metricsForMegan\southwestColorado\scratch.gdb" #arcpy.GetParameterAsText(0)
wireless = arcpy.GetParameterAsText(4) #r"C:\GOIT\Production_OCT2015\OITFinal\OITFinalTemplate.gdb\wireless" #arcpy.GetParameterAsText(4)
# Set Workspace
arcpy.env.workspace = workspace
arcpy.env.overwriteOutput = True


# Local variables:
baseMetricsMove = "baseMetricsMove"
baseMetricsLayer = "baseMetricsLayer"
wirelineSelect = "wirelineSelect"
wirelessSelect = "wirelessSelect"
wirelessSpatialJoin = "wirelessSpatialJoin"
terrifix_merge = "terrifix_merge"
terrifix_dissolve = "terrifix_dissolve"
TERRIFIXMAX = "TERRIFIXMAX"

# Process: Make Feature Layer
arcpy.CopyFeatures_management(baseMetrics, "baseMetricsMove")

arcpy.MakeFeatureLayer_management(baseMetricsMove, "baseMetricsLayer", "", workspace, "OBJECTID OBJECTID VISIBLE NONE;Shape Shape VISIBLE NONE;FID_plssMerge_Dissolve FID_plssMerge_Dissolve VISIBLE NONE;OIT_ID OIT_ID VISIBLE NONE;FID_censusid FID_censusid VISIBLE NONE;COUNTYFP10 COUNTYFP10 VISIBLE NONE;GEOID10 GEOID10 VISIBLE NONE;POP100 POP100 VISIBLE NONE;HU100 HU100 VISIBLE NONE;HseHolds HseHolds VISIBLE NONE;Adjusted_HseHolds Adjusted_HseHolds VISIBLE NONE;FREQUENCY FREQUENCY VISIBLE NONE;Shape_Length Shape_Length VISIBLE NONE;Shape_Area Shape_Area VISIBLE NONE")

# Process: select 4/1 wireline
arcpy.Select_analysis(plss, "wirelineSelect", "MAXADDOWN >= 4 AND MAXADUP >=  1 AND ENDUSERCAT <> '2'")
arcpy.AddMessage("Selected all wireline meeting 4mbps download and 1mbps upload.")

# Process: select 4/1 fixed wireless
arcpy.Select_analysis(wireless, "wirelessSelect", "TRANSTECH BETWEEN 70 AND 71 AND MAXADDOWN >= 4 AND MAXADUP >=  1 AND ENDUSERCAT <> '2'")
arcpy.AddMessage("Selected all wireless meeting 4mbps download and 1mbps upload.")

# Process: Spatial Join
arcpy.SpatialJoin_analysis(OIT_PLSS_QQ, wirelessSelect, "wirelessSpatialJoin", "JOIN_ONE_TO_ONE", "KEEP_COMMON")
arcpy.AddMessage("Spatial joined wireless maximum advertised speeds into 'OIT_PLSS_QQ'.")

# Process: Merges\\workswce.gdb\\WirelessSelect2,PROVNAME,-1,-1;DBANAME \"DBANAME\" true true false 200 Text 0 0 ,First,#,C:\\Users\\rezaghok\\Desktop\\SCRATCH\\oitMetrics\\workspace.gdb\\WirelessSelect2,DBANAME,-1,-1;FRN \"FRN\" true true false 10 Text 0 0 ,First,#,C:\\Users\\rezaghok\\Desktop\\SCRATCH\\oitMetrics\\workspace.gdb\\WirelessSelect2,FRN,-1,-1;TRANSTECH \"TRANSTECH\" true true false 2 Short 0 0 ,First,#,C:\\Users\\rezaghok\\Desktop\\SCRATCH\\oitMetrics\\workspace.gdb\\WirelessSelect2,TRANSTECH,-1,-1;SPECTRUM \"SPECTRUM\" true true false 2 Short 0 0 ,First,#,C:\\Users\\rezaghok\\Desktop\\SCRATCH\\oitMetrics\\workspace.gdb\\WirelessSelect2,SPECTRUM,-1,-1;MAXADDOWN \"MAXADDOWN\" true true false 8 Double 0 0 ,Max,#,C:\\Users\\rezaghok\\Desktop\\SCRATCH\\oitMetrics\\workspace.gdb\\WirelessSelect2,MAXADDOWN,-1,-1;MAXADUP \"MAXADUP\" true true false 8 Double 0 0 ,Max,#,C:\\Users\\rezaghok\\Desktop\\SCRATCH\\oitMetrics\\workspace.gdb\\WirelessSelect2,MAXADUP,-1,-1;CONFIDENCE \"CONFIDENCE\" true true false 8 Double 0 0 ,First,#,C:\\Users\\rezaghok\\Desktop\\SCRATCH\\oitMetrics\\workspace.gdb\\WirelessSelect2,CONFIDENCE,-1,-1;PRICE \"PRICE\" true true false 8 Double 0 0 ,First,#,C:\\Users\\rezaghok\\Desktop\\SCRATCH\\oitMetrics\\workspace.gdb\\WirelessSelect2,PRICE,-1,-1;STATEABBR \"STATEABBR\" true true false 2 Text 0 0 ,First,#,C:\\Users\\rezaghok\\Desktop\\SCRATCH\\oitMetrics\\workspace.gdb\\WirelessSelect2,STATEABBR,-1,-1;ENDUSERCAT \"ENDUSERCAT\" true true false 2 Text 0 0 ,First,#,C:\\Users\\rezaghok\\Desktop\\SCRATCH\\oitMetrics\\workspace.gdb\\WirelessSelect2,ENDUSERCAT,-1,-1", "INTERSECT", "", "")w
arcpy.Merge_management([wirelineSelect,wirelessSpatialJoin], "terrifix_merge")
arcpy.AddMessage("Merged wireless plss and wireline plss.")

# Process: Dissolve
arcpy.Dissolve_management(terrifix_merge, "terrifix_dissolve", "OIT_ID", "MAXADDOWN MAX;MAXADUP MAX", "MULTI_PART", "DISSOLVE_LINES")
arcpy.AddMessage("Dissolved merged wireless and wireline data.")

# Process: Join Field
arcpy.JoinField_management(baseMetricsLayer, "OIT_ID", terrifix_dissolve, "OIT_ID", "")
arcpy.AddMessage("Joined maximum advertised speeds into household data.")

# Process: Feature Class to Feature Class
arcpy.FeatureClassToFeatureClass_conversion(baseMetricsLayer, workspace, "TERRIFIXMAX")
arcpy.AddMessage("Created final 'TERRIFIXMAX' fc.")

#Clear Workspace
arcpy.DeleteFeatures_management(wirelessSelect)
arcpy.DeleteFeatures_management(baseMetricsMove)
arcpy.DeleteFeatures_management(terrifix_dissolve)
arcpy.DeleteFeatures_management(terrifix_merge)
arcpy.DeleteFeatures_management(wirelessSpatialJoin)
arcpy.DeleteFeatures_management(wirelineSelect)
arcpy.AddMessage("Workspace cleared of processing / scratch data.")