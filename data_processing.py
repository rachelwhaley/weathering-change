import sys 
import pandas as pd 
import time
import csv
#0        1         2         3         4         5         6         7         8         9         0         1         2         3         4         5         6         7         8     
#12345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345
#AQW00061705 01 10 -9999    838C   840S   835S   835C   833S   835S   842C   860S   878S   883C   896S   896S   894C   896S   896S   891C   878S   871S   856C   849S   846S   846C   842S
STATION_COLS = [(0,11), (12,20), (21,30), (31,37), (38,40),
                (41,70), (72,75), (76,79), (80,86), (87,None)]
ZIP_COLS = [(0,11), (12,17), (18,None)]

# this version includes the codes
'''HLY_TEMP_COLS = [(0,11),(12,14),(15,17),(20,24),(27,31),(34,38),(41,45),
                 (48,52),(55,59),(62,66),(69,73),(76,80),(83,87),(90,94),
                 (97,101),(104,108),(111,115),(118,122),(125,129),(132,136),
                 (139,143),(146,150),(153,157),(160,164),(167,171),(174,178)]'''

# this version omits the codes
HLY_TEMP_COLS = [(0,11),(12,14),(15,17), # station_code', 'month', 'day'
                 #(18,23),(25,30),(32,37),(39,44), # hours 0-3
                 #(46,51),(53,58),(60,65), # hours 4-6
                 (67,72),(74,79),(81,86),(88,93), # hours 7-10
                 (95,100),(102,107),(109,114),(116,121),(123,128),(130,135), # hours 11-16
                 (137,142),(144,149),(151,156) # hours 17-19
                 #(158,163),(165,170),(172,177),(181,184)
                 ]

# blanks are -9999
# P = provisinal, filter out?

# result row for each hour for a year
# column for each city

# feed in all the files (13 weather files)
# all files need headers

# read in all the weather files and parse and merge

# process the fixed width files

def station_config(station_file, zip_file,selected_stations):
    # column definitions at https://www1.ncdc.noaa.gov/pub/data/normals/1981-2010/readme.txt
    stations_df = pd.read_fwf(station_file, 
                              colspecs = STATION_COLS, 
                              names = ['station_code', 'lat', 'lon', 'elevation', 'state', 'name', 'gsn_flag', 'hcn_flag', 'wmo_id', 'method'])
    # print(stations_df.shape)
    # print(stations_df.iloc[:3])

    # filter for only the stations dad selected
    stations_filtered = stations_df[stations_df['station_code'].isin(selected_stations)]
    stations_filtered = stations_filtered.reset_index(drop=True)

    print("length of filtered stations = " + str(stations_filtered.shape[0]))

    zip_df = pd.read_fwf(zip_file, colspecs = ZIP_COLS, names = ['station_code', 'zip_code', 'city'])
    result_df = pd.merge(stations_filtered, zip_df, on='station_code', how='left')
    print(result_df.iloc[:20])
    print("length of results = " + str(result_df.shape[0]))
    return result_df

def weather_temp_config(stations_df, weather_file):
    this_weather_df = pd.read_fwf(weather_file, 
                                  colspecs = HLY_TEMP_COLS, 
                                  names = ['station_code', 'month', 'day', '7','8','9','10','11','12','13','14','15','16','17','18','19'])
#                                 names = ['station_code', 'month', 'day', '0', '1', '2', '3', '4', '5', '6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','23'])
    
    # filter for only the stations dad selected
    include_file = open('StationInclude.csv', 'r')
    include_list = csv.reader(include_file)
    selected_stations = []

    for item in include_list:
        selected_stations.append(item[0])

    this_weather_filtered = this_weather_df[this_weather_df['station_code'].isin(selected_stations)]
    this_weather_filtered = this_weather_filtered.reset_index(drop=True)
    
    this_weather_filtered.replace(to_replace = -9999, value=None, inplace=True)
    # calculate average for the day
    this_weather_filtered.iloc[:, 3:].div(10)
    this_weather_filtered['average'] = this_weather_filtered.iloc[:, 3:].astype(float).mean(axis=1)/10

    # TO ADD THE STATIONS BACK IN 
    # new_df = pd.merge(stations_df, this_weather_df, on='station_code', how='left')

    print(this_weather_filtered.shape)
    # print(this_weather_df.iloc[:20])

    return this_weather_filtered

