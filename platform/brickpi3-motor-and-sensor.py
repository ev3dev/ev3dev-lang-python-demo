#!/usr/bin/env python3

"""
The Brickpi3 doesn't support auto-detecting motors and sensors. To use devices
connected to the input ports, you must specify what type of device it is.
Output ports are pre-configured as NXT Large motors and do not need to be
configured manually.
"""

from time import sleep
from ev3dev2 import list_devices
from ev3dev2.port import LegoPort
from ev3dev2.motor import OUTPUT_A, LargeMotor, SpeedPercent
from ev3dev2.sensor import INPUT_1
from ev3dev2.sensor.lego import UltrasonicSensor

p1 = LegoPort(INPUT_1)
# http://docs.ev3dev.org/projects/lego-linux-drivers/en/ev3dev-stretch/brickpi3.html#brickpi3-in-port-modes
p1.mode = 'ev3-uart'
# http://docs.ev3dev.org/projects/lego-linux-drivers/en/ev3dev-stretch/sensors.html#supported-sensors
p1.set_device = 'lego-ev3-us'

# allow for some time to load the new drivers
sleep(0.5)

s = UltrasonicSensor(INPUT_1)
m = LargeMotor(OUTPUT_A)

print("Running motor...")

while True:
    dist = s.distance_centimeters
    if dist < 50:
        m.on(SpeedPercent(30))
    else:
        m.on(SpeedPercent(-30))

    sleep(0.05)
