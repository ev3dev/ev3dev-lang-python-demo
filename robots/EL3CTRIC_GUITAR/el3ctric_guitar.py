#!/usr/bin/env micropython


from ev3dev2.motor import MediumMotor, OUTPUT_D
from ev3dev2.sensor import INPUT_1, INPUT_4
from ev3dev2.sensor.lego import TouchSensor, InfraredSensor
from ev3dev2.led import Leds
from ev3dev2.sound import Sound

from time import sleep


class El3ctricGuitar:
    NOTES = [1318, 1174, 987, 880, 783, 659, 587, 493, 440, 392, 329, 293]
    N_NOTES = len(NOTES)

    def __init__(
            self, lever_motor_port: str = OUTPUT_D,
            touch_sensor_port: str = INPUT_1, ir_sensor_port: str = INPUT_4):
        self.lever_motor = MediumMotor(address=lever_motor_port)

        self.touch_sensor = TouchSensor(address=touch_sensor_port)

        self.ir_sensor = InfraredSensor(address=ir_sensor_port)
        
        self.leds = Leds()

        self.speaker = Sound()

    def start_up(self):
        self.leds.animate_flash(
            color='ORANGE',
            groups=('LEFT', 'RIGHT'),
            sleeptime=0.5,
            duration=3,
            block=True)

        self.lever_motor.on_for_seconds(
            speed=5,
            seconds=1,
            brake=False,
            block=True)

        self.lever_motor.on_for_degrees(
            speed=-5,
            degrees=30,
            brake=True,
            block=True)

        sleep(0.1)

        self.lever_motor.reset()

    def play_music(self):
        if self.touch_sensor.is_released:
            raw = sum(self.ir_sensor.proximity for _ in range(4)) / 4

            self.speaker.tone(
                self.NOTES[min(round(raw / 5), self.N_NOTES - 1)]
                - 11 * self.lever_motor.position,
                100,
                play_type=Sound.PLAY_WAIT_FOR_COMPLETE)

    def main(self):
        self.start_up()
        while True:
            self.play_music()


if __name__ == '__main__':
    EL3CTRIC_GUITAR = El3ctricGuitar()
    EL3CTRIC_GUITAR.main()
