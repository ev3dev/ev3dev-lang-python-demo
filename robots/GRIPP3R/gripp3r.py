#!/usr/bin/env python3


from ev3dev.ev3 import (
    Motor, LargeMotor, MediumMotor, OUTPUT_A, OUTPUT_B, OUTPUT_C,
    TouchSensor, InfraredSensor, RemoteControl, INPUT_1, INPUT_4,
    Sound
)
from ev3dev.helper import RemoteControlledTank

from multiprocessing import Process


class Gripp3r(RemoteControlledTank):
    def __init__(
            self,
            grip_motor_port: str = OUTPUT_A,
            left_motor_port: str = OUTPUT_B, right_motor_port: str = OUTPUT_C,
            touch_sensor_port: str = INPUT_1,
            ir_sensor_port: str = INPUT_4, ir_beacon_channel: int = 1):
        super().__init__(
            left_motor=left_motor_port, right_motor=right_motor_port,
            polarity='normal')

        self.grip_motor = MediumMotor(address=grip_motor_port)

        self.touch_sensor = TouchSensor(address=touch_sensor_port)

        self.speaker = Sound()


    def grip_or_release_by_ir_beacon(self):
        while True:
            if self.remote.beacon:
                if self.touch_sensor.is_pressed:
                    self.speaker.play(wav_file='Air release.wav')

                    self.grip_motor.run_timed(
                        speed_sp=500,
                        time_sp=1000,
                        stop_action=Motor.STOP_ACTION_BRAKE)
                    self.grip_motor.wait_while(Motor.STATE_RUNNING)

                else:
                    self.speaker.play(wav_file='Airbrake.wav')

                    self.grip_motor.run_forever(speed_sp=-500)

                    while not self.touch_sensor.is_pressed:
                        pass
            
                    self.grip_motor.stop(stop_action=Motor.STOP_ACTION_BRAKE)

                while self.remote.beacon:
                    pass

        
    def main(self):
        self.grip_motor.run_timed(
            speed_sp=-500,
            time_sp=1000,
            stop_action=Motor.STOP_ACTION_BRAKE)
        self.grip_motor.wait_while(Motor.STATE_RUNNING)

        Process(target=self.grip_or_release_by_ir_beacon,
                daemon=True).start()

        super().main()
            

if __name__ == '__main__':
    GRIPP3R = Gripp3r()
    GRIPP3R.main()
