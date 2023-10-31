
# robot

import os
import sys
import time
from dotenv import load_dotenv
import socketio
import rospy2 as rospy
import json
import numpy as np
from std_msgs.msg import String
from mcity_msg.msg import MAPPTrigger

'''
meters_per_second = 0
if len(sys.argv) == 3:
    meters = float(sys.argv[1])
    meters_per_second = float(sys.argv[2])
else:
    meters = 1.0
    meters_per_second = 0.5
'''
meters = 1.0
meters_per_second = 0.5

# Load environment variables and configure
load_dotenv(dotenv_path='./robot_env.env')
api_key = os.environ.get('MCITY_OCTANE_KEY', 'reticulatingsplines')
server = os.environ.get('MCITY_OCTANE_SERVER', 'wss://octane.mvillage.um.city/')
proxy_id = os.environ.get('MCITY_ROBOT_ID', 1)
channel = "robot_proxy"
room = "robot"

namespace = "/octane"
connected = False
sent = False

robot_lon = 0
robot_lat = 0
robot_timestamp = 0
# If no API Key provided, exit.
if not api_key:
    print("NO API KEY SPECIFIED. EXITING")
    exit()

# Create an SocketIO Python client.
sio = socketio.Client()
# Async client is available also: sio = socketio.AsyncClient()

def send_auth():
    """
    Emit an authentication event.
    """
    sio.emit('auth', {'x-api-key': api_key}, namespace=namespace)


# Define event callbacks
@sio.on('connect', namespace=namespace)
def on_connect():
    """
    Handle connection event and send authentication key
    """
    send_auth()


@sio.on('join', namespace=namespace)
def on_join(data):
    """
    Event fired when user joins a channel
    """
    print('Robot join received with ', data)
    if data.get('join', None) == room:
        global connected
        connected = True


@sio.on('auth_ok', namespace=namespace)
def on_auth_ok(data):
    # print('\n\nGot auth ok event')
    print('Joining robot room')
    sio.emit('join', {'channel': room}, namespace=namespace)

@sio.on('robot_proxy', namespace=namespace)
def on_robot_proxy(data):
    #print(f"data: {data}")
    global meters
    global meters_per_second
    global proxy_id
    if 'data' in data.keys():
        print(data)
        data = json.loads(data['data']['navsat_fix'])
        msg = {
            "time": rospy.get_time(),
            "sensor_id": 'proxy',
            "BSMs": []
        }
        rs = {
            "id": 'proxy_' + str(proxy_id),
            "time": rospy.get_time(),
            "src": data['status'],
            "type": 'ped',
            "sx": 1.,
            "sy": 1.,
            "sz": .5,
            "angle": 0,
            "vx": meters_per_second,
            "z": 0,
            "lon": data['longitude'],
            "lat": data['latitude']
        }
        msg["BSMs"].append(rs)
        pub_mapp_state.publish(json.dumps(msg))
        #print(data)
        global robot_timestamp
        robot_timestamp = rs['time']
        global robot_lon
        global robot_lat
        robot_lon = data['longitude']
        robot_lat = data['latitude']
    else:
        print(f"Data received from {server} is incomplete.")


def trigger_callback():
    global sent
    sent = True
    print("Message sent")


def trigger(proxy_id, meters, meters_per_second):
    print(f"Sending trigger for ID {proxy_id} to {server}")
    global sent
    sent = False
    sio.emit(
        channel,
        {
            "id": proxy_id,
            "type": "action",
            "action": "move_distance",
            "cancel": False,
            "values": {
                "move_distance_goal": {
                    "meters_per_second": meters_per_second,
                    "meters": meters
                }
            }
        },
        namespace=namespace,
        callback=trigger_callback
    )
    while not sent:
        time.sleep(0.001)


def trigger_msg(msg):
    proxy_id = msg.proxy_id
    meters = msg.meter
    meters_per_second = msg.speed
    print(f"Sending trigger for ID {proxy_id} to {server}. Distance: {meters}, speed: {meters_per_second}")
    sio.emit(
        channel,
        {
            "id": proxy_id,
            "type": "action",
            "action": "move_distance",
            "cancel": False,
            "values": {
                "move_distance_goal": {
                    "meters_per_second": meters_per_second,
                    "meters": meters
                }
            }
        },
        namespace=namespace,
        callback=trigger_callback
    )

def cancel(proxy_id):
    sio.emit(
        channel,
        {
            "id": proxy_id,
            "type": "action",
            "cancel": True,
        },
        namespace=namespace,
        callback=sent
    )

