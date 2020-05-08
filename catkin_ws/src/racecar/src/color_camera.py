#!/usr/bin/python

# Placeholder ROS node until realsense-ros is figured our
#TODO: Configure Realsense-ROS and pull images through that

import rospy
from sensor_msgs.msg import Image

import cv2 as cv
import numpy as np

# Connect to the camera
camera = cv.VideoCapture(1)

# Initialize camera node
rospy.init_node('color_camera')
image_topic = rospy.Publisher('/camera/color/image_raw',
                              Image,
                              queue_size=1)

while not rospy.is_shutdown():
    # Take image
    _, frame = camera.read()
    if frame is None:
        continue

    # Build image message
    msg = Image()
    msg.height = frame.shape[0]
    msg.width = frame.shape[1]
    msg.encoding = 'bgr8'
    msg.is_bigendian = 0
    msg.step = 3 * msg.width
    msg.data = frame.flatten().tostring()

    # send image
    image_topic.publish(msg)

camera.release()
"""

import rospy
from sensor_msgs.msg import Image as msg_Image
from cv_bridge import CvBridge, CvBridgeError
import sys
import os

class ImageListener:
    def __init__(self, topic):
        self.topic = topic
        self.bridge = CvBridge()
        self.sub = rospy.Subscriber(topic, msg_Image, self.imageDepthCallback)

    def imageDepthCallback(self, data):
        try:
            cv_image = self.bridge.imgmsg_to_cv2(data, data.encoding)
            pix = (data.width/2, data.height/2)
            sys.stdout.write('%s: Depth at center(%d, %d): %f(mm)\r' % (self.topic, pix[0], pix[1], cv_image[pix[1], pix[0]]))
            sys.stdout.flush()
        except CvBridgeError as e:
            print(e)
            return

def main():
    topic = '/camera/depth/image_rect_raw'
    listener = ImageListener(topic)
    rospy.spin()

if __name__ == '__main__':
    node_name = os.path.basename(sys.argv[0]).split('.')[0]
    rospy.init_node(node_name)
    main()"""
