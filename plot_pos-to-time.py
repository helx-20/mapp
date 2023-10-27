import csv
import matplotlib.pyplot as plt
for name in ['robot_pos_refine1','robot_pos_refine2','vehicle_pos_refine1','vehicle_pos_refine2']:
    data = []
    x_list = []
    y_list = []
    with open(name+'.csv', newline='') as csvfile:
        csv_reader = csv.reader(csvfile)

        for row in csv_reader:
            data.append(row)
            x_list.append(row[0])
            y_list.append(row[1])

    x_list = [float(x)%10 for x in x_list]
    y_list = [float(y)%10 for y in y_list]
    x_list = [x-(min(x_list)+max(x_list))/2 for x in x_list]
    y_list = [y-(min(y_list)+max(y_list))/2 for y in y_list]
    #print(x_list)
    plt.plot(x_list,y_list,label=name)
    #plt.xticks([min(x_list),(min(x_list)+max(x_list))/2,max(x_list)])
    #plt.yticks([min(y_list),(min(y_list)+max(y_list))/2,max(y_list)])
    plt.xticks([-0.6,-0.3,0,0.3,0.6])
    plt.yticks([-0.6,-0.3,0,0.3,0.6])
    plt.xlabel("x")
    plt.ylabel("y")
    plt.legend()
    #plt.title(name)
    plt.title("pos of robot and vehicle")
    #plt.savefig(name+".png")
    #plt.close("all")
plt.savefig("all.png")