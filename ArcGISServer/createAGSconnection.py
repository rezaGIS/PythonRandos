#Modified ESRI's Create AGS Connection script.
# This will iterate through all of OIT's AGS urls and create a connection
# file (.ags) that can be used with OIT's service publishing script.
# Use this script to create new .ags files when there are any changes
# to ArcGIS for Server instance name / location and/or changes to the
# admin credentials.

import arcpy

outdir = 'C:/users/rezaghok/desktop/agsConnections'
out_folder_path = outdir
out_names = ['dev_104.ags',
             'secureActive_105.ags',
             'securePassive_106.ags',
             'gpActive_107.ags',
             'gpPassive_108.ags',
             'publicActive_109.ags',
             'publicPassive_110.ags']
server_urls = ['https://yoururl/oit/admin',
               'https://yoururl/secure/admin',
               'https://yoururl/secure/admin',
               'https://yoururl/gp/admin',
               'https://yoururl/gp/admin',
               'https://yoururl/public/admin',
               'https://yoururl/public/admin']
use_arcgis_desktop_staging_folder = False
staging_folder_path = outdir
username = 'username'
password = 'passsword'
# used for array to match items
i = 0
for server_url in server_urls:
    saveLocation = out_names[i]
    arcpy.mapping.CreateGISServerConnectionFile("ADMINISTER_GIS_SERVICES",
                                                out_folder_path,
                                                saveLocation,
                                                server_url,
                                                "ARCGIS_SERVER",
                                                use_arcgis_desktop_staging_folder,
                                                staging_folder_path,
                                                username,
                                                password,
                                                "SAVE_USERNAME")
    i += 1