def estop(proxy_id):
    sio.emit(
        channel,
        {
            "id": proxy_id,
            "type": "estop"
        },
        namespace=namespace,
        callback=sent
    )

rospy.init_node('MAPP_Driver', anonymous=True)
rospy.Subscriber('/mapp/trigger', MAPPTrigger, trigger)
pub_mapp_state = rospy.Publisher('/mapp/state', String, queue_size=1)



########################################################################
# vehicle

from utils import *

# Load environment variables
load_dotenv(dotenv_path='./vehicle_env.env')
api_key2 = os.environ.get('MCITY_OCTANE_KEY', '7AaZH0x9Fo')
server2 = os.environ.get('MCITY_OCTANE_SERVER', 'wss://octane.um.city/')
namespace2 = "/octane"
vehicle_id = 'B7A5A2'
#vehicle_id = '731485'

data_gps_box = []
path = './'
if not os.path.exists(path):
    os.mkdir(path)

# record vehicle info
vehicle_lon = -83
vehicle_lat = 42
vehicle_last_lon = -83
vehicle_last_lat = 42
vehicle_heading = []
Timestamp = []
vehicle_v = 0
vehicle_acc = 0
beacon_update_flag = False

# If no API Key provided, exit.
if not api_key2:
    print ("No API KEY SPECIFIED. EXITING")
    exit()

# Create an SocketIO Python client.
sio2 = socketio.Client()

# Async client is available also: sio = socketio.AsyncClient()
def send_auth2():
    """
    Emit an authentication event.
    """
    print("sent veh auth")
    sio2.emit('auth', {'x-api-key': api_key2}, namespace=namespace2)

# Define event callbacks
@sio2.on('connect', namespace=namespace2)
def on_connect():
    """
    Handle connection event and send authentication key
    """
    print("try to connect")
    send_auth2()

@sio2.on('join', namespace=namespace2)
def on_join(data):
    """
    Event fired when user joins a channel
    """
    print('Vehicle join received with ', data)

@sio2.on('channels', namespace=namespace2)
def on_channels(data):
    """
    Event fired when a user requests current channel information.
    """
    print('Channel information', data)

@sio2.on('disconnect', namespace=namespace2)
def on_disconnect():
    """
    Event fired on disconnect.
    """
    print('disconnected from vehicle server')

@sio2.on('auth_ok', namespace=namespace2)
def on_auth_ok(data):
    global sio2
    print('\n\ngot auth ok event')
    print('Subscribing to beacon channel')
    sio2.emit('join', {'channel': 'beacon'}, namespace=namespace2)
    sio2.emit('join', {'channel': 'v2x_obu_parsed'}, namespace=namespace2)

@sio2.on('beacon_update', namespace=namespace2)
def on_beacon_update(data):
    '''
    Fired each time a beacon sends us position data
    '''    
    #print('Beacon update: ', data)
    global beacon_update_flag
    beacon_update_flag = True
    if data['id'] == vehicle_id:
        #print(data)
        keys = ['id', 'UTC Timestamp', 'lon', 'lat', 'speed', 'heading', 'acceleration']
        data_gps_box.append(
            [1,
            data['state']['dynamics']['updated'],
            data['state']['dynamics']['longitude'],
            data['state']['dynamics']['latitude'],
            data['state']['dynamics']['velocity'],
            data['state']['dynamics']['heading'],
            data['state']['dynamics']['acceleration']]
        )
        global Timestamp
        global vehicle_v
        global vehicle_acc
        Timestamp = data['state']['dynamics']['updated']
        vehicle_v = data['state']['dynamics']['velocity']
        vehicle_acc = data['state']['dynamics']['acceleration']
        global vehicle_last_lat
        global vehicle_last_lon
        global vehicle_lon
        global vehicle_lat
        global vehicle_heading
        vehicle_last_lat = vehicle_lat
        vehicle_last_lon = vehicle_lon
        vehicle_lon = data['state']['dynamics']['longitude']
        vehicle_lat = data['state']['dynamics']['latitude']
        vehicle_heading = data['state']['dynamics']['heading']
        #if len(data_gps_box) % 1 == 0:
        #    save_csv(data_gps_box, keys, path, 'gps_box_data', False)

@sio2.on('v2x_BSM', namespace=namespace2)
def on_v2x(data):
    #pass
    '''
    Fired each time a beacon sends us position data
    '''    
    #print('Beacon update (BSM): ', data)
    print('Beacon update (BSM)')



