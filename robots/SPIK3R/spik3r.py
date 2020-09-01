#!/usr/bin/env micropython


from ev3dev2.motor import LargeMotor, MediumMotor, OUTPUT_A, OUTPUT_B, OUTPUT_D
from ev3dev2.sensor import INPUT_1, INPUT_4
from ev3dev2.sensor.lego import TouchSensor, InfraredSensor
from ev3dev2.sound import Sound


class Spik3r:
    def __init__(
            self,
            claw_motor_port: str = OUTPUT_A,
            move_motor_port: str = OUTPUT_B,
            sting_motor_port: str = OUTPUT_D,
            touch_sensor_port: str = INPUT_1,
            ir_sensor_port: str = INPUT_4, ir_beacon_channel: int = 1):
        self.claw_motor = MediumMotor(address=claw_motor_port)
        self.move_motor = LargeMotor(address=move_motor_port)
        self.sting_motor = LargeMotor(address=sting_motor_port)

        self.ir_sensor = InfraredSensor(address=ir_sensor_port)
        self.ir_beacon_channel = ir_beacon_channel

        self.touch_sensor = TouchSensor(address=touch_sensor_port)

        self.speaker = Sound()

    def snap_claw_if_touched(self):
        if self.touch_sensor.is_pressed:
            self.claw_motor.on_for_seconds(
                speed=50,
                seconds=1,
                brake=True,
                block=True)

            self.claw_motor.on_for_seconds(
                speed=-50,
                seconds=0.3,
                brake=True,
                block=True)

    def move_by_ir_beacon(self):
        if self.ir_sensor.top_left(channel=self.ir_beacon_channel) and \
                self.ir_sensor.top_right(channel=self.ir_beacon_channel):
            self.move_motor.on(
                speed=100,
                block=False,
                brake=False)

        elif self.ir_sensor.top_right(channel=self.ir_beacon_channel):
            self.move_motor.on(
                speed=-100,
                brake=False,
                block=False)

        else:
            self.move_motor.off(brake=False)

    def sting_by_ir_beacon(self):
        if self.ir_sensor.beacon(channel=self.ir_beacon_channel):
            self.sting_motor.on_for_degrees(
                speed=-75,
                degrees=220,
                brake=True,
                block=False)

            self.speaker.play_file(
                wav_file='Blip 3.wav',
                volume=100,
                play_type=Sound.PLAY_WAIT_FOR_COMPLETE)

            self.sting_motor.on_for_seconds(
                speed=-100,
                seconds=1,
                brake=True,
                block=True)

            self.sting_motor.on_for_seconds(
                speed=40,
                seconds=1,
                brake=True,
                block=True)

            while self.ir_sensor.beacon(channel=self.ir_beacon_channel):
                pass

    def main(self):
        while True:
            self.snap_claw_if_touched()
            self.move_by_ir_beacon()
            self.sting_by_ir_beacon()


if __name__ == '__main__':
    SPIK3R = Spik3r()
    SPIK3R.main()
