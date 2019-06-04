#! /usr/bin/env python
import rospy
import random
from std_msgs.msg import Float64

pub = rospy.Publisher('/fake_fault', Float64 , queue_size=10)
rospy.init_node('failure_publisher', anonymous=True)
rate = rospy.Rate(50) # 10hz

voltage = 22.00
i = 0
#print ("forcing voltage of " + str(voltage))
while not rospy.is_shutdown():
 if i == 50:
  voltage = random.uniform(20, 30)
  i = 0
  print ("forcing voltage of " + str(voltage))
 pub.publish(voltage)
 i = i + 1
 rate.sleep()
 #rospy.signal_shutdown("Done")


