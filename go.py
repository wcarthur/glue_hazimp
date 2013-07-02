
"""
Script to test running TCRM and HazImp combined.

"""
import os

from subprocess import call

from Utilities import nc2txt

from core_hazimp import hazimp

# Run TCRM
ini_file = os.path.abspath("port_hedland.ini")
print "ini_file", ini_file
call(["python", "../tcrm/main.py", ini_file])

# Convert the .nc gust files to ...
ncpath = os.path.join('output', 'port_hedland', 'windfield')
ncfiles = os.listdir(ncpath)
 
ncfiles = [x for x in ncfiles if x[-3:] == '.nc']
gridfiles = [os.path.abspath(os.path.join(ncpath, 
                                          x[:-2] + 'txt')) for x in ncfiles]



for ncfile in ncfiles:
    ncfile =  os.path.abspath(os.path.join(ncpath, ncfile))
    call(["python", "../tcrm/Utilities/nc2txt.py", "-v", "vmax", 
          "--filename", ncfile])

# Run HazImp
exp_file = 'qldsmall.csv'
exp_file = 'smaller_quoted.csv'
exp_file = 'smaller_missing.csv'
exp_file = 'QLD_Residential_Wind_Exposure_201212_for_TCRM.CSV'

exp_filename = os.path.abspath(
    os.path.join('..', 'exposure_data', exp_file))

config = {
    'template': 'windv1',
    'load_csv_exposure': {'file_name': exp_filename,
                      'exposure_latitude': 'LATITUDE',
                      'exposure_longitude': 'LONGITUDE'},
    'load_wind_tcrm_ascii': [gridfiles[1]],
    'save': 'impact.npz'}
    
# It takes a while
hazimp.main(config_dic=config)
