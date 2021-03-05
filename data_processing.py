import sys 
import pandas as pd 

#1234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890

STATION_COLS = [(0,11), (12,20), (21,30), (31,37), (38,40),
                (41,70), (72,75), (76,79), (80,86), (87,None)]
ZIP_COLS = [(0,11), (12,17), (18,None)]

# this version includes the codes
'''HLY_TEMP_COLS = [(0,11),(12,14),(15,17),(20,24),(27,31),(34,38),(41,45),
                 (48,52),(55,59),(62,66),(69,73),(76,80),(83,87),(90,94),
                 (97,101),(104,108),(111,115),(118,122),(125,129),(132,136),
                 (139,143),(146,150),(153,157),(160,164),(167,171),(174,178)]'''

# this version omits the codes
HLY_TEMP_COLS = [(0,11),(12,14),(15,17),(20,23),(27,30),(34,37),(41,44),
                 (48,51),(55,58),(62,65),(69,72),(76,79),(83,86),(90,93),
                 (97,100),(104,107),(111,114),(118,121),(125,128),(132,135),
                 (139,142),(146,149),(153,156),(160,163),(167,170),(174,177)]

# blanks are -9999
# P = provisinal, filter out?

# result row for each hour for a year
# column for each city

# feed in all the files (13 weather files)
# all files need headers

# read in all the weather files and parse and merge

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

def weather_config(stations_df, weather_file):
    this_weather_df = pd.read_fwf(weather_file, 
                                  colspecs = HLY_TEMP_COLS, 
                                  names = ['station_code', 'month', 'day', '0', '1', '2', '3', '4', '5', '6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','23'])
    new_df = pd.merge(stations_df, this_weather_df, on='station_code', how='right')
    # calculate average for the day
    new_df['average'] = new_df.iloc[:, 13:].astype(float).mean(axis=1)

    print(new_df.shape)
    print(new_df.iloc[:20])
    return new_df

# read in each weather attribute

if __name__=='__main__':
    if len(sys.argv) == 0:
        print("Usage: ")
    stations = station_config(sys.argv[1], sys.argv[2])
    weather = weather_config(stations,sys.argv[3])
