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
recvData = ''
recvLine = ''


global right_1st
global right_2ed
global right_3rd
global right_4th
global right_5th
global right_degX
global right_degY
global right_degZ
global right_accX
global right_accY
global right_accZ
global right_lstX

global left_1st
global left_2ed
global left_3rd
global left_4th
global left_5th
global left_degX
global left_degY
global left_degZ
global left_accX
global left_accY
global left_accZ
global left_lstX

global R_gap_right_DegX  # 현재 DegX - 지난 DegX
global R_gap_right_DegY  # 현재 DegY - 지난 DegY
global R_gap_right_DegZ  # 현재 DegZ - 지난 DegZ
global R_noChangeDeg  # 변화 여부 체크
global R_gap_right_AccX  # 현재 AccX - 지난 AccX
global R_gap_right_AccY  # 현재 AccY - 지난 AccY
global R_gap_right_AccZ  # 현재 AccZ - 지난 AccZ
global R_noChangeAcc  # 변화 여부 체크
global R_gap_past_right_DegX  # 지난 DegX - 지지난 DegX
global R_gap_past_right_DegY  # 지난 DegY - 지지난 DegY
global R_gap_past_right_DegZ  # 지난 DegZ - 지지난 DegZ
global R_noChangeDeg_past  # 지난 변화 여부 체크
global R_gap_past_right_AccX  # 지난 AccX - 지지난 AccX
global R_gap_past_right_AccY  # 지난 AccY - 지지난 AccY
global R_gap_past_right_AccZ  # 지난 AccZ - 지지난 AccZ
global R_noChangeAcc_past  # 지난 변화 여부 체크
global R_Energy

global L_gap_right_DegX  # 현재 DegX - 지난 DegX
global L_gap_right_DegY  # 현재 DegY - 지난 DegY
global L_gap_right_DegZ  # 현재 DegZ - 지난 DegZ
global L_noChangeDeg  # 변화 여부 체크
global L_gap_right_AccX  # 현재 AccX - 지난 AccX
global L_gap_right_AccY  # 현재 AccY - 지난 AccY
global L_gap_right_AccZ  # 현재 AccZ - 지난 AccZ
global L_noChangeAcc  # 변화 여부 체크
global L_gap_past_right_DegX  # 지난 DegX - 지지난 DegX
global L_gap_past_right_DegY  # 지난 DegY - 지지난 DegY
global L_gap_past_right_DegZ  # 지난 DegZ - 지지난 DegZ
global L_noChangeDeg_past  # 지난 변화 여부 체크
global L_gap_past_right_AccX  # 지난 AccX - 지지난 AccX
global L_gap_past_right_AccY  # 지난 AccY - 지지난 AccY
global L_gap_past_right_AccZ  # 지난 AccZ - 지지난 AccZ
global L_noChangeAcc_past  # 지난 변화 여부 체크

check_header = ''
global num_of_Null
num_of_Null = 0
R_Energy = 0
global R_recent_char
R_recent_char=''
global is_R_moving
is_R_moving = []

global index_x
global index_y

index_x = 0
index_y = 0

right_1st = []  # 오른손 엄지손가락
right_2ed = []  # 오른손 검지손가락
right_3rd = []  # 오른손 중지손가락
right_4th = []  # 오른손 약지손가락
right_5th = []  # 오른손 새끼손가락
right_degX = []  # 오른손 X축 기울기
right_degY = []  # 오른손 Y축 기울기
right_degZ = []  # 오른손 Z축 기울기
right_accX = []  # 오른손 X축 가속도
right_accY = []  # 오른손 Y축 가속도
right_accZ = []  # 오른손 Z축 가속도
right_lstX = []  # 리스트 인덱스 # 리스트 길이

left_1st = []  # 왼손 엄지손가락
left_2ed = []  # 왼손 검지손가락
left_3rd = []  # 왼손 중지손가락
left_4th = []  # 왼손 약지손가락
left_5th = []  # 왼손 새끼손가락
left_degX = []  # 왼손 X축 기울기
left_degY = []  # 왼손 Y축 기울기
left_degZ = []  # 왼손 Z축 기울기
left_accX = []  # 왼손 X축 가속도
left_accY = []  # 왼손 Y축 가속도
left_accZ = []  # 왼손 Z축 가속도
left_lstX = []  # 리스트 인덱스 # 리스트 길이


