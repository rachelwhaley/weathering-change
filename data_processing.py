import sys 
import pandas as pd 

STATION_COLS = [(0,11), (12,20), (21,30), (31,37), (38,40),
                (41,70), (72,75), (76,79), (80,86), (87,None)]

# blanks are -9999
# P = provisinal, filter out?

# result row for each hour for a year
# column for each city

# feed in all the files (13 weather files)
# all files need headers


# read in the stations
# process as fixed width
# get zip codes from zips file
def station_config(station_file): # , zip_file):
    # column definitions at https://www1.ncdc.noaa.gov/pub/data/normals/1981-2010/readme.txt
    stations_df = pd.read_fwf(station_file, 
                              colspecs = STATION_COLS, 
                              names = ['station_code', 'lat', 'lon', 'elevation', 'state', 'name', 'gsn_flag', 'hcn_flag', 'wmo_id', 'method'])
    print(stations_df.shape)
    print(stations_df.iloc[:3])
    return 

# read in each weather attribute

if __name__=='__main__':
    if len(sys.argv) == 0:
        print("Usage: ")
    station_config(sys.argv[1])