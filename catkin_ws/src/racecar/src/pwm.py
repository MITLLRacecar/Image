#!/usr/bin/python

# Abstraction layer for controlling the motors

import rospy
import maestro
from ackermann_msgs.msg import AckermannDriveStamped
from std_msgs.msg import String
import time

PWM_SPEED_MAX = 9000
PWM_SPEED_MIN = 3000
PWM_SPEED_CHANNEL = 0

PWM_TURN_LEFT = 9000
PWM_TURN_RIGHT = 3000
PWM_TURN_LEFT_CAP = 9000
PWM_TURN_RIGHT_CAP = 3000
PWM_TURN_CHANNEL = 1

pwm_debug_channel = rospy.Publisher("/pwm_debug", String, queue_size=1)

def motor_callback(msg):
    """
    Callback function passed to the ROS subscriber /motor to compute signals to send to the PWM
    """
    global controller

    # Set drive speed
    controller.setTarget(PWM_SPEED_CHANNEL, int(msg.drive.speed))

    # Set drive angle
    controller.setTarget(PWM_TURN_CHANNEL, int(msg.drive.turn))
    
    pwm_debug_channel.publish(  "Velocity Signal: " + \
                                str(velocity_signal) + " | "\
                                "Turn Signal: " + \
                                str(turn_signal))



# initialize servo controller
controller = maestro.Controller()

# speed config
controller.setRange(PWM_SPEED_CHANNEL, PWM_SPEED_MIN, PWM_SPEED_MAX)
controller.setSpeed(PWM_SPEED_CHANNEL, 0)
controller.setAccel(PWM_SPEED_CHANNEL, 0)
controller.setTarget(PWM_SPEED_CHANNEL, (PWM_SPEED_MAX + PWM_SPEED_MIN) // 2)

# turning config
controller.setRange(PWM_TURN_CHANNEL, PWM_TURN_RIGHT, PWM_TURN_LEFT)
controller.setSpeed(PWM_TURN_CHANNEL, 0)
controller.setAccel(PWM_TURN_CHANNEL, 0)
controller.setTarget(PWM_TURN_CHANNEL, (PWM_TURN_RIGHT + PWM_TURN_LEFT) // 2)

# initialize ros
rospy.init_node('pwm')
rospy.Subscriber('/drive', AckermannDriveStamped, motor_callback)

# wait and shutdown
rospy.spin()
controller.close()
