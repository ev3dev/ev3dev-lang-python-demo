#!/usr/bin/env python3


from ev3dev.ev3 import (
    Motor, MediumMotor, LargeMotor, OUTPUT_A, OUTPUT_B, OUTPUT_C,
    InfraredSensor, RemoteControl, INPUT_4,
    Sound
)

from time import sleep


class Rac3Truck:
    def __init__(
            self,
            left_motor_port: str = OUTPUT_B, right_motor_port: str = OUTPUT_C,
            polarity: str = Motor.POLARITY_INVERSED,
            steer_motor_port: str = OUTPUT_A,
            ir_sensor_port: str = INPUT_4, ir_beacon_channel: int = 1,
            fast=False):
        self.left_motor = LargeMotor(address=left_motor_port)
        self.right_motor = LargeMotor(address=right_motor_port)

        self.steer_motor = MediumMotor(address=steer_motor_port)

        self.left_motor.polarity = self.right_motor.polarity = polarity

        self.ir_sensor = InfraredSensor(address=ir_sensor_port)
        self.remote_control = RemoteControl(sensor=self.ir_sensor,
                                            channel=ir_beacon_channel)

        self.speaker = Sound()

    def reset(self):
        self.steer_motor.run_timed(
            speed_sp=300,
            time_sp=1500,
            stop_action=Motor.STOP_ACTION_COAST)
        self.steer_motor.wait_while(Motor.STATE_RUNNING)

        self.steer_motor.run_to_rel_pos(
            speed_sp=500,
            position_sp=-120,
            stop_action=Motor.STOP_ACTION_HOLD)
        self.steer_motor.wait_while(Motor.STATE_RUNNING)

        self.steer_motor.reset()

    def steer_left(self):
        if self.steer_motor.position > -65:
            self.steer_motor.run_to_abs_pos(
                speed_sp=-200,
                position_sp=-65,
                stop_action=Motor.STOP_ACTION_HOLD)
            self.steer_motor.wait_while(Motor.STATE_RUNNING)

        else:
            self.steer_motor.stop(stop_action=Motor.STOP_ACTION_HOLD)

    def steer_right(self):
        if self.steer_motor.position < 65:
            self.steer_motor.run_to_abs_pos(
                speed_sp=200,
                position_sp=65,
                stop_action=Motor.STOP_ACTION_HOLD)
            self.steer_motor.wait_while(Motor.STATE_RUNNING)

        else:
            self.steer_motor.stop(stop_action=Motor.STOP_ACTION_HOLD)

    def steer_center(self):
        if self.steer_motor.position < -7:
            self.steer_motor.run_to_abs_pos(
                speed_sp=200,
                position_sp=4,
                stop_action=Motor.STOP_ACTION_HOLD)
            self.steer_motor.wait_while(Motor.STATE_RUNNING)

        elif self.steer_motor.position > 7:
            self.steer_motor.run_to_abs_pos(
                speed_sp=-200,
                position_sp=-4,
                stop_action=Motor.STOP_ACTION_HOLD)
            self.steer_motor.wait_while(Motor.STATE_RUNNING)

        self.steer_motor.stop(stop_action=Motor.STOP_ACTION_HOLD)

        sleep(0.1)

    def drive_by_ir_beacon(self):
        # forward
        if self.remote_control.red_up and self.remote_control.blue_up:
            self.left_motor.run_forever(speed_sp=800)
            self.right_motor.run_forever(speed_sp=800)

            self.steer_center()

        # backward
        elif self.remote_control.red_down and self.remote_control.blue_down:
            self.left_motor.run_forever(speed_sp=-800)
            self.right_motor.run_forever(speed_sp=-800)

            self.steer_center()

        # turn left forward
        elif self.remote_control.red_up:
            self.left_motor.run_forever(speed_sp=600)
            self.right_motor.run_forever(speed_sp=1000)

            self.steer_left()

        # turn right forward
        elif self.remote_control.blue_up:
            self.left_motor.run_forever(speed_sp=1000)
            self.right_motor.run_forever(speed_sp=600)

            self.steer_right()

        # turn left backward
        elif self.remote_control.red_down:
            self.left_motor.run_forever(speed_sp=-600)
            self.right_motor.run_forever(speed_sp=-1000)

            self.steer_left()

        # turn right backward
        elif self.remote_control.blue_down:
            self.left_motor.run_forever(speed_sp=-1000)
            self.right_motor.run_forever(speed_sp=-600)

            self.steer_right()

        # otherwise stop
        else:
            self.left_motor.stop(stop_action=Motor.STOP_ACTION_COAST)
            self.right_motor.stop(stop_action=Motor.STOP_ACTION_COAST)

            self.steer_center()

    def main(self):
        self.reset()

        sleep(1)

        while True:
            self.drive_by_ir_beacon()


if __name__ == '__main__':
    RAC3_TRUCK = Rac3Truck()
    RAC3_TRUCK.main()
