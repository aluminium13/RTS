from random import randint
from math import sin
import matplotlib.pyplot as plt
# number of harmonicas in signal
n = 10
# limit of frequency
wlim = 1500
# number of discrete countdown
N = 256


def x(t):
    return sum(A[p]*sin(wp[p]*t + phi[p]) for p in range(0, n))


def mathExp(x, N):
    return sum(x)/N


def dispersion(x, mx, N):
    return sum([(xi - mx)**2 for xi in x])/(N- 1)


if __name__ == "__main__":

   print("Laboratory Work 1")

   A = [randint(-10, 10) for _ in range(n)]
   phi = [randint(0, 10) for _ in range(n)]
   wp = [randint(0, wlim) for _ in range(n)]

   k = 3
   f = 100
   dt = 1/(k * f)

   Mx = []
   Dx = []
   Nlist = list(range(300,400))
   
   for N in Nlist:   
      tk = [dt * i for i in range(N)]
      xlist = [x(t) for t in tk]

      mx = mathExp(xlist, N)
      Mx.append(mx)
   #  print("Math Exp: ", Mx)
      Dx.append(dispersion(xlist, mx, N))
   #  print("Dispersion: ", Dx)
   
   print("mX", Mx)
   print("Dx", Dx)

   # fig, ax = plt.subplots()
   # ax.plot(tk, x)

   # ax.set(xlabel='discrete time', ylabel='x(t)',
   #     title='Mx={}\nDx={}'.format(Mx, Dx))

   # plt.show()