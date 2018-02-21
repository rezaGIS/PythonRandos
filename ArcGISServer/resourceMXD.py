import arcpy, os
#used for debugging to find sde path
#mxd = arcpy.mapping.MapDocument(r"C:\Users\rezaghok\Desktop\DWR\MapserviceMXDs\Stage\DNR\County_Parcel_OIT.mxd")
#for lyr in arcpy.mapping.ListLayers(mxd):
    #print lyr.dataSource
folderPath = r"C:\Users\rezaghok\Desktop\DWR\MapserviceMXDs\Stage\DNR"
for filename in os.listdir(folderPath):
    fullpath = os.path.join(folderPath, filename)
    if os.path.isfile(fullpath):
        basename, extension = os.path.splitext(fullpath)
        if extension.lower() == ".mxd":
            mxd = arcpy.mapping.MapDocument(fullpath)
            mxd.findAndReplaceWorkspacePaths(r"C:\DNRScripts\DB_Connect\Staging_10.12.1.40.sde", r"C:\Users\rezaghok\Desktop\SDEConnection\Production_OITPRDDB.sde")
            mxd.save()
del mxd