import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import matplotlib
import random
matplotlib.use("TkAgg")
import numpy as np

style.use('fivethirtyeight')
fig = plt.figure()
ax1 = fig.add_subplot(1, 1, 1)




def animate(i):
    print("call")
    graph_data = open('new1.txt', 'r+').read()
    lines = graph_data.split('\n')
    xs = []
    ys = []
    print("2 call")
    for line in lines:
        if len(line) > 1:
            x, y = line.split(',')
            xs.append(x)
            ys.append(y)
    ax1.clear()
    ax1.plot(xs[-100:], ys[-100:])
    print("3 call")

ani = animation.FuncAnimation(fig, animate, interval=1000)

plt.show()

