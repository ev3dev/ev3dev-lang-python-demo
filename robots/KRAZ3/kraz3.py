#!/usr/bin/env python3


from ev3dev.ev3 import (
    Motor, MediumMotor, OUTPUT_A, OUTPUT_B, OUTPUT_C,
    TouchSensor, ColorSensor, INPUT_1, INPUT_3,
    Leds, Sound
)
from ev3dev.helper import RemoteControlledTank

from random import randint
from multiprocessing import Process
from time import sleep


class Kraz3(RemoteControlledTank):
    def __init__(
            self,
            left_motor_port: str = OUTPUT_C, right_motor_port: str = OUTPUT_B,
            wiggle_motor_port: str = OUTPUT_A,
            touch_sensor_port: str = INPUT_1,
            color_sensor_port: str = INPUT_3):
        super().__init__(
            left_motor=left_motor_port, right_motor=right_motor_port,
            polarity='inversed')

        self.wiggle_motor = MediumMotor(address=wiggle_motor_port)

        self.touch_sensor = TouchSensor(address=touch_sensor_port)

        self.color_sensor = ColorSensor(address=color_sensor_port)

        self.leds = Leds()
        self.speaker = Sound()

    def kungfu_manoeuvre_if_touched_or_remote_controlled(self):
        """
        Kung-Fu manoeuvre via Touch Sensor and Remote Control of head and arms
        """
        while True:
            if self.touch_sensor.is_pressed:
                self.speaker.play(wav_file='media/Kung fu.wav')

                self.wiggle_motor.run_to_rel_pos(
                    speed_sp=500,
                    position_sp=360,
                    stop_action=Motor.STOP_ACTION_HOLD)

            elif self.remote.beacon:
                self.wiggle_motor.run_forever(speed_sp=111)

            else:
                self.wiggle_motor.stop(stop_action=Motor.STOP_ACTION_HOLD)

            sleep(0.01)

    def keep_reacting_to_colors(self):
        while True:
            detected_color = self.color_sensor.color

            if detected_color == ColorSensor.COLOR_YELLOW:
                self.speaker.play(wav_file='media/Yellow.wav')

                self.wiggle_motor.run_to_rel_pos(
                    speed_sp=860,
                    position_sp=-360,
                    stop_action=Motor.STOP_ACTION_HOLD)
                self.wiggle_motor.wait_while(Motor.STATE_RUNNING)

                self.speaker.play(wav_file='media/Uh-oh.wav').wait()

                sleep(0.5)

                self.speaker.play(wav_file='media/Sneezing.wav').wait()

                sleep(0.5)

            elif detected_color == ColorSensor.COLOR_RED:
                self.speaker.play(wav_file='media/Shouting.wav').wait()

                for _ in range(randint(1, 6)):
                    self.speaker.play(wav_file='media/Smack.wav').wait()

                self.leds.set_color(
                    group=Leds.LEFT,
                    color=Leds.RED,
                    pct=1)
                self.leds.set_color(
                    group=Leds.RIGHT,
                    color=Leds.RED,
                    pct=1)

                self.wiggle_motor.run_to_rel_pos(
                    speed_sp=170,
                    position_sp=360,
                    stop_action=Motor.STOP_ACTION_HOLD)
                self.wiggle_motor.wait_while(Motor.STATE_RUNNING)

                self.speaker.play(wav_file='media/LEGO.wav').wait()
                self.speaker.play(wav_file='media/MINDSTORMS.wav').wait()

                self.leds.all_off()

            elif detected_color == ColorSensor.COLOR_BROWN:
                self.speaker.play(wav_file='media/Brown.wav').wait()

                sleep(1)

                self.wiggle_motor.run_to_rel_pos(
                    speed_sp=200,
                    position_sp=-360,
                    stop_action=Motor.STOP_ACTION_HOLD)
                self.wiggle_motor.wait_while(Motor.STATE_RUNNING)

                self.speaker.play(wav_file='media/Crying.wav').wait()

            elif detected_color == ColorSensor.COLOR_GREEN:
                self.speaker.play(wav_file='media/Green.wav').wait()

                self.wiggle_motor.run_to_rel_pos(
                    speed_sp=400,
                    position_sp=-360,
                    stop_action=Motor.STOP_ACTION_HOLD)
                self.wiggle_motor.wait_while(Motor.STATE_RUNNING)

                self.speaker.play(wav_file='media/Yes.wav').wait()

                sleep(1)

            elif detected_color == ColorSensor.COLOR_BLUE:
                self.speaker.play(wav_file='media/Blue.wav').wait()

                self.speaker.play(wav_file='media/Fantastic.wav').wait()

                self.speaker.play(wav_file='media/Good job.wav')

                self.wiggle_motor.run_to_rel_pos(
                    speed_sp=750,
                    position_sp=360,
                    stop_action=Motor.STOP_ACTION_HOLD)
                self.wiggle_motor.wait_while(Motor.STATE_RUNNING)

                self.speaker.play(wav_file='media/Magic wand.wav').wait()

            sleep(0.01)

    def main(self):
        Process(
            target=self.kungfu_manoeuvre_if_touched_or_remote_controlled,
            daemon=True).start()

        Process(
            target=self.keep_reacting_to_colors,
            daemon=True).start()

        super().main()


if __name__ == '__main__':
    KRAZ3 = Kraz3()

    KRAZ3.main()
