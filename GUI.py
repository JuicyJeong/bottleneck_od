import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
import datetime
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

#UI파일 연결
#단, UI파일은 Python 코드 파일과 같은 디렉토리에 위치해야한다.
form_class = uic.loadUiType("untitled.ui")[0]

#화면을 띄우는데 사용되는 Class 선언
class WindowClass(QMainWindow, form_class) :
    '''
    pt 0
    데이터 불러오기, 데이터 타입 초기화
    '''

    # 프레임 넘버 카운터. 1부터 시작
    frame_count_num = 1

    # 최종 결과물(리스트) 초기화
    final_list = []
    # 공정 1, 공정 2에 몇개의 오브젝트가 있는지 확인. 임시로 공정 1만 정의. 그 외에는 공정 2로 처리.
    factory_status = [0, 0, 0, 0]
    '''
    [그 이외에 잡히는 곳, 
    1공정 que에 잡히는 오브젝트 갯수,
    2공정 que에 잡히는 오브젝트 갯수,
    3공정 que에 잡히는 오브젝트 갯수]
    '''

    count_by_sec = []


    # 공정 좌표를 미리 정의. 좌표는 직접 확인하는게 좋으며 이때는 일단 작동하는지 확인을 위해 임시로 해보겠음.
    f1_xmin = 430
    f1_ymin = 320
    f1_xmax = 1310
    f1_ymax = 530

    #n번위치~ 1번위치 순으로 입력.(역으로 입력하기)
    f1_count_pos = [[856,563,973,733],[938,568,1056,739],[1025,573,1142,743],[1107,583,1222,754],[1190,588,1306,761][1277,595,1393,763],[1352,601,1470,771]]


    f2_xmin = 1310
    f2_ymin = 1039
    f2_xmax = 2295
    f2_ymax = 1635
    f2_count_pos = {}

    f3_xmin = 0
    f3_ymin = 0
    f3_xmax = 1920
    f3_ymax = 1080
    f3_count_pos = {}

    # 공정 좌표를 미리 정의. 좌표는 직접 확인하는게 좋으며 이때는 일단 작동하는지 확인을 위해 임시로 해보겠음.

    f1_que_max = 7
    f2_que_max = 5
    f3_que_max = 4

    #불러올 텍스트 파일 변수 선언
    txtfile = None

    # 영상이 몇초인지 출력하는 변수
    video_sec = 0

    #이용률 시스템 메세지 선언
    lambda_sys_message = "[00:00:00]: 시스템을 시작합니다.\n"

    #용적률 시스템 메세지 선언
    od_sys_message = "[00:00:00]: 시스템을 시작합니다.\n"

    #타이머 시간 입력하여 유틸, 용적률 출력하게 할때 쓰는 시간 변수
    time_text = '000000'

    fig = plt.Figure()
    canvas = FigureCanvas(fig)

    def __init__(self) :
        super().__init__()
        self.setupUi(self)
        self.timer_input.returnPressed.connect(self.onchange_time_input)
        self.file_pushButton.clicked.connect(self.onchange_file)

        self.file_pushButton_1min.clicked.connect(self.onclick_1min)
        self.file_pushButton_2min.clicked.connect(self.onclick_2min)
        self.file_pushButton_5min.clicked.connect(self.onclick_5min)
        self.file_pushButton_10min.clicked.connect(self.onclick_10min)
        self.time_text = self.timer_input.text()
        self.verticalLayout_right.addWidget(self.canvas)

    # 위치 포지션에 따라 몇번째 위치에 있는지 확인하는 함수
    def object_detection(self,xmin,ymin,xmax,ymax):
        count = 0
        obj_num = self.f1_que_max
        #1공정에 있는게 확인 되었을때
        if self.f1_xmin < xmin and self.f1_ymin < ymin and self.f1_xmax > xmax and self.f1_ymax > ymax:
            while self.f1_count_pos[count][0] < xmin and self.f1_count_pos[count][1] < ymin and self.f1_count_pos[count][2] > xmax and self.f1_count_pos[count][3] > ymax:
                count +=1
                obj_num -=1
                if obj_num ==0:
                    break
        else:
            pass
        return (obj_num)





        pass
    def onchange_file(self):
        '''
        파일 호출 후, 프레임당 잡히는 오브젝트들을 초로 변환하여 1초당 몇개의 오브젝트가 탐지되는지
        출력. 출력형태는
        list = [[아무것도 아닌곳,1공정 탐지수,2공정 탐지수,3공정 탐지수,],...]
        으로 나온다. 여기서 리스트의 인덱스는 영상의 초와 대응한다.
        (ex: 리스트의 7번 인덱스는 영상의 7초에서 탐지되는 오브젝트 수.)
        '''
        fname = QFileDialog.getOpenFileName(self)
        print(fname[0])
        print(fname[1])
        self.txtfile = open(fname[0],'r')

        while True:
            line = self.txtfile.readline()
            if not line: break
            # print(line)
            ## 프레임 번호를 ID 키값으로
            # 프레임 번호가 라인에 있을 때: 프레임 번호를 출력
            if 'Frame' in line:
                frame_dict = 'Frame_{}'.format(self.frame_count_num)
                self.frame_count_num += 1
                # print(frame_dict)
                globals()[frame_dict] = {}  # 동적 변수 선언

            # #트래킹 아이디가 있을 때, 트래킹 좌표만 출력.
            elif 'Tracker ID' in line:
                str_spl_comma = line.split(',')
                str_spl = line.split('(')

                tracker_ID = str_spl_comma[0][12:]  # 아이디 값(숫자만 출력)
                # 트래킹 좌표값 정수로 변환
                tracker_val = str_spl[2][:-2]
                pos = tracker_val.split(',')
                # print(pos)
                xmin = int(pos[0])
                ymin = int(pos[1])
                xmax = int(pos[2])
                ymax = int(pos[3])

                ###### 공정 bbox 위치 선언 구간####
                # 공정1 위치에 오브젝츠가 잡힐때
                if self.f1_xmin < xmin and self.f1_ymin < ymin and self.f1_xmax > xmax and self.f1_ymax > ymax:
                    self.factory_status[1] += 1

                    # 공정2 위치에 오브젝트가 잡힐때:
                elif self.f2_xmin < xmin and self.f2_ymin < ymin and self.f2_xmax > xmax and self.f2_ymax > ymax :
                    self.factory_status[2] += 1

                # 공정3 위치에 오브젝트가 잡힐때:
                # elif self.f3_xmin < xmin and self.f3_ymin < ymin and self.f3_xmax > xmax and self.f3_ymax > ymax :
                # factory_status[3] += 1

                else:  # fps 나오고 해당 프레임의 마지막 라인인것을 아니 여기서 선언하고 한번에 입력하면 될듯?
                    self.factory_status[0] += 1
                ###### 공정 bbox 위치 선언 구간####



            elif 'FPS' in line:  # FPS 라인 읽을때. 해당 프레임의 끝 임을 이용하여 리스트 초기화
                self.final_list.append(self.factory_status)  # 여기를 제일 아래단으로?
                self.factory_status = [0, 0, 0, 0]  # 다시 초기화...
                # print(tracker_ID)
                # print(xmin,ymin,xmax,ymax)

        # self.txtfile

        # print(self.final_list)

        '''
        pt1 
        윗 부분까지 프레임 별로 어느 공정에 있는지 딕셔너리로 추가 완료. 이제 몇초동안 어디에 있었는지, 
        1초당 프레임이 몇이었는지, 것들을 계산해서 입력해야함.
        '''
        frame_per_second = 30  # fps 값 임시로 설정.
        self.video_sec = len(self.final_list) // frame_per_second
        total_frame = self.video_sec * frame_per_second  # 끝에 1초미만의 영상의 프레임을 떨구는 것으로 결정.

        print('영상길이:{}초'.format(self.video_sec))
        print('Frame Per Second: {}'.format(frame_per_second))
        print('총 프레임 수: {}'.format(total_frame))

        # 프레임별로 탐지된 오브젝트 수를 초 단위로 변환하여 초당 탐지된 오브젝트 수들을 출력(반올림)
        for sec_num in range(0, self.video_sec):
            # 공정 갯수만큼 초기화시키기
            sum_fac0 = 0
            sum_fac1 = 0
            sum_fac2 = 0
            sum_fac3 = 0
            for frame_num in range(0, frame_per_second):  # 0부터 시작하는 것 때문에... +1, -1 잘 확인하여 입력하기.

                sum_fac0 += self.final_list[(sec_num - 1) * frame_per_second + frame_num - 1][0]
                sum_fac1 += self.final_list[(sec_num - 1) * frame_per_second + frame_num - 1][1]
                sum_fac2 += self.final_list[(sec_num - 1) * frame_per_second + frame_num - 1][2]
                sum_fac3 += self.final_list[(sec_num - 1) * frame_per_second + frame_num - 1][3]

            # print('{}초에 탐지된 오브젝트 수'.format(sec_num))
            sum_fac1 = round(sum_fac1 / frame_per_second)  # FPS 값 만큼 나누고 반올림
            sum_fac2 = round(sum_fac2 / frame_per_second)
            sum_fac3 = round(sum_fac3 / frame_per_second)
            sum_fac0 = round(sum_fac0 / frame_per_second)

            print('1공정:{},'
                  '\n2공정:{},'
                  '\n3공정:{},'
                  '\n그 외:{}'
                  .format(sum_fac1, sum_fac2, sum_fac3, sum_fac0))
            self.count_by_sec.append([sum_fac0,sum_fac1,sum_fac2,sum_fac3])
        # print(self.count_by_sec)

        self.txtfile = None # 텍스트 파일 초기화.


    def onclick_1min(self):
        '''
        단위시간 버튼
        1분,2분,5분,10분 버튼 클릭시, 단위시간에 따른 utilization과 용적률 경고메세지를 출력.
        ************TODO:   matplotlib을 이용해 그래프도 같이 출력을 해야함.*******************
        '''

        self.od_sys_message = "[00:00:00]: 시스템을 시작합니다.\n"
        min = 2 #임시 선언 숫자. 나중에 초로 나누자.
        min_counter = 0
        ######## 단위시간 별로 끊은 초의 오브젝트 값을 리스트로 갖고 있는 변수 ##########
        obj_num1 = []
        obj_num2 = []
        obj_num3 = []

        while  min_counter < len(self.count_by_sec):
            count_time = str(datetime.timedelta(seconds=min_counter))
            area_1 = self.count_by_sec[min_counter][1]/self.f1_que_max
            area_2 = self.count_by_sec[min_counter][2]/self.f2_que_max
            area_3 = self.count_by_sec[min_counter][3]/self.f3_que_max


            obj_num1.append(area_1)
            obj_num2.append(area_2)
            obj_num3.append(area_3)

            #### juicy: 여기 퍼센테이지 용적률을 각각 바꿔야함.###
            if area_1 > 0.5:
                self.od_sys_message =self.od_sys_message + "[{}]: 현재 공정 1이 용적률 {}%를 넘어섰습니다.\n".format(count_time,area_1*100)
                # print("현재 공정 1이 용적률 {}%를 넘어섰습니다.".format(area_1*100))
            if area_2 >0.5:
                self.od_sys_message = self.od_sys_message + "[{}]: 현재 공정 2이 용적률 {}%를 넘어섰습니다.\n".format(count_time,area_2*100)

            if area_3 > 0.5:
                self.od_sys_message = self.od_sys_message + "[{}]: 현재 공정 3이 용적률 {}%를 넘어섰습니다.\n".format(count_time,area_3*100)
            min_counter += min

        self.onchange_sys_message_right(self.od_sys_message)

        divide_by_min = list(range(0, self.video_sec,min))

        self.draw_right_graph(divide_by_min, obj_num1, obj_num2, obj_num3)

    def onclick_2min(self):
        self.od_sys_message = "[00:00:00]: 시스템을 시작합니다.\n"
        min = 5  # 임시 선언 숫자. 나중에 초로 나누자.
        min_counter = 0
        obj_num1 = []
        obj_num2 = []
        obj_num3 = []

        while min_counter < len(self.count_by_sec):
            count_time = str(datetime.timedelta(seconds=min_counter))
            area_1 = self.count_by_sec[min_counter][1] / self.f1_que_max
            area_2 = self.count_by_sec[min_counter][2] / self.f2_que_max
            area_3 = self.count_by_sec[min_counter][3] / self.f3_que_max

            obj_num1.append(area_1)
            obj_num2.append(area_2)
            obj_num3.append(area_3)
            #### juicy: 여기 퍼센테이지 용적률을 각각 바꿔야함.###
            if area_1 > 0.5:
                self.od_sys_message = self.od_sys_message + "[{}]: 현재 공정 1이 용적률 {}%를 넘어섰습니다.\n".format(count_time,
                                                                                                       area_1 * 100)
                # print("현재 공정 1이 용적률 {}%를 넘어섰습니다.".format(area_1*100))
            if area_2 > 0.5:
                self.od_sys_message = self.od_sys_message + "[{}]: 현재 공정 2이 용적률 {}%를 넘어섰습니다.\n".format(count_time,
                                                                                                       area_2 * 100)

            if area_3 > 0.5:
                self.od_sys_message = self.od_sys_message + "[{}]: 현재 공정 3이 용적률 {}%를 넘어섰습니다.\n".format(count_time,
                                                                                                       area_3 * 100)
            min_counter += min
        self.onchange_sys_message_right(self.od_sys_message)

        divide_by_min = list(range(0, self.video_sec, min))

        self.draw_right_graph(divide_by_min, obj_num1, obj_num2, obj_num3)

    def onclick_5min(self):
        self.od_sys_message = "[00:00:00]: 시스템을 시작합니다.\n"
        min = 10  # 임시 선언 숫자. 나중에 초로 나누자.
        min_counter = 0
        obj_num1 = []
        obj_num2 = []
        obj_num3 = []

        while min_counter < len(self.count_by_sec):
            count_time = str(datetime.timedelta(seconds=min_counter))
            area_1 = self.count_by_sec[min_counter][1] / self.f1_que_max
            area_2 = self.count_by_sec[min_counter][2] / self.f2_que_max
            area_3 = self.count_by_sec[min_counter][3] / self.f3_que_max

            obj_num1.append(area_1)
            obj_num2.append(area_2)
            obj_num3.append(area_3)

            #### juicy: 여기 퍼센테이지 용적률을 각각 바꿔야함.###
            if area_1 > 0.5:
                self.od_sys_message = self.od_sys_message + "[{}]: 현재 공정 1이 용적률 {}%를 넘어섰습니다.\n".format(count_time,
                                                                                                       area_1 * 100)
                # print("현재 공정 1이 용적률 {}%를 넘어섰습니다.".format(area_1*100))
            if area_2 > 0.5:
                self.od_sys_message = self.od_sys_message + "[{}]: 현재 공정 2이 용적률 {}%를 넘어섰습니다.\n".format(count_time,
                                                                                                       area_2 * 100)

            if area_3 > 0.5:
                self.od_sys_message = self.od_sys_message + "[{}]: 현재 공정 3이 용적률 {}%를 넘어섰습니다.\n".format(count_time,
                                                                                                       area_3 * 100)
            min_counter += min
        self.onchange_sys_message_right(self.od_sys_message)

        divide_by_min = list(range(0, self.video_sec, min))

        self.draw_right_graph(divide_by_min, obj_num1, obj_num2, obj_num3)

    def onclick_10min(self):
        min = 10  # 임시 선언 숫자. 나중에 초로 나누자.
        min_counter = 0
        obj_num1 = []
        obj_num2 = []
        obj_num3 = []
        while min_counter < len(self.count_by_sec):
            count_time = str(datetime.timedelta(seconds=min_counter))
            area_1 = self.count_by_sec[min_counter][1] / self.f1_que_max
            area_2 = self.count_by_sec[min_counter][2] / self.f2_que_max
            area_3 = self.count_by_sec[min_counter][3] / self.f3_que_max

            obj_num1.append(area_1)
            obj_num2.append(area_2)
            obj_num3.append(area_3)

            #### juicy: 여기 퍼센테이지 용적률을 각각 바꿔야함.###
            if area_1 > 0.5:
                self.od_sys_message = self.od_sys_message + "[{}]: 현재 공정 1이 용적률 {}%를 넘어섰습니다.\n".format(count_time,
                                                                                                       area_1 * 100)
                # print("현재 공정 1이 용적률 {}%를 넘어섰습니다.".format(area_1*100))
            if area_2 > 0.5:
                self.od_sys_message = self.od_sys_message + "[{}]: 현재 공정 1이 용적률 {}%를 넘어섰습니다.\n".format(count_time,
                                                                                                       area_2 * 100)

            if area_3 > 0.5:
                self.od_sys_message = self.od_sys_message + "[{}]: 현재 공정 1이 용적률 {}%를 넘어섰습니다.\n".format(count_time,
                                                                                                       area_3 * 100)
            min_counter += min
        self.onchange_sys_message_right(self.od_sys_message)

        divide_by_min = list(range(0, self.video_sec, min))

        self.draw_right_graph(divide_by_min, obj_num1, obj_num2, obj_num3)


    def onchange_sys_message_right(self,sys_message):
        self.plainTextEdit_od.setPlainText(sys_message)


    def onchange_time_input(self):
        '''
        공장 시간 입력후 엔터 누를시, 해당 시간(초)로 나타내는 함수.
        혼자 쓰이지 않고 밑에 이용률, 용적률 반환하는 함수와 같이 쓰임.
        이용률, 용적률은 여기서 계산함.
        '''

        text = self.timer_input.text()
        # if text != self.time_text:
        text = text.split(':')
        try :
            s = int(text[0]) * 3600 + int(text[1]) * 60 + int(text[2])
            print(self.count_by_sec[s])

            #용적률 계산
            area_1 = self.count_by_sec[s][1] / self.f1_que_max
            area_2 = self.count_by_sec[s][2] / self.f2_que_max
            area_3 = self.count_by_sec[s][3] / self.f3_que_max

            #용적률 변환 텍스트박스 함수 호출
            self.onchange_delta_lambda_od(dl='l', number=1, value=area_1)
            self.onchange_delta_lambda_od(dl='l', number=2, value=area_2)
            self.onchange_delta_lambda_od(dl='l', number=3, value=area_3)
        except Exception as e:
            print(e)


    def onchange_delta_lambda_od(self, dl='d', number=1, value=''):
        # 용적률 변환 텍스트박스 함수

        if dl == 'd':
            if number == 1:
                label = self.label_row_1
            elif number == 2:
                label = self.label_row_2
            else:
                label = self.label_row_3

        else:
            if number == 1:
                label = self.label_area_ratio1
            elif number == 2:
                label = self.label_area_ratio2
            else:
                label = self.label_area_ratio3

        label.setText(str(value))

    def draw_right_graph(self, divide_by_min, obj_num1, obj_num2, obj_num3):

        ax = self.fig.clear() #이전 그래프 한번 초기화


        ax = self.fig.add_subplot(131)
        ax.plot(divide_by_min, obj_num1)
        ax.set_xlabel("time")
        # ax[0].xlim(0,10)
        # ax.set_ylabel("per")
        print(type(ax))

        ax = self.fig.add_subplot(132)
        ax.plot(divide_by_min, obj_num2)
        ax.yaxis.set_visible(False) # 축 정보를 비활성화. 그래프 미관에 방해되서.
        # ax.set_ylabel("per")

        ax = self.fig.add_subplot(133)
        ax.plot(divide_by_min, obj_num3)
        ax.yaxis.set_visible(False)# 축 정보를 비활성화. 그래프 미관에 방해되서.
        # ax.set_xlabel("time")

        # ax.legend()
        self.canvas.draw()


    def onchange_left_graph(self):
        pass


if __name__ == "__main__" :
    #QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv)

    #WindowClass의 인스턴스 생성
    myWindow = WindowClass()

    #프로그램 화면을 보여주는 코드
    myWindow.show()

    #프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()


