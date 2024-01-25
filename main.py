import numpy as np
import math
import random
import matplotlib.pyplot as plt


def exp(la):
    return -math.log(random.random()) / la


def Poisson(la):
    s = 0.0
    k = -1
    while True:
        s += exp(1)
        k += 1
        if not s < la:
            break
    return k


def Time_sharing(ax1, ax2, ax3, la, M):
    Mn = np.zeros(la.size)
    Md = np.zeros(la.size)
    Me = np.zeros(la.size)
    Ml = np.zeros(la.size)

    for l in la:
        Nsum = 0
        Dsum = 0
        Ssum = 0
        Esum = 0
        Subs = np.zeros(M)
        queue = np.zeros(M)
        k = 0
        for window in range(time):
            for i, _ in enumerate(Subs):
                Subs[i] = Poisson(l / M)
                for s in range(int(Subs[i])):
                    Dsum += random.random()
                    Ssum += 1
            if queue[k] != 0:
                queue[k] -= 1
                Esum += 1
            for i, sub in enumerate(Subs):
                queue[i] += sub
                Nsum += queue[i]
                Dsum += queue[i]
            k = (k + 1) % M
        Mn[np.where(la == l)] = Nsum / time
        Md[np.where(la == l)] = Dsum / Ssum if Ssum != 0 else 1
        Me[np.where(la == l)] = Esum / time
        Ml[np.where(la == l)] = Ssum / time

    ax1.plot(la, Mn, label="M[N]")
    ax2.plot(la, Md, label="M[D]")
    ax3.plot(la, Me, label="Lвых")
    ax3.plot(la, Ml, label="Lпракт")


def On_reqest(ax1, ax2, ax3, la, ty, M):
    Mn = np.zeros(la.size)
    Md = np.zeros(la.size)
    Me = np.zeros(la.size)
    Ml = np.zeros(la.size)
    for l in la:
        Nsum = 0
        Dsum = 0
        Ssum = 0
        Esum = 0
        Subs = np.zeros(M, dtype=int)
        queue = np.zeros(M)
        k = 0
        for window in range(time):
            h = np.zeros(M, dtype=int)
            for i, _ in enumerate(Subs):
                Subs[i] = Poisson((l * ty) / M)
                for s in range(Subs[i]):
                    Dsum += random.uniform(0.0, ty)
                    Ssum += 1
            if queue[k] != 0:
                queue[k] -= 1
                for j, q in enumerate(queue):
                    Dsum += q
                    h[j] = Poisson(l / M)
                    Dsum += random.random()
                    Ssum += h[j]
                Esum += 1
            for i, sub in enumerate(Subs):
                queue[i] += sub
                Dsum += queue[i] * ty
                queue[i] += h[i]
                Nsum += queue[i]
            k = (k + 1) % M
        Mn[np.where(la == l)] = Nsum / ((time) * ty + Esum)
        Md[np.where(la == l)] = Dsum / Ssum if Ssum != 0 else 1
        Me[np.where(la == l)] = Esum / ((time) * ty + Esum)
        Ml[np.where(la == l)] = Ssum / ((time) * ty + Esum)

    ax1.plot(la, Mn, label="M[N]req")
    ax2.plot(la, Md, label="M[D]req")
    ax3.plot(la, Me, label="Lвыхreq")
    ax3.plot(la, Ml, label="Lпрактreq")


la = np.arange(0.001, 1.5, 0.1)
M = int(input("Enter M = "))
ty = float(input("Enter ty = "))
time = 10000

fig1, ax1 = plt.subplots()
fig2, ax2 = plt.subplots()
fig3, ax3 = plt.subplots()

Time_sharing(ax1, ax2, ax3, la, M)
On_reqest(ax1, ax2, ax3, la, ty, M)

ax1.set_ylim([0, 10])
ax1.grid()
ax1.legend()
ax2.set_ylim([0, 10])
ax2.grid()
ax2.legend()
ax3.grid()
ax3.legend()
plt.show()