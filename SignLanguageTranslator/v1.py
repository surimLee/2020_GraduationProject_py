from socket import *
from matplotlib import pyplot as plt
from matplotlib import animation
from matplotlib import style
import tkinter as tk
import numpy as np
import threading
import time

plt.style.use('fivethirtyeight')
port = 9999  # 소켓 통신할 포트번호
isGetBlank = 0  # 공백문자를 받으면 카운팅되는 변수 -> 3번이상 공백문자 받으면 소켓 종료해야함
recvData = ''
recvLine = ''


global right_1st
global right_2ed
global right_3rd
global right_4th
global right_5th
global right_accX
global right_accY
global right_accZ
global right_degX
global right_degY
global right_degZ
global right_lstX

global left_1st
global left_2ed
global left_3rd
global left_4th
global left_5th
global left_accX
global left_accY
global left_accZ
global left_degX
global left_degY
global left_degZ
global left_lstX

global R_gap_right_AccX  # 현재 AccX - 지난 AccX
global R_gap_right_AccY  # 현재 AccY - 지난 AccY
global R_gap_right_AccZ  # 현재 AccZ - 지난 AccZ
global R_noChangeAcc  # 변화 여부 체크
global R_gap_right_DegX  # 현재 DegX - 지난 DegX
global R_gap_right_DegY  # 현재 DegY - 지난 DegY
global R_gap_right_DegZ  # 현재 DegZ - 지난 DegZ
global R_noChangeDeg  # 변화 여부 체크
global R_gap_past_right_AccX  # 지난 AccX - 지지난 AccX
global R_gap_past_right_AccY  # 지난 AccY - 지지난 AccY
global R_gap_past_right_AccZ  # 지난 AccZ - 지지난 AccZ
global R_noChangeAcc_past  # 지난 변화 여부 체크
global R_gap_past_right_DegX  # 지난 DegX - 지지난 DegX
global R_gap_past_right_DegY  # 지난 DegY - 지지난 DegY
global R_gap_past_right_DegZ  # 지난 DegZ - 지지난 DegZ
global R_noChangeDeg_past  # 지난 변화 여부 체크

check_header = ''

global num_of_Null
num_of_Null = 0  # 연속으로 Null이 오는 횟수 체크

right_1st = []  # 오른손 엄지손가락
right_2ed = []  # 오른손 검지손가락
right_3rd = []  # 오른손 중지손가락
right_4th = []  # 오른손 약지손가락
right_5th = []  # 오른손 새끼손가락
right_accX = []  # 오른손 X축 가속도
right_accY = []  # 오른손 Y축 가속도
right_accZ = []  # 오른손 Z축 가속도
right_degX = []  # 오른손 X축 기울기
right_degY = []  # 오른손 Y축 기울기
right_degZ = []  # 오른손 Z축 기울기
right_lstX = []  # 리스트 인덱스 # 리스트 길이

left_1st = []  # 왼손 엄지손가락
left_2ed = []  # 왼손 검지손가락
left_3rd = []  # 왼손 중지손가락
left_4th = []  # 왼손 약지손가락
left_5th = []  # 왼손 새끼손가락
left_accX = []  # 왼손 X축 가속도
left_accY = []  # 왼손 Y축 가속도
left_accZ = []  # 왼손 Z축 가속도
left_degX = []  # 왼손 X축 기울기
left_degY = []  # 왼손 Y축 기울기
left_degZ = []  # 왼손 Z축 기울기
left_lstX = []  # 리스트 인덱스 # 리스트 길이


root = tk.Tk()
root.wm_title("SignLanguageTranslator")  # 창이름

fig = plt.figure(figsize=(10,5), dpi=100)     #figure(도표) 생성
ax1 = fig.add_subplot(211, ylim=(0,60))
ax2 = fig.add_subplot(212, ylim=(0,60))

