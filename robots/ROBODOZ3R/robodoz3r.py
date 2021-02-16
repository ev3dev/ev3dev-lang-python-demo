#!/usr/bin/env python3


from ev3dev.ev3 import (
    Motor, MediumMotor, OUTPUT_A, OUTPUT_B, OUTPUT_C,
    TouchSensor, RemoteControl, INPUT_1, INPUT_4,
    Screen, Sound
)

from time import sleep, time

from rc_tank_util import RemoteControlledTank


class RoboDoz3r(RemoteControlledTank):
    def __init__(
            self,
            left_motor_port: str = OUTPUT_C, right_motor_port: str = OUTPUT_B,
            shovel_motor_port: str = OUTPUT_A,
            touch_sensor_port: str = INPUT_1,
            ir_sensor_port: str = INPUT_4,
            tank_drive_ir_beacon_channel: int = 1,
            shovel_control_ir_beacon_channel: int = 4):
        super().__init__(
            left_motor_port=left_motor_port, right_motor_port=right_motor_port,
            polarity=Motor.POLARITY_INVERSED,
            ir_sensor_port=ir_sensor_port,
            ir_beacon_channel=tank_drive_ir_beacon_channel)

        self.shovel_motor = MediumMotor(address=shovel_motor_port)

        self.touch_sensor = TouchSensor(address=touch_sensor_port)

        self.shovel_control_remote_control = \
            RemoteControl(
                sensor=self.ir_sensor,
                channel=shovel_control_ir_beacon_channel)

        self.screen = Screen()
        self.speaker = Sound()

    def raise_or_lower_shovel_by_ir_beacon(self):
        """
        If the channel 4 is selected on the IR remote
        then you can control raising and lowering the shovel on the RoboDoz3r.

        Raise the shovel by pressing either Up button,
        or lower the shovel by pressing either Down button.
        """
        # raise the shovel
        if self.shovel_control_remote_control.red_up or \
                self.shovel_control_remote_control.blue_up:
            self.shovel_motor.run_forever(speed_sp=100)

        # lower the shovel
        elif self.shovel_control_remote_control.red_down or \
                self.shovel_control_remote_control.blue_down:
            self.shovel_motor.run_forever(speed_sp=-100)

        else:
            self.shovel_motor.stop(stop_action=Motor.STOP_ACTION_HOLD)

    def main(self, driving_speed: float = 1000):
        """
        This is the main control program for the RoboDoz3r
        """
        self.screen.draw.text(
            xy=(2, 2),
            text='ROBODOZ3R',
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

        self.speaker.play(wav_file='media/Motor start.wav').wait()

        # Engine Idle:
        # Let the engine sound idle for 2 seconds
        motor_idle_start_time = time()
        while time() - motor_idle_start_time <= 2:
            self.speaker.play(
                wav_file='media/Motor idle.wav').wait()

        while True:
            # Driving Mode:
            # Manual mode where the movement of the RoboDoz3r is controlled
            # by the IR remote
            while not self.touch_sensor.is_pressed:
                self.raise_or_lower_shovel_by_ir_beacon()
                self.drive_by_ir_beacon(speed=driving_speed)
                sleep(0.01)

            self.speaker.play(wav_file='media/Airbrake.wav').wait()

            # Auto Mode:
            # In autonomous mode the RoboDoz3r uses the IR sensor
            # in proximity mode to detect nearby obstacles in its path
            while not self.touch_sensor.is_pressed:
                if self.ir_sensor.proximity < 50:
                    self.left_motor.stop(stop_action=Motor.STOP_ACTION_HOLD)
                    self.right_motor.stop(stop_action=Motor.STOP_ACTION_HOLD)

                    sleep(1)

                    self.left_motor.run_timed(
                        speed_sp=-300,
                        time_sp=1000,
                        stop_action=Motor.STOP_ACTION_HOLD)
                    self.right_motor.run_timed(
                        speed_sp=-300,
                        time_sp=1000,
                        stop_action=Motor.STOP_ACTION_HOLD)
                    self.left_motor.wait_while(Motor.STATE_RUNNING)
                    self.right_motor.wait_while(Motor.STATE_RUNNING)

                    self.left_motor.run_timed(
                        speed_sp=500,
                        time_sp=1000,
                        stop_action=Motor.STOP_ACTION_HOLD)
                    self.right_motor.run_timed(
                        speed_sp=-500,
                        time_sp=1000,
                        stop_action=Motor.STOP_ACTION_HOLD)
                    self.left_motor.wait_while(Motor.STATE_RUNNING)
                    self.right_motor.wait_while(Motor.STATE_RUNNING)

                else:
                    self.left_motor.run_forever(speed_sp=500)
                    self.right_motor.run_forever(speed_sp=500)

                sleep(0.01)

            self.speaker.play(wav_file='media/Airbrake.wav').wait()


if __name__ == '__main__':
    ROBODOZ3R = RoboDoz3r()
    ROBODOZ3R.main()
