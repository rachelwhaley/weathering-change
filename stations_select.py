import csv
import pandas as pd 

full_file = open('hly-inventory.txt', 'r') 
full_list = csv.reader(full_file)

include_file = open('StationInclude.csv', 'r')
include_list = csv.reader(include_file)
# include_stations = include_list.read()

# include_stations = include_stations.split()
print(include_list)
selected_stations = []

for item in include_list:
    selected_stations.append(item[0])

for item in full_list:
    if item[0] in include_list:
        selected_stations.append(item[0])

print(str(len(selected_stations)))
print(selected_stations)
'''
with open('selected.txt', 'w') as f:
    f.write(str(exclude_list))
    f.close()'''