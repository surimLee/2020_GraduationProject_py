from socket import *

from matplotlib import pyplot as plt
from matplotlib import animation
from matplotlib import style
import tkinter as tk
import numpy as np
import threading
import time
import copy

port = 9999  # 소켓 통신할 포트번호

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

finger_language = {'ㄱ':(0, 0, 10, 10, 10, -74, 22, 20, -3, -30, -30),
                   'ㄴ':(0, 0, 10, 10, 10, 4, 86, -34, 1, 1, -2),
                   'ㄷ':(6, 0, 0, 10, 10, -12, 82, -45, -1, -1, 0),
                   'ㄹ':(7, 0, 0, 0, 10, -17, 88, -37, -2, -2, -1),
                   'ㅁ':(10, 5, 10, 10, 10, 84, 3, 21, -3, 0, -1),
                   'ㅂ':(9, 0, 0, 0, 0, 84, 4, 23, -2, 2, -1),
                   'ㅅ':(7, 0, 0, 10, 10, -90, 6, 13, -2, 0, -1),
                   'ㅇ':(7, 4, 0, 5, 0, 83, 13, 23, -1, 0, -1),
                   'ㅈ':(0, 0, 0, 10, 10, -89, 22, 22, -1, 1, -1),
                   'ㅊ':(0, 0, 0, 0, 9, -89, 14, 19, -1, 0, -1),
                   'ㅋ':(0, 6, 0, 10, 10, -90, 21, 13, -1, 0, -1),
                   'ㅌ':(3, 0, 0, 0, 10, 10, 87, -31, -2, 0, -1),
                   'ㅍ':(8, 9, 10, 10, 10, 73, 28, 35, -2, 1, -1),
                   'ㅎ':(0, 8, 10, 10, 10, 11, 82, -32, -3, 1, -5),
                   'ㅏ':(10, 0, 10, 10, 10, 84, 12, 12, -1, 0, 0),
                   'ㅑ': (7, 0, 0, 10, 10, 86, -12, 12, -1, 0, 0),
                   'ㅓ': (8, 0, 10, 10, 10, -14, 90, -28, -1, 2, -1),
                   'ㅕ': (6, 0, 0, 10, 8, -11, 89, -25, 0, 3, 1),
                   'ㅗ': (7, 0, 10, 10, 10, 84, 22, -9, 0, 0, -1),
                   'ㅛ': (7, 0, 0, 10, 8, 85, 14, -5, -2, 0, -1),
                   'ㅜ': (7, 0, 10, 10, 10, -90, 18, -7, -2, 0, -2),
                   'ㅠ': (7, 0, 0, 10, 7, -90, 20, -3, -1, 0, -1),
                   'ㅡ': (9, 5, 10, 10, 0, 5, 76, -58, -2, -1, 0),
                   'ㅣ': (9, 8, 10, 10, 0, 84, -16, 1, -3, 0, -2),
                   # 'ㅐ': (8, 0, 10, 10, 0, 85, -3, 19, -2, -1, 0),
                   # 'ㅒ': (6, 0, 0, 10, 0, 86, -1, 14, -1, 0, -1),
                   # 'ㅔ': (7, 0, 10, 10, 0, -7, 89, -16, -2, 0, -1),
                   # 'ㅖ': (6, 0, 0, 10, 0, -5, 90, -13, -3, -1, -1),
                   # 'ㅚ': (7, 0, 10, 10, 0, 87, 1, -8, -2, 0, -2),
                   # 'ㅟ': (6, 0, 10, 10, 0, -89, 31, -4, 0, 0, -1),
                   # 'ㅢ': (7, 0, 10, 10, 0, -13, 81, -47, -1, -1, -3),
                   }

check_header = ''
global num_of_Null
num_of_Null = 0
R_Energy = 0
global R_recent_char
R_recent_char = ''
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


# 전송부
def send(data):
    while True:
        SendData = input('')
        SendData = SendData + "\n"
        data.send(SendData.encode('utf-8'))


# 수신부
def receive(data):
    global num_of_Null

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
                # print(line)
            #  잘못 잘려진 라인인 경우 그냥 버림
            else:
                pass


