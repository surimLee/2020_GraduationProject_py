import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import random

fig = plt.figure()  # 그래프가 그려질 전체 창을 확인
ax1 = fig.add_subplot(1,1,1)  # fig.add_subplot(m,n,poistion index)
                        # 전체 그래프창을 m*n 공간으로 나누고


# def 그래프 그리는 애니메이션
plt.axes([0,512,0,1])

xs = []
for index in range(512):
    xs.append(index)

def animate(i):
    global xs
    ys=[]
    for index in range(512):
        ys.append(random.random())
    ax1.clear()
    ax1.plot(xs,ys,label=("랜덤벨류"), linewidth=1)

ani = animation.FuncAnimation(fig, animate, interval=10)
plt.draw()

