#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

import pcraster as pcr

# period selected
sta_year = 1990
end_year = 2010

# main output folder
main_output_folder = "/scratch-shared/edwin/water_temperature/only_climatology/" + str(sta_year) + "_to_" + str(end_year) + "/"
# - prepare the directory
if os.path.exists(main_output_folder) == False: os.makedirs(main_output_folder)
cmd = "rm -r " + main_output_folder + "/*"
print(cmd)
os.system(cmd)

# location of netcdf input files
pcrglobwb_output_folder = "/scratch-shared/edwinhs/water_temperature_niko/"
# - list of netcdf input files
pcrglobwb_output_files = [
"waterTemperature_monthAvg_1990_to_2010.nc"
]

for file_name in pcrglobwb_output_files:
    
    # input netcdf file name
    input_nc_file = pcrglobwb_output_folder + "/" + file_name
    
    # making output directory
    output_directory = main_output_folder + "/" + file_name.split("_")[0] + "/"
    if os.path.exists(output_directory) == False: os.makedirs(output_directory)

    # climatology output netcdf file name 
    climatology_nc_file = output_directory + "/" + file_name.split(".")[0] + "_climatology_" + \
                                                   str(sta_year) + "_to_" + str(end_year) + ".nc"
    
    # using cdo to calculate climatology over a certain period
    # - an example: cdo -L -f nc4 -z zip -ymonavg -selyear,1990/2010 discharge_monthAvg_output.nc discharge_monthAvg_climatology_1990_to_2010.nc
    cmd = 'cdo -L -f nc4 -z zip -ymonavg -selyear,' + str(sta_year) + "/" + str(end_year) + " " +\
                                                      input_nc_file + " " +\
                                                      climatology_nc_file
    print(cmd)
    os.system(cmd)

    # selecting the lat lon block extent
    # - input netcdf file 
    inp_global_climatology_nc_file = climatology_nc_file
    # - extent of study area, e.g. sellonlatbox,120,-90,20,-20
    sellonlatbox_argument = "-sellonlatbox,120,-90,20,-20" 
    # - output netcdf file 
    climatology_nc_file = output_directory + "/" + "study_area" + "_" + file_name.split(".")[0] + "_climatology_" + \
                                                   str(sta_year) + "_to_" + str(end_year) + ".nc"
    cmd = 'cdo -L -f nc4 -z zip ' + sellonlatbox_argument + " " + inp_global_climatology_nc_file + " " +\
                                                                  climatology_nc_file
    print(cmd)
    os.system(cmd)
    
    # split the climatology nc file per month
    for i_month in range(1, 12 +1):
        
        # nc file for every month
        month_in_string = str(i_month)
        if i_month < 10: month_in_string = "0" + month_in_string
        monthly_nc_file = climatology_nc_file.split(".")[0] + "_month_" + month_in_string + ".nc"
        
        # using cdo to select the time step
        # - an example: cdo -L -f nc4 -z zip -seltimestep,1 discharge_monthAvg_climatology_1990_to_2010.nc discharge_monthAvg_climatology_1990_to_2010_month_01.nc
        cmd = 'cdo -L -f nc4 -z zip -seltimestep,' + str(i_month) + " " +\
                                                     climatology_nc_file + " " +\
                                                     monthly_nc_file
        print(cmd)
        os.system(cmd)
        
        # convert nc file to a pcraster map
        cmd = 'gdal_translate -of PCRaster ' + monthly_nc_file + " " +\
                                               monthly_nc_file.split(".")[0] + ".map"
        print(cmd)
        os.system(cmd)



