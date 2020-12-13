#!/usr/bin/env micropython


from ev3dev2.motor import \
    Motor, LargeMotor, MediumMotor, \
    OUTPUT_A, OUTPUT_B, OUTPUT_C
from ev3dev2.sensor import INPUT_1, INPUT_4
from ev3dev2.sensor.lego import TouchSensor
from ev3dev2.console import Console
from ev3dev2.sound import Sound

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
            motor_class=LargeMotor, polarity=Motor.POLARITY_INVERSED,
            ir_sensor_port=ir_sensor_port,
            ir_beacon_channel=tank_drive_ir_beacon_channel)

        self.shovel_motor = MediumMotor(address=shovel_motor_port)

        self.touch_sensor = TouchSensor(address=touch_sensor_port)

        self.shovel_control_ir_beacon_channel = \
            shovel_control_ir_beacon_channel

        self.console = Console()
        self.speaker = Sound()

    def raise_or_lower_shovel_once_by_ir_beacon(self):
        """
        If the channel 4 is selected on the IR remote
        then you can control raising and lowering the shovel on the RoboDoz3r
        - Raise the shovel by either Up button
        - Raise the shovel by either Down button
        """
        # raise the shovel
        if self.ir_sensor.top_left(
                    channel=self.shovel_control_ir_beacon_channel) or \
                self.ir_sensor.top_right(
                    channel=self.shovel_control_ir_beacon_channel):
            self.shovel_motor.on(
                speed=10,
                brake=False,
                block=False)

        # lower the shovel
        elif self.ir_sensor.bottom_left(
                    channel=self.shovel_control_ir_beacon_channel) or \
                self.ir_sensor.bottom_right(
                    channel=self.shovel_control_ir_beacon_channel):
            self.shovel_motor.on(
                speed=-10,
                brake=False,
                block=False)

        else:
            self.shovel_motor.off(brake=True)

    def main(self, driving_speed: float = 100):
        self.console.text_at(
            text='ROBODOZ3R',
            column=2,
            row=2,
            reset_console=False,
            inverse=False,
            alignment='L')

        self.speaker.play_file(
            wav_file='media/Motor start.wav',
            volume=56,
            play_type=Sound.PLAY_WAIT_FOR_COMPLETE)

        motor_idle_start_time = time()
        while time() - motor_idle_start_time <= 2:
            self.speaker.play_file(
                wav_file='media/Motor idle.wav',
                volume=51,
                play_type=Sound.PLAY_WAIT_FOR_COMPLETE)

        while True:
            while self.touch_sensor.is_released:
                self.raise_or_lower_shovel_once_by_ir_beacon()
                self.drive_by_ir_beacon(speed=driving_speed)
                sleep(0.01)

            self.speaker.play_file(
                wav_file='media/Airbrake.wav',
                volume=100,
                play_type=Sound.PLAY_WAIT_FOR_COMPLETE)

            while self.touch_sensor.is_released:
                if self.ir_sensor.proximity < 50:
                    self.tank_driver.off(brake=True)

                    sleep(1)

                    self.tank_driver.on_for_seconds(
                        left_speed=-30,
                        right_speed=-30,
                        seconds=1,
                        brake=True,
                        block=True)

                    self.tank_driver.on_for_seconds(
                        left_speed=50,
                        right_speed=-50,
                        seconds=1,
                        brake=True,
                        block=True)

                else:
                    self.tank_driver.on(
                        left_speed=50,
                        right_speed=50)

                sleep(0.01)

            self.speaker.play_file(
                wav_file='media/Airbrake.wav',
                volume=100,
                play_type=Sound.PLAY_WAIT_FOR_COMPLETE)


if __name__ == '__main__':
    ROBODOZ3R = RoboDoz3r()
    ROBODOZ3R.main()
