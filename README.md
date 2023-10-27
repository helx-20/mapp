# mapp
## mapp setup
1. configure ubuntu-22.04 
https://ubuntu.com/download/desktop

2. install ros2(humble) 
https://docs.ros.org/en/humble/Installation/Alternatives/Ubuntu-Development-Setup.html

3. install mcity_msg/MAPPTrigger.msg to ros2
https://docs.ros.org/en/humble/Tutorials/Beginner-Client-Libraries/Custom-ROS2-Interfaces.html
3.1 cd ros2_humble/src
3.2 ros2 pkg create --build-type ament_cmake mcity_msg
3.3 copy "mcity_msg/msg" folder into the new "mcity_msg" folder
3.4 add the following lines to the CMakeLists.txt inside:
find_package(rosidl_default_generators REQUIRED)
rosidl_generate_interfaces(${PROJECT_NAME}
  "msg/MAPPTrigger.msg"
)
3.5 add the following lines to the package.xml:
<buildtool_depend>rosidl_default_generators</buildtool_depend>
<exec_depend>rosidl_default_runtime</exec_depend>
<member_of_group>rosidl_interface_packages</member_of_group>
3.6 cd ros2_humble/src
3.7 colcon build --packages-select mcity_msg
3.8 . ~/ros2_humble/install/local_setup.bash

4. configure python environment
4.1 conda create -n mapp python=3.10 (need to be the same version as ros2)
4.2 pip install:
python-dotenv==1.0.0
rospy2==1.0.3
setuptools==68.2.2
flask-socketio==5.3.4
numpy==1.26.1
pandas==2.1.1
requests==2.31.0

5. enable remote control
5.1 ssh connect to mcity server 35.0.1.xxx
5.2 proxy_launch.sh / proxy_control.sh (setup environment)
5.3 proxy_enable.sh (enable remote control of the robot)

6. run the code to trigger movement
