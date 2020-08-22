#!/usr/bin/env python3


from ev3dev.ev3 import ( 
    Motor, LargeMotor, MediumMotor, OUTPUT_A, OUTPUT_B, OUTPUT_D,
    TouchSensor, InfraredSensor, RemoteControl, INPUT_1, INPUT_4,
    Sound
)


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

        self.remote_control = RemoteControl(sensor=InfraredSensor(address=ir_sensor_port),
                                            channel=ir_beacon_channel)

        self.touch_sensor = TouchSensor(address=touch_sensor_port)

        self.speaker = Sound()


    def snap_claw_if_touched(self):
        if self.touch_sensor.is_pressed:
            self.claw_motor.run_timed(
                speed_sp=500,
                time_sp=1000,
                stop_action=Motor.STOP_ACTION_HOLD)
            self.claw_motor.wait_while(Motor.STATE_RUNNING)

            self.claw_motor.run_timed(
                speed_sp=-500,
                time_sp=300,
                stop_action=Motor.STOP_ACTION_HOLD)
            self.claw_motor.wait_while(Motor.STATE_RUNNING)

                    
    def move_by_ir_beacon(self):
        if self.remote_control.red_up and self.remote_control.blue_up:
            self.move_motor.run_forever(speed_sp=1000)

        elif self.remote_control.blue_up:
            self.move_motor.run_forever(speed_sp=-1000)

        else:
            self.move_motor.stop(stop_action=Motor.STOP_ACTION_COAST)

    
    def sting_by_ir_beacon(self):
        if self.remote_control.beacon:
            self.sting_motor.run_to_rel_pos(
                speed_sp=750,
                position=-220,
                stop_action=Motor.STOP_ACTION_HOLD)
            self.sting_motor.wait_while(Motor.STATE_RUNNING)

            self.speaker.play(wav_file='/home/robot/sound/Blip 3.wav').wait()

            self.sting_motor.run_timed(
                speed_sp=-1000,
                time_sp=1000,
                stop_action=Motor.STOP_ACTION_HOLD)
            self.sting_motor.wait_while(Motor.STATE_RUNNING)

            self.sting_motor.run_timed(
                speed_sp=1000,
                time_sp=1000,
                stop_action=Motor.STOP_ACTION_HOLD)
            self.sting_motor.wait_while(Motor.STATE_RUNNING)

            while self.remote_control.beacon:
                pass


    def main(self):
        while True:
            self.snap_claw_if_touched()
            self.move_by_ir_beacon()
            self.sting_by_ir_beacon()


if __name__ == '__main__':
    SPIK3R = Spik3r()

    SPIK3R.main()
