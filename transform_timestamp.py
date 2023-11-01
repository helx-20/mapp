import csv
import datetime
import pytz

iso_datetime_str = "2023-10-27T02:31:47.941+00:00"
iso_datetime = datetime.datetime.fromisoformat(iso_datetime_str)
utc_timezone = pytz.timezone('UTC')
utc_datetime = iso_datetime.astimezone(utc_timezone)
utc_timestamp = (utc_datetime - datetime.datetime(1970, 1, 1, tzinfo=pytz.utc)).total_seconds()

data = []
with open('./gps_test_data2/gpsbox_data.csv', newline='') as csvfile:
    csv_reader = csv.reader(csvfile)
    base_h = 0
    base_m = 0
    base_s = 0
    update_base = 1
    for row in csv_reader:
        iso_datetime_str = row[2]
        iso_datetime = datetime.datetime.fromisoformat(iso_datetime_str)
        utc_timezone = pytz.timezone('UTC')
        utc_datetime = iso_datetime.astimezone(utc_timezone)
        utc_timestamp = (utc_datetime - datetime.datetime(1970, 1, 1, tzinfo=pytz.utc)).total_seconds()
        row[2] = utc_timestamp
        '''
        time = row[2].split('T')[1].split('+')[0].split(":") # xx:yy:zz.abc
        hour = float(time[0])
        minute = float(time[1])
        second = float(time[2])
        if update_base:
            base_h = hour
            base_m = minute
            base_s = second
            update_base = 0
        row[2] = (hour - base_h) * 3600 + (minute - base_m) * 60 + (second - base_s) + time_start
        '''
        data.append(row)

with open('./gpsbox_transform_data.csv', 'a', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    for row in data:
        csvwriter.writerow(row)