root = tk.Tk()
root.wm_title("SignLanguageTranslator")  # 창이름

fig = plt.figure(figsize=(10,5), dpi=100)     #figure(도표) 생성
ax1 = fig.add_subplot(222, ylim=(0,60)) #오른손 Acc
ax2 = fig.add_subplot(224, ylim=(0,60)) #오른손 Deg
ax3 = fig.add_subplot(221, ylim=(0,60)) #왼손 Acc
ax4 = fig.add_subplot(223, ylim=(0,60)) #왼손 Deg

# 오른손 기울기 그래프
def animate(i):  # Deg Graph
    graph_data = open('saveDataR.txt','r').read()
    lines = graph_data.split('\n')
    deg_x = []  #x축
    deg_Y1 = []  #y축 DegX
    deg_Y2 = []  #y축 DegY
    deg_Y3 = []  #y축 DegZ

    for line in lines:
        if len(line) > 1:
            deg_x.append(int(line.split(' ')[0]))
            deg_Y1.append(int(line.split(' ')[6]))
            deg_Y2.append(int(line.split(' ')[7]))
            deg_Y3.append(int(line.split(' ')[8]))

    ax1.clear()
    ax1.plot(deg_x[-30:], deg_Y1[-30:], color='red', linewidth=1, label="DegX")
    ax1.plot(deg_x[-30:], deg_Y2[-30:], color='blue', linewidth=1, label="DegY")
    ax1.plot(deg_x[-30:], deg_Y3[-30:], color='green', linewidth=1, label="DegZ")
    ax1.legend(loc='upper right')
    ax1.set_title("Degree")

# 오른손 가속도 그래프
def animate2(i):  # Acc Graph
    graph_data = open('saveDataR.txt','r').read()
    lines = graph_data.split('\n')
    acc_x = []  #x축
    acc_Y1 = []  #y축 accX
    acc_Y2 = []  #y축 accY
    acc_Y3 = []  #y축 accZ
    for line in lines:
        if len(line) > 1:
            acc_x.append(int(line.split(' ')[0]))
            acc_Y1.append(int(line.split(' ')[9]))
            acc_Y2.append(int(line.split(' ')[10]))
            acc_Y3.append(int(line.split(' ')[11]))

    ax2.clear()
    ax2.plot(acc_x[-30:], acc_Y1[-30:], color='red', linewidth=1, label="accX")
    ax2.plot(acc_x[-30:], acc_Y2[-30:], color='blue', linewidth=1, label="accY")
    ax2.plot(acc_x[-30:], acc_Y3[-30:], color='green', linewidth=1, label="accZ")
    ax2.legend(loc='upper right')
    ax2.set_title("Acceleration")

# 왼손 기울기 그래프
def animate3(i):  # Deg Graph
    graph_data = open('saveDataL.txt','r').read()
    lines = graph_data.split('\n')
    deg_x = []  #x축
    deg_Y1 = []  #y축 DegX
    deg_Y2 = []  #y축 DegY
    deg_Y3 = []  #y축 DegZ

    for line in lines:
        if len(line) > 1:
            deg_x.append(int(line.split(' ')[0]))
            deg_Y1.append(int(line.split(' ')[6]))
            deg_Y2.append(int(line.split(' ')[7]))
            deg_Y3.append(int(line.split(' ')[8]))

    ax3.clear()
    ax3.plot(deg_x[-30:], deg_Y1[-30:], color='red', linewidth=1, label="DegX")
    ax3.plot(deg_x[-30:], deg_Y2[-30:], color='blue', linewidth=1, label="DegY")
    ax3.plot(deg_x[-30:], deg_Y3[-30:], color='green', linewidth=1, label="DegZ")
    ax3.legend(loc='upper right')
    ax3.set_title("Degree")

# 오른손 가속도 그래프
def animate4(i):  # Acc Graph
    graph_data = open('saveDataL.txt','r').read()
    lines = graph_data.split('\n')
    acc_x = []  #x축
    acc_Y1 = []  #y축 accX
    acc_Y2 = []  #y축 accY
    acc_Y3 = []  #y축 accZ
    for line in lines:
        if len(line) > 1:
            acc_x.append(int(line.split(' ')[0]))
            acc_Y1.append(int(line.split(' ')[9]))
            acc_Y2.append(int(line.split(' ')[10]))
            acc_Y3.append(int(line.split(' ')[11]))

    ax4.clear()
    ax4.plot(acc_x[-30:], acc_Y1[-30:], color='red', linewidth=1, label="accX")
    ax4.plot(acc_x[-30:], acc_Y2[-30:], color='blue', linewidth=1, label="accY")
    ax4.plot(acc_x[-30:], acc_Y3[-30:], color='green', linewidth=1, label="accZ")
    ax4.legend(loc='upper right')
    ax4.set_title("Acceleration")

