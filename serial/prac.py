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

POSSIBLE_COLORS = [Color.RED,Color.BLUE]

# This program requires LEGO EV3 MicroPython v2.0 or higher.
# Click "Open user guide" on the EV3 extension tab for more information.
# POSSIBLE_COLORS = [Color.RED, Color.GREEN, Color.BLUE, Color.YELLOW]
# POSSIBLE_COLORS = [Color.RED,Color.BLUE]



# Create your objects here.
ev3 = EV3Brick()
# Write your program here. #시동음으로 하자.
ev3.speaker.beep()

# stop = True
# color_sensor1 = ColorSensor(Port.S1)
# color_sensor_right = ColorSensor(Port.S2)
motor = Motor(Port.A)
# while True:
motor.run_until_stalled(360, Stop.BRAKE,100)

    # motor.run(1000)
    # if color_sensor.color() in POSSIBLE_COLORS:
    #     print("감지된 색깔:{}".format(color_sensor.color))
    # else:
    #     pass



# This program requires LEGO EV3 MicroPython v2.0 or higher.
# Click "Open user guide" on the EV3 extension tab for more information.
# POSSIBLE_COLORS = [Color.RED, Color.GREEN, Color.BLUE, Color.YELLOW]
POSSIBLE_COLORS = [Color.RED,Color.BLUE]



# Create your objects here.
ev3 = EV3Brick()
# Write your program here. #시동음으로 하자.
ev3.speaker.beep()

'''
stop: 불린 값. 해당 값이 False로 변할 경우, while문이 종료된다.
color_sensor_left(right): 컬러센서(왼쪽,오른쪽). 포트넘버는 앞에 S를 붙이고 숫자를 입력할것. 
'''
# stop = True
# color_sensor_left = ColorSensor(Port.S1)
# color_sensor_right = ColorSensor(Port.S2)
# motor1_speed = 0
# motor2_speed = 0
# motor = Motor(Port.A)

# print('dummy')
# print(time.strftime('%Y-%m-%d', time.localtime(time.time())))
# print(time.strftime('%H시 %M분 %S초', time.localtime(time.time())))

# fac1_count = 0 
# fac2_count = 0
# fac2_cue = 0
# fac3_count = 0
# fac_3cue = 0

#공정1의 모터속도  = 익스포넨셜 몇
#공정2의 모터속도  = 익스포넨셜 몇
#공정3의 모터속도  = 익스포넨셜 몇


#시작시간을 찍기
# while stop:


    #if 1차 공정의 큐에 공이 있음 and fac1_count==0:
        #공정1의 큐 모터를 돌려서 공정 1안으로 집어넣기
        #fac1_count += 1 

    # if 1차공정에서 공 나온것이 탐지되었을때: 
        #1차 공정에서 나왔을때의 타임스탬프를 찍기>> 1차공정이 1회 끝난 시간, 뒷 시간이랑 비교하면 공정시간을 알 수 있음.
        # fac1_count -=1

        #wait() >> 레일에서 2차 공정 큐의 이동시간이 몇초인지 확인하고 입력하기
        # fac2_cue +=1


    # 2차 공정에 공이 들어갑니다.
    #if fac2_count == 0 and fac2_cue >=1:
        #2차공정 큐모터 움직임
        #fac2_count +=1
        #fac2_cue -=1
    
    #if 2차공정에서 공 나온것이 탐지되었을때: 
        #2차 공정에서 나왔을때의 타임스탬프를 찍기>> 2차공정이 1회 끝난 시간, 뒷 시간이랑 비교하면 공정시간을 알 수 있음.
        # fac2_count -=1

        #wait() >> 레일에서 3차 공정 큐의 이동시간이 몇초인지 확인하고 입력하기
        # fac3_cue +=1

    #3차 공정에 큐가 들어갑니다.
    #if fac3_count == 0 and fac3_cue >=1:
        #3차공정 큐모터 움직임
        #fac2_count +=1
        #fac2_cue -=1

    #if 3차공정에서 공 나온것이 탐지되었을때: 
        #2차 공정에서 나왔을때의 타임스탬프를 찍기>> 2차공정이 1회 끝난 시간, 뒷 시간이랑 비교하면 공정시간을 알 수 있음.
        # fac3_count -=1

     


        

# 컬러센서 10번 탐지하게 하는 메서드. 
# color_sensor = ColorSensor(Port.S1)

# count = 0
# print('센서 ')
# while count < 10:
#     if color_sensor.color() in POSSIBLE_COLORS:
#         count+=1
#         ev3.speaker.beep(2000, 100)
#         print("감지된 색깔:{}".format(color_sensor.color))
#         print('{}번 감지 되었습니다.3초 후 다시 측정합니다.'.format(count))
#         wait(3000)
#     else:
#         print('감지 안됨')
        

    # ev3.speaker.beep(2000, 100)

speed = 500
# Write your program here.
motor1 = Motor(Port.A)
motor2 = Motor(Port.B)
motor1.run(600)
motor2.run(600)

while True:
    print('test')
    wait(2000)
# motor.run_until_stalled(360, Stop.BRAKE,100)
# motor.run_time(speed, 6000, then=Stop.HOLD, wait=True)
# print('speed:{}'.format(speed))


motor1.run(speed)
# motor2.run(speed)
count = 0

while True:
    print(count)
    if count == 10:
        speed = 800
        motor1.run(speed)
    count +=1
    print(motor1.speed())
    wait(2000)