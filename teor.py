import random
import matplotlib.pyplot as plt

lam = 0.5
mu = 1


def n_average(lam):
    return (lam * (2 - lam)) / (2 * (1 - lam))


def d_average_async(lam):
    return n_average(lam) / (1 - lam)


def d_average_sync(lam):
    return (n_average(lam) / (1 - lam)) + 0.5


# draw graphic
x = []
y = []
N = 25
for i in range(N):
    i = i / N
    x.append(i)
    y.append(n_average(i))

plt.plot(x, y)
plt.xlabel('lambda')
plt.ylabel('n_average')
plt.title('График зависимости n_average от lambda')
plt.savefig('teor_n.png')
plt.close()

x = []
y = []
N = 10
for i in range(N):
    i = i / N
    x.append(i)
    y.append(d_average_sync(i))
plt.plot(x, y, color='r', label='sync')
x = []
y = []
for i in range(N):
    i = i / N
    x.append(i)
    y.append(d_average_async(i))
plt.plot(x, y, color='b', label='async')
plt.legend()
plt.xlabel('lambda')
plt.ylabel('d_average')
plt.title('График зависимости d_average от lambda')
plt.savefig('teor_d.png')
plt.show()


