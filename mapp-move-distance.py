"""
control-proxy.py

Sample Mcity OS script to control a MAPP, moving forward in a straight line.

Either edit the default values below or pass in the values as command line arguments.
"""
import os
import sys
import time
from dotenv import load_dotenv
import socketio
import rospy2 as rospy
#from rosros import rospify as rospy
import json
from std_msgs.msg import String
from mcity_msg.msg import MAPPTrigger
#import MAPPTrigger


meters_per_second = 0
if len(sys.argv) == 3:
    meters = float(sys.argv[1])
    meters_per_second = float(sys.argv[2])
else:
    meters = 1.0
    meters_per_second = 0.5

# Load environment variables and configure
load_dotenv()
api_key = os.environ.get('MCITY_OCTANE_KEY', 'reticulatingsplines')
server = os.environ.get('MCITY_OCTANE_SERVER', 'wss://octane.mvillage.um.city/')
proxy_id = os.environ.get('MCITY_ROBOT_ID', 1)
# api_key = 'reticulatingsplines'
# server = 'wss://octane.mvillage.um.city/'
# proxy_id = os.environ.get('MCITY_ROBOT_ID', 2)
channel = "robot_proxy"
room = "robot"

namespace = "/octane"
connected = False
sent = False



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
    print('Join received with ', data)
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
    print(f"data: {data}")
    if 'data' in data.keys():
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
        print(data)
    else:
        print(f"Data received from {server} is incomplete.")


def trigger_callback():
    global sent
    sent = True
    print("Message sent")


def trigger(proxy_id, meters, meters_per_second):
    print(f"Sending trigger for ID {proxy_id} to {server}")
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

if __name__ == '__main__':

    # Make connection.
    sio.connect(server, namespaces=[namespace])

    # Wait until we are subscribed to the ipc channel for publishing
    while not connected:
        time.sleep(0.02)

    # Send request. Ideally this is incorporated into a running interpreter, so the connection above is already
    # available before calling this function, for lowest latency
    # trigger_msg(msg)
    trigger(proxy_id, meters, meters_per_second)
    # while not rospy.is_shutdown():
    #     time.sleep(0.01)

    # Wait until the message has been sent
    while not sent:
        time.sleep(0.02)

    #time.sleep(meters/meters_per_second+4)
    #trigger(proxy_id, -meters, meters_per_second)

    sio.wait()

    sio.disconnect()

