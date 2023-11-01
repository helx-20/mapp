import csv
data = []
with open('vehicle_pos.csv', newline='') as csvfile:
    csv_reader = csv.reader(csvfile)

    for row in csv_reader:
        data.append(row)

total = len(data)
for i in range(total):
    if data[total-1-i] == data[total-2-i]:
        data.pop(total-1-i)
print(total/len(data))

with open('./vehicle_pos_refine.csv', 'a', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    for row in data:
        csvwriter.writerow(row)