# 오른손 가속도 그래프
def animate(i):  # Acc Graph
    graph_data = open('saveData.txt','r').read()
    lines = graph_data.split('\n')
    acc_x = []  #x축
    acc_Y1 = []  #AccX
    acc_Y2 = []  #AccY
    acc_Y3 = []  #AccZ

    for line in lines:
        if len(line) > 1:
            acc_x.append(int(line.split(' ')[0]))
            acc_Y1.append(int(line.split(' ')[6]))
            acc_Y2.append(int(line.split(' ')[7]))
            acc_Y3.append(int(line.split(' ')[8]))

    ax1.clear()
    ax1.plot(acc_x[-30:], acc_Y1[-30:], color='red', linewidth=1, label="AccX")
    ax1.plot(acc_x[-30:], acc_Y2[-30:], color='blue', linewidth=1, label="AccY")
    ax1.plot(acc_x[-30:], acc_Y3[-30:], color='green', linewidth=1, label="AccZ")
    ax1.legend(loc='upper right')
    ax1.set_title("Acceleration")

# 오른손 각도 그래프
def animate2(i):  # Deg Graph
    graph_data = open('saveData.txt','r').read()
    lines = graph_data.split('\n')
    deg_x = []  #x축
    deg_Y1 = []  #degX
    deg_Y2 = []  #degY
    deg_Y3 = []  #degZ
    for line in lines:
        if len(line) > 1:
            deg_x.append(int(line.split(' ')[0]))
            deg_Y1.append(int(line.split(' ')[9]))
            deg_Y2.append(int(line.split(' ')[10]))
            deg_Y3.append(int(line.split(' ')[11]))

    ax2.clear()
    ax2.plot(deg_x[-30:], deg_Y1[-30:], color='red', linewidth=1, label="degX")
    ax2.plot(deg_x[-30:], deg_Y2[-30:], color='blue', linewidth=1, label="degY")
    ax2.plot(deg_x[-30:], deg_Y3[-30:], color='green', linewidth=1, label="degZ")
    ax2.legend(loc='upper right')
    ax2.set_title("Degree")


# 전송부
def send(data):

    while True:
        SendData=input('>>>>>>>')
        SendData=SendData+"\n"
        data.send(SendData.encode('utf-8'))

# 수신부
def receive(data):
    while True:
        ############### 예고없이 연결 끊겼을 때 재연결 가능하도록 ################
        try :
            recv_temp = data.recv(1024)

            # 스크롤 올라가는 에러 처리
            if len(recv_temp) < 6 :
                num_of_Null = num_of_Null + 1
                if num_of_Null > 10 :
                    print("[ERROR] NULL 문자 많이 옴")
                    reconnect()
            else : num_of_Null = 0

        except :
            print("[ERROR] 클라이언트 연결 끊김")
            reconnect()

        ########## 전송되는 메세지 인코딩 해서 화면에 sender랑 함께 표기 ##########
        recvData = recv_temp.decode('utf-8')

        lines = recvData.split("Q\n")  # 여러줄이 수신된 경우 개행문자를 기준으로 분리

        #  개행문자를 기준으로 분리한 라인들을 파일에 쓰고 화면에 출력
        for line in lines:
            #  잘못 잘려진 라인은 버려지도록 길이 체크
            if len(line) > 10:
                #  제대로 데이터 수신된 경우에만 화면에 출력
                print(addr, " : ", line)
                #  어느 손인지 나눠서 text 파일에 쓸 수 있도록 함수 호출
                input_txt(line)
            #  잘못 잘려진 라인인 경우 그냥 버림
            else :
                pass



