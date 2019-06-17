import numpy as np
import matplotlib.pyplot as plt
from math import sin, pi, cos
from random import uniform

n = 10
w = 1500
N = 256
wp = [w/n * i for i in range(1, n+1)]

def genwave():
    A = [uniform(0, 6) for _ in range(n)]
    phi = [uniform(0, pi*2) for _ in range(n)]
    return [sum(A[i] * sin(wp[i] * t + phi[i]) for i in range(n)) for t in range(N)]

def digitreversal(xarray, radix, log2length, length):
    '''
    digitreversal
    '''
    if log2length % 2 == 0:
        n1var = int(np.sqrt(length))  # seed table size
    else:
        n1var = int(np.sqrt(int(length/radix)))
    # algorithm 2,  compute seed table
    reverse = np.zeros(n1var, dtype=int)
    reverse[1] = int(length/radix)
    for jvar in range(1, radix):
        reverse[jvar] = reverse[jvar-1]+reverse[1]
        for i in range(1, int(n1var/radix)):
            reverse[radix*i] = int(reverse[i]/radix)
            for jvar in range(1, radix):
                reverse[int(radix*i)+jvar] = reverse[int(radix*i)] + \
                    reverse[jvar]
    # algorithm 1
    for i in range(0, n1var-1):
        for jvar in range(i+1, n1var):
            uvar = i+reverse[jvar]
            vvar = jvar+reverse[i]
            xarray[uvar], xarray[vvar] = xarray[vvar], xarray[uvar]
            if log2length % 2 == 1:
                for zvar in range(1, radix):
                    uvar = i+reverse[jvar]+(zvar*n1var)
                    vvar = jvar+reverse[i]+(zvar*n1var)
                    xarray[uvar], xarray[vvar] = xarray[vvar], xarray[uvar]
    return xarray


def fft4(xarray, twiddles, svar):
    '''
    radix-4 dit fft
    '''
    nvar = 4
    tss = int(np.power(4, svar-1))
    krange = 1
    block = int(N/4)
    base = 0
    for _ in range(0, svar):
        for _ in range(0, block):
            for kvar in range(0, krange):
                # butterfly
                offset = int(nvar/4)
                avar = int(base+kvar)
                bvar = int(base+kvar+offset)
                cvar = int(base+kvar+(2*offset))
                dvar = int(base+kvar+(3*offset))
                if kvar == 0:
                    xbr1 = xarray[bvar]
                    xcr2 = xarray[cvar]
                    xdr3 = xarray[dvar]
                else:
                    r1var = twiddles[int(kvar*tss)]
                    r2var = twiddles[int(2*kvar*tss)]
                    r3var = twiddles[int(3*kvar*tss)]
                    xbr1 = (xarray[bvar]*r1var)
                    xcr2 = (xarray[cvar]*r2var)
                    xdr3 = (xarray[dvar]*r3var)
                evar = xarray[avar]+xcr2
                fvar = xarray[avar]-xcr2
                gvar = xbr1+xdr3
                hvar = xbr1-xdr3
                j_h = 1j*hvar
                xarray[avar] = evar+gvar
                xarray[bvar] = fvar-j_h
                xarray[cvar] = -gvar+evar
                xarray[dvar] = j_h+fvar
            base = base+(4*krange)
        block = int(block/4)
        nvar = 4*nvar
        krange = 4*krange
        base = 0
        tss = float(tss)/4.
    return xarray


def built_fft(x):
    return np.absolute(np.fft.fft(x))

if __name__ == "__main__":
    fig, (a1, a2, a3) = plt.subplots(3, 1, sharey=False)    
    y = genwave()    
    gg = built_fft(y)
    svar = 4
    kmax = 3*((float(N)/4.)-1)
    k_wavenumber = np.linspace(0, kmax, kmax+1)
    twiddlefactors = np.exp(-2j*np.pi*k_wavenumber/N)
    y = digitreversal(y, 4, svar, N)
    a1.plot(list(y))
    a1.set_ylabel('Y')
    a2.bar(list(range(N)), np.absolute(fft4(y, twiddlefactors, svar)))
    a2.set_ylabel('radix-4 dit')
    a3.bar(list(range(N)), gg)
    a3.set_ylabel('numpy')
    plt.show()
