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

'''
********************NOTICE************************
##################################################
##########해당부분 종윤이 체크 부탁 ####################
##################################################
이라고 작성한 부분들은 직접 확인 후에 주석부분들을 삭제 할 것.
********************NOTICE************************
'''


############### ev3 초기화 구간 ###############
ev3 = EV3Brick()
ev3.speaker.beep()
############### ev3 초기화 구간 ###############

############### 입력디바이스 초기화 구간 ###############
motor1 = Motor(Port.A)
motor2 = Motor(Port.B)
motor3 = Motor(Port.C)

sensor_left = ColorSensor(Port.S1)
sensor_right = ColorSensor(Port.S2)
######## 포트에 꽂힌 만큼만 선언하기. 안그러면 에러남.
############### 입력디바이스 초기화 구간 ###############

############### 번수 선언 ###############
condition1,condition2 = 0 #조건 1과 조건 2가 둘다 1이 되면 둘다 공이 들어와있는 것으로 판단.
que1_counter,que2_counter = 0 # 추후에 공을 들어가게 하기 위해 써둔 변수. 지금은 신경 안써도 됨. 

##################################################
##########해당부분 종윤이 체크 부탁 ####################
##################################################
speed1 = 400 # 타워 1 모터 속도 값을 조절 해서 10초, 20초, 30초만에 나오게 하려면 스피드를 얼만큼을 줘야하는지 확인 요청. 모터 거꾸로 돌릴땐 - 붙이기
speed2 = 400
##################################################
##########해당부분 종윤이 체크 부탁 ####################
##################################################


POSSIBLE_COLORS = [Color.RED,Color.BLUE]
counter =list(range(60)) 
############### 번수 선언 ###############


#초기 좌우모터 
motor1.run(speed)
motor2.run(speed)


while True:
    
    if sensor_left.color() in POSSIBLE_COLORS:
        ev3.speaker.beep(2000, 200)
        condition1 = 1
        #타임스탬프 찍기

    if sensor_right.color() in POSSIBLE_COLORS:
        ev3.speaker.beep(2000, 200)
        condition2 = 1
        # 타임스탬프 찍기

    if condition1 ==1 and condition2 ==1:
        condition1 = 0
        condition2 = 0
        ev3.speaker.beep(2000, 100)
        print('머지모터 작동')
        #타임스탬프 찍기.

        ##################################################
        ##########해당부분 종윤이 체크 부탁 ####################
        ##################################################
        motor3.run_time(-400, 6000, then=Stop.HOLD, wait=True) # 모터 속도와 시간초를 조절해서 레일이 움직여서 공이 떨어지는지 값을 확인 후 설정 부탁.
        ##################################################
        ##########해당부분 종윤이 체크 부탁 ####################
        ##################################################


