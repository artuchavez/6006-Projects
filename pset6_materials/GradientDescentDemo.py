"""
The aim of this script is to demonstrate different performance characteristics of gradient descent
over different functions. In particular, you'll see where choosing a fixed learning parameter can get you in trouble.

You need to enter three parameters in the command line, the squeeze factor, the learning rate, and the delay, eg

python GradientDescentDemo.py 3 0.05 1000

The purpose of these parameters is specified below. Consider plugging in the following combinations of parameters.

1 0.2 1000
1 1 1000
3 0.1 1000
5 0.2 1000
10 0.02 1000
10 0.08 1000
10 0.2 1000
10 0.3 1000

Through these demos, hopefully you notice a demonstration for how the wrong learning parameter than throw things into
disarray, particularly when there's a high squish factor!

"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from random import random
import sys

"""
INPUTS:
    squeeze_factor: A positive real value. Determines how vertically squeezed you want the paraboloid to be.
                    1 leads to a symmetric function, 10 leads to pretty heavy squeezing, 0.1 to vertical stretching.
                    Default is 3.
    lrate:          The learning rate. Some constant by which you scale your gradient update. Smaller rates are less
                    prone to oscillation but lead to slower convergence. Consider keeping them in the interval (0,1].
                    Default is 0.5.
    delay:          Delay of the run in milliseconds. Default is 1000.
"""
def oblong_paraboloid(squeeze_factor=3,lrate=0.5,delay=1000):
    fig, ax = plt.subplots()
    line, = ax.plot([], [], lw=2,marker='s',markerfacecolor='red')

    cos = np.array([np.cos(i*0.01) for i in xrange(700)])
    number = 1.0/squeeze_factor
    sin = number*np.array([np.sin(i*0.01) for i in xrange(700)])
    ax.set_ylim(-5, 5)
    ax.set_xlim(-5,5)
    for i in xrange(1,int(5*max(squeeze_factor,1/squeeze_factor)),3):
        ax.plot(i*cos,i*sin)
    ax.grid()
    xdata, ydata = [3+random()], [3+random()]

    print "Gradient descent for the function z = x^2+{0}*y^2".format(squeeze_factor)

    def run(i):
        # update the data
        t,y = xdata[-1]*(1-lrate),ydata[-1]*(1-squeeze_factor*lrate)
        xdata.append(t)
        ydata.append(y)
        xmin, xmax = ax.get_xlim()

        if t >= xmax:
            ax.set_xlim(xmin, 2*xmax)
            ax.figure.canvas.draw()
        line.set_data(xdata, ydata)

        return line,

    ani = animation.FuncAnimation(fig, run, 100,  blit=True, interval=delay,
        repeat=False)
    plt.show()


if __name__ == "__main__":
    _,squeeze_factor,lrate,delay = sys.argv
    oblong_paraboloid(float(squeeze_factor),float(lrate),int(delay))