# 전송부
def send(data):
    while True:
        SendData = input('')
        SendData = SendData+"\n"
        data.send(SendData.encode('utf-8'))

# 수신부
def receive(data):
    global num_of_Null
    #현재시간
    fseconds = time.time()
    stime = int(fseconds%60)
    fseconds//=60
    mtime = fseconds%60
    fseconds//=60
    htime = fseconds%24
    htime = (htime+9)%24

    while True:
        ############### 예고없이 연결 끊겼을 때 재연결 가능하도록 ################
        try:
            recv_temp = data.recv(1024)
            # 스크롤 올라가는 에러 처리
            if len(recv_temp) < 6:
                num_of_Null += 1
                if num_of_Null > 10:
                    print("[ERROR] NULL 문자 많이 옴")
                    reconnect()  # 커널에서 오류발생, 초기화 더 해줘야 할 것 추가해야 함
            else:
                num_of_Null = 0

        except:
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
                # print(int(htime), "시", int(mtime), "분", stime, "초", " : ", line) ####################################################################
                #  어느 손인지 나눠서 text 파일에 쓸 수 있도록 함수 호출
                input_txt(line)
            #  잘못 잘려진 라인인 경우 그냥 버림
            else :
                pass



# 라인별로 분리한 데이터를 헤더파일에 맞춰 알맞은 파일에 쓰기
def input_txt(line):
    global index_x
    global index_y
    global is_R_moving
    fR = open("saveDataR.txt", 'a')
    fL = open("saveDataL.txt", 'a')
    recv_line = line
    if ((recv_line.split(' ')[0]) == 'R'):
        index_x += 1
        if (index_x%2 == 1):
            try:
                #  오른손 데이터 파일에 쓰기
                fR.write(str(len(right_1st) + 1) + ' ' + recv_line + '\n')
                fR.close()

                right_1st.append(int(recv_line.split(' ')[1]))
                right_2ed.append(int(recv_line.split(' ')[2]))
                right_3rd.append(int(recv_line.split(' ')[3]))
                right_4th.append(int(recv_line.split(' ')[4]))
                right_5th.append(int(recv_line.split(' ')[5]))
                right_degX.append(int(recv_line.split(' ')[6]))
                right_degY.append(int(recv_line.split(' ')[7]))
                right_degZ.append(int(recv_line.split(' ')[8]))
                right_accX.append(int(recv_line.split(' ')[9]))
                right_accY.append(int(recv_line.split(' ')[10]))
                right_accZ.append(int(recv_line.split(' ')[11]))
                right_lstX.append(len(right_1st))

                # if (len(right_1st) > 15):
                #     check_gap_R(right_1st[-1], right_2ed[-1], right_3rd[-1], right_4th[-1], right_5th[-1],
                #               right_degX[-1], right_degY[-1], right_degZ[-1], right_accX[-1], right_accY[-1], right_accZ[-1]
                #               , right_degX[-2], right_degY[-2], right_degZ[-2], right_accX[-2], right_accY[-2],
                #               right_accZ[-2], right_degX[-3], right_degY[-3], right_degZ[-3], right_accX[-3], right_accY[-3],
                #               right_accZ[-3])
                #     print("check_gap_R으로 진입\n")

                # 실행하고 5초정도 후에
                if (len(right_1st) > 7):
                    R_Energy = calculate_Energy(right_accX[-1], right_accY[-1], right_accZ[-1], right_accX[-2], right_accY[-2], right_accZ[-2])

                    # 현재 동작중이면
                    if (R_Energy > 500):
                        is_R_moving.append(1)
                        # print("동작중임")

                        if (is_R_moving[-2] == 0):
                            print("동작시작")
                    else:
                        is_R_moving.append(0)
                        # print("동작중 아님")

                        if(is_R_moving[-2] == 1 ):
                            print("끝점 : ", right_1st[-1], right_2ed[-1], right_3rd[-1], right_4th[-1], right_5th[-1],
                                  right_degX[-1], right_degY[-1], right_degZ[-1], right_accX[-1], right_accY[-1], right_accZ[-1])

                            match_fingerLanguage(right_1st[-1], right_2ed[-1], right_3rd[-1], right_4th[-1], right_5th[-1],
                                  right_degX[-1], right_degY[-1], right_degZ[-1])
                        else:
                            pass

            # 오른손 센서값 넣는 와중에 클라이언트가 강제 종료되면 다시 소켓 연결 대기
            except:
                pass
                # print("[ERROR] 오른손 형식 오류")
                # reconnect()
        else:
            pass

    # 헤더가 'L'이면 왼손손에 정보 넣기
    elif ((recv_line.split(' ')[0]) == 'L'):
        index_y += 1
        if (index_y%2==1):
            try:
                #  왼손 데이터 파일에 쓰기
                fL.write(str(len(left_1st) + 1) + ' ' + recv_line + '\n')
                fL.close()

                left_1st.append(int(recv_line.split(' ')[1]))
                left_2ed.append(int(recv_line.split(' ')[2]))
                left_3rd.append(int(recv_line.split(' ')[3]))
                left_4th.append(int(recv_line.split(' ')[4]))
                left_5th.append(int(recv_line.split(' ')[5]))
                left_degX.append(int(recv_line.split(' ')[6]))
                left_degY.append(int(recv_line.split(' ')[7]))
                left_degZ.append(int(recv_line.split(' ')[8]))
                left_accX.append(int(recv_line.split(' ')[9]))
                left_accY.append(int(recv_line.split(' ')[10]))
                left_accZ.append(int(recv_line.split(' ')[11]))
                left_lstX.append(len(left_1st))

                # 실행하고 5초정도 후에
                if (len(left_1st) > 7):
                    L_Energy = calculate_Energy(left_degX[-1], left_degY[-1], left_accZ[-1], left_accX[-2], left_accY[-2], left_accZ[-2])

                    # 현재 동작중이면
                    if (L_Energy > 700):
                        pass

            # 오른손 센서값 넣는 와중에 클라이언트가 강제 종료되면 다시 소켓 연결 대기
            except:
                pass
                # print("[ERROR] 왼손 형식 오류")
                # reconnect()
        else:
            pass

