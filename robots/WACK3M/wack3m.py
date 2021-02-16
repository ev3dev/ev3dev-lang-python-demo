#!/usr/bin/env python3


from ev3dev.ev3 import (
    Motor, MediumMotor, LargeMotor, OUTPUT_A, OUTPUT_B, OUTPUT_C,
    TouchSensor, InfraredSensor, INPUT_1, INPUT_4,
    Leds, Screen, Sound
)

from PIL import Image
from random import randint, uniform
from time import sleep, time


class Wack3m:
    N_WHACK_TIMES = 10

    def __init__(
            self,
            left_motor_port: str = OUTPUT_B, right_motor_port: str = OUTPUT_C,
            middle_motor_port: str = OUTPUT_A,
            touch_sensor_port: str = INPUT_1, ir_sensor_port: str = INPUT_4):
        self.left_motor = LargeMotor(address=left_motor_port)
        self.right_motor = LargeMotor(address=right_motor_port)
        self.middle_motor = MediumMotor(address=middle_motor_port)

        self.touch_sensor = TouchSensor(address=touch_sensor_port)

        self.ir_sensor = InfraredSensor(address=ir_sensor_port)

        self.leds = Leds()
        self.screen = Screen()
        self.speaker = Sound()

    def start_up(self):
        self.leds.set_color(
            group=Leds.LEFT,
            color=Leds.RED,
            pct=1)
        self.leds.set_color(
            group=Leds.RIGHT,
            color=Leds.RED,
            pct=1)

        self.screen.clear()
        self.screen.draw.text(
            xy=(5, 2),
            text='WACK3M',
            fill=None,
            font=None,
            anchor=None,
            spacing=4,
            align='left',
            direction=None,
            features=None,
            language=None,
            stroke_width=0,
            stroke_fill=None)
        self.screen.update()

        self.left_motor.run_timed(
            speed_sp=-300,
            time_sp=1000,
            stop_action=Motor.STOP_ACTION_HOLD)
        self.left_motor.wait_while(Motor.STATE_RUNNING)

        self.left_motor.reset()

        self.middle_motor.run_timed(
            speed_sp=-50,
            time_sp=2000,
            stop_action=Motor.STOP_ACTION_HOLD)
        self.middle_motor.wait_while(Motor.STATE_RUNNING)

        self.middle_motor.reset()

        self.right_motor.run_timed(
            speed_sp=-300,
            time_sp=1000,
            stop_action=Motor.STOP_ACTION_HOLD)
        self.right_motor.wait_while(Motor.STATE_RUNNING)

        self.right_motor.reset()

    def main(self):
        self.start_up()

        while True:
            self.speaker.play(wav_file='media/Start.wav').wait()

            self.screen.clear()
            self.screen.image.paste(im=Image.open('media/Touch sensor.bmp'))
            self.screen.update()

            self.leds.set_color(
                group=Leds.LEFT,
                color=Leds.ORANGE,
                pct=1)
            self.leds.set_color(
                group=Leds.RIGHT,
                color=Leds.ORANGE,
                pct=1)

            while not self.touch_sensor.is_pressed:
                pass

            self.speaker.play(wav_file='media/Go.wav').wait()

            self.leds.set_color(
                group=Leds.LEFT,
                color=Leds.GREEN,
                pct=1)
            self.leds.set_color(
                group=Leds.RIGHT,
                color=Leds.GREEN,
                pct=1)

            total_response_time = 0

            sleep(1)

            for _ in range(self.N_WHACK_TIMES):
                self.leds.set_color(
                    group=Leds.LEFT,
                    color=Leds.GREEN,
                    pct=1)
                self.leds.set_color(
                    group=Leds.RIGHT,
                    color=Leds.GREEN,
                    pct=1)

                self.screen.clear()
                self.screen.image.paste(im=Image.open('media/EV3 icon.bmp'))
                self.screen.update()

                sleep(uniform(0.1, 3))

                which_motor = randint(1, 3)

                self.screen.clear()

                if which_motor == 1:
                    self.left_motor.run_to_rel_pos(
                        speed_sp=1000,
                        position_sp=60,
                        stop_action=Motor.STOP_ACTION_COAST)
                    start_time = time()
                    self.left_motor.wait_while(Motor.STATE_RUNNING)

                    self.screen.image.paste(
                        im=Image.open('media/Middle left.bmp'))
                    self.screen.update()

                    self.left_motor.run_timed(
                        speed_sp=-400,
                        time_sp=500,
                        stop_action=Motor.STOP_ACTION_HOLD)
                    self.left_motor.wait_while(Motor.STATE_RUNNING)

                    proximity = self.ir_sensor.proximity
                    while abs(self.ir_sensor.proximity - proximity) <= 4:
                        pass

                elif which_motor == 2:
                    self.middle_motor.run_to_rel_pos(
                        speed_sp=1000,
                        position_sp=170,
                        stop_action=Motor.STOP_ACTION_COAST)
                    start_time = time()
                    self.middle_motor.wait_while(Motor.STATE_RUNNING)

                    self.screen.image.paste(im=Image.open('media/Neutral.bmp'))
                    self.screen.update()

                    self.middle_motor.run_timed(
                        speed_sp=-400,
                        time_sp=400,
                        stop_action=Motor.STOP_ACTION_COAST)
                    self.middle_motor.wait_while(Motor.STATE_RUNNING)

                    proximity = self.ir_sensor.proximity
                    while abs(self.ir_sensor.proximity - proximity) <= 5:
                        pass

                else:
                    self.right_motor.run_to_rel_pos(
                        speed_sp=1000,
                        position_sp=60,
                        stop_action=Motor.STOP_ACTION_COAST)
                    start_time = time()
                    self.right_motor.wait_while(Motor.STATE_RUNNING)

                    self.screen.image.paste(
                        im=Image.open('media/Middle right.bmp'))
                    self.screen.update()

                    self.right_motor.run_timed(
                        speed_sp=-400,
                        time_sp=500,
                        stop_action=Motor.STOP_ACTION_HOLD)
                    self.right_motor.wait_while(Motor.STATE_RUNNING)

                    proximity = self.ir_sensor.proximity
                    while abs(self.ir_sensor.proximity - proximity) <= 5:
                        pass

                response_time = time() - start_time

                self.screen.clear()
                self.screen.image.paste(im=Image.open('media/Dizzy.bmp'))
                self.screen.draw.text(
                    xy=(0, 11),
                    text='Reponse Time: {:.1f}s'.format(response_time),
                    fill=None,
                    font=None,
                    anchor=None,
                    spacing=4,
                    align='left',
                    direction=None,
                    features=None,
                    language=None,
                    stroke_width=0,
                    stroke_fill=None)
                self.screen.update()

                self.leds.set_color(
                    group=Leds.LEFT,
                    color=Leds.RED,
                    pct=1)
                self.leds.set_color(
                    group=Leds.RIGHT,
                    color=Leds.RED,
                    pct=1)

                self.speaker.play(wav_file='media/Boing.wav').wait()

                total_response_time += response_time

            average_response_time = total_response_time / self.N_WHACK_TIMES

            self.screen.clear()
            self.screen.draw.text(
                xy=(6, 3),
                text='Average Response Time: {:.1f}s'
                     .format(average_response_time),
                fill=None,
                font=None,
                anchor=None,
                spacing=4,
                align='left',
                direction=None,
                features=None,
                language=None,
                stroke_width=0,
                stroke_fill=None)
            self.screen.update()

            self.speaker.play(
                wav_file='media/Fantastic.wav'
                         if average_response_time <= 1
                         else 'media/Good job.wav').wait()

            self.speaker.play(wav_file='media/Game over.wav').wait()

            self.leds.set_color(
                group=Leds.LEFT,
                color=Leds.RED,
                pct=1)
            self.leds.set_color(
                group=Leds.RIGHT,
                color=Leds.RED,
                pct=1)

            sleep(4)


if __name__ == '__main__':
    WACK3M = Wack3m()

    WACK3M.main()
