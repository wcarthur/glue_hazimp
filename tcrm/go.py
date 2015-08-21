"""
Script to test running TCRM and HazImp combined.

This is meant to execute a TCRM simulation then execute HazImp, using
the wind field(s) generated by TCRM as input. Presently only executes
HazImp, reading the list of '.nc' files from the output directory of
TCRM.

"""
import os
from os.path import abspath, join as pjoin
from core_hazimp import hazimp

# Run TCRM
ini_file = os.path.abspath("port_hedland.ini")
print "ini_file", ini_file
#call(["python", "../../tcrm/tcrm.py -c ", ini_file])

# Convert the .nc gust files to ...
ncpath = os.path.join('output', 'port_hedland', 'windfield')
ncfiles = [abspath(pjoin(ncpath, x)) for x in
           os.listdir(ncpath) if x.endswith('.nc')]

# Run HazImp
exp_file = 'QLD_Residential_Wind_Exposure_201212_for_TCRM.CSV'

exp_filename = abspath(pjoin('..', 'exposure_data', exp_file))

config = [
    {'template': 'wind_v3'},
    {'load_exposure': {'file_name': exp_filename,
                      'exposure_latitude': 'LATITUDE',
                      'exposure_longitude': 'LONGITUDE'}},
    {'load_wind_ascii': gridfiles},
    {'calc_struct_loss':
        {'replacement_value_label': 'REPLACEMENT_VALUE'}},
    {'save': 'impact_all.csv'}]
    
# It takes a while
hazimp.start(config_list=config)