# Energy 값 계산
def calculate_Energy(recent_accX, recent_accY, recent_accZ, past_accX, past_accY, past_accZ) :
    Energy = ((past_accX-recent_accX)**2) + ((past_accY-recent_accY)**2) + ((past_accZ-recent_accZ)**2)
    return Energy

def mark_finger(finger):
    if (finger < 4):
        return 'X'
    elif (3 < finger < 8):
        return 'M'
    else:
        return 'O'

def mark_degree(degree):
    if (degree <-50):
        return "X"
    elif (-51<degree<50):
        return 'M'
    else:
        return "O"

def match_fingerLanguage(r_1st, r_2ed, r_3rd, r_4th, r_5th, r_degX, r_degY, r_degZ):
        global R_recent_char
        mark_r_1st = mark_finger(r_1st)
        mark_r_2ed = mark_finger(r_2ed)
        mark_r_3rd = mark_finger(r_3rd)
        mark_r_4th = mark_finger(r_4th)
        mark_r_5th = mark_finger(r_5th)
        mark_r_degX = mark_degree(r_degX)
        mark_r_degY = mark_degree(r_degY)
        mark_r_degZ = mark_degree(r_degZ)
        print(mark_r_1st, mark_r_2ed, mark_r_3rd, mark_r_4th, mark_r_5th, mark_r_degX, mark_r_degY, mark_r_degZ)
        if(mark_r_1st == 'X'):
            if(mark_r_2ed == 'X' and mark_r_3rd=='O' and mark_r_4th=='O' and mark_r_5th=='O'):
                if (mark_r_degX=='X' and mark_r_degY=='M' and mark_r_degZ=='M'):
                    conn.send("ㄱ\n".encode('utf-8'))
                    print("[Result] ㄱ")
                elif (mark_r_degX=='M' and mark_r_degY=='O' and mark_r_degZ=='M'):
                    if (R_recent_char == 'ㄴ'):
                        pass
                    else:
                        R_recent_char = 'ㄴ'
                        conn.send("ㄴ\n".encode('utf-8'))
                        print("[Result] ㄴ")
        elif(mark_r_3rd=='X' and mark_r_4th=='X' and mark_r_5th=='X'):
            if(mark_r_2ed == 'X' and mark_r_degX=='O'and mark_r_degY=='M' and mark_r_degZ=='M'):
                if (R_recent_char == 'ㅂ'):
                    pass
                else:
                    R_recent_char = 'ㅂ'
                    conn.send("ㅂ\n".encode('utf-8'))
                    print("[Result] ㅂ")
            elif(mark_r_2ed == 'M' and mark_r_degX=='O'and mark_r_degY=='M' and mark_r_degZ=='M'):
                conn.send("ㅇ\n".encode('utf-8'))
                print("[Result] ㅇ")
        elif(mark_r_degX=='X'):
            if(mark_r_degY=='M' and mark_r_degZ=='M' and mark_r_2ed == 'X' and mark_r_3rd=='X'):
                if (R_recent_char == 'ㅅ'):
                    pass
                else:
                    R_recent_char = 'ㅅ'
                    conn.send("ㅅ\n".encode('utf-8'))
                    print("[Result] ㅅ")
        elif(mark_r_1st == 'O'):
            if(mark_r_2ed == 'O' and mark_r_3rd=='O' and mark_r_4th=='O' and mark_r_5th=='O'):
                if(mark_r_degX=='O'):
                    if (R_recent_char == 'ㅍ'):
                        pass
                    else:
                        R_recent_char = 'ㅍ'
                        conn.send("ㅍ\n".encode('utf-8'))
                        print("[Result] ㅍ")
            elif (mark_r_2ed == 'X' and mark_r_3rd == 'X' and mark_r_4th == 'X' and mark_r_5th == 'O'):
                if (R_recent_char == 'ㄹ'):
                    pass
                else:
                    R_recent_char = 'ㄹ'
                    conn.send("ㄹ\n".encode('utf-8'))
                    print("[Result] ㄹ")
            elif(mark_r_2ed == 'X' and mark_r_3rd == 'X' and mark_r_4th == 'O' and mark_r_5th == 'O'):
                if (mark_r_degX == 'M' and mark_r_degY == 'O' and mark_r_degZ == 'M'):
                    if (R_recent_char == 'ㄷ'):
                        pass
                    else:
                        R_recent_char = 'ㄷ'
                        conn.send("ㄷ\n".encode('utf-8'))
                        print("[Result] ㄷ")
        elif(mark_r_1st=='M'):
            if(mark_r_3rd=='O' and mark_r_4th=='O' and mark_r_5th=='O'):
                if (R_recent_char == 'ㅁ'):
                    pass
                else:
                    R_recent_char = 'ㅁ'
                    conn.send("ㅁ\n".encode('utf-8'))
                    print("[Result] ㅁ")
            elif(mark_r_2ed == 'X' and mark_r_3rd=='X' and mark_r_4th=='X' and mark_r_5th=='X'):
                if(mark_r_degX=='O' and mark_r_degY=='M' and mark_r_degZ=='M'):
                    if (R_recent_char == 'ㅂ'):
                        pass
                    else:
                        R_recent_char = 'ㅂ'
                        conn.send("ㅂ\n".encode('utf-8'))
                        print("[Result] ㅂ")
        elif(mark_r_1st=='M' or mark_r_1st=='O'):
            if(mark_r_degX=='O' and mark_r_3rd=='O' and mark_r_4th=='O' and mark_r_5th=='O'):
                if (R_recent_char=='ㅁ'):
                    pass
                else:
                    R_recent_char = 'ㅁ'
                    conn.send("ㅁ\n".encode('utf-8'))
                    print("[Result] ㅁ")
        else:
            pass

    # if (r_1st<3 and r_2ed<3 and r_3rd>7 and r_4th>7 and r_5th>7 and r_degX<-50 and r_degY>40 and 0<r_degZ<30):
