import matplotlib.pyplot as plt
from clear_aloha import Simulation

lam = 0.9
T = 1000
M = 3
r = 0.2
time_interval = 0.001
x = [i / 10 for i in range(1, 15)]
temp = []
for i in x:
    s = Simulation(i, T, M, r, time_interval)
    temp.append(s.run())

plt.figure(0)
plt.plot(x, [i[0] for i in temp])
plt.grid()
plt.xlabel("Интенсивность входного потока")
plt.ylabel("Среднее время задержки")
plt.savefig("ALOHAas_M_D.png")

plt.figure(1)
plt.plot(x, [i[1] for i in temp])
plt.grid()
plt.xlabel("Интенсивность входного потока")
plt.ylabel("Количество отправленных сообщений")
plt.savefig("ALOHAas_sent.png")

plt.figure(2)
plt.plot(x, [i[3] for i in temp])
plt.grid()
plt.xlabel("Интенсивность входного потока")
plt.ylabel("Количество коллизий")
plt.savefig("ALOHAas_col.png")

plt.figure(3)
plt.plot(x, [i[1] / T for i in temp])
plt.grid()
plt.xlabel("Интенсивность входного потока")
plt.ylabel("Интенсивность выходного потока")
plt.savefig("ALOHAas_lam.png")

x = [i for i in range(1, 10)]
temp = []
for i in x:
    s = Simulation(lam, T, i, r, time_interval)
    temp.append(s.run())

plt.figure(4)
plt.plot(x, [i[3] for i in temp])
plt.grid()
plt.xlabel("Количество абонентов")
plt.ylabel("Количество коллизий")
plt.savefig("ALOHAas_col2.png")

plt.figure(5)
plt.plot(x, [i[0] for i in temp])
plt.grid()
plt.xlabel("Количество абонентов")
plt.ylabel("Среднее время задержки")
plt.savefig("ALOHAas_M_D2.png")

plt.figure(6)
plt.plot(x, [i[1] for i in temp])
plt.grid()
plt.xlabel("Количество абонентов")
plt.ylabel("Количество отправленных сообщений")
plt.savefig("ALOHAas_sent2.png")
