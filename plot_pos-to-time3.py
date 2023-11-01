import csv
import matplotlib.pyplot as plt
plt.figure(figsize=(6, 6))
for name in ['gpsbox_final_data','mkz_final_data']:
    data = []
    x_list = []
    y_list = []
    with open('./gps_test_data3/'+name+'.csv', newline='') as csvfile:
        csv_reader = csv.reader(csvfile)

        for row in csv_reader:
            data.append(row)
            x_list.append(row[0])
            y_list.append(row[1])

    x_list = [float(x) for x in x_list[0:430]]
    y_list = [float(y) for y in y_list[0:430]]
    plt.plot(x_list,y_list,label=name)
    plt.xlim(1640,1760)
    plt.ylim(120,300)
    #plt.xticks([4,5,6,7,8])
    #plt.yticks([2.5,3.5,4.5,5.5,6.5])
    plt.xlabel("x")
    plt.ylabel("y")
    plt.legend()
    #plt.title(name)
    #plt.savefig(name+".png")
    #plt.close("all")
plt.title("pos of gps-box and mkz")
plt.savefig("./gps_test_data3/all.png",dpi=300)
plt.close("all")

plt.figure(figsize=(6, 6))
for name in ['gpsbox_final_data','mkz_final_data']:
    data = []
    x_list = []
    y_list = []
    with open('./gps_test_data3/'+name+'.csv', newline='') as csvfile:
        csv_reader = csv.reader(csvfile)

        for row in csv_reader:
            data.append(row)
            x_list.append(row[0])
            y_list.append(row[1])

    x_list = [float(x) for x in x_list[430:]]
    y_list = [float(y) for y in y_list[430:]]
    plt.plot(x_list,y_list,label=name)
    plt.xlim(1640,1760)
    plt.ylim(120,300)
    #plt.xticks([4,5,6,7,8])
    #plt.yticks([2.5,3.5,4.5,5.5,6.5])
    plt.xlabel("x")
    plt.ylabel("y")
    plt.legend()
plt.title("pos of gps-box and mkz")
plt.savefig("./gps_test_data3/all2.png",dpi=300)
plt.close("all")

gps_time = []
gps_x = []
gps_y = []
with open('./gps_test_data3/gpsbox_final_data.csv', newline='') as csvfile:
    csv_reader = csv.reader(csvfile)

    for row in csv_reader:
        gps_time.append(float(row[2]))
        gps_x.append(float(row[0]))
        gps_y.append(float(row[1]))

mkz_time = []
mkz_x = []
mkz_y = []
with open('./gps_test_data3/mkz_final_data.csv', newline='') as csvfile:
    csv_reader = csv.reader(csvfile)

    for row in csv_reader:
        mkz_time.append(float(row[2]))
        mkz_x.append(float(row[0]))
        mkz_y.append(float(row[1]))

import numpy as np
x_error = np.array(mkz_x) - np.array(gps_x)
y_error = np.array(mkz_y) - np.array(gps_y)
timestamp = (np.array(gps_time)+np.array(mkz_time))/2 - (gps_time[0]+mkz_time[0])/2
plt.plot(timestamp,x_error,label='x error')
plt.plot(timestamp,y_error,label='y error')
error = np.sqrt(np.square(x_error)+np.square(y_error))
plt.plot(timestamp,error,label='L2 error')
plt.legend()
plt.xlabel("time / s")
plt.ylabel("error (mkz-gps) / m")
plt.title("error of gps-box and mkz")
plt.savefig("./gps_test_data3/error.png",dpi=300)
plt.close("all")

plt.plot(np.array(gps_time)-gps_time[0],gps_x,label='gps-box x-coordinate')
plt.plot(np.array(mkz_time)-mkz_time[0],mkz_x,label='mkz x-coordinate')
plt.legend()
plt.xlabel("time / s")
plt.ylabel("x / m")
plt.title("x-coordinate of gps-box and mkz")
plt.savefig("./gps_test_data3/x.png",dpi=300)
plt.close("all")