# 라인별로 분리한 데이터를 헤더파일에 맞춰 알맞은 파일에 쓰기
def input_txt(line):
    fR = open("saveDataR.txt", 'a')
    fL = open("saveDataL.txt", 'a')
    recv_line = line
    if ((recv_line.split(' ')[0]) == 'R'):
        try:
            #  오른손 데이터 파일에 쓰기
            fR.write(str(len(right_1st) + 1) + ' ' + recv_line + '\n')
            fR.close()

            right_1st.append(int(recv_line.split(' ')[1]))
            right_2ed.append(int(recv_line.split(' ')[2]))
            right_3rd.append(int(recv_line.split(' ')[3]))
            right_4th.append(int(recv_line.split(' ')[4]))
            right_5th.append(int(recv_line.split(' ')[5]))
            right_accX.append(int(recv_line.split(' ')[6]))
            right_accY.append(int(recv_line.split(' ')[7]))
            right_accZ.append(int(recv_line.split(' ')[8]))
            right_degX.append(int(recv_line.split(' ')[9]))
            right_degY.append(int(recv_line.split(' ')[10]))
            right_degZ.append(int(recv_line.split(' ')[11]))
            right_lstX.append(len(right_1st))

            if (len(right_1st) > 15):
                check_gap(right_1st[-1], right_2ed[-1], right_3rd[-1], right_4th[-1], right_5th[-1],
                          right_accX[-1], right_accY[-1], right_accZ[-1], right_degX[-1], right_degY[-1], right_degZ[-1]
                          , right_accX[-2], right_accY[-2], right_accZ[-2], right_degX[-2], right_degY[-2],
                          right_degZ[-2], right_accX[-3], right_accY[-3], right_accZ[-3], right_degX[-3], right_degY[-3],
                          right_degZ[-3])


        # 오른손 센서값 넣는 와중에 클라이언트가 강제 종료되면 다시 소켓 연결 대기
        except:
            print("[ERROR] 오른손 형식 오류")
            reconnect()

    # 헤더가 'L'이면 왼손손에 정보 넣기
    elif ((recv_line.split(' ')[0]) == 'L'):
        try:
            #  왼손 데이터 파일에 쓰기
            fL.write(str(len(left_1st) + 1) + ' ' + recv_line + '\n')
            fL.close()

            left_1st.append(int(recv_line.split(' ')[1]))
            left_2ed.append(int(recv_line.split(' ')[2]))
            left_3rd.append(int(recv_line.split(' ')[3]))
            left_4th.append(int(recv_line.split(' ')[4]))
            left_5th.append(int(recv_line.split(' ')[5]))
            left_accX.append(int(recv_line.split(' ')[6]))
            left_accY.append(int(recv_line.split(' ')[7]))
            left_accZ.append(int(recv_line.split(' ')[8]))
            left_degX.append(int(recv_line.split(' ')[9]))
            left_degY.append(int(recv_line.split(' ')[10]))
            left_degZ.append(int(recv_line.split(' ')[11]))
            left_lstX.append(len(left_1st))
        # 오른손 센서값 넣는 와중에 클라이언트가 강제 종료되면 다시 소켓 연결 대기
        except:
            print("[ERROR] 왼손 형식 오류")
            reconnect()


# 예상치 못하게 소켓 연결이 끊어지는 경우 소켓 재연결
def reconnect():
    svrsock.close()
    setSoket()
    # animation 지워줘야 함
    # datasave 한 거 날려줘야 함

