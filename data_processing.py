import pandas as pd 
from datetime import datetime
import csv
#0        1         2         3         4         5         6         7         8         9         0         1         2         3         4         5         6         7         8     
#12345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345
#AQW00061705 01 10 -9999    838C   840S   835S   835C   833S   835S   842C   860S   878S   883C   896S   896S   894C   896S   896S   891C   878S   871S   856C   849S   846S   846C   842S
STATION_COLS = [(0,11), (12,20), (21,30), (31,37), (38,40),
                (41,70), (72,75), (76,79), (80,86), (87,None)]
ZIP_COLS = [(0,11), (12,17), (18,None)]

# this version omits the codes (e.g. P = provisional)
HLY_TEMP_COLS = [(0,11),(12,14),(15,17), # station_code', 'month', 'day'
                 #(18,23),(25,30),(32,37),(39,44), # hours 0-3
                 #(46,51),(53,58),(60,65), # hours 4-6
                 (67,72),(74,79),(81,86),(88,93), # hours 7-10
                 (95,100),(102,107),(109,114),(116,121),(123,128),(130,135), # hours 11-16
                 (137,142),(144,149),(151,156) # hours 17-19
                 #(158,163),(165,170),(172,177),(181,184) # hours 20-23
                 ]

def station_config(station_file, zip_file,selected_stations):
    # column definitions at https://www1.ncdc.noaa.gov/pub/data/normals/1981-2010/readme.txt
    stations_df = pd.read_fwf(station_file, 
                              colspecs = STATION_COLS, 
                              names = ['station_code', 'lat', 'lon', 'elevation', 'state', 'name', 'gsn_flag', 'hcn_flag', 'wmo_id', 'method'])

    # filter for only the stations selected
    stations_filtered = stations_df[stations_df['station_code'].isin(selected_stations)]
    stations_filtered = stations_filtered.reset_index(drop=True)

    print("Configuring stations...")

    zip_df = pd.read_fwf(zip_file, colspecs = ZIP_COLS, names = ['station_code', 'zip_code', 'city'])
    result_df = pd.merge(stations_filtered, zip_df, on='station_code', how='left')

    return result_df

# construct weather-hour table: takes in all the weather files and list of stations to filter by
# returns StationCode, DateHourCode, and 13 weather facts
def weather_hour_config(selected_stations):

    ALL_WEATHER_FILES = ['hly-temp-normal.txt', 'hly-temp-10pctl.txt', 'hly-temp-90pctl.txt',
                         'hly-dewp-normal.txt', 'hly-dewp-10pctl.txt', 'hly-dewp-90pctl.txt',
                         'hly-clod-pctbkn.txt', 'hly-clod-pctclr.txt', 'hly-clod-pctfew.txt',
                         'hly-clod-pctovc.txt', 'hly-hidx-normal.txt', 'hly-wind-avgspd.txt',
                         'hly-wind-pctclm.txt']

    all_weather_dfs = []
    for file in ALL_WEATHER_FILES:
        this_filename = file.split('.')[0]
        print("Processing " + this_filename + " data...")
        this_weather_df = pd.read_fwf(file, 
                                  colspecs = HLY_TEMP_COLS, 
                                  names = ['station_code', 'month', 'day', '7','8','9','10','11','12','13','14','15','16','17','18','19'])
        this_weather_filtered = this_weather_df[this_weather_df['station_code'].isin(selected_stations)]
        this_weather_filtered = this_weather_filtered.reset_index(drop=True)
        
        # preprocessing of data
        this_weather_filtered.replace(to_replace = -9999, value=None, inplace=True)  # -9999s are blanks
        # construct new dataframe with one row per date-hour
        hour_date_dicts = []
        for index, row in this_weather_filtered.iterrows() :
            date_code = 'D' + '{0:02d}{1:02d}'.format(row['month'], row['day'])
            for hour_code in ['7','8','9','10','11','12','13','14','15','16','17','18','19']:
                date_hour_code = date_code + hour_code
                hourly = {'station_code': row['station_code'], 'date_hour_code': date_hour_code, this_filename : row[hour_code]}
                hour_date_dicts.append(hourly)
        new_df = pd.DataFrame(hour_date_dicts)
        if 'temp' in this_filename:  # divide temps by 10 for human-readable
            new_df[this_filename] = new_df[this_filename]/10
        all_weather_dfs.append(new_df)
    
    df = all_weather_dfs[0]
    for x in all_weather_dfs[1:]:
        new_df = pd.merge(df, x, how='left', left_on=['station_code','date_hour_code'], right_on = ['station_code','date_hour_code'])
        df = new_df
    
    print("Final dataframe size is " + str(new_df.shape))

    return new_df


if __name__=='__main__':
    
    # filter for only the stations selected
    include_file = open('StationInclude.csv', 'r')
    include_list = csv.reader(include_file)
    selected_stations = []
    for item in include_list:
        selected_stations.append(item[0])
    
    # create the stations table
    stations = station_config('hly-inventory.txt', 'zipcodes-normals-stations.txt', selected_stations)
    stations.to_csv('stations' + str(datetime.now())  + '.csv')

    # create the weather hour table
    weather_facts = weather_hour_config(selected_stations)
    weather_facts.to_csv('weatherfacts' + str(datetime.now()) + '.csv')