################################################################################################
import math
# trigger signal
def trigger_flag(trigger_dis,robot_pos,vehicle_pos):
    L2_dis = np.linalg.norm(robot_pos-vehicle_pos)
    heading = get_heading()
    angle = math.atan2(heading[1],heading[0]) / math.pi * 180
    if angle < 0:
        angle = angle + 2 * 180
    dis = np.dot(robot_pos-vehicle_pos,heading)
    #dis = np.linalg.norm(robot_pos-vehicle_pos)
    #trigger_dis = 30
    print(dis,trigger_dis,np.sqrt(pow(max(L2_dis,dis),2)-pow(dis,2)),L2_dis,heading,angle)
    gps_to_car_head_dis = 2
    if dis < trigger_dis + gps_to_car_head_dis and dis > 0 and angle > 225 and angle < 300 and dis_buffer[-1] < dis_buffer[-2]:
        return True
    else:
        return False
    
# reverse signal
def reverse_flag():
    global dis_buffer
    vehicle_pos,robot_pos = get_pos()
    distance = np.linalg.norm(robot_pos-vehicle_pos)
    if distance > 15 and dis_buffer[-1] > dis_buffer[-2]:
        return True
    else:
        return False

# transition from lat lon to pos
import utm
def convert(pos):# set to Mcity local position
    pos[0] = pos[0] - 276000 + 102.89
    pos[1] = pos[1] - 4686800 + 281.25
    return pos
def get_pos():
    global vehicle_lat,vehicle_lon,robot_lat,robot_lon
    vehicle_pos_tmp = utm.from_latlon(vehicle_lat,vehicle_lon)
    vehicle_pos = np.array(vehicle_pos_tmp[0:2])
    vehicle_pos = convert(vehicle_pos)
    robot_pos_tmp = utm.from_latlon(robot_lat,robot_lon)
    robot_pos = np.array(robot_pos_tmp[0:2])
    robot_pos = convert(robot_pos)
    return vehicle_pos,robot_pos

# get vehicle heading by distance difference
def get_heading():
    global vehicle_last_lat,vehicle_last_lon
    vehicle_pos,robot_pos = get_pos()
    vehicle_last_pos_tmp = utm.from_latlon(vehicle_last_lat,vehicle_last_lon)
    vehicle_last_pos = np.array(vehicle_last_pos_tmp[0:2])
    vehicle_last_pos = convert(vehicle_last_pos)
    direction = vehicle_pos - vehicle_last_pos
    if np.all(vehicle_last_pos == vehicle_pos):
        direction = robot_pos - vehicle_pos
    heading = direction / np.linalg.norm(direction)
    return heading

# distance error
def get_err(trigger_dis):
    vehicle_pos,robot_pos = get_pos()
    heading = get_heading()
    distance = np.dot(robot_pos-vehicle_pos,heading)
    #distance = np.linalg.norm(robot_pos-vehicle_pos)
    dis_err = np.abs(trigger_dis-distance)
    return dis_err
    
# get test info from json file
import json
def load_test_info(path):
    with open(path, "r", encoding="utf-8") as f:
        content = json.load(f)
    test_info_dict = []
    for level in ['low','mid','high']:
        for info in content[level]:
            info.update({'Risk level':level})
            test_info_dict.append(info)
    return test_info_dict

# init distance buffer
def init_dis_buffer(buffer_len):
    dis_buffer = []
    for i in range(buffer_len):
        time.sleep(0.01)
        vehicle_pos,robot_pos = get_pos()
        dis_buffer.append(np.linalg.norm(vehicle_pos-robot_pos))
    print("distance buffer ready")
    return dis_buffer

# extract test info
def extract_test_info(test_info):
    meters = test_info['crossing dis']
    meters = 10
    meters_per_second = test_info['crossing sp']
    trigger_dis = test_info['triggered dis']
    return meters, meters_per_second, trigger_dis