# 라인별로 분리한 데이터를 헤더파일에 맞춰 알맞은 파일에 쓰기
def input_txt(line):
    global index_x
    global index_y
    global is_R_moving
    fR = open("saveDataR.txt", 'a')
    fL = open("saveDataL.txt", 'a')
    recv_line = line
    if (recv_line.split(' ')[0] == 'R'):
        index_x += 1
        if (index_x % 2 == 1):
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
                right_lstX.append(len(right_1st))  # 현재까지 들어온 데이터 갯수

                # 실행하고 5초정도 후에
                if (len(right_1st) > 7):
                    R_Energy = calculate_Energy(right_accX[-1], right_accY[-1], right_accZ[-1], right_accX[-2],
                                                right_accY[-2], right_accZ[-2])

                    # 현재 동작중이면
                    if (R_Energy > 300):
                        is_R_moving.append(1)
                        # print("동작중임")

                        if (is_R_moving[-2] == 0):
                            print("동작시작")
                    else:
                        is_R_moving.append(0)
                        # print("동작중 아님")

                        if (is_R_moving[-2] == 1):
                            # print("끝점 : ", right_1st[-1], right_2ed[-1], right_3rd[-1], right_4th[-1], right_5th[-1], right_degX[-1], right_degY[-1], right_degZ[-1], right_accX[-1], right_accY[-1], right_accZ[-1], R_Energy)
                            # match_fingerLanguage(right_lstX[-1] - 1, R_Energy)
                            euclid(right_lstX[-1] - 1, R_Energy)
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
        if (index_y % 2 == 1):
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
                    global L_Energy
                    L_Energy = calculate_Energy(left_accX[-1], left_accY[-1], left_accZ[-1], left_accX[-2],
                                                left_accY[-2], left_accZ[-2])


            # 오른손 센서값 넣는 와중에 클라이언트가 강제 종료되면 다시 소켓 연결 대기
            except:
                pass
                # print("[ERROR] 왼손 형식 오류")
                # reconnect()
        else:
            pass

def euclid(index, r_Energy):

    global R_recent_char
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

    mark_r_1st = right_1st[index]
    mark_r_2ed = right_2ed[index]
    mark_r_3rd = right_3rd[index]
    mark_r_4th = right_4th[index]
    mark_r_5th = right_5th[index]
    mark_r_degX = right_degX[index]
    mark_r_degY = right_degY[index]
    mark_r_degZ = right_degZ[index]
    mark_r_accX = right_accX[index]
    mark_r_accY = right_accY[index]
    mark_r_accZ = right_accZ[index]

    mark_l_1st = left_1st[index]
    mark_l_2ed = left_2ed[index]
    mark_l_3rd = left_3rd[index]
    mark_l_4th = left_4th[index]
    mark_l_5th = left_5th[index]
    mark_l_degX = left_degX[index]
    mark_l_degY = left_degY[index]
    mark_l_degZ = left_degZ[index]
    mark_l_accX = left_accX[index]
    mark_l_accY = left_accY[index]
    mark_l_accZ = left_accZ[index]

    print("오른손 끝점 : ", mark_r_1st, mark_r_2ed, mark_r_3rd, mark_r_4th, mark_r_5th, mark_r_degX, mark_r_degY, mark_r_degZ,
    mark_r_accX, mark_r_accY, mark_r_accZ, r_Energy)
    print("왼손 끝점 : ", mark_l_1st, mark_l_2ed, mark_l_3rd, mark_l_4th, mark_l_5th, mark_l_degX,
          mark_l_degY, mark_l_degZ, mark_l_accX, mark_l_accY, mark_l_accZ, L_Energy)

    finger_language_value = copy.deepcopy(finger_language)

    for fingerSign, (r1, r2, r3, r4, r5, rdX, rdY, rdZ, raX, raY, raZ) in finger_language.items():
        gap_r1 = abs(mark_r_1st - r1)*10
        gap_r2 = abs(mark_r_2ed - r2)*30
        gap_r3 = abs(mark_r_3rd - r3)*30
        gap_r4 = abs(mark_r_4th - r4)*30
        gap_r5 = abs(mark_r_5th - r5)*10
        gap_rdX = abs(mark_r_degX - rdX)*15
        gap_rdY = abs(mark_r_degY - rdY)*15
        gap_rdZ = abs(mark_r_degZ - rdZ)

        if (fingerSign=='ㅛ' or fingerSign=='ㅑ' ):
            print (
            fingerSign, (gap_r1 + gap_r2 + gap_r3 + gap_r4 + gap_r5 + gap_rdX + gap_rdY + gap_rdZ), gap_r1, gap_r2,
            gap_r3, gap_r4, gap_r5, gap_rdX, gap_rdY, gap_rdZ)

        # print (fingerSign, (gap_r1 + gap_r2 + gap_r3 + gap_r4 + gap_r5 + gap_rdX + gap_rdY + gap_rdZ), gap_r1, gap_r2, gap_r3, gap_r4, gap_r5,  gap_rdX, gap_rdY, gap_rdZ)
        finger_language_value[fingerSign] = (gap_r1 + gap_r2 + gap_r3 + gap_r4 + gap_r5 + gap_rdX + gap_rdY + gap_rdZ)
        # print(gap_r1, gap_r2, gap_r3, gap_r4, gap_r5,  gap_rdX, gap_rdY, gap_rdZ, gap_raX, gap_raY, gap_raZ)

    min = 1000
    result = ''
    for fingerSign, value in finger_language_value.items():
        if value < min:
            result = fingerSign
            min = value


    a = sorted(finger_language_value.items(), key=lambda x:x[1])
    print(a)

    print(result)
    conn.send(result)






