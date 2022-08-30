import sys



'''
pt 0 
데이터 불러오기, 데이터 타입 초기화
'''
#텍스트파일 경로 항상 확인.
# f = open("C:/Users/jinwoo Jeong/Desktop/ML/yolov4-deepsort-master/output.txt", 'r')
f = open("output.txt", 'r')


#프레임 넘버 카운터. 1부터 시작
frame_count_num = 1

#최종 결과물(리스트) 초기화
final_list = []
#공정 1, 공정 2에 몇개의 오브젝트가 있는지 확인. 임시로 공정 1만 정의. 그 외에는 공정 2로 처리.
factory_status = [0,0,0,0]
'''
[그 이외에 잡히는 곳, 
1공정 que에 잡히는 오브젝트 갯수,
2공정 que에 잡히는 오브젝트 갯수,
3공정 que에 잡히는 오브젝트 갯수]
'''

que1_max = 10
que2_max = 10
que3_max = 10

#공정 좌표를 미리 정의. 좌표는 직접 확인하는게 좋으며 이때는 일단 작동하는지 확인을 위해 임시로 해보겠음.
f1_xmin = 0
f1_ymin = 0
f1_xmax = 1920
f1_ymax = 1080

f2_xmin = 0
f2_ymin = 0
f2_xmax = 1920
f2_ymax = 1080

f3_xmin = 0
f3_ymin = 0
f3_xmax = 1920
f3_ymax = 1080

#공정 좌표를 미리 정의. 좌표는 직접 확인하는게 좋으며 이때는 일단 작동하는지 확인을 위해 임시로 해보겠음.


f1_que_max = 10
f2_que_max = 12
f3_que_max = 15

'''
pt 0 
데이터 불러오기, 데이터 타입 초기화
'''


'''
pt1 텍스트 파일에서 프레임별로 오브젝트 위치를 불러옴.
그 후 오브젝트가 몇 공정에 있는지 리스트에 각각 집어넣음
리스트 = [1공정 갯수, 2공정 갯수, 3공정 갯수, 아무것도 아닌곳에 있는 갯수] 형태로 출력
'''

while True:
    line = f.readline()
    if not line: break
    # print(line)


## 프레임 번호를 ID 키값으로
    #프레임 번호가 라인에 있을 때: 프레임 번호를 출력
    if 'Frame' in line:
        frame_dict = 'Frame_{}'.format(frame_count_num)
        frame_count_num += 1
        # print(frame_dict)
        globals()[frame_dict] = {} #동적 변수 선언

    # #트래킹 아이디가 있을 때, 트래킹 좌표만 출력.
    elif 'Tracker ID' in line:
        str_spl_comma = line.split(',')
        str_spl = line.split('(')

        tracker_ID = str_spl_comma[0][12:] #아이디 값(숫자만 출력)
        #트래킹 좌표값 정수로 변환
        tracker_val = str_spl[2][:-2]
        pos = tracker_val.split(',')
        # print(pos)
        xmin =int(pos[0])
        ymin =int(pos[1])
        xmax =int(pos[2])
        ymax =int(pos[3])


        ###### 공정 bbox 위치 선언 구간####
            #공정1 위치에 오브젝츠가 잡힐때
        if f1_xmin < xmin and f1_ymin < ymin and f1_xmax > xmax and f1_ymax > ymax :
            factory_status[1] += 1

            # 공정2 위치에 오브젝트가 잡힐때:
        #elif f2_xmin < xmin and f2_ymin < ymin and f2_xmax > xmax and f2_ymax > ymax :
            #factory_status[2] += 1

            # 공정3 위치에 오브젝트가 잡힐때:
        # elif f3_xmin < xmin and f3_ymin < ymin and f2_xmax > xmax and f2_ymax > ymax :
            # factory_status[3] += 1


        else: #fps 나오고 해당 프레임의 마지막 라인인것을 아니 여기서 선언하고 한번에 입력하면 될듯?
            factory_status[0] += 1
        ###### 공정 bbox 위치 선언 구간####



    elif 'FPS' in line: #FPS 라인 읽을때. 해당 프레임의 끝 임을 이용하여 리스트 초기화
        final_list.append(factory_status)   #여기를 제일 아래단으로?
        factory_status = [0, 0, 0, 0] #다시 초기화...
        # print(tracker_ID)
        # print(xmin,ymin,xmax,ymax)

f.close()

print(final_list)

'''
pt1 
윗 부분까지 프레임 별로 어느 공정에 있는지 딕셔너리로 추가 완료. 이제 몇초동안 어디에 있었는지, 
1초당 프레임이 몇이었는지, 것들을 계산해서 입력해야함.
'''

frame_per_second = 30 #fps 값 임시로 설정.
video_sec = len(final_list)//frame_per_second
total_frame = video_sec*frame_per_second # 끝에 1초미만의 영상의 프레임을 떨구는 것으로 결정.

print('영상길이:{}초'.format(video_sec))
print('Frame Per Second: {}'.format(frame_per_second))
print('총 프레임 수: {}'.format(total_frame))


# 프레임별로 탐지된 오브젝트 수를 초 단위로 변환하여 초당 탐지된 오브젝트 수들을 출력(반올림)
for sec_num in range(1,video_sec+1):
    #공정 갯수만큼 초기화시키기
    sum_fac0 = 0
    sum_fac1 = 0
    sum_fac2 = 0
    sum_fac3 = 0
    for frame_num in range(1,frame_per_second+1): #0부터 시작하는 것 때문에... +1, -1 잘 확인하여 입력하기.

        sum_fac0 += final_list[(sec_num - 1) * frame_per_second + frame_num - 1][0]
        sum_fac1 += final_list[(sec_num-1)*frame_per_second+ frame_num-1][1]
        sum_fac2 += final_list[(sec_num-1)*frame_per_second+ frame_num-1][2]
        sum_fac3 += final_list[(sec_num-1)*frame_per_second+ frame_num-1][3]


    print('{}초에 탐지된 오브젝트 수'.format(sec_num))
    sum_fac1 = round(sum_fac1/frame_per_second) #FPS 값 만큼 나누고 반올림
    sum_fac2 = round(sum_fac2/frame_per_second)
    sum_fac3 = round(sum_fac3/frame_per_second)
    sum_fac0 = round(sum_fac0/frame_per_second)

    print('1공정:{},'
          '\n2공정:{},'
          '\n3공정:{},'
          '\n그 외:{}'
          .format(sum_fac1,sum_fac2,sum_fac3, sum_fac0))



    sum_fac0 = 0
    sum_fac1 = 0
    sum_fac2 = 0
    sum_fac3 = 0
'''
pt2 초당 어느 공정에 몇개의 오브젝트가 있는지 출력. 이걸... gui로 나타낼 수 있나? 아니면 어떤 방식으로...?
'''
import GUI