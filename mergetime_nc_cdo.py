#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

import pcraster as pcr

# starting and end years
sta_year = ['1958', '2008']
end_year = ['2007', '2015']

clone_area = "M05"

# main output folder
main_output_folder = "/scratch-shared/edwinhs/pcrglobwb2_output_gmd_paper_rerun_201902XX/05min/non-natural_1_fat_node/merged/" + clone_area + "/" 
# - prepare the directory
if os.path.exists(main_output_folder) == False: os.makedirs(main_output_folder)
cmd = "rm -r " + main_output_folder + "/*"
print(cmd)
os.system(cmd)


# location of netcdf input files
pcrglobwb_output_folder = "/scratch-shared/edwinhs/pcrglobwb2_output_gmd_paper_rerun_201902XX/05min/non-natural_1_fat_node/"
# - list of netcdf input files
pcrglobwb_output_files = [
'channelStorage_monthAvg_output.nc',
'discharge_monthAvg_output.nc',
'dynamicFracWat_monthAvg_output.nc',
'precipitation_monthTot_output.nc',
'runoff_monthTot_output.nc',
'satDegLow_monthAvg_output.nc',
'satDegUpp_monthAvg_output.nc',
'storGroundwaterFossil_monthAvg_output.nc',
'storGroundwater_monthAvg_output.nc',
'storLowTotal_monthAvg_output.nc',
'storUppTotal_monthAvg_output.nc',
'surfaceWaterStorage_monthAvg_output.nc',
'temperature_monthAvg_output.nc',
'totalActiveStorageThickness_monthAvg_output.nc',
'totalEvaporation_monthTot_output.nc',
'totalRunoff_monthTot_output.nc',
'totalWaterStorageThickness_monthAvg_output.nc',
'referencePotET_monthTot_output.nc',
'waterBodyActEvaporation_monthTot_output.nc',
'waterBodyPotEvaporation_monthTot_output.nc',
'totalLandSurfacePotET_monthTot_output.nc',
'totalPotentialEvaporation_monthTot_output.nc'
]


# initiating cmd line
cdo_cmd_line = ""

for file_name in pcrglobwb_output_files:
    
    # an example of cdo line: cdo -L -mergetime -selyear,1958/2007 ../../*1958/M02/netcdf/precipitation_monthTot_output.nc -selyear,2008/2015 ../../*2008/M02/netcdf/precipitation_monthTot_output.nc precipitation_monthTot_output.nc
    
    
    # cdo main command
    cdo_cmd_line += 'cdo -L -mergetime' 
    
    # input netcdf file names and selecting years 
    for i_year in range(0, len(sta_year)):
        cdo_cmd_line += ' -selyear,' + sta_year[i_year] + "/" + end_year[i_year] + " " + pcrglobwb_output_folder + "/*" + sta_year[i_year] + "/" + clone_area + "/netcdf/" + file_name
    
    # output netcdf file
    cdo_cmd_line += " " + main_output_folder + "/" + file_name
    
    # make it parallel
    cdo_cmd_line += ' & '

cdo_cmd_line += "wait"
print(cdo_cmd_line)
os.system(cdo_cmd_line)