#     #     conn.send("ㄱ\n".encode('utf-8'))
#     #     print("[Result] ㄱ")
#     # elif (r_1st<3 and r_2ed<3 and r_3rd>7 and r_4th>7 and r_5th>7 and -20<r_degX<20 and 70<r_degY and -70<r_degZ<10):
#     #     conn.send("ㄴ\n".encode('utf-8'))
#     #     print("[Result] ㄴ")
#     # elif (3<r_1st<10 and r_2ed<3 and r_3rd<3 and r_4th>5 and r_5th>7 and -25<r_degX<20 and 40<r_degY and -45<r_degZ<0):
#     #     conn.send("ㄷ\n".encode('utf-8'))
#     #     print("[Result] ㄷ")
#     # elif (6<r_1st and r_2ed>6 and r_3rd>6 and r_4th>6 and r_5th>6 and -25<r_degX<30 and -30<r_degY<60 and 40<r_degZ):
#     #     conn.send("안녕하세요\n".encode('utf-8'))
#     #     print("[Result] 안녕하세요")
#     # else:
#     #     pass



# 예상치 못하게 소켓 연결이 끊어지는 경우 소켓 재연결
def reconnect():
    svrsock.close()
    setSoket()
    # animation 지워줘야 함
    # datasave 한 거 날려줘야 함