# 동작 구간 판별을 위해 움직임 정도를 체크하는 함수
def check_gap(R_recent_1st, R_recent_2nd, R_recent_3rd, R_recent_4th, R_recent_5th,
              R_recent_accX, R_recent_accY, R_recent_accZ, R_recent_degX, R_recent_degY, R_recent_degZ
              ,R_past_accX, R_past_accY, R_past_accZ, R_past_degX, R_past_degY, R_past_degZ
              ,R_ppast_accX, R_ppast_accY, R_ppast_accZ, R_ppast_degX, R_ppast_degY, R_ppast_degZ):

    R_gap_right_AccX = abs(R_recent_accX-R_past_accX)
    R_gap_right_AccY = abs(R_recent_accY-R_past_accY)
    R_gap_right_AccZ = abs(R_recent_accZ-R_past_accZ)
    R_gap_right_DegX = abs(R_recent_degX-R_past_degX)
    R_gap_right_DegY = abs(R_recent_degY-R_past_degY)
    R_gap_right_DegZ = abs(R_recent_degZ-R_past_degZ)

    R_gap_past_right_AccX = abs(R_past_accX-R_ppast_accX)
    R_gap_past_right_AccY = abs(R_past_accY-R_ppast_accY)
    R_gap_past_right_AccZ = abs(R_past_accZ-R_ppast_accZ)
    R_gap_past_right_DegX = abs(R_past_degX-R_ppast_degX)
    R_gap_past_right_DegY = abs(R_past_degY-R_ppast_degY)
    R_gap_past_right_DegZ = abs(R_past_degZ-R_ppast_degZ)

    # 현재 가속도 값 변화량 체크
    if (R_gap_right_AccX < 10 and R_gap_right_AccY < 10 and R_gap_right_AccZ < 10):
        noChangeAcc = True
    else : noChangeAcc = False
    print("[check] 현재 가속도 값 변화 : " + noChangeAcc)

    # 현재 기울기 값 변화량 체크
    if (R_gap_right_DegX < 10 and R_gap_right_DegY < 10 and R_gap_right_DegZ < 10):
        noChangeDeg = True
    else : noChangeDeg = False
    print("[check] 현재 기울기 값 변화 : " + noChangeDeg)

    # 지난 가속도 값 변화량 체크
    if (R_gap_past_right_AccX < 10 and R_gap_past_right_AccY < 10 and R_gap_past_right_AccZ < 10):
        noChangeAcc_past = True
    else : noChangeAcc_past = False
    print("[check] 지난 가속도 값 변화 : " + noChangeAcc_past)

    # 지난 기울기 값 변화량 체크
    if (R_gap_past_right_DegX < 10 and R_gap_past_right_DegY < 10 and R_gap_past_right_DegZ < 10):
        noChangeDeg_past = True
    else : noChangeDeg_past = False
    print("[check] 지난 기울기 값 변화 : " + noChangeDeg_past)

    # 만약 움직이다 멈춘 경우이면
    if(noChangeAcc == True and noChangeAcc_past == False and noChangeDeg == True and noChangeDeg_past == False):
        match_Sign(R_recent_1st, R_recent_2nd, R_recent_3rd, R_recent_4th, R_recent_5th,
                   R_recent_accX, R_recent_accY, R_recent_accZ, R_recent_degX, R_recent_degY, R_recent_degZ)


def match_Sign(R_recent_1st, R_recent_2nd, R_recent_3rd, R_recent_4th, R_recent_5th
               ,R_recent_accX, R_recent_accY, R_recent_accZ, R_recent_degX, R_recent_degY, R_recent_degZ):
    print("[State] 오른손 지화 패턴 매칭 시작")

    if (R_recent_1st< 3 and R_recent_2nd < 3 and R_recent_3rd > 8 and R_recent_4th > 8 and R_recent_5th > 8 and
            R_recent_accX < -70 and R_recent_accY > 0 and R_recent_accY < 20 and R_recent_accZ > -10 and R_recent_accZ < 10) :
        print("[Result] 기역!!!!!!!!!!")

    elif (R_recent_1st< 3 and R_recent_2nd < 3 and R_recent_3rd > 8 and R_recent_4th > 8 and R_recent_5th > 8 and
            R_recent_accX < 10 and R_recent_accX > -30 and R_recent_accY > 70 and  R_recent_accZ > -20 and R_recent_accZ < 10) :
        print("[Result] 니은!!!!!!!!!!")

    elif (R_recent_1st > 5 and R_recent_2nd < 3 and R_recent_3rd < 3 and R_recent_4th > 8 and R_recent_5th > 5 and
            R_recent_accX < 0 and R_recent_accX > -30 and R_recent_accY > 70 and  R_recent_accZ > -20 and R_recent_accZ < 10) :
        print("[Result] 디귿!!!!!!!!!!")
    else :
        pass



