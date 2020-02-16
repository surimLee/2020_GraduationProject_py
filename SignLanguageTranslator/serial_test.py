import serial
from numpy import *
from matplotlib import pyplot as plt

ard = serial.Serial('COM4', 9600)
ard.readline()
ard.flush()

lstX = []
lstY = []
arrX=None
arrY=None

plt.ion()
fig = plt.figure()
sf = fig.add_subplot(1,1,1)
plt.xlim([0,60])
plt.ylim([0,30])
line1, = sf.plot(arrX,arrY,'-r')

while True:
    # 아두이노에서 데이터를 한 절 전송받는다
    bytesR = ard.readline()
    lstR = eval(bytesR[:-2].decode())

    # 시간을 초단위로 계산하고 센서값을 리스트에 각각 저장한다
    timeR = lstR[0] / 1000.0
    lstX.append(timeR)
    lstY.append(lstR[1])

    # 갱신된 데이터를 플로팅 객체에 등록한다
    line1.set_xdata(lstX)
    line1.set_ydata(lstY)

    # 그래프를 즉시 그린다
    plt.draw(), plt.pause(0.0001)
    print('time:%.3fs, value:%d' % (timeR, lstR[1]))

au.close()