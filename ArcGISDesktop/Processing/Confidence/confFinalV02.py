#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
# Author:      seiferdb
# Created:     05/01/2017
# Copyright:   (c) seiferdb 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import os
import sys
import arcpy

def writeMessage(messageText):
	print messageText
	arcpy.AddMessage(messageText)

writeMessage("Imported Libraries: Success")

##confTable = r'C:\Users\filipiaa\Desktop\Broadband\Confidence\CursorErrorTesting\Data.gdb\ConfidenceData'
##plssProvStaging = r'C:\Users\filipiaa\Desktop\Broadband\Confidence\CursorErrorTesting\Data.gdb\bigsandyplss'
##wirelessProvStaging = ""

confTable = arcpy.GetParameterAsText(0)
plssProvStaging = arcpy.GetParameterAsText(1)
wirelessProvStaging = arcpy.GetParameterAsText(2)

writeMessage("Required data submitted, please stand by...")

cCursor = arcpy.SearchCursor(confTable)
for row in cCursor:
# Gets all the attributes from each row that will be used to work out the confidence score,
#    Key = row.getValue('Key')

    ProvAliasConfidence = row.getValue('ProvAliasConfidence')
#    print(ProvAliasConfidence) # Debuging it, right. . . at least slowly
    writeMessage(("Working on provider " + ProvAliasConfidence + "..."))
    ServiceType = row.getValue('ServiceType')
    writeMessage(("Provider type: " + ServiceType + "..."))
#    print(ServiceType) # debugging helper

# Type of provider
    RawDataTypeLandline = row.getValue('LandlineRawDataType')
    print(RawDataTypeLandline)
    RawDataTypeWireless = row.getValue('WirelessRawDataType')
    print(RawDataTypeWireless)
# Updates for data
    UpdatesLandline = row.getValue('LandlineUpdates')
    UpdatesWireless = row.getValue('WirelessUpdates')
# Midmile accounted for
    MidmileLL = row.getValue('LandlineMidmile')
    MidmileWR = row.getValue('WirelessMidmile')
# Midmile attributes
    MidmileLatLong = row.getValue('MidmileLatLong')
    MidmileBHCAP = row.getValue('MidmileBHCapacity')
    MidmileBHType = row.getValue('MidmileBHType')
    MidmileOwnership = row.getValue('MidmileOwnership')
    MidmileElevation = row.getValue('MidmileElevation')
# plss Attributes
    PLSSSubSpeeds = row.getValue('PLSSSubSpeeds')
    PLSSEndUserCat = row.getValue('PLSSEndUserCat')
    PLSSTypSpeeds = row.getValue('PLSSTypSpeeds')
    PLSSPrice = row.getValue('PLSSPrice')
# Wireless Attributes
    WirelessSubSpeeds = row.getValue('WirelessSubSpeeds')
    WirelessEndUserCat = row.getValue('WirelessEndUserCat')
    WirelessTypSpeeds = row.getValue('WirelessTypSpeeds')
    WirelessPrice = row.getValue('WirelessPrice')

# Freshness - yeah you read that right, we need data that is
# less then two years old or its skunked

    FreshnessLL = row.getValue('LandlineFreshness')
    FreshnessWR = row.getValue('WirelessFreshness')
 # ########################################################
# #########################################################
 # ########################################################
# Wireless data type - Step 1

    if (((ServiceType == 'Wireless') or (ServiceType == 'Both'))  and (RawDataTypeWireless == 'PropagatedModel')):
        wrlss = 90
        print(wrlss)
    elif (((ServiceType == 'Wireless') or (ServiceType == 'Both')) and (RawDataTypeWireless == 'RadioMobile')):
        wrlss = 100
        print(wrlss)
    elif (((ServiceType == 'Wireless') or (ServiceType == 'Both')) and (RawDataTypeWireless == 'ShapeMisc')):
        wrlss = 70
        print(wrlss)
    elif (ServiceType  == ''):
        wrlss = 100
        print(wrlss)
    else:
        pass

# Land line data type Step 1

    if (((ServiceType == 'Both') or (ServiceType == 'Landline')) and (RawDataTypeLandline == 'ShapeMisc')):
        plss = 70
        print(plss)
    elif (((ServiceType == 'Landline') or (ServiceType == 'Both')) and (RawDataTypeLandline == 'LatLong')):
        plss = 90
        print(plss)
    elif (((ServiceType == 'Both') or (ServiceType == 'Landline')) and (RawDataTypeLandline == 'Address')):
        plss = 100
        print(plss)
    elif (((ServiceType == 'Landline') or (ServiceType == 'Both')) and (RawDataTypeLandline == 'Census')):
        plss = 50
        print(plss)
    elif (ServiceType  == ''):
        plss = 100
        print(plss)
    else:
        pass


 # ########################################################
