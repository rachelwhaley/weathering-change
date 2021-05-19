# weathering-change

This project visualizes US weather data, allowing users to explore weather trends in over 200 locations at specific times of day and days of the year via a Tableau Public dashboard: https://public.tableau.com/profile/jeff.whaley#!/vizhome/TempMap_16213096909840/Dashboard1

## Data source
NOAA historical weather data from https://www1.ncdc.noaa.gov/pub/data/normals/1981-2010/readme.txt

## Data model
The data model is a simple snowflake schema consisting of 3 tables:
* Weather facts (station code, date-hour code, and 13 types of weather measurements)
* Station table (details about stations)
* Date-hour table (date-hour codes to machine-readable datetime format)

## Data pipeline
To run the data processing pipeline, run:

`python3 data_processing.py `

To generate the date-hour code table, run:

`python3 create_date_table.py > date_table.csv`