#-------------------------------------------------------------------------------
# Name:        Compass Imagery Directory
# Purpose:	   Simple tool to transfer folder structure
#
# Author:      Kass Rezagholi
#
# Created:     02/10/2017
# Copyright:   (c) rezaghok 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import shutil
from shutil import copytree, ignore_patterns
import os
source = "//10.12.1.221/gis-gcdp/applications/OAHP_Images/"
moveTo = "c:/users/rezaghok/desktop/test1234"
# create a backup directory
shutil.copytree(source, moveTo, ignore=ignore_patterns('*.pdf', '*.db'))