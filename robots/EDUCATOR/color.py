#!/usr/bin/env python3
"""Make robot say whatever color it observes with the color sensor."""

from ev3dev2.sensor.lego import ColorSensor
from time import sleep
from ev3dev2.sound import Sound

color_sensor = ColorSensor()
sound = Sound()

while True:
    color = color_sensor.color
    text = ColorSensor.COLORS[color]
    sound.speak(text)
    sleep(2)
