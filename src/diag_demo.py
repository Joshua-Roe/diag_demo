#! /usr/bin/env python
import rospy
from diagnostic_msgs.msg import DiagnosticArray 

def diagCallback(data):
 for i in data.status:
  if i.name == "husky_node: power_status":
   batteryPercent = i.values[0].value
  if i.name == "husky_node: system_status":
   batteryVoltage = i.values[1].value
   print i.values[1].key + " " + batteryVoltage

rospy.init_node('diag_demo')
rospy.Subscriber('/diagnostics', DiagnosticArray , diagCallback)
rate = rospy.Rate(10)

while not rospy.is_shutdown():
 #print batteryVoltage
 rate.sleep()