# 버리는 함수
# 동작 구간 판별을 위해 움직임 정도를 체크하는 함수
def check_gap_R(R_recent_1st, R_recent_2nd, R_recent_3rd, R_recent_4th, R_recent_5th,
              R_recent_degX, R_recent_degY, R_recent_degZ, R_recent_accX, R_recent_accY, R_recent_accZ
              ,R_past_degX, R_past_degY, R_past_degZ, R_past_accX, R_past_accY, R_past_accZ
              ,R_ppast_degX, R_ppast_degY, R_ppast_degZ, R_ppast_accX, R_ppast_accY, R_ppast_accZ):

    R_gap_right_DegX = abs(R_recent_degX-R_past_degX)
    R_gap_right_DegY = abs(R_recent_degY-R_past_degY)
    R_gap_right_DegZ = abs(R_recent_degZ-R_past_degZ)
    R_gap_right_AccX = abs(R_recent_accX - R_past_accX)
    R_gap_right_AccY = abs(R_recent_accY - R_past_accY)
    R_gap_right_AccZ = abs(R_recent_accZ - R_past_accZ)

    print("오른손 Acc, Deg 차이 : ", R_gap_right_AccX, R_gap_right_AccY, R_gap_right_AccZ, R_gap_right_DegX, R_gap_right_DegY, R_gap_right_DegZ)

    R_gap_past_right_AccX = abs(R_past_accX-R_ppast_accX)
    R_gap_past_right_AccY = abs(R_past_accY-R_ppast_accY)
    R_gap_past_right_AccZ = abs(R_past_accZ-R_ppast_accZ)
    R_gap_past_right_DegX = abs(R_past_degX-R_ppast_degX)
    R_gap_past_right_DegY = abs(R_past_degY-R_ppast_degY)
    R_gap_past_right_DegZ = abs(R_past_degZ-R_ppast_degZ)

    # 현재 가속도 값 변화량 체크
    if (R_gap_right_AccX < 10 and R_gap_right_AccY < 10 and R_gap_right_AccZ < 10):
        R_noChangeAcc = True
        print("[check] 현재 가속도 값 변화 : ", str(R_noChangeAcc))

    else :
        R_noChangeAcc = False
        print("[check] 현재 가속도 값 변화 : ", str(R_noChangeAcc))

    # 현재 기울기 값 변화량 체크
    if (R_gap_right_DegX < 10 and R_gap_right_DegY < 10 and R_gap_right_DegZ < 10):
        R_noChangeDeg = True
        print("[check] 현재 가속도 값 변화 : " + str(R_noChangeDeg))
    else :
        R_noChangeDeg = False
        print("[check] 현재 기울기 값 변화 : " + str(R_noChangeDeg))

    # 지난 가속도 값 변화량 체크
    if (R_gap_past_right_AccX < 10 and R_gap_past_right_AccY < 10 and R_gap_past_right_AccZ < 10):
        R_noChangeAcc_past = True
        print("[check] 현재 가속도 값 변화 : " + str(R_noChangeAcc_past))
    else :
        R_noChangeAcc_past = False
        print("[check] 지난 가속도 값 변화 : " + str(R_noChangeAcc_past))

    # 지난 기울기 값 변화량 체크
    if (R_gap_past_right_DegX < 10 and R_gap_past_right_DegY < 10 and R_gap_past_right_DegZ < 10):
        R_noChangeDeg_past = True
        print("[check] 지난 기울기 값 변화 : " + str(R_noChangeDeg_past))
    else :
        R_noChangeDeg_past = False
        print("[check] 지난 기울기 값 변화 : " + str(R_noChangeDeg_past))

    # # 만약 움직이다 멈춘 경우이면
    # if(noChangeAcc == True and noChangeAcc_past == False and noChangeDeg == True and noChangeDeg_past == False):
    #     match_Sign(R_recent_1st, R_recent_2nd, R_recent_3rd, R_recent_4th, R_recent_5th,
    #                R_recent_accX, R_recent_accY, R_recent_accZ)

    # # 만약 움직이다 멈춘 경우이면
    # print(str(R_noChangeAcc), str(R_noChangeDeg) , "True, True이면 match_Sign시작\n")
    # if(R_noChangeAcc == True and R_noChangeDeg == True):
    #     match_Sign(R_recent_1st, R_recent_2nd, R_recent_3rd, R_recent_4th, R_recent_5th,
    #                R_recent_accX, R_recent_accY, R_recent_accZ)


