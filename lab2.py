import matplotlib.pyplot as plt
import numpy as np
from random import randint, uniform
from math import sin, pi

n = 10
N = 256
wlim = 1500


def gen_wave(t, A, phi):
    return sum(A[i] * sin(wp[i] * t + phi[i]) for i in range(0, n))


def me(x):
    return sum(x)/len(x)


def ds(x, mx):
    return sum((xi - mx)**2 for xi in x)/(N - 1)


if __name__ == '__main__':

    wp = [(wlim / n) * i for i in range(1, n + 1)]

    Ax = [randint(0, 100) for _ in range(n)]
    phix = [randint(0, 100) for _ in range(n)]

    Ay = [randint(-10, 10) for _ in range(n)]
    phiy = [randint(0, 10) for _ in range(n)]

    waveX = [gen_wave(i, Ax, phix) for i in range(N)]
    mx = me(waveX)
    dx = ds(waveX, mx)

    waveY = [gen_wave(i, Ay, phiy) for i in range(N)]
    my = me(waveY)
    dy = ds(waveY, my)

    half = int(N/2)
    rxx = [sum((waveX[t] - mx)*(waveX[t+tau] - mx)
               for t in range(half))/(half - 1)/dx for tau in range(half)]
    ryy = [sum((waveY[t] - my)*(waveY[t+tau] - my)
               for t in range(half))/(half - 1)/dy for tau in range(half)]
    rxy = [sum((waveX[t] - mx)*(waveY[t+tau] - my)
               for t in range(half))/(half - 1)/(dy + dx)/2 for tau in range(half)]

    xnp = np.array(waveX)
    normx = np.sum((xnp-np.mean(xnp))**2)/(N-1)

    ynp = np.array(waveY)
    normy = np.sum((ynp-np.mean(ynp))**2)/(N-1)

    corrX = np.correlate(xnp, xnp, mode='same')/normx
    corrX = corrX[half:]

    corrY = np.correlate(ynp, ynp, mode='same')/normy
    corrY = corrY[half:]

    corrXY = np.correlate(xnp, ynp, mode='same')/((normx+normy)/2)
    corrXY = corrXY[half:]

    resXX, resYY, resXY = [], [], []
    for i in range(half):
        resXX.append(abs(abs(rxx[i]) - abs(corrX[i]))/100)
        resYY.append(abs(abs(ryy[i]) - abs(corrY[i]))/100)
        resXY.append(abs(abs(rxy[i]) - abs(corrXY[i]))/100)

    fig, axes = plt.subplots(3, 1)
    axes[0].plot(resXX)
    axes[1].plot(resYY)
    axes[2].plot(resXY)
    plt.show()
