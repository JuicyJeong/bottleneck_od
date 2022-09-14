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


############### ev3 초기화 구간 ###############
ev3 = EV3Brick()
ev3.speaker.beep()
############### ev3 초기화 구간 ###############

############### 입력디바이스 초기화 구간 ###############
motor1 = Motor(Port.A)
motor2 = Motor(Port.B)
motor3 = Motor(Port.C)

sensor_1 = ColorSensor(Port.S1)
sensor_2 = ColorSensor(Port.S2)
sensor_3 = ColorSensor(Port.S3)
############### 입력디바이스 초기화 구간 ###############

############### 번수 선언 ###############
condition1,condition2 = 0
que1_counter,que2_counter = 0
POSSIBLE_COLORS = [Color.RED,Color.BLUE]
counter =list(range(60)) 
que1_counter,que2_counter = 0
stop = True
############### 번수 선언 ###############



while True:

    if #컬러센서:1큐가 인식되었을때 and condition ==0:#1공정에 센서가 있어야할듯...
        #1공정 큐모터 움직이기
        #타임스탬프 찍기.
        condition1 +=1

    if sensor_2.color in POSSIBLE_COLORS: #1공정에서 나갔음 = 2공정에 큐가 들어옴.
        #타임스탬프를 찍기.
        #1공정 큐의 타임 스탬프 찍기.
        condition-=1
        que2_counter += 1
    
    if que2_counter == 0 and que 

     if sensor_3.color in POSSIBLE_COLORS: #2공정에서 나갔음 = 3공정에 큐가 들어옴.
        #타임스탬프를 찍기.
        #1공정 큐의 타임 스탬프 찍기.
        que1_counter -= 1
        que2_counter += 1