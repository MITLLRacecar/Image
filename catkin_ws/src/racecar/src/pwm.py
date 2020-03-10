#!/usr/bin/python

# Abstraction layer for controlling the motors

import rospy
import maestro
from ackermann_msgs.msg import AckermannDriveStamped
from std_msgs.msg import String
import time

CAR_MAX_SPEED = 1.0
CAR_MAX_TURN = 1.0

PWM_SPEED_MAX = 9000
PWM_SPEED_MIN = 3000
PWM_SPEED_CHANNEL = 0

PWM_TURN_LEFT = 9000
PWM_TURN_RIGHT = 3000
PWM_TURN_LEFT_CAP = 8000
PWM_TURN_RIGHT_CAP = 4000
PWM_TURN_CHANNEL = 1

pwm_debug_channel = rospy.Publisher("/pwm_debug", String, queue_size=1)

def remap_to_range(val,old_min,old_max,new_min,new_max):
    """
    Helper function here being used to remap a value from a given range to a new range.

    Inputs:
        val (number): number in old range to be rescaled
        old_min (number): 'lower' bound of old range
        old_max (number): 'upper' bound of old range
        new_min (number): 'lower' bound of new range
        new_max (number): 'upper' bound of new range

    Note: min need not be less than max in general.
    Flipping the direction will cause the sign of the mapping to flip (examples below).

    Example:

        >>> remap_to_range(5,0,10,0,50)
        25

        >>> remap_to_range(5,0,20,1000,900)
        975

    """
    old_span = old_max-old_min
    new_span = new_max-new_min
    return new_min + new_span*(float(val-old_min)/float(old_span))

def motor_callback(msg):
    """
    Callback function passed to the ROS subscriber /motor to compute signals to send to the PWM
    """
    global controller

    velocity_signal = int(remap_to_range(msg.drive.speed, \
            -CAR_MAX_SPEED, CAR_MAX_SPEED, PWM_SPEED_MIN, PWM_SPEED_MAX))
    
    turn_signal = int(remap_to_range(msg.drive.steering_angle, \
            -CAR_MAX_TURN, CAR_MAX_TURN, PWM_TURN_LEFT_CAP, PWM_TURN_RIGHT_CAP))
    
    # Set drive speed
    controller.setTarget(PWM_SPEED_CHANNEL, velocity_signal)

    # Set drive angle
    controller.setTarget(PWM_TURN_CHANNEL, turn_signal)
    
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