plt.plot(np.array(gps_time)-gps_time[0],gps_y,label='gps-box y-coordinate')
plt.plot(np.array(mkz_time)-mkz_time[0],mkz_y,label='mkz y-coordinate')
plt.legend()
plt.xlabel("time / s")
plt.ylabel("y / m")
plt.title("y-coordinate of gps-box and mkz")
plt.savefig("./gps_test_data3/y.png",dpi=300)
plt.close("all")

miss_point = []
for i in range(len(gps_x)-1):
    if gps_x[i+1] == gps_x[i] and gps_y[i+1] == gps_y[i]:
        miss_point.append(i+1)
print(len(gps_x)/len(miss_point))
print(miss_point)
not_miss = []
for i in range(len(gps_x)):
    if i in miss_point:
        continue
    else:
        not_miss.append(i)
plt.scatter(np.array(gps_time)[miss_point]-gps_time[0],np.ones(len(miss_point)),s=0.5)
plt.xlabel("time / s")
plt.title('missed point')
plt.savefig("./gps_test_data3/miss_point.png",dpi=300)
plt.close("all")

plt.scatter(np.array(mkz_x)[miss_point],np.array(mkz_y)[miss_point],s=0.8)
plt.xlabel("x")
plt.ylabel("y")
plt.title("missed points' position")
plt.savefig("./gps_test_data3/miss_point_position.png",dpi=300)
plt.close("all")

speed = np.sqrt(np.square(np.array(mkz_x[1:])-np.array(mkz_x[:-1]))+np.square(np.array(mkz_y[1:])-np.array(mkz_y[:-1]))) / (np.array(mkz_time[1:])-np.array(mkz_time[:-1]))
plt.plot(np.array(mkz_time[1:])-mkz_time[1],speed,label="speed")
plt.ylabel("speed / m/s")
plt.xlabel("time / s")
plt.title("speed")
plt.savefig("./gps_test_data3/speed.png",dpi=300)
plt.close("all")

plt.plot(np.array(mkz_time[1:])-mkz_time[1],speed,label="speed")
plt.plot(timestamp[1:],error[1:],label='L2 error',alpha=0.7)
plt.legend()
plt.xlabel("time / s")
plt.title("speed and error")
plt.savefig("./gps_test_data3/speed_and_error.png",dpi=300)
plt.close("all")

plt.scatter(speed,error[1:],s=0.7)
plt.xlabel("speed / m/s")
plt.ylabel('error / m')
plt.title("error to speed")
plt.savefig("./gps_test_data3/error_to_speed.png",dpi=300)
plt.close("all")

plt.scatter(np.abs(np.array(mkz_time)-np.array(gps_time)),np.ones(len(mkz_time)),s=0.7)
plt.xlabel("time gap between mkz and gps box")
plt.title("time gap")
plt.savefig("./gps_test_data3/time_gap.png",dpi=300)
plt.close("all")

bins_num = 50
hist,bins = np.histogram(speed,bins=bins_num)
hist2 = np.zeros_like(np.array(hist))
for i in range(len(miss_point)):
    if miss_point[i] == len(speed):
        break
    speed_tmp = speed[miss_point[i]]
    bin_id = min(int((speed_tmp - bins[0]) / (bins[-1] - bins[0]) * bins_num), bins_num-1)
    hist2[bin_id] = hist2[bin_id] + 1
print(hist2)
hist_rate = hist2 / (np.array(hist) + 0.0001)
plt.plot(np.array(bins[1:])-(bins[1]-bins[0])/2,hist_rate)
plt.xlabel("speed / m/s")
plt.ylabel("miss rate")
plt.ylim(0,1)
plt.title("miss rate to speed")
plt.savefig("./gps_test_data3/miss_rate_to_speed.png",dpi=300)
plt.close("all")

