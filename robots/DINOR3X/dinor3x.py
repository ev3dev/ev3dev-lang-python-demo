#!/usr/bin/env python3


from ev3dev.ev3 import (
    Motor, LargeMotor, MediumMotor, OUTPUT_A, OUTPUT_B, OUTPUT_C,
    TouchSensor, ColorSensor, InfraredSensor, RemoteControl,
    INPUT_1, INPUT_3, INPUT_4,
    Sound
)


class Dinor3x:
    FAST_WALK_SPEED = 800
    NORMAL_WALK_SPEED = 400
    SLOW_WALK_SPEED = 200

    def __init__(
            self,
            jaw_motor_port: str = OUTPUT_A,
            left_motor_port: str = OUTPUT_B, right_motor_port: str = OUTPUT_C,
            touch_sensor_port: str = INPUT_1, color_sensor_port: str = INPUT_3,
            ir_sensor_port: str = INPUT_4, ir_beacon_channel: int = 1):
        self.jaw_motor = MediumMotor(address=jaw_motor_port)

        self.left_motor = LargeMotor(address=left_motor_port)
        self.right_motor = LargeMotor(address=right_motor_port)

        self.touch_sensor = TouchSensor(address=touch_sensor_port)
        self.color_sensor = ColorSensor(address=color_sensor_port)

        self.ir_sensor = InfraredSensor(address=ir_sensor_port)
        self.remote_control = RemoteControl(sensor=self.ir_sensor,
                                            channel=ir_beacon_channel)

        self.speaker = Sound()

        self.roaring = False
        self.walk_speed = self.NORMAL_WALK_SPEED

    def roar_by_ir_beacon(self):
        """
        Dinor3x roars when the Beacon button is pressed
        """
        if self.remote_control.beacon:
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
            self.speaker.speak(text='RUN!')
            self.walk_speed = self.FAST_WALK_SPEED
            self.walk(speed=self.walk_speed)

        elif self.color_sensor.color == ColorSensor.COLOR_GREEN:
            self.speaker.speak(text='Normal')
            self.walk_speed = self.NORMAL_WALK_SPEED
            self.walk(speed=self.walk_speed)

        elif self.color_sensor.color == ColorSensor.COLOR_WHITE:
            self.speaker.speak(text='slow...')
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
        if self.remote_control.red_up and self.remote_control.blue_up:
            self.walk(speed=self.walk_speed)

        # backward
        elif self.remote_control.red_down and self.remote_control.blue_down:
            self.walk(speed=-self.walk_speed)

        # turn left on the spot
        elif self.remote_control.red_up:
            self.turn(speed=self.walk_speed)

        # turn right on the spot
        elif self.remote_control.blue_up:
            self.turn(speed=-self.walk_speed)

        # stop
        elif self.remote_control.red_down:
            self.left_motor.stop(stop_action=Motor.STOP_ACTION_HOLD)
            self.right_motor.stop(stop_action=Motor.STOP_ACTION_HOLD)

        # calibrate legs
        elif self.remote_control.blue_down:
            self.calibrate_legs()

    def calibrate_legs(self):
        self.left_motor.run_forever(speed_sp=100)
        self.right_motor.run_forever(speed_sp=200)

        while self.touch_sensor.is_pressed:
            pass

        self.left_motor.stop(stop_action=Motor.STOP_ACTION_HOLD)
        self.right_motor.stop(stop_action=Motor.STOP_ACTION_HOLD)

        self.left_motor.run_forever(speed_sp=400)

        while not self.touch_sensor.is_pressed:
            pass

        self.left_motor.stop(stop_action=Motor.STOP_ACTION_HOLD)

        self.left_motor.run_to_rel_pos(
            position_sp=-0.2 * 360,
            speed_sp=500,
            stop_action=Motor.STOP_ACTION_HOLD)
        self.left_motor.wait_while(Motor.STATE_RUNNING)

        self.right_motor.run_forever(speed_sp=400)

        while not self.touch_sensor.is_pressed:
            pass

        self.right_motor.stop(stop_action=Motor.STOP_ACTION_HOLD)

        self.right_motor.run_to_rel_pos(
            position_sp=-0.2 * 360,
            speed_sp=500,
            stop_action=Motor.STOP_ACTION_HOLD)
        self.right_motor.wait_while(Motor.STATE_RUNNING)

        self.left_motor.reset()
        self.right_motor.reset()

    def walk(self, speed: float = 1000):
        self.calibrate_legs()

        self.left_motor.run_forever(speed_sp=-speed)
        self.right_motor.run_forever(speed_sp=-speed)

    def turn(self, speed: float = 1000):
        self.calibrate_legs()

        if speed >= 0:
            self.left_motor.run_to_rel_pos(
                position_sp=180,
                speed_sp=speed,
                stop_action=Motor.STOP_ACTION_HOLD)
            self.left_motor.wait_while(Motor.STATE_RUNNING)

        else:
            self.right_motor.run_to_rel_pos(
                position_sp=180,
                speed_sp=-speed,
                stop_action=Motor.STOP_ACTION_HOLD)
            self.right_motor.wait_while(Motor.STATE_RUNNING)

        self.left_motor.run_forever(speed_sp=speed)
        self.right_motor.run_forever(speed_sp=-speed)

    def close_mouth(self):
        self.jaw_motor.run_timed(
            speed_sp=-200,
            time_sp=1000,
            stop_action=Motor.STOP_ACTION_COAST)

    def open_mouth(self):
        self.jaw_motor.run_timed(
            speed_sp=200,
            time_sp=1000,
            stop_action=Motor.STOP_ACTION_COAST)

    def roar(self):
        self.speaker.play(wav_file='/home/robot/sound/T-rex roar.wav')

        self.jaw_motor.run_timed(
            speed_sp=-200,
            time_sp=0.5 * 1000,
            stop_action=Motor.STOP_ACTION_COAST)
        self.jaw_motor.wait_while(Motor.STATE_RUNNING)

        self.jaw_motor.run_timed(
            speed_sp=200,
            time_sp=0.5 * 1000,
            stop_action=Motor.STOP_ACTION_COAST)
        self.jaw_motor.wait_while(Motor.STATE_RUNNING)

    def main(self):
        self.close_mouth()

        while True:
            self.roar_by_ir_beacon()
            self.change_speed_by_color()
            self.walk_by_ir_beacon()


if __name__ == '__main__':
    DINOR3X = Dinor3x()
    DINOR3X.main()