# #########################################################
 # ########################################################

# Data Updates, pre-existing metric removed from original data type score, see Step 1
# Or nothing removed from pre-exisiting data type score
# Landline data type step 2

    if UpdatesLandline == "OldDataFail":
        ##upDLL = .5
        upDLLF = (plss *.5)
        print(upDLLF)
    elif UpdatesLandline == "OldDataPass":
        ##upDLL = .8
        upDLLF = (plss *.8)
        print(upDLLF)
    elif UpdatesLandline == 'FreshData':
        ##upDLL = ((plss) *1)
        upDLLF = (plss *1)
        print(upDLLF)
    elif UpdatesLandline == 'FreshDataIncomplete':
        upDLL = (plss *.05)
        upDLLF = (plss - upDLL)
        print(upDLLF)
    elif UpdatesLandline == 'NA':
        ##upDLL = (plss) * 1
        upDLLF = (plss *1)
        print(upDLLF)
    else:
        pass

# Below as above, the metrics are recalcualted based on the update value, wireless below
# Wireless data type step 2
    if UpdatesWireless == "OldDataFail":
        ##upDLW = ((wrlss) * .5)
        ##upDLWF = (wrlss - upDLW)
        upDLWF = ((wrlss) *.5)
        print(upDLWF)
    elif UpdatesWireless == "NA":
        upDLWF = ((wrlss) * 1)
        print(upDLWF)
    elif UpdatesWireless == 'FreshData':
        upDLWF = ((wrlss) *1)
        print(upDLWF)
    elif UpdatesWireless == 'FreshDataIncomplete':
        ##upDLWF = (wrlss) - .05
        upDLW = ((wrlss) *.05)
        upDLWF = (wrlss - upDLW)
        print(upDLWF)
    elif UpdatesWireless == "OldDataPass":
        ##upDLW = ((wrlss) * .80)
        ##upDLWF = (wrlss - upDLW)
        upDLWF = ((wrlss) *.8)
        print(upDLWF)
    else:
        pass
# The below section checks for the existence of midmile sumbission and removes a pre-determined metric when appropriate
# plss/landline submissions do not require a midmile and none is requested in out reach so no penelty is applied if the
# midmile data is not part of the submission, the wireless submissions are reduced if no midmile is present

    if ((MidmileLL == 1) and ((ServiceType =='Landline') or (ServiceType == 'Both'))):
        ##mMile = 1.0
        ##llmMile = plss
        llDtFin = upDLLF
        print(llDtFin)
    elif((MidmileLL == 0) and ((ServiceType == 'Landline') or (ServiceType == 'Both'))):
        mMile = .05
        llmMile = (upDLLF * mMile)
        llDtFin = (upDLLF - llmMile)
        print(llDtFin)
    else:
        pass
    if ((MidmileWR == True) and ((ServiceType == 'Wireless') or (ServiceType == 'Both'))):
        ##mMile = 1.0
        ##wrlssmMile = (wrlss * mMile)
        wrlssDtFin = upDLWF
        print(wrlssDtFin)
    elif ((MidmileWR == False) and ((ServiceType == 'Wireless') or (ServiceType == 'Both'))):
        mMile = .25
        wrlssmMile = (upDLWF * mMile)
        wrlssDtFin = (upDLWF - wrlssmMile)
        print(wrlssDtFin)
    else:
        pass




