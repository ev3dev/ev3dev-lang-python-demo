#!/usr/bin/env micropython


from ev3dev2.motor import (
    LargeMotor, MediumMotor, MoveTank, MoveSteering,
    OUTPUT_A, OUTPUT_B, OUTPUT_C
)
from ev3dev2.sensor import INPUT_1, INPUT_3, INPUT_4
from ev3dev2.sensor.lego import TouchSensor, ColorSensor, InfraredSensor
from ev3dev2.sound import Sound


class Dinor3x:
    FAST_WALK_SPEED = 80
    NORMAL_WALK_SPEED = 40
    SLOW_WALK_SPEED = 20

    def __init__(
            self,
            jaw_motor_port: str = OUTPUT_A,
            left_motor_port: str = OUTPUT_B, right_motor_port: str = OUTPUT_C,
            touch_sensor_port: str = INPUT_1, color_sensor_port: str = INPUT_3,
            ir_sensor_port: str = INPUT_4, ir_beacon_channel: int = 1):
        self.jaw_motor = MediumMotor(address=jaw_motor_port)

        self.left_motor = LargeMotor(address=left_motor_port)
        self.right_motor = LargeMotor(address=right_motor_port)
        self.tank_driver = MoveTank(left_motor_port=left_motor_port,
                                    right_motor_port=right_motor_port,
                                    motor_class=LargeMotor)
        self.steer_driver = MoveSteering(left_motor_port=left_motor_port,
                                         right_motor_port=right_motor_port,
                                         motor_class=LargeMotor)

        self.touch_sensor = TouchSensor(address=touch_sensor_port)
        self.color_sensor = ColorSensor(address=color_sensor_port)

        self.ir_sensor = InfraredSensor(address=ir_sensor_port)
        self.ir_beacon_channel = ir_beacon_channel

        self.speaker = Sound()

        self.roaring = False
        self.walk_speed = self.NORMAL_WALK_SPEED

    def roar_by_ir_beacon(self):
        """
        Dinor3x roars when the Beacon button is pressed
        """
        if self.ir_sensor.beacon(channel=self.ir_beacon_channel):
            self.roaring = True
            self.open_mouth()
            self.roar()

        elif self.roaring:
            self.roaring = False
            self.close_mouth()

    def change_speed_by_color(self):
        """
        Dinor3x changes its speed when detecting some colors
        - Red: walk fast
        - Green: walk normally
        - White: walk slowly
        """
        if self.color_sensor.color == ColorSensor.COLOR_RED:
            self.speaker.speak(
                text='RUN!',
                volume=100,
                play_type=Sound.PLAY_NO_WAIT_FOR_COMPLETE)
            self.walk_speed = self.FAST_WALK_SPEED
            self.walk(speed=self.walk_speed)

        elif self.color_sensor.color == ColorSensor.COLOR_GREEN:
            self.speaker.speak(
                text='Normal',
                volume=100,
                play_type=Sound.PLAY_NO_WAIT_FOR_COMPLETE)
            self.walk_speed = self.NORMAL_WALK_SPEED
            self.walk(speed=self.walk_speed)

        elif self.color_sensor.color == ColorSensor.COLOR_WHITE:
            self.speaker.speak(
                text='slow...',
                volume=100,
                play_type=Sound.PLAY_NO_WAIT_FOR_COMPLETE)
            self.walk_speed = self.SLOW_WALK_SPEED
            self.walk(speed=self.walk_speed)

    def walk_by_ir_beacon(self):
        """
        Dinor3x walks or turns according to instructions from the IR Beacon
        - 2 top/up buttons together: walk forward
        - 2 bottom/down buttons together: walk backward
        - Top Left / Red Up: turn left on the spot
        - Top Right / Blue Up: turn right on the spot
        - Bottom Left / Red Down: stop
        - Bottom Right / Blue Down: calibrate to make the legs straight
        """

        # forward
        if self.ir_sensor.top_left(channel=self.ir_beacon_channel) and \
                self.ir_sensor.top_right:
            self.walk(speed=self.walk_speed)

        # backward
        elif self.ir_sensor.bottom_left(channel=self.ir_beacon_channel) and \
                self.ir_sensor.bottom_right(channel=self.ir_beacon_channel):
            self.walk(speed=-self.walk_speed)

        # turn left on the spot
        elif self.ir_sensor.top_left(channel=self.ir_beacon_channel):
            self.turn(speed=self.walk_speed)

        # turn right on the spot
        elif self.ir_sensor.top_right(channel=self.ir_beacon_channel):
            self.turn(speed=-self.walk_speed)

        # stop
        elif self.ir_sensor.bottom_left(channel=self.ir_beacon_channel):
            self.tank_driver.off(brake=True)

        # calibrate legs
        elif self.ir_sensor.bottom_right(channel=self.ir_beacon_channel):
            self.calibrate_legs()

    def calibrate_legs(self):
        self.tank_driver.on(
            left_speed=10,
            right_speed=20)

        self.touch_sensor.wait_for_released()

        self.tank_driver.off(brake=True)

        self.left_motor.on(speed=40)

        self.touch_sensor.wait_for_pressed()

        self.left_motor.off(brake=True)

        self.left_motor.on_for_rotations(
            rotations=-0.2,
            speed=50,
            brake=True,
            block=True)

        self.right_motor.on(speed=40)

        self.touch_sensor.wait_for_pressed()

        self.right_motor.off(brake=True)

        self.right_motor.on_for_rotations(
            rotations=-0.2,
            speed=50,
            brake=True,
            block=True)

        self.left_motor.reset()
        self.right_motor.reset()

    def walk(self, speed: float = 100):
        self.calibrate_legs()

        self.steer_driver.on(
            steering=0,
            speed=-speed)

    def turn(self, speed: float = 100):
        self.calibrate_legs()

        if speed >= 0:
            self.left_motor.on_for_degrees(
                degrees=180,
                speed=speed,
                brake=True,
                block=True)

        else:
            self.right_motor.on_for_degrees(
                degrees=180,
                speed=-speed,
                brake=True,
                block=True)

        self.tank_driver.on(
            left_speed=speed,
            right_speed=-speed)

    def close_mouth(self):
        self.jaw_motor.on_for_seconds(
            speed=-20,
            seconds=1,
            brake=False,
            block=False)

    def open_mouth(self):
        self.jaw_motor.on_for_seconds(
            speed=20,
            seconds=1,
            block=False,
            brake=False)

    def roar(self):
        self.speaker.play_file(
            wav_file='T-rex roar.wav',
            volume=100,
            play_type=Sound.PLAY_NO_WAIT_FOR_COMPLETE)

        self.jaw_motor.on_for_degrees(
            speed=40,
            degrees=-60,
            block=True,
            brake=True)

        for i in range(12):
            self.jaw_motor.on_for_seconds(
                speed=-40,
                seconds=0.05,
                block=True,
                brake=True)

            self.jaw_motor.on_for_seconds(
                speed=40,
                seconds=0.05,
                block=True,
                brake=True)

        self.jaw_motor.on_for_seconds(
            speed=20,
            seconds=0.5,
            brake=False,
            block=True)

    def main(self):
        self.close_mouth()

        while True:
            self.roar_by_ir_beacon()
            self.change_speed_by_color()
            self.walk_by_ir_beacon()


if __name__ == '__main__':
    DINOR3X = Dinor3x()
    DINOR3X.main()