# 소켓을 셋팅하는 함수
def setSoket():
    global addr
    global svrsock
    # 소켓 객체를 생성합니다.
    # 주소 체계(address family)로 IPv4, 소켓 타입으로 TCP 사용합니다.
    svrsock=socket(AF_INET,SOCK_STREAM)

    # bind 함수는 소켓을 특정 네트워크 인터페이스와 포트 번호에 연결하는데 사용됩니다.
    # HOST는 hostname, ip address, 빈 문자열 ""이 될 수 있습니다.
    # 빈 문자열이면 모든 네트워크 인터페이스로부터의 접속을 허용합니다.
    # PORT는 1-65535 사이의 숫자를 사용할 수 있습니다.
    svrsock.bind(("", port))

    # 서버가 하나의 클라이언트의 접속을 허용하도록 합니다.
    svrsock.listen(1)
    print ("[STATE] TCP Server Waiting for client...")

    # accept 함수에서 대기하다가 클라이언트가 접속하면 새로운 소켓을 리턴합니다.
    conn,addr=svrsock.accept()

    # 연결 요청 성공. 접속한 클라이언트의 주소입니다.
    print("[STATE] I got a connection from ", addr)

    sender=threading.Thread(target=send, args=(conn,))
    receiver=threading.Thread(target=receive, args=(conn,))

    sender.start()
    receiver.start()

    plt.show()
    print("[STATE] 그래프 Floating Start")

    while True:
        time.sleep(1)
        pass

# Flex 센서 UI 셋팅 (임시)
def setFlex():
    global root
    global flexSensorValue1
    root = tk.Tk()
    root.wm_title("Flex Sensor")
    root.geometry("350x350")
    print(">>> Set Flex Sensor")

    flexSensor = tk.LabelFrame(root, text="FlexSeneor", height=300, width=250, font=("",16))

    flexSensor1 = tk.Label(flexSensor, text=" 엄지손가락 :  ", font=("", 12))
    flexSensor1.place(x=20, y=30, width=100, height=40)
    flexSensorValue1 = tk.StringVar()
    flexSensorValue1.set("0")
    #flexSensorValue1.place(x=120, y=30, width=30, height=40)

    flexSensor2 = tk.Label(flexSensor, text=" 검지손가락 :  ", font=("", 12))
    flexSensor2.place(x=20, y=70, width=100, height=40)

    flexSensor3 = tk.Label(flexSensor, text=" 중지손가락 :  ", font=("", 12))
    flexSensor3.place(x=20, y=110, width=100, height=40)


    flexSensor4 = tk.Label(flexSensor, text=" 약지손가락 :  ", font=("", 12))
    flexSensor4.place(x=20, y=150, width=100, height=40)

    flexSensor5 = tk.Label(flexSensor, text=" 새끼손가락 :  ", font=("", 12))
    flexSensor5.place(x=20, y=190, width=100, height=40)

    flexSensor.pack(pady=10)

#    root.mainloop()
#    print(">>> MainLoop")

# 첫 실행 시 파일 리셋하고 소켓이랑 애니메이션 settiong하는 부분
def main():

    fR = open("saveDataR.txt", 'w')
    fR.close()
    fL = open("saveDataL.txt", 'w')
    fL.close()

    # ani = threading.Thread(target=animation.FuncAnimation(fig, animate, interval=200))
#    ani = animation.FuncAnimation(fig, animate, interval=100)  # Acc
#    ani2 = animation.FuncAnimation(fig, animate2, interval=100)  #Deg
    print("[STATE] Animation Set")

    # setflex = threading.Thread(target=setFlex)
    # setflex.start()
    setSoket()


#############################################################

main()