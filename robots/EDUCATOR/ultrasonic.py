#!/usr/bin/env python3
"""
Use robot to reposition cuboid.

This script is a simple demonstration of the ultrasonic sensor and medium
motor.
"""

from ev3dev2.motor import (
    MoveSteering, MediumMotor, OUTPUT_A, OUTPUT_B, OUTPUT_C)
from ev3dev2.sensor.lego import UltrasonicSensor
from time import sleep

motor_pair = MoveSteering(OUTPUT_B, OUTPUT_C)
medium_motor = MediumMotor(OUTPUT_A)
ultrasonic_sensor = UltrasonicSensor()

# Start robot moving forward
motor_pair.on(steering=0, speed=10)

# Wait until robot less than 3.5cm from cuboid
while ultrasonic_sensor.distance_centimeters > 3.5:
    sleep(0.01)

# Stop moving forward
motor_pair.off()

# Lower robot arm over cuboid
medium_motor.on_for_degrees(speed=-10, degrees=90)

# Drag cuboid backwards for 2 seconds
motor_pair.on_for_seconds(steering=0, speed=-20, seconds=2)

# Raise robot arm
medium_motor.on_for_degrees(speed=10, degrees=90)

# Move robot away from cuboid
motor_pair.on_for_seconds(steering=0, speed=-20, seconds=2)
