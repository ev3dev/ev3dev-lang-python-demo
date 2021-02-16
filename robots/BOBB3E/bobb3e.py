#!/usr/bin/env micropython


from ev3dev2.motor import \
    Motor, LargeMotor, MediumMotor, MoveTank, MoveSteering, \
    OUTPUT_A, OUTPUT_B, OUTPUT_C
from ev3dev2.sensor import INPUT_4
from ev3dev2.sensor.lego import InfraredSensor
from ev3dev2.console import Console
from ev3dev2.sound import Sound

from threading import Thread
from time import sleep


class Bobb3e:
    def __init__(
            self,
            left_motor_port: str = OUTPUT_B, right_motor_port: str = OUTPUT_C,
            lift_motor_port: str = OUTPUT_A,
            ir_sensor_port: str = INPUT_4, ir_beacon_channel: int = 1):
        self.tank_driver = \
            MoveTank(
                left_motor_port=left_motor_port,
                right_motor_port=right_motor_port,
                motor_class=LargeMotor)
        self.steer_driver = \
            MoveSteering(
                left_motor_port=left_motor_port,
                right_motor_port=right_motor_port,
                motor_class=LargeMotor)
        self.tank_driver.left_motor.polarity = \
            self.tank_driver.right_motor.polarity = \
            self.steer_driver.left_motor.polarity = \
            self.steer_driver.right_motor.polarity = Motor.POLARITY_INVERSED

        self.lift_motor = MediumMotor(address=lift_motor_port)

        self.ir_sensor = InfraredSensor(address=ir_sensor_port)
        self.ir_beacon_channel = ir_beacon_channel

        self.console = Console()
        self.speaker = Sound()

        self.reversing = False

    def drive_or_operate_forks_by_ir_beacon(self, driving_speed: float = 100):
        """
        Read the commands from the remote control and convert them into actions
        such as go forward, lift and turn.
        """
        while True:
            # lower the forks
            if self.ir_sensor.top_left(
                        channel=self.ir_beacon_channel) and \
                    self.ir_sensor.bottom_left(
                        channel=self.ir_beacon_channel):
                self.reversing = False

                self.tank_driver.off(brake=True)

                self.lift_motor.on(
                    speed=10,
                    brake=False,
                    block=False)

            # raise the forks
            elif self.ir_sensor.top_right(
                        channel=self.ir_beacon_channel) and \
                    self.ir_sensor.bottom_right(
                        channel=self.ir_beacon_channel):
                self.reversing = False

                self.tank_driver.off(brake=True)

                self.lift_motor.on(
                    speed=-10,
                    brake=False,
                    block=False)

            # forward
            elif self.ir_sensor.top_left(
                        channel=self.ir_beacon_channel) and \
                    self.ir_sensor.top_right(
                        channel=self.ir_beacon_channel):
                self.reversing = False

                self.tank_driver.on(
                    left_speed=driving_speed,
                    right_speed=driving_speed)

                self.lift_motor.off(brake=True)

            # backward
            elif self.ir_sensor.bottom_left(
                        channel=self.ir_beacon_channel) and \
                    self.ir_sensor.bottom_right(
                        channel=self.ir_beacon_channel):
                self.reversing = True

                self.tank_driver.on(
                    left_speed=-driving_speed,
                    right_speed=-driving_speed)

                self.lift_motor.off(brake=True)

            # turn left on the spot
            elif self.ir_sensor.top_left(
                        channel=self.ir_beacon_channel) and \
                    self.ir_sensor.bottom_right(
                        channel=self.ir_beacon_channel):
                self.reversing = False

                self.steer_driver.on(
                    steering=-100,
                    speed=driving_speed)

                self.lift_motor.off(brake=True)

            # turn right on the spot
            elif self.ir_sensor.top_right(
                        channel=self.ir_beacon_channel) and \
                    self.ir_sensor.bottom_left(
                        channel=self.ir_beacon_channel):
                self.reversing = False

                self.steer_driver.on(
                    steering=100,
                    speed=driving_speed)

                self.lift_motor.off(brake=True)

            # turn left forward
            elif self.ir_sensor.top_left(channel=self.ir_beacon_channel):
                self.reversing = False

                self.steer_driver.on(
                    steering=-50,
                    speed=driving_speed)

                self.lift_motor.off(brake=True)

            # turn right forward
            elif self.ir_sensor.top_right(channel=self.ir_beacon_channel):
                self.reversing = False

                self.steer_driver.on(
                    steering=50,
                    speed=driving_speed)

                self.lift_motor.off(brake=True)

            # turn left backward
            elif self.ir_sensor.bottom_left(channel=self.ir_beacon_channel):
                self.reversing = True

                self.tank_driver.on(
                    left_speed=0,
                    right_speed=-driving_speed)

                self.lift_motor.off(brake=True)

            # turn right backward
            elif self.ir_sensor.bottom_right(channel=self.ir_beacon_channel):
                self.reversing = True

                self.tank_driver.on(
                    left_speed=-driving_speed,
                    right_speed=0)

                self.lift_motor.off(brake=True)

            # otherwise stop
            else:
                self.reversing = False

                self.tank_driver.off(brake=True)

                self.lift_motor.off(brake=True)

            sleep(0.01)

    def sound_alarm_whenever_reversing(self):
        while True:
            if self.reversing:
                self.speaker.play_file(
                    wav_file='/home/robot/sound/Backing alert.wav',
                    volume=100,
                    play_type=Sound.PLAY_WAIT_FOR_COMPLETE)

            sleep(0.01)

    def main(self, driving_speed: float = 100):
        self.console.text_at(
            text='BOBB3E',
            column=3,
            row=2,
            reset_console=False,
            inverse=False,
            alignment='L')

        Thread(target=self.sound_alarm_whenever_reversing).start()

        self.drive_or_operate_forks_by_ir_beacon(driving_speed=driving_speed)


if __name__ == '__main__':
    BOBB3E = Bobb3e()
    BOBB3E.main()
