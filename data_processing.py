import sys 
import pandas as pd 

STATION_COLS = [(0,11), (12,20), (21,30), (31,37), (38,40),
                (41,70), (72,75), (76,79), (80,86), (87,None)]
ZIP_COLS = [(0,11), (12,17), (18,None)]

# blanks are -9999
# P = provisinal, filter out?

# result row for each hour for a year
# column for each city

# feed in all the files (13 weather files)
# all files need headers

# process the fixed width files
def station_config(station_file, zip_file):
    # column definitions at https://www1.ncdc.noaa.gov/pub/data/normals/1981-2010/readme.txt
    stations_df = pd.read_fwf(station_file, 
                              colspecs = STATION_COLS, 
                              names = ['station_code', 'lat', 'lon', 'elevation', 'state', 'name', 'gsn_flag', 'hcn_flag', 'wmo_id', 'method'])
    print(stations_df.shape)
    print(stations_df.iloc[:3])

    zip_df = pd.read_fwf(zip_file, colspecs = ZIP_COLS, names = ['station_code', 'zip_code', 'city'])
    print(zip_df.shape)
    print(zip_df.iloc[:3])
    result_df = pd.merge(stations_df, zip_df, on='station_code', how='left')
    print(result_df.iloc[:20])
    return result_df

# read in each weather attribute

if __name__=='__main__':
    if len(sys.argv) == 0:
        print("Usage: ")
    station_config(sys.argv[1], sys.argv[2])