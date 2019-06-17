import matplotlib.pyplot as plt
import numpy as np
from random import randint, uniform
from math import sin, cos, pi, sqrt
import time

n = 10
N = 256
wlim = 1500


def gen_wave():
    wp   = [(wlim / n) * i for i in range(1, n + 1)]
    A = [uniform(0, 6) for _ in range(n)]
    phi = [uniform(0, pi*2) for _ in range(n)]
    return [sum(A[i] * sin(wp[i] * t + phi[i]) for i in range(n)) for t in range(N)]


def my_fft(x):

    if N % 2 > 0:
        raise ValueError("size of x must be a power of 2")
    else:
        fp = []
        for p in range(N-1):
            fp.append(sum(x[k]*np.exp(-1j*2*pi*p*k/N) for k in range(N-1)))
    return fp

def built_fft(x):
    return np.fft.fft(x)

if __name__ == '__main__':
    
    waveX =gen_wave()

    Mx = sum(waveX)/N
    Dx = sum((waveX[i] - Mx)**2 for i in range(N))/(N-1)

    re, im = [], []

    c = time.clock()

    for p in range(N-1):
        re.append(sum([waveX[k] * cos(2*pi/N *p *k) for k in range(N-1)]))
        im.append(sum([waveX[k] * sin(2*pi/N *p *k) for k in range(N-1)]))
    f = [sqrt(re[p]**2 + im[p]**2) for p in range(N-1)]

    d = time.clock()

    print("Time for standart: ",d-c)

    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, sharex=True)

    dictionary = {}
    re = [0 for i in range(N-1)]
    lm = [0 for i in range(N-1)]

    for i in range(N):
        dictionary[i] = (cos(2*pi/N*i), sin(2*pi/N*i))

    a = time.clock()

    for p in range(N-1):
        for k in range(N-1):
            re[p] += waveX[k] * dictionary[p*k%N][0]
            lm[p] += waveX[k] * dictionary[p*k%N][1]

    f1 = []

    for i in range(N-1):
        f1.append(sqrt(re[i]**2 + lm[i]**2))
    b = time.clock()   
    print("Time for table: ",b-a)


    ax1.plot(list(range(N)), waveX)
    ax1.set_xlim([0, N])
    ax1.set_title('Mx = {}, Dx = {}'.format(Mx, Dx))
    ax1.set_ylabel('x(t)')
    ax2.bar(list(range(N-1)), f)
    ax3.bar(list(range(N-1)), f1)

    plt.show()

    # waveX = gen_wave()
        
    # fig, axes = plt.subplots(3, 1)

    # axes[0].plot(waveX)
    # axes[0].set_ylabel('x(t)')
    # axes[0].grid(True)
    # axes[1].plot(my_fft(waveX))
    # axes[1].set_ylabel('My spectre')
    # axes[1].grid(True)
    # axes[2].plot(built_fft(waveX))
    # axes[2].set_ylabel('Module spectre')
    # axes[2].grid(True)

    # plt.show()
