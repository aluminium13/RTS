import matplotlib.pyplot as plt
import numpy as np
from math import sin, pi, cos
from random import uniform
from time  import time

n = 10
w = 1500
N = 256
wp = [w/n * i for i in range(1, n+1)]


def genwave(N):
    A = [uniform(0, 6) for _ in range(n)]
    phi = [uniform(0, pi*2) for _ in range(n)]
    return [sum(A[i] * sin(wp[i] * t + phi[i]) for i in range(n)) for t in range(N)]


def DFT_slow(x, N):
    """Compute the discrete Fourier Transform of the 1D array x"""
    x = np.asarray(x, dtype=float)
    N = x.shape[0]
    n = np.arange(N)
    k = n.reshape((N, 1))
    M = np.exp(-2j * np.pi * k * n / N)
    return np.dot(M, x)


def FFT(x, N):
    """A recursive implementation of the 1D Cooley-Tukey FFT"""
    x = np.asarray(x, dtype=float)
    N = x.shape[0]

    if N % 2 > 0:
        raise ValueError("size of x must be a power of 2")
    elif N <= 32:  # this cutoff should be optimized
        return DFT_slow(x, N)
    else:
        X_even = FFT(x[::2], N)
        X_odd = FFT(x[1::2], N)
        factor = np.exp(-2j * np.pi * np.arange(N) / N)
        return np.absolute(np.concatenate([X_even + factor[:int(N / 2)] * X_odd, X_even + factor[int(N / 2):] * X_odd]))

def my_fft(x, N):

    if N % 2 > 0:
        raise ValueError("size of x must be a power of 2")
    else:
        fp = []
        for p in range(N-1):
            fp.append(sum(x[k]*np.exp(-1j*2*pi*p*k/N) for k in range(N-1)))
    return fp

def built_fft(x, N):
    return np.fft.fft(x)

def table(x,N):
    dictionary = {}
    re = [0 for i in range(N-1)]
    lm = [0 for i in range(N-1)]

    for i in range(N):
        dictionary[i] = (cos(2*pi/N*i), sin(2*pi/N*i))
   
if __name__ == '__main__':
    # fig, (a1, a2) = plt.subplots(2, 1, sharey=False)
    # a1.plot(list(y))
    # a1.set_ylabel('Y')
    # a2.bar(list(range(N)), FFT(y))
    # a2.set_ylabel('FFT(Y)')
    # plt.show()
    timeDFT, timeTable, timeFFT, timeNP = [], [], [], []
    scale = []
    for exp in range(7,14):
        scale.append(exp)

        N = 2 ** exp
        y = genwave(N)
        
        a = time()
        my_fft(y, N)
        b = time()
        curr = b -a 

        a = time()
        table(y, N)
        b = time()
        timeTable.append((b-a)/curr)

        print(timeTable)
        a = time()
        FFT(y, N)
        b = time()
        timeFFT.append((b-a)/curr)

        a = time()
        built_fft(y, N)
        b = time()
        timeNP.append((b-a)/curr)

    fig, a1 = plt.subplots(1, 1, sharey=False)
    a1.plot(timeTable)
    a1.plot(timeFFT)
    a1.plot(timeNP)

    plt.show()