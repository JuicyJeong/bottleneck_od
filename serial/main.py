#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile
import os 
import time
import machine


############### ev3 초기화 구간 ###############
ev3 = EV3Brick()
ev3.speaker.beep()
############### ev3 초기화 구간 ###############

############### 입력디바이스 초기화 구간 ###############
# motor1 = Motor(Port.A)
# motor2 = Motor(Port.B)
# sensor_1 = ColorSensor(Port.S1)
# sensor_2 = ColorSensor(Port.S2)
############### 입력디바이스 초기화 구간 ###############
rtc = machine.RTC()
rtc.datetime((2020, 1, 21, 2, 10, 32, 36, 0))

POSSIBLE_COLORS = [Color.RED,Color.BLUE]
# motor1.run(200)
# motor2.run(-200)

while True:
    # print(time.strftime('%Y-%m-%d', time.localtime(time.time())))
    print(rtc.datetime())
    # print(time.strftime('%H시 %M분 %S초', time.localtime(time.time())))
    wait(1000)
    # if sensor_1.color() in POSSIBLE_COLORS:
    #     ev3.speaker.beep()
    #     print('공 감지. 모터가 가동됩니다.')
    #     motor1.run_angle(-200, 70, then=Stop.HOLD, wait=True)
    #     wait(1000)
    #     motor1.run_angle(200, 70,then=Stop.HOLD, wait=True)