def match_Sign(R_recent_1st, R_recent_2nd, R_recent_3rd, R_recent_4th, R_recent_5th
               ,R_recent_degX, R_recent_degY, R_recent_degZ):
    print("[State] 오른손 지화 패턴 매칭 시작")

    if (R_recent_1st< 3 and R_recent_2nd < 3 and R_recent_3rd > 8 and R_recent_4th > 8 and R_recent_5th > 8 and
            R_recent_degX < -70 and 30 > R_recent_degY > -20 and 20 > R_recent_degZ > -20) :
        print("[Result] 기역!!!!!!!!!!")
        conn.send("ㄱ\n".encode('utf-8'))

    elif (R_recent_1st< 3 and R_recent_2nd < 3 and R_recent_3rd > 8 and R_recent_4th > 8 and R_recent_5th > 8 and
            -30 < R_recent_degX < 10 and R_recent_degY > 70 and  10 > R_recent_degZ > -20) :
        print("[Result] 니은!!!!!!!!!!")
        conn.send("ㄴ\n".encode('utf-8'))

    elif (R_recent_1st > 5 and R_recent_2nd < 3 and R_recent_3rd < 3 and R_recent_4th > 8 and R_recent_5th > 5 and
           -30 < R_recent_degX < 0 and R_recent_degY > 70 and  10 > R_recent_degZ > -20) :
        print("[Result] 디귿!!!!!!!!!!")
        conn.send("ㄷ\n".encode('utf-8'))
    else :
        pass



# 소켓을 셋팅하는 함수
def setSoket():
    global addr
    global svrsock
    global conn
    # 소켓 객체를 생성합니다.
    # 주소 체계(address family)로 IPv4, 소켓 타입으로 TCP 사용합니다.
    svrsock=socket(AF_INET,SOCK_STREAM)

    # bind 함수는 소켓을 특정 네트워크 인터페이스와 포트 번호에 연결하는데 사용됩니다.
    # HOST는 hostname, ip address, 빈 문자열 ""이 될 수 있습니다.
    # 빈 문자열이면 모든 네트워크 인터페이스로부터의 접속을 허용합니다.
    # PORT는 1-65535 사이의 숫자를 사용할 수 있습니다.
    svrsock.bind(('', port))

    # 서버가 하나의 클라이언트의 접속을 허용하도록 합니다.
    svrsock.listen(1)
    print ("[STATE] 클라이언트 접속 대기")

    # accept 함수에서 대기하다가 클라이언트가 접속하면 새로운 소켓을 리턴합니다.
    conn,addr=svrsock.accept()

    # 연결 요청 성공. 접속한 클라이언트의 주소입니다.
    print("[STATE] 클라이언트 접속, ", addr)

    sender=threading.Thread(target=send, args=(conn,))
    receiver=threading.Thread(target=receive, args=(conn,))

    sender.start()
    receiver.start()

    plt.show()
    print("[STATE] 센서값 플로팅 시작")

    while True:
        time.sleep(1)
        pass

# 버리는 함수
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

    ani = animation.FuncAnimation(fig, animate, interval=100)  # Deg 오른손
    ani2 = animation.FuncAnimation(fig, animate2, interval=100)  # Acc 오른손
    ani3 = animation.FuncAnimation(fig, animate3, interval=100)  # Deg 왼손
    ani4 = animation.FuncAnimation(fig, animate4, interval=100)  # Acc 왼손
    print("[STATE] 애니메이션 세팅")

    # setflex = threading.Thread(target=setFlex)  # 버리는 함수
    # setflex.start()  # 버리는 함수
    setSoket()


#############################################################

main()