##    if ((Midmile == 0.0) and ((ServiceType == 'Wireless') or (ServiceType == 'Both'))):
##        Mmile = .25
##        wrlssMidmile = (wrlss * Mmile)
##        wrlssDtFin = (upDLW - wrlssMidmile)
##    elif ((Midmile == 1.00) and ((ServiceType == 'Wireless') or (ServiceType == 'Both'))):
##        wrlssDtFin = (upDLW)
##    elif((Midmile == 0.0) and ((ServiceType == 'Landline') or (ServiceType == 'Both'))):
##        Mmile = 1.00 #.05
##        llMidmile = (plss * Mmile)
##        llDtFin = (upDLL - llMidmile)
##    elif ((Midmile == 1.00) and ((ServiceType == 'Landline') or (ServiceType == 'Both'))):
##        llDtFin = (upDLL)
##    else:
##        pass

    if (MidmileWR == 1): # and (ServiceType == 'Wireless')):
        mmll = (MidmileLatLong * 50)
        mmbhc = (MidmileBHCAP * 30)
        mmbht = (MidmileBHType * 12)
        mmO = (MidmileOwnership * 3)
        mmel = (MidmileElevation * 5)
        mmWAtts = (mmll + mmbhc + mmbht + mmO +mmel)
        print(mmWAtts)
    elif (MidmileWR == 0): # and (ServiceType == 'Wireless')):
        mmWAtts = 0
        print(mmWAtts)
    else:
        pass

    if (MidmileLL == 1): # and (ServiceType == 'Wireless')):
        mmll = (MidmileLatLong * 50)
        mmbhc = (MidmileBHCAP * 30)
        mmbht = (MidmileBHType * 12)
        mmO = (MidmileOwnership * 3)
        mmel = (MidmileElevation * 5)
        mmLAtts = (mmll + mmbhc + mmbht + mmO +mmel)
        print(mmLAtts)
    elif (MidmileLL == 0): # and (ServiceType == 'Wireless')):
        mmLAtts = 0
        print(mmLAtts)
    else:
        pass


    if ((ServiceType == 'Wireless') or (ServiceType == 'Both')): # or ServiceType == 'Landline' # Additional Attributes
        sbSps = (WirelessSubSpeeds * 35)
        ndsrct = (WirelessEndUserCat * 5)
        typspds = (WirelessTypSpeeds * 5)
        prc = (WirelessPrice * 25)
        mmW = (mmWAtts * .30)
        Watrbt = (sbSps + ndsrct + typspds + prc + mmW) # Attribute value calculation with midmile . . . Final attribute value
        print(Watrbt)
    else:
        pass
    if ((ServiceType == 'Landline') or (ServiceType == 'Both')):
        sbSps = (PLSSSubSpeeds * 35)
        ndsrct = (PLSSEndUserCat * 5)
        typspds = (PLSSTypSpeeds * 5)
        prc = (PLSSPrice * 25)
        mmL = (mmLAtts * .30)
        Latrbt = (sbSps + ndsrct + typspds + prc + mmL)
        print(Latrbt)
    else:
        pass

    if (FreshnessWR == 1):
        Wfrshns = 100
        print(Wfrshns)
    elif(FreshnessWR == 0):
        Wfrshns = 0
        print(Wfrshns)
    else:
        pass

    if (FreshnessLL == 1): #$ Freshness data score, that is all
        Lfrshns = 100
        print(Lfrshns)
    elif (FreshnessLL == 0):
        Lfrshns = 0
        print(Lfrshns)
    else:
        pass
##
##    if (Freshness == True) and (ServiceType == 'Landline'): # Freshness data score, that is it, all there is to it...
##        frshns = 1
##    elif (Freshness == False) and (ServiceType == 'Landline'):
##        frshns = 0
##    else:
##        pass
# ###########################################################################################################################################
# ###########################################################################################################################################
    if (ServiceType == 'Wireless') or (ServiceType == "Both"):
        ##preWrFinal = ((frshns *.25) + (Watrbt *.25) + (wrlssDtFin * .5))
        ##wrFinal = (preWrFinal*100)
        wrFinal = ((Wfrshns *.25) + (Watrbt *.25) + (wrlssDtFin * .5))
#        wrFinal= (round(preWrFinal, 2)*100)
        writeMessage(("Final Confidence score: " + str(wrFinal)  + " Wireless"))
    else:
        pass

    if (ServiceType == "Landline") or (ServiceType == "Both"):
        ##prellFinal = ((frshns *.25) + (Latrbt *.25) + (llDtFin * .5))
        ##llFinal = (prellFinal*100)
        llFinal = ((Lfrshns *.25) + (Latrbt *.25) + (llDtFin * .5))
#        llFinal = (round(prellFinal, 2)*100)
        writeMessage(("Final Confidence score: " + str(llFinal) + " Landline"))
    else:
        pass

    if plssProvStaging <> "":
        llCursor = arcpy.UpdateCursor(plssProvStaging)
        for roww in llCursor:
            provalias = roww.getValue('PROVALIAS')
#            print("Plss Provalaias: " + provalias)
            if (provalias == ProvAliasConfidence):
                roww.setValue('CONFIDENCE', round(llFinal))
                llCursor.updateRow(roww)
    else:
        pass

    if wirelessProvStaging <> "":
        wrCursor = arcpy.UpdateCursor(wirelessProvStaging)
        for row2 in wrCursor:
            provalias = row2.getValue('PROVALIAS')
#            print("Wrless Provalias: " + provalias)
            if (provalias == ProvAliasConfidence):
                row2.setValue('CONFIDENCE', round(wrFinal))
                wrCursor.updateRow(row2)
    else:
        pass