# Energy 값 계산
def calculate_Energy(recent_accX, recent_accY, recent_accZ, past_accX, past_accY, past_accZ):
    Energy = (((past_accX - recent_accX) ** 2) + ((past_accY - recent_accY) ** 2) + (
                (past_accZ - recent_accZ) ** 2) // 3)
    int(Energy)
    return Energy


def match_fingerLanguage(index, r_Energy):
    global R_recent_char
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

    mark_r_1st = right_1st[index]
    mark_r_2ed = right_2ed[index]
    mark_r_3rd = right_3rd[index]
    mark_r_4th = right_4th[index]
    mark_r_5th = right_5th[index]
    mark_r_degX = right_degX[index]
    mark_r_degY = right_degY[index]
    mark_r_degZ = right_degZ[index]
    mark_r_accX = right_accX[index]
    mark_r_accY = right_accY[index]
    mark_r_accZ = right_accZ[index]

    mark_l_1st = left_1st[index]
    mark_l_2ed = left_2ed[index]
    mark_l_3rd = left_3rd[index]
    mark_l_4th = left_4th[index]
    mark_l_5th = left_5th[index]
    mark_l_degX = left_degX[index]
    mark_l_degY = left_degY[index]
    mark_l_degZ = left_degZ[index]
    mark_l_accX = left_accX[index]
    mark_l_accY = left_accY[index]
    mark_l_accZ = left_accZ[index]

    print("오른손 끝점 : ", mark_r_1st, mark_r_2ed, mark_r_3rd, mark_r_4th, mark_r_5th, mark_r_degX, mark_r_degY, mark_r_degZ,
    mark_r_accX, mark_r_accY, mark_r_accZ, r_Energy)
    print("왼손 끝점 : ", mark_l_1st, mark_l_2ed, mark_l_3rd, mark_l_4th, mark_l_5th, mark_l_degX,
          mark_l_degY, mark_l_degZ, mark_l_accX, mark_l_accY, mark_l_accZ, L_Energy)

    if (L_Energy < 9):  # 왼손을 안 움직이고 = 지화
        if (mark_r_degX < -60 and mark_r_degY > -20 and mark_r_degZ > -20):
            if (mark_r_1st < 3 and mark_r_2ed < 3 and mark_r_3rd > 6 and mark_r_4th > 7 and mark_r_5th > 7):
                if (R_recent_char == 'ㄱ'):
                    if (r_Energy > 7):
                        conn.send("ㄱ\n".encode('utf-8'))
                        print("[Result] ㄱ")
                else:
                    conn.send("ㄱ\n".encode('utf-8'))
                    print("[Result] ㄱ")
                    R_recent_char = 'ㄱ'
            if (mark_r_1st > 7 and mark_r_2ed < 3 and mark_r_3rd < 3 and mark_r_4th > 8 and mark_r_5th > 8):
                if (R_recent_char == 'ㅅ'):
                    if (r_Energy > 10):
                        conn.send("ㅅ\n".encode('utf-8'))
                        print("[Result] ㅅ")
                else:
                    conn.send("ㅅ\n".encode('utf-8'))
                    print("[Result] ㅅ")
                    R_recent_char = 'ㅅ'
            if (mark_r_1st < 3 and mark_r_2ed < 3 and mark_r_3rd < 3 and mark_r_4th > 6 and mark_r_5th > 6):
                if (R_recent_char == 'ㅈ'):
                    if (r_Energy > 10):
                        conn.send("ㅈ\n".encode('utf-8'))
                        print("[Result] ㅈ")
                else:
                    conn.send("ㅈ\n".encode('utf-8'))
                    print("[Result] ㅈ")
                    R_recent_char = 'ㅈ'
            if (mark_r_1st < 3 and mark_r_2ed > 4 and mark_r_3rd < 3 and mark_r_4th > 7 and mark_r_5th > 6):
                if (R_recent_char == 'ㅋ'):
                    if (r_Energy > 15):
                        conn.send("ㅋ\n".encode('utf-8'))
                        print("[Result] ㅋ")
                else:
                    conn.send("ㅋ\n".encode('utf-8'))
                    print("[Result] ㅋ")
                    R_recent_char = 'ㅋ'
            if (mark_r_1st < 3 and mark_r_2ed < 3 and mark_r_3rd < 3 and mark_r_4th < 3 and mark_r_5th > 5):
                if (R_recent_char == 'ㅊ'):
                    if (r_Energy > 10):
                        conn.send("ㅊ\n".encode('utf-8'))
                        print("[Result] ㅊ")
                else:
                    conn.send("ㅊ\n".encode('utf-8'))
                    print("[Result] ㅊ")
                    R_recent_char = 'ㅊ'
            if (3 < mark_r_1st < 8 and mark_r_2ed < 3 and 5 < mark_r_3rd and mark_r_4th > 7 and mark_r_5th > 7):
                if (R_recent_char == 'ㅜ'):
                    if (r_Energy > 10):
                        conn.send("ㅜ\n".encode('utf-8'))
                        print("[Result] ㅜ")
                else:
                    conn.send("ㅜ\n".encode('utf-8'))
                    print("[Result] ㅜ")
                    R_recent_char = 'ㅜ'
            if (7 > mark_r_1st > 2 and mark_r_2ed < 3 and mark_r_3rd < 3 and mark_r_4th > 7 and 9 > mark_r_5th > 4):
                if (R_recent_char == 'ㅠ'):
                    if (r_Energy > 10):
                        conn.send("ㅠ\n".encode('utf-8'))
                        print("[Result] ㅠ")
                else:
                    conn.send("ㅠ\n".encode('utf-8'))
                    print("[Result] ㅠ")
                    R_recent_char = 'ㅠ'
            elif (mark_r_1st > 5 and mark_r_2ed < 3 and mark_r_3rd > 7 and mark_r_4th > 7 and mark_r_5th < 3):
                if (R_recent_char == 'ㅟ'):
                    if (r_Energy > 8):
                        conn.send("ㅟ\n".encode('utf-8'))
                        print("[Result] ㅟ")
                else:
                    conn.send("ㅟ\n".encode('utf-8'))
                    print("[Result] ㅟ")
                    R_recent_char = 'ㅟ'
        elif (mark_r_degX < 10 and mark_r_degY > 60 and mark_r_degZ < 20):
            if (mark_r_1st < 3 and mark_r_2ed < 4 and mark_r_3rd > 7 and mark_r_4th > 7 and mark_r_5th > 7):
                if (R_recent_char == 'ㄴ'):
                    if (r_Energy > 7):
                        conn.send("ㄴ\n".encode('utf-8'))
                        print("[Result] ㄴ")
                else:
                    conn.send("ㄴ\n".encode('utf-8'))
                    print("[Result] ㄴ")
                    R_recent_char = 'ㄴ'
            elif (
                    mark_r_1st > 3 and mark_r_2ed < 4 and mark_r_3rd < 4 and mark_r_4th > 7 and mark_r_5th > 5 and -8 > mark_r_degX):
                if (R_recent_char == 'ㄷ'):
                    if (r_Energy > 8):
                        conn.send("ㄷ\n".encode('utf-8'))
                        print("[Result] ㄷ")
                else:
                    conn.send("ㄷ\n".encode('utf-8'))
                    print("[Result] ㄷ")
                    R_recent_char = 'ㄷ'

            elif (mark_r_1st > 6 and mark_r_2ed > 5 and mark_r_3rd > 7 and mark_r_4th > 7 and mark_r_5th < 3):
                if (R_recent_char == 'ㅡ'):
                    if (r_Energy > 8):
                        conn.send("ㅡ\n".encode('utf-8'))
                        print("[Result] ㅡ")
                else:
                    conn.send("ㅡ\n".encode('utf-8'))
                    print("[Result] ㅡ")
                    R_recent_char = 'ㅡ'
            elif (mark_r_1st > 3 and mark_r_2ed < 4 and mark_r_3rd < 4 and mark_r_4th < 4 and mark_r_5th > 5):
                if (R_recent_char == 'ㄹ'):
                    if (r_Energy > 7):
                        conn.send("ㄹ\n".encode('utf-8'))
                        print("[Result] ㄹ")
                else:
                    conn.send("ㄹ\n".encode('utf-8'))
                    print("[Result] ㄹ")
                    R_recent_char = 'ㄹ'
            elif (mark_r_1st > 5 and 9 > mark_r_2ed > 3 and mark_r_3rd < 4 and mark_r_4th < 4 and mark_r_5th < 4):
                conn.send("ㅌ\n".encode('utf-8'))
                print("[Result] ㅌ")
                R_recent_char = 'ㅌ'
            elif (
                    mark_r_1st > 5 and mark_r_2ed < 3 and mark_r_3rd > 7 and mark_r_4th > 7 and mark_r_5th < 3 and mark_r_degX < -3):
                if (R_recent_char == 'ㅢ'):
                    if (r_Energy > 8):
                        conn.send("ㅢ\n".encode('utf-8'))
                        print("[Result] ㅢ")
                else:
                    conn.send("ㅢ\n".encode('utf-8'))
                    print("[Result] ㅢ")
                    R_recent_char = 'ㅢ'
        if (-20 < mark_r_degX < 50 and 40 < mark_r_degY and mark_r_degZ < 20):
            if (4 > mark_r_1st and 5 < mark_r_2ed and mark_r_3rd > 7 and mark_r_4th > 7 and mark_r_5th > 7):
                conn.send("ㅎ\n".encode('utf-8'))
                print("[Result] ㅎ")
                R_recent_char = 'ㅎ'
            if (mark_r_1st > 5 and mark_r_2ed < 4 and mark_r_3rd > 7 and mark_r_4th > 7 and mark_r_5th > 7):
                if (R_recent_char == 'ㅓ'):
                    if (r_Energy > 15):
                        conn.send("ㅓ\n".encode('utf-8'))
                        print("[Result] ㅓ")
                else:
                    conn.send("ㅓ\n".encode('utf-8'))
                    print("[Result] ㅓ")
                    R_recent_char = 'ㅓ'
            elif (
                    mark_r_1st > 4 and mark_r_2ed < 3 and mark_r_3rd < 3 and mark_r_4th > 7 and mark_r_5th > 7 and -8 < mark_r_degX < 28):
                if (R_recent_char == 'ㅕ'):
                    if (r_Energy > 15):
                        conn.send("ㅕ\n".encode('utf-8'))
                        print("[Result] ㅕ")
                else:
                    conn.send("ㅕ\n".encode('utf-8'))
                    print("[Result] ㅕ")
                    R_recent_char = 'ㅕ'
            elif (
                    mark_r_1st > 5 and mark_r_2ed < 3 and mark_r_3rd > 7 and mark_r_4th > 7 and mark_r_5th < 3 and mark_r_degX > 8):
                if (R_recent_char == 'ㅔ'):
                    if (r_Energy > 8):
                        conn.send("ㅔ\n".encode('utf-8'))
                        print("[Result] ㅔ")
                else:
                    conn.send("ㅔ\n".encode('utf-8'))
                    print("[Result] ㅔ")
                    R_recent_char = 'ㅔ'
            elif (9 > mark_r_1st > 3 and mark_r_2ed < 3 and mark_r_3rd < 3 and mark_r_4th > 7 and mark_r_5th < 3):
                if (R_recent_char == 'ㅖ'):
                    if (r_Energy > 15):
                        conn.send("ㅖ\n".encode('utf-8'))
                        print("[Result] ㅖ")
                else:
                    conn.send("ㅖ\n".encode('utf-8'))
                    print("[Result] ㅖ")
                    R_recent_char = 'ㅖ'

        elif (mark_r_degX > 55 and -40 < mark_r_degY < 60 and -10 < mark_r_degZ < 55):
            if (4 < mark_r_1st and 1 < mark_r_2ed < 8 and mark_r_3rd > 7 and mark_r_4th > 7 and mark_r_5th > 7):
                if (R_recent_char == 'ㅁ'):
                    if (r_Energy > 12):
                        conn.send("ㅁ\n".encode('utf-8'))
                        print("[Result] ㅁ")
                else:
                    conn.send("ㅁ\n".encode('utf-8'))
                    print("[Result] ㅁ")
                    R_recent_char = 'ㅁ'
            if (7 < mark_r_1st and 7 < mark_r_2ed and mark_r_3rd > 7 and mark_r_4th > 7 and mark_r_5th > 7):
                if (R_recent_char == 'ㅍ'):
                    if (r_Energy > 12):
                        conn.send("ㅍ\n".encode('utf-8'))
                        print("[Result] ㅍ")
                else:
                    conn.send("ㅍ\n".encode('utf-8'))
                    print("[Result] ㅍ")
                    R_recent_char = 'ㅍ'
            if (4 < mark_r_1st and 2 < mark_r_2ed < 8 and mark_r_3rd < 3 and mark_r_4th < 8 and mark_r_5th < 3):
                if (R_recent_char == 'ㅇ'):
                    if (r_Energy > 13):
                        conn.send("ㅇ\n".encode('utf-8'))
                        print("[Result] ㅇ")
                else:
                    conn.send("ㅇ\n".encode('utf-8'))
                    print("[Result] ㅇ")
                    R_recent_char = 'ㅇ'
            elif (4 < mark_r_1st and mark_r_2ed < 4 and mark_r_3rd < 4 and mark_r_4th < 4 and mark_r_5th < 4):
                if (R_recent_char == 'ㅂ'):
                    if (r_Energy > 20):
                        conn.send("ㅂ\n".encode('utf-8'))
                        print("[Result] ㅂ")
                else:
                    conn.send("ㅂ\n".encode('utf-8'))
                    print("[Result] ㅂ")
                    R_recent_char = 'ㅂ'
            elif (mark_r_1st > 6 and mark_r_2ed > 5 and mark_r_3rd > 7 and mark_r_4th > 7 and mark_r_5th < 3):
                if (R_recent_char == 'ㅣ'):
                    if (r_Energy > 8):
                        conn.send("ㅣ\n".encode('utf-8'))
                        print("[Result] ㅣ")
                else:
                    conn.send("ㅣ\n".encode('utf-8'))
                    print("[Result] ㅣ")
                    R_recent_char = 'ㅣ'
            elif (mark_r_1st > 5 and mark_r_2ed < 3 and mark_r_3rd > 7 and mark_r_4th > 7 and mark_r_5th < 3):
                if (R_recent_char == 'ㅐ'):
                    if (r_Energy > 8):
                        conn.send("ㅐ\n".encode('utf-8'))
                        print("[Result] ㅐ")
                else:
                    conn.send("ㅐ\n".encode('utf-8'))
                    print("[Result] ㅐ")
                    R_recent_char = 'ㅐ'
            elif (5 < mark_r_1st and mark_r_2ed < 4 and mark_r_3rd > 6 and mark_r_4th > 6 and mark_r_5th > 6):
                if (R_recent_char == 'ㅏ'):
                    if (r_Energy > 10):
                        conn.send("ㅏ\n".encode('utf-8'))
                        print("[Result] ㅏ")
                else:
                    conn.send("ㅏ\n".encode('utf-8'))
                    print("[Result] ㅏ")
                    R_recent_char = 'ㅏ'
            elif (3 < mark_r_1st < 9 and mark_r_2ed < 4 and mark_r_3rd < 4 and mark_r_4th > 6 and mark_r_5th > 6):
                if (R_recent_char == 'ㅑ'):
                    if (r_Energy > 20):
                        conn.send("ㅑ\n".encode('utf-8'))
                        print("[Result] ㅑ")
                else:
                    conn.send("ㅑ\n".encode('utf-8'))
                    print("[Result] ㅑ")
                    R_recent_char = 'ㅑ'
            elif (9 > mark_r_1st > 3 and mark_r_2ed < 3 and mark_r_3rd < 3 and mark_r_4th > 7 and mark_r_5th < 3):
                if (R_recent_char == 'ㅒ'):
                    if (r_Energy > 15):
                        conn.send("ㅒ\n".encode('utf-8'))
                        print("[Result] ㅒ")
                else:
                    conn.send("ㅒ\n".encode('utf-8'))
                    print("[Result] ㅒ")
                    R_recent_char = 'ㅒ'

        elif (mark_r_degX > 55 and -40 < mark_r_degY < 60 and mark_r_degZ < 0):
            if (4 < mark_r_1st < 9 and mark_r_2ed < 3 and mark_r_3rd > 7 and mark_r_4th > 7 and mark_r_5th > 7):
                if (R_recent_char == 'ㅗ'):
                    if (r_Energy > 12):
                        conn.send("ㅗ\n".encode('utf-8'))
                        print("[Result] ㅗ")
                else:
                    conn.send("ㅗ\n".encode('utf-8'))
                    print("[Result] ㅗ")
                    R_recent_char = 'ㅗ'
            if (4 < mark_r_1st < 9 and mark_r_2ed < 3 and mark_r_3rd < 3 and mark_r_4th > 7 and mark_r_5th > 7):
                if (R_recent_char == 'ㅛ'):
                    if (r_Energy > 12):
                        conn.send("ㅛ\n".encode('utf-8'))
                        print("[Result] ㅛ")
                else:
                    conn.send("ㅛ\n".encode('utf-8'))
                    print("[Result] ㅛ")
                    R_recent_char = 'ㅛ'
            elif (mark_r_1st > 5 and mark_r_2ed < 3 and mark_r_3rd > 7 and mark_r_4th > 7 and mark_r_5th < 3):
                if (R_recent_char == 'ㅚ'):
                    if (r_Energy > 8):
                        conn.send("ㅚ\n".encode('utf-8'))
                        print("[Result] ㅚ")
                else:
                    conn.send("ㅚ\n".encode('utf-8'))
                    print("[Result] ㅚ")
                    R_recent_char = 'ㅚ'
    elif (L_Energy > 8):
        if (
                30 > mark_r_degX > -30 and 30 < mark_r_degY and mark_r_degZ > 30 and 50 > mark_l_degX > -30 and -50 < mark_l_degY < 20 and mark_l_degZ > 40):
            if (
                    6 < mark_r_1st and mark_r_2ed > 5 and mark_r_3rd > 7 and mark_r_4th > 7 and mark_r_5th > 7 and 5 < mark_l_1st and mark_l_2ed > 5 and mark_l_3rd > 5 and mark_l_4th > 5 and mark_l_5th > 5):
                conn.send("안녕하세요\n".encode('utf-8'))
                print("[Result] 안녕하세요")
                R_recent_char = '안녕하세요'
        elif (
                40 > mark_r_degX > -10 and 40 < mark_r_degY and mark_r_degZ < 5 and 10 > mark_l_degX > -30 and -60 < mark_l_degY < 10 and mark_l_degZ > 60):
            if (
                    5 > mark_r_1st and mark_r_2ed < 5 and mark_r_3rd < 5 and mark_r_4th < 5 and mark_r_5th < 5 and 8 > mark_l_1st and mark_l_2ed < 5 and mark_l_3rd < 5 and mark_l_4th < 5):
                conn.send("감사합니다\n".encode('utf-8'))
                print("[Result] 감사합니다")
                R_recent_char = '감사합니다'
        elif (
                mark_r_degX > 60 and -5 < mark_r_degY < 30 and -50 < mark_r_degZ < -10 and mark_l_degX > 60 and -30 < mark_l_degY < 50 and 10 > mark_l_degZ > -40):
            if (
                    mark_r_1st > 3 and mark_r_2ed < 4 and mark_r_3rd > 6 and mark_r_4th > 7 and mark_r_5th > 7 and 9 > mark_l_1st > 2 and mark_l_2ed < 4 and mark_l_3rd > 5 and mark_l_4th > 6 and mark_l_5th > 6):
                conn.send("만나서\n".encode('utf-8'))
                print("[Result] 만나서")
                R_recent_char = '만나서'
        elif (
                mark_r_degX < -5 and mark_r_degY > 60 and -65 < mark_r_degZ < 40 and -20 < mark_l_degX < 40 and -30 > mark_l_degY and 20 > mark_l_degZ > -40):
            if (
                    mark_r_1st < 3 and mark_r_2ed < 4 and mark_r_3rd < 3 and mark_r_4th < 3 and mark_r_5th < 3 and 6 > mark_l_1st and mark_l_2ed < 5 and mark_l_3rd < 5 and mark_l_4th < 4):
                conn.send("반갑습니다\n".encode('utf-8'))
                print("[Result] 반갑습니다")
                R_recent_char = '반갑습니다'

        elif (
                mark_r_degX < -20 and mark_r_degY > 45 and 55 < mark_r_degZ and -10 < mark_l_degX < 50 and -30 > mark_l_degY < 10 and mark_l_degZ < -50):
            if (
                    mark_r_1st < 3 and mark_r_2ed < 4 and mark_r_3rd < 3 and mark_r_4th < 3 and mark_r_5th < 3 and 6 > mark_l_1st and mark_l_2ed < 5 and mark_l_3rd < 5 and mark_l_4th < 4 and mark_l_5th < 4):
                conn.send("입니다\n".encode('utf-8'))
                print("[Result] 입니다")
                R_recent_char = '입니다'


# 예상치 못하게 소켓 연결이 끊어지는 경우 소켓 재연결
def reconnect():
    svrsock.close()
    setSoket()
    # animation 지워줘야 함
    # datasave 한 거 날려줘야 함


# 소켓을 셋팅하는 함수
def setSoket():
    global addr
    global svrsock
    global conn
    # 소켓 객체를 생성합니다.
    # 주소 체계(address family)로 IPv4, 소켓 타입으로 TCP 사용합니다.
    svrsock = socket(AF_INET, SOCK_STREAM)

    # bind 함수는 소켓을 특정 네트워크 인터페이스와 포트 번호에 연결하는데 사용됩니다.
    # HOST는 hostname, ip address, 빈 문자열 ""이 될 수 있습니다.
    # 빈 문자열이면 모든 네트워크 인터페이스로부터의 접속을 허용합니다.
    # PORT는 1-65535 사이의 숫자를 사용할 수 있습니다.
    svrsock.bind(('', port))

    # 서버가 하나의 클라이언트의 접속을 허용하도록 합니다.
    svrsock.listen(1)
    print ("[STATE] 클라이언트 접속 대기")

    # accept 함수에서 대기하다가 클라이언트가 접속하면 새로운 소켓을 리턴합니다.
    conn, addr = svrsock.accept()

    # 연결 요청 성공. 접속한 클라이언트의 주소입니다.
    print("[STATE] 클라이언트 접속, ", addr)

    sender = threading.Thread(target=send, args=(conn,))
    receiver = threading.Thread(target=receive, args=(conn,))

    sender.start()
    receiver.start()

    plt.show()
    print("[STATE] 센서값 플로팅 시작")

    while True:
        time.sleep(1)
        pass


# 첫 실행 시 파일 리셋하고 소켓이랑 애니메이션 settiong하는 부분
def main():
    fR = open("saveDataR.txt", 'w')
    fR.close()
    fL = open("saveDataL.txt", 'w')
    fL.close()

    setSoket()

#############################################################

main()