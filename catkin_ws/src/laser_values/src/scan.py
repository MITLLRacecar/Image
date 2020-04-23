#! /usr/bin/env python
 
import rospy
from sensor_msgs.msg import LaserScan

def callback(msg):
    forward =  msg.ranges[340:370]
    #print(sum(forward)/len(forward))
    #print("-------------")
    
    clean = filter(lambda a: a != 0.0, msg.ranges)
    print(min(clean))


rospy.init_node('scan_values')
sub = rospy.Subscriber('/scan', LaserScan, callback)
rospy.spin()