# get gps test data
import csv
def gps_test(path,vehicle_pos,robot_pos):
    with open(path+'vehicle_pos.csv', 'a', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(list(vehicle_pos)+[Timestamp])
    with open(path+'robot_pos.csv', 'a', newline='') as csvfile2:
        csvwriter2 = csv.writer(csvfile2)
        csvwriter2.writerow(list(robot_pos)+[robot_timestamp])

# update distance buffer
def update_dis_buffer():
    vehicle_pos,robot_pos = get_pos()
    buffer_len = len(dis_buffer)
    dis_buffer.append(np.linalg.norm(vehicle_pos-robot_pos))
    dis_buffer.pop(0)
    dis_buffer[buffer_len-1] = np.mean(np.array(dis_buffer[buffer_len-1-100:buffer_len]))

# record all case data
import pandas as pd
def record_all_case_data(all_case_data,path,current_case_id=0,test_info=None,mode='running'):
    test_key_all = ["case_id","Risk level","Triggered dis",'Crossing sp',"Crossing dis",'Initial timestamp',"Dis err",'Sp err','VUT init sp']
    if mode == 'running':
        meters, meters_per_second, trigger_dis = extract_test_info(test_info)
        tmp_data = [[current_case_id+1,test_info["Risk level"],trigger_dis,
                meters_per_second,meters,Timestamp,get_err(trigger_dis),0,vehicle_v]]
        all_case_data.append(tmp_data)
        data_tmp = pd.DataFrame(columns=test_key_all,data=tmp_data)
        data_tmp.to_csv(path+'all_case_{}_{}.csv'.format(current_case_id+1,time.time()),index=False)
        return all_case_data
    else:
        data_tmp = pd.DataFrame(columns=test_key_all,data=all_case_data)
        data_tmp.to_csv(path,index=False)
# record each case data
def record_each_case_data(path,meters_per_second,need_header=True):
    test_key_each = ['timestamp', 'VUT x', 'VUT y', 'VUT sp', 'VUT lon sp', 'VUT lat sp', 'VUT acc', 'VUT lon acc', 'VUT lat acc', 'VUT heading', 'challenger x', 'challenger y', 'challenger sp', 'challenger lon sp', 'challenger lat sp', 'challenger acc', 'challenger lon acc', 'challenger lat acc', 'challenger heading']
    vehicle_pos,robot_pos = get_pos()
    each_case_data = [[Timestamp,vehicle_pos[0],vehicle_pos[1],
                        vehicle_v,0,0,vehicle_acc,0,0,vehicle_heading,
                        robot_pos[0],robot_pos[1],meters_per_second,0,0,0,0,0,0]]   # 0 : unknown
    data_tmp = pd.DataFrame(columns=test_key_each,data=each_case_data)
    data_tmp.to_csv(path,mode='a',header=need_header,index=False)

# wait while update distance buffer
def smart_wait(slp_time,path,sp):
    for _ in range(int(slp_time/0.02)):
        update_dis_buffer()
        record_each_case_data(path,sp,need_header=False)
        time.sleep(0.02)


####################################################################################################
# control logic

# connect to vehicle
sio2.connect(server2, namespaces=[namespace2])

# connect to robot
sio.connect(server, namespaces=[namespace])
while not connected:
    time.sleep(0.02)
print("connected")

# receive vehicle info and trigger robot   
test_info_dict = load_test_info("./VRU_crosswalk.json")
total_case_num = len(test_info_dict)
if len(sys.argv) == 2:
    current_case_id = int(sys.argv[1])
    if current_case_id > total_case_num - 1:
        print("error case id, max value is ", total_case_num - 1)
else:
    current_case_id = 0

print(current_case_id)
each_data_path = './cases_data/case_{}_{}.csv'.format(current_case_id+1,time.time())
all_data_path = './cases_data/all_case_{}_{}.csv'.format(current_case_id+1,time.time())
all_case_data = []
dis_buffer = init_dis_buffer(buffer_len=200)
while current_case_id < total_case_num:
    time.sleep(0.02)
    test_info = test_info_dict[current_case_id]
    meters, meters_per_second, trigger_dis = extract_test_info(test_info)
    vehicle_pos,robot_pos = get_pos()
    record_each_case_data(each_data_path,meters_per_second,need_header=False)
    #gps_test('./',vehicle_pos,robot_pos)
    #print(np.linalg.norm(vehicle_pos-robot_pos))
    update_dis_buffer()
    if trigger_flag(trigger_dis,robot_pos,vehicle_pos):
        print("trigger")
        # go ahead
        trigger(proxy_id, meters, meters_per_second)
        all_case_data = record_all_case_data(all_case_data,all_data_path,current_case_id,test_info)
        record_each_case_data(each_data_path,meters_per_second,need_header=False)
        current_case_id = current_case_id + 1
        smart_wait(meters/meters_per_second + 3, each_data_path, meters_per_second)
        # reverse
        while not reverse_flag():
            update_dis_buffer()
            record_each_case_data(each_data_path,meters_per_second,need_header=False)
            time.sleep(0.02)
        trigger(proxy_id, -meters, meters_per_second)
        smart_wait(meters/meters_per_second + 3, each_data_path, meters_per_second)

record_all_case_data(all_case_data,all_data_path,mode='end')

# exit
sio.disconnect()
sio2.disconnect()