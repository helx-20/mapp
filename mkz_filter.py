import csv
data = []
import csv
gps_data = []
with open('gps_test_data3/gpsbox_transform_data.csv', newline='') as csvfile:
    csv_reader = csv.reader(csvfile)

    for row in csv_reader:
        gps_data.append(row)

with open('gps_test_data2/mkz_transform_data.csv', newline='') as csvfile:
    csv_reader = csv.reader(csvfile)

    for row in csv_reader:
        data.append(row)

total = len(data)
gps_data_id = 0
data_id = 0
delay = 0
for i in range(total):
    if data_id == len(data)-1 or float(data[data_id][2]) > float(gps_data[-1][2]) - delay or gps_data_id == len(gps_data):
        data.pop(data_id)
        continue
    elif abs(float(data[data_id][2]) - float(gps_data[gps_data_id][2])+delay) > abs(float(data[data_id+1][2]) - float(gps_data[gps_data_id][2])+delay):
        data.pop(data_id)
    else:
        gps_data_id = gps_data_id + 1
        data_id = data_id + 1

with open('./mkz_final_data.csv', 'a', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    for row in data:
        csvwriter.writerow(row)