# construct weather-hour table (THIS IS THE NEW ONE)
def weather_hour_config(selected_stations):
    # takes in all the weather files and list of stations to filter by
    # returns StationCode, DateHourCode, and 13 weather facts

    # filter out the stations we're not using
    this_weather_df = pd.read_fwf('hly-temp-normal.txt', 
                                  colspecs = HLY_TEMP_COLS, 
                                  names = ['station_code', 'month', 'day', '7','8','9','10','11','12','13','14','15','16','17','18','19'])
    this_weather_filtered = this_weather_df[this_weather_df['station_code'].isin(selected_stations)]
    this_weather_filtered = this_weather_filtered.reset_index(drop=True)

    print(this_weather_filtered.shape)

    # preprocessing of data
    this_weather_filtered.replace(to_replace = -9999, value=None, inplace=True)
    # calculate average for the day
    this_weather_filtered.iloc[:, 3:].div(10)
    #TODO: divide weather #s like temps by 10

    # this_weather_filtered['average'] = this_weather_filtered.iloc[:, 3:].astype(float).mean(axis=1)/10

    # start with 1 file to construct the DateHourCodes and grab the weather facts
    hour_date_dicts = []
    for index, row in this_weather_filtered.iterrows() :
        date_code = 'D' + '{0:02d}{1:02d}'.format(row['month'], row['day'])
        # date_code = str(row['month']) + str(row['day'])
        for hour_code in ['7','8','9','10','11','12','13','14','15','16','17','18','19']:
            date_hour_code = date_code + hour_code
            hourly = {'station_code': row['station_code'], 'date_hour_code': date_hour_code, 'temp_normal': row[hour_code]}
            hour_date_dicts.append(hourly)

    df = pd.DataFrame(hour_date_dicts) 
    print(df.shape)
    print(df.iloc[:20])

    # then add in the rest of the files
    #TODO: Make this DRY
    more_weather_files = ['hly-temp-10pctl.txt', 'hly-temp-90pctl.txt']
    #TODO: Add the rest of the weather files
    more_weather_dfs = []
    for file in more_weather_files:
        this_weather_df = pd.read_fwf(file, 
                                  colspecs = HLY_TEMP_COLS, 
                                  names = ['station_code', 'month', 'day', '7','8','9','10','11','12','13','14','15','16','17','18','19'])
        this_weather_filtered = this_weather_df[this_weather_df['station_code'].isin(selected_stations)]
        this_weather_filtered = this_weather_filtered.reset_index(drop=True)
        hour_date_dicts = []
        for index, row in this_weather_filtered.iterrows() :
            date_code = 'D' + '{0:02d}{1:02d}'.format(row['month'], row['day'])
            # date_code = str(row['month']) + str(row['day'])
            for hour_code in ['7','8','9','10','11','12','13','14','15','16','17','18','19']:
                date_hour_code = date_code + hour_code
                hourly = {'station_code': row['station_code'], 'date_hour_code': date_hour_code, file.split('.')[0] : row[hour_code]}
                hour_date_dicts.append(hourly)
        new_df = pd.DataFrame(hour_date_dicts)
        more_weather_dfs.append(new_df)
    
    for x in more_weather_dfs:
        new_df = pd.merge(df, x, how='left', left_on=['station_code','date_hour_code'], right_on = ['station_code','date_hour_code'])
        df = new_df
    
    print(new_df.shape)
    print(new_df.iloc[:20])

    return new_df


if __name__=='__main__':
    if len(sys.argv) == 0:
        print("Usage: ")
    
    # filter for only the stations dad selected
    include_file = open('StationInclude.csv', 'r')
    include_list = csv.reader(include_file)
    selected_stations = []

    for item in include_list:
        selected_stations.append(item[0])
    
    # create the stations table
    stations = station_config('hly-inventory.txt', 'zipcodes-normals-stations.txt', selected_stations)
    stations.to_csv('stations' + str(time.time())  + '.csv')

    # create the weather hour table
    weather_facts = weather_hour_config(selected_stations)
    weather_facts.to_csv('weatherfacts' + str(time.time()) + '.csv')

    '''    
    # temps 
    weather_avg = weather_temp_config(stations, 'hly-temp-normal.txt')
    weather_ten_pct = weather_temp_config(stations, 'hly-temp-10pctl.txt')
    weather_90_pct = weather_temp_config(stations,'hly-temp-90pctl.txt') 
    
    # dewpoints
    dewp_normal = weather_temp_config(stations,'hly-dewp-normal.txt') 
    dewp_10_pct = weather_temp_config(stations, 'hly-dewp-10pctl.txt')
    dewp_90_pct = weather_temp_config(stations, 'hly-dewp-90pctl.txt')

    # cloud percentages
    clod_pctbkn = weather_temp_config(stations, 'hly-clod-pctbkn.txt')
    clod_pctclr = weather_temp_config(stations, 'hly-clod-pctclr.txt')
    clod_pctfew = weather_temp_config(stations, 'hly-clod-pctfew.txt')
    clod_pctovc = weather_temp_config(stations, 'hly-clod-pctovc.txt')

    # heat index
    hidx_normal = weather_temp_config(stations, 'hly-hidx-normal.txt')

    # wind speed
    wind_avg = weather_temp_config(stations, 'hly-wind-avgspd.txt')
    wind_clm = weather_temp_config(stations, 'hly-wind-pctclm.txt')'''

    # weather.to_csv('output.csv')

    # stations = station_config(sys.argv[1], sys.argv[2])
    # weather = weather_config(stations,sys.argv[3])
