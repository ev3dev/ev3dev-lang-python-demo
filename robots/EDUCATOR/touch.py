#!/usr/bin/env python3
"""
Reverse robot if bumps into wall.

This script is a simple demonstration of the touch sensor.
"""

from ev3dev2.motor import MoveSteering, OUTPUT_B, OUTPUT_C
from ev3dev2.sensor.lego import TouchSensor

motor_pair = MoveSteering(OUTPUT_B, OUTPUT_C)
touch_sensor = TouchSensor()

# Start robot moving forward
motor_pair.on(steering=0, speed=10)

# Wait until robot touches wall
touch_sensor.wait_for_pressed()

# Stop moving forward
motor_pair.off()

# Reverse away from wall
motor_pair.on_for_seconds(steering=0, speed=-10, seconds=2)
