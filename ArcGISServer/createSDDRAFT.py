import arcpy
import xml.dom.minidom as DOM

mapDoc = arcpy.mapping.MapDocument('C:/Users/rezaghok/Desktop/baseData.mxd')
service = 'Counties'
sddraft = 'C:/Users/rezaghok/Desktop/' + service + '.sddraft'
sd = 'C:/Users/rezaghok/Desktop/' + service + '.sd'
inMaxRecordCount = 9999
arcpy.mapping.CreateMapSDDraft(mapDoc, sddraft, service, 'ARCGIS_SERVER')
# Set service type to esriServiceDefinitionType_Replacement
arcpy.AddMessage("Setting the service type to be a replacement.")

newType = 'esriServiceDefinitionType_Replacement'
xml = sddraft
doc = DOM.parse(xml)
descriptions = doc.getElementsByTagName('Type')
for desc in descriptions:
    if desc.parentNode.tagName == 'SVCManifest':
        if desc.hasChildNodes():
            desc.firstChild.data = newType
outXml = xml
f = open(outXml, 'w')
doc.writexml( f )
f.close()
keys = doc.getElementsByTagName('Key')
for key in keys:
    if key.hasChildNodes():
        if key.firstChild.data == 'maxRecordCount':
            # modify the TextAntiAliasingMode value
            key.nextSibling.firstChild.data = inMaxRecordCount
f = open(outXml, 'w')
doc.writexml( f )
f.close()


