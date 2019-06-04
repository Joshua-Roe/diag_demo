#! /usr/bin/env python
import rospy
import actionlib   # navigation
from diagnostic_msgs.msg import DiagnosticArray
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal


# function: Callback function for diagnostics
def diagCallback(data):
 for i in data.status:
  if i.name == "husky_node: power_status":
   batteryPercent = i.values[0].value
  if i.name == "husky_node: system_status":
   #batteryVoltage = i.values[1].value
   battery_voltage(i.values[1].value)
   print("callback" + i.values[1].value)
   #print i.values[1].key + " " + batteryVoltage

  
# function: Move the base of the robot Husky
def movebase_client(trans,quaternion,frame):
 client = actionlib.SimpleActionClient('move_base',MoveBaseAction)
 client.wait_for_server()

 goal = MoveBaseGoal()
 goal.target_pose.header.frame_id = frame
 goal.target_pose.header.stamp = rospy.Time.now()
 # Transition forward
 goal.target_pose.pose.position.x = trans[0]
 goal.target_pose.pose.position.y = trans[1]
 #goal.target_pose.pose.position.z = trans[2] we don't need the z dim only x and y
 # Turning in term of x,y,z,w https://www.andre-gaschler.com/rotationconverter/
 goal.target_pose.pose.orientation.x = quaternion[0]
 goal.target_pose.pose.orientation.y = quaternion[1]
 goal.target_pose.pose.orientation.z = quaternion[2]
 goal.target_pose.pose.orientation.w = quaternion[3]
 #test voltage
 print(battery_voltage())
 min_volt = 24.00
 #if min_volt >= float(battery_voltage()):
 # check the votlage of the battery during navigation
 if float(battery_voltage()) <= min_volt:   
  print("battery low")
  return False
 client.send_goal(goal)
 wait = client.wait_for_result()
 if not wait:
  rospy.logerr("Action server not available!")
  rospy.signal_shutdown("Action server not available!")
 else:
  return client.get_result()

# function: battery_voltage to store the voltage value of the battery ak all time
def battery_voltage(voltage = -1):
 global cur_volt # to keep it static for next time yo access the function
 if voltage != -1:
  cur_volt = voltage
 return cur_volt

#init
rospy.init_node('navigation_failure', anonymous=True)
battery_voltage(1)
t_frame = "base_link"

t_trans = [] # linear goal
t_x = 3
t_y = 0
t_z = 0
t_trans.append(t_x)
t_trans.append(t_y)
t_trans.append(t_z)

t_quaternion = [] # rotational goal
t_qx = 0
t_qy = 0
t_qz = 0.7071068
t_qw = 0.7071068
t_quaternion.append(t_qx)
t_quaternion.append(t_qy)
t_quaternion.append(t_qz)
t_quaternion.append(t_qw)
# subscribe to rospy diagnostics - Callback function for diagnostics starts
rospy.Subscriber('/diagnostics', DiagnosticArray , diagCallback)
rate = rospy.Rate(1) # 1 Hz to start Sync
rate.sleep() #wait for first data
rate = rospy.Rate(10) # 10 Hz bwtween itreation
#main loop - GO
while not rospy.is_shutdown():
 t_quaternion[2] = 0
 t_quaternion[3] = 1 # dont rotate
 t_trans[0] = 4# 1 meter
 for i in range(0,1): # 4 times - 0,1,2,3
  print("step..." + str(i+1))
  result = movebase_client(t_trans,t_quaternion,t_frame) #call function
  if result:
   rospy.loginfo("Goal execution done!")
  else:
   #recovery plan TBC
   print("recovery")
  rate.sleep()
  #if i == 2: battery_voltage(15)
  # self certification check
 print("complete")
 rospy.signal_shutdown("Done")