plt.scatter(speed[miss_point[:-1]]*(np.array(mkz_time[1:])-np.array(mkz_time[:-1]))[miss_point[:-1]],np.ones(len(miss_point[:-1])),s=0.7)
plt.scatter(speed*(np.array(mkz_time[1:])-np.array(mkz_time[:-1])),0.5*np.ones(len(speed)),s=0.7)
plt.xlabel("distance between adjacent points / m")
plt.yticks([0.5,1],["all","missed"])
plt.ylim(0,1.5)
plt.title("distance of miss point")
plt.savefig("./gps_test_data3/miss_distance.png",dpi=300)
plt.close("all")

plt.hist(error[not_miss],bins=100,alpha=0.7)
plt.xlabel("error / m")
plt.title("error (without miss point) histogram")
plt.savefig("./gps_test_data3/error_without_miss_histogram.png",dpi=300)
plt.close("all")

plt.hist(error,bins=100,alpha=0.7)
plt.xlabel("error / m")
plt.title("error (with miss point) histogram")
plt.savefig("./gps_test_data3/error_histogram.png",dpi=300)
plt.close("all")

plt.plot(np.array(mkz_time)[not_miss]-mkz_time[0],error[not_miss])
plt.xlabel("time / s")
plt.ylabel("error / m")
plt.title("L2 error (without miss) of gps-box and mkz")
plt.savefig("./gps_test_data3/error_without_miss.png",dpi=300)
plt.close("all")

slope,intersect = np.polyfit(speed[not_miss[1:]],error[not_miss[1:]],1)
line = slope * speed + intersect
plt.scatter(speed[not_miss[1:]],error[not_miss[1:]],s=0.7)
plt.plot(speed,line)
plt.xlabel("speed / m/s")
plt.ylabel('error / m')
plt.ylim(-0.5,11)
plt.title("error (without miss) = {} * speed + {}".format(round(slope,2),round(intersect,2)))
plt.savefig("./gps_test_data3/error_without_miss_to_speed.png",dpi=300)
plt.close("all")

slope,intersect = np.polyfit(speed[miss_point[1:-1]],error[miss_point[1:-1]],1)
line = slope * speed + intersect
plt.scatter(speed[miss_point[1:-1]],error[miss_point[1:-1]],s=0.7)
plt.plot(speed,line)
plt.xlabel("speed / m/s")
plt.ylabel('error / m')
plt.ylim(-0.5,11)
plt.title("error (miss) = {} * speed + {}".format(round(slope,2),round(intersect,2)))
plt.savefig("./gps_test_data3/error_miss_to_speed.png",dpi=300)
plt.close("all")

plt.hist(np.array(mkz_time[1:])-np.array(mkz_time[:-1]),bins=100,alpha=0.7)
plt.xlabel("delta-T / s")
plt.title("delta-T histogram")
plt.savefig("./gps_test_data3/dt_histogram.png",dpi=300)
plt.close("all")

plt.hist(np.ones(len(mkz_time)-1) / (np.array(mkz_time[1:])-np.array(mkz_time[:-1])),bins=100,alpha=0.7)
plt.xlabel("frequency / Hz")
plt.title("frequency histogram")
plt.savefig("./gps_test_data3/frequency_histogram.png",dpi=300)
plt.close("all")

miss_duration = []
tmp_duration = 0
for i in range(len(miss_point)):
    tmp_duration = tmp_duration + mkz_time[miss_point[i]] - mkz_time[miss_point[i]-1]
    if i == len(miss_point)-1:
        miss_duration.append(tmp_duration)
        break
    if miss_point[i+1] == miss_point[i] + 1:
        continue
    else:
        miss_duration.append(tmp_duration)
        tmp_duration = 0

plt.hist(np.array(miss_duration),bins=100,alpha=0.7)
plt.xlabel("miss duration / s")
plt.title("miss duration histogram")
plt.savefig("./gps_test_data3/miss_duration_histogram.png",dpi=300)
plt.close("all")

