import csv
import matplotlib.pyplot as plt
data = []
x_list = []
y_list = []
name = 'robot_pos_refine2'
with open(name+'.csv', newline='') as csvfile:
    csv_reader = csv.reader(csvfile)

    for row in csv_reader:
        data.append(row)
        x_list.append(row[0])
        y_list.append(row[1])

x_list = [float(x)%10 for x in x_list]
y_list = [float(y)%10 for y in y_list]
#print(x_list)
plt.plot(x_list,y_list)
plt.xticks([min(x_list),(min(x_list)+max(x_list))/2,max(x_list)])
plt.yticks([min(y_list),(min(y_list)+max(y_list))/2,max(y_list)])
plt.xlabel("x")
plt.ylabel("y")
plt.title(name)
plt.savefig(name+".png")