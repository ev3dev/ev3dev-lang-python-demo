#!/usr/bin/env python3


from ev3dev.ev3 import (
    Motor, MediumMotor, LargeMotor, OUTPUT_A, OUTPUT_B, OUTPUT_C,
    InfraredSensor, RemoteControl, INPUT_4,
    Screen, Sound
)

from threading import Thread
from time import sleep


class Bobb3e:
    def __init__(
            self,
            left_motor_port: str = OUTPUT_B, right_motor_port: str = OUTPUT_C,
            lift_motor_port: str = OUTPUT_A,
            ir_sensor_port: str = INPUT_4, ir_beacon_channel: int = 1):
        self.left_motor = LargeMotor(address=left_motor_port)
        self.right_motor = LargeMotor(address=right_motor_port)
        self.left_motor.polarity = self.right_motor.polarity = \
            Motor.POLARITY_INVERSED

        self.lift_motor = MediumMotor(address=lift_motor_port)

        self.ir_sensor = InfraredSensor(address=ir_sensor_port)
        self.remote_control = RemoteControl(sensor=self.ir_sensor,
                                            channel=ir_beacon_channel)

        self.screen = Screen()
        self.speaker = Sound()

        self.reversing = False

    def drive_or_operate_forks_by_ir_beacon(self, driving_speed: float = 1000):
        """
        Read the commands from the remote control and convert them into actions
        such as go forward, lift and turn.
        """
        while True:
            # lower the forks
            if self.remote_control.red_up and self.remote_control.red_down:
                self.reversing = False

                self.left_motor.stop(stop_action=Motor.STOP_ACTION_HOLD)
                self.right_motor.stop(stop_action=Motor.STOP_ACTION_HOLD)

                self.lift_motor.run_forever(speed_sp=100)

            # raise the forks
            elif self.remote_control.blue_up and self.remote_control.blue_down:
                self.reversing = False

                self.left_motor.stop(stop_action=Motor.STOP_ACTION_HOLD)
                self.right_motor.stop(stop_action=Motor.STOP_ACTION_HOLD)

                self.lift_motor.run_forever(speed_sp=-100)

            # forward
            elif self.remote_control.red_up and self.remote_control.blue_up:
                self.reversing = False

                self.left_motor.run_forever(speed_sp=driving_speed)
                self.right_motor.run_forever(speed_sp=driving_speed)

                self.lift_motor.stop(stop_action=Motor.STOP_ACTION_HOLD)

            # backward
            elif self.remote_control.red_down and \
                    self.remote_control.blue_down:
                self.reversing = True

                self.left_motor.run_forever(speed_sp=-driving_speed)
                self.right_motor.run_forever(speed_sp=-driving_speed)

                self.lift_motor.stop(stop_action=Motor.STOP_ACTION_HOLD)

            # turn left on the spot
            elif self.remote_control.red_up and self.remote_control.blue_down:
                self.reversing = False

                self.left_motor.run_forever(speed_sp=-driving_speed)
                self.right_motor.run_forever(speed_sp=driving_speed)

                self.lift_motor.stop(stop_action=Motor.STOP_ACTION_HOLD)

            # turn right on the spot
            elif self.remote_control.red_down and self.remote_control.blue_up:
                self.reversing = False

                self.left_motor.run_forever(speed_sp=driving_speed)
                self.right_motor.run_forever(speed_sp=-driving_speed)

                self.lift_motor.stop(stop_action=Motor.STOP_ACTION_HOLD)

            # turn left forward
            elif self.remote_control.red_up:
                self.reversing = False

                self.right_motor.run_forever(speed_sp=driving_speed)

                self.lift_motor.stop(stop_action=Motor.STOP_ACTION_HOLD)

            # turn right forward
            elif self.remote_control.blue_up:
                self.reversing = False

                self.left_motor.run_forever(speed_sp=driving_speed)

                self.lift_motor.stop(stop_action=Motor.STOP_ACTION_HOLD)

            # turn left backward
            elif self.remote_control.red_down:
                self.reversing = True

                self.right_motor.run_forever(speed_sp=-driving_speed)

                self.lift_motor.stop(stop_action=Motor.STOP_ACTION_HOLD)

            # turn right backward
            elif self.remote_control.blue_down:
                self.reversing = True

                self.left_motor.run_forever(speed_sp=-driving_speed)

                self.lift_motor.stop(stop_action=Motor.STOP_ACTION_HOLD)

            # otherwise stop
            else:
                self.reversing = False

                self.left_motor.stop(stop_action=Motor.STOP_ACTION_HOLD)
                self.right_motor.stop(stop_action=Motor.STOP_ACTION_HOLD)

                self.lift_motor.stop(stop_action=Motor.STOP_ACTION_HOLD)

            sleep(0.01)

    def sound_alarm_whenever_reversing(self):
        while True:
            if self.reversing:
                self.speaker.play(wav_file='Backing alert.wav').wait()

            sleep(0.01)

    def main(self, driving_speed: float = 1000):
        self.screen.draw.text(
            xy=(3, 2),
            text='BOBB3E',
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

        Thread(target=self.sound_alarm_whenever_reversing,
               daemon=True).start()

        self.drive_or_operate_forks_by_ir_beacon(driving_speed=driving_speed)


if __name__ == '__main__':
    BOBB3E = Bobb3e()
    BOBB3E.main(driving_speed=1000)
