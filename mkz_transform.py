import csv
import utm
import numpy as np
def convert(pos):# set to Mcity local position
    pos[0] = pos[0] - 276000 + 102.89
    pos[1] = pos[1] - 4686800 + 281.25
    return pos
data = []
with open('mkz_data.csv', newline='') as csvfile:
    csv_reader = csv.reader(csvfile)
    row_id = 0
    for row in csv_reader:
        if row_id == 0:
            row_id = 1
            continue
        lon = float(row[2])
        lat = float(row[3])
        pos = utm.from_latlon(lat,lon)
        pos = convert(np.array(pos[0:2]))
        data.append(list(pos)+[row[1]])

with open('./mkz_transform_data.csv', 'a', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    for row in data:
        csvwriter.writerow(row)

