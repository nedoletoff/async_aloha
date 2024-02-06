import random
import scipy.stats as stats
import matplotlib.pyplot as plt

from main import fact


class Messages:
    def __init__(self, M, T, stock=0):
        self.moved = False
        self.delay = []
        self.M = M
        self.T = T
        self.arr = [[[0] for _ in range(M)] for _ in range(T + stock + 1)]
        self.size = 0

    def __str__(self):
        return f'{self.M=} {self.T=}\n{self.arr}\n'

    def callculate(self) -> int:
        self.size = 0
        for i in range(self.T):
            for j in range(self.M):
                self.size += self.arr[i][j]
                for _ in range(self.arr[i][j]):
                    self.delay.append(i)
        return self.size

    def get(self, m: int, t: int) -> int:
        return self.arr[t][m]

    def set(self, m: int, t: int, val: int):
        self.arr[t][m] = val

    def move(self, m: int, t: int):
        self.moved = True
        self.arr[t + 1][m] += self.arr[t][m]
        self.set(m, t, 0)

    def inc(self, m: int, t: int):
        self.arr[t][m] += 1

    def dec(self, m: int, t: int):
        self.arr[t][m] -= 1
        self.moved = False
        return self.delay.pop(0)

    def len(self):
        return self.size

    def poisson(self, lam: float):
        for i in range(self.T):
            for j in range(self.M):
                self.arr[i][j] = stats.poisson.rvs(lam / self.M, size=1)[0]
                #if self.arr[i][j] > 1:
                #    self.arr[i][j] = 1
                # print(f'{i=} {j=} {self.arr[i][j]=}')


def simulate(M, lam, T, p_ab=0.3, optional=False):
    """
    Simulates a system with M users.

    Args:
    M (int): Number of users
    lambda (float): Arrival rate
    T (int): Simulation time

    Returns:
    (float, float): Average delay, average number of users
    """
    if M <= 0:
        raise ValueError("M must be positive")
    # Initialize the system
    n_message = Messages(M, T, stock=T * 10)
    t = -1
    # Generate random number of arrivals for each user
    n_message.poisson(lam)
    # print(n_message)
    message_num = n_message.callculate()
    n_arrived = 0
    delay = []
    l_of_arr = []

    # Simulation loop
    while n_arrived != message_num and t < T*10:
    #while t != 1000:
        t += 1
        busy = 0
        l_of_arr.clear()
        # Check if there are any arrivals
        for user in range(M):
            if n_message.get(user, t) > 0:
                if optional and not n_message.moved:
                    busy += 1
                    l_of_arr.append(user)
                elif random.random() < p_ab:
                    busy += 1
                    l_of_arr.append(user)
        # Process any arrivals that have arrived
        if busy == 1:
            n_arrived += 1
            d = n_message.dec(l_of_arr[0], t)
            delay.append(t - d)
        # Move rest of messages
        for user in range(M):
            try:
                n_message.move(user, t)
            except:
                print(f'{message_num}')
                print(n_arrived)
                print(f'{user=} {t=}')
                break

    # Calculate the average delay and number of users
    # T = t
    MD = 0
    if len(delay) != 0:
        MD = sum(delay) / len(delay)
    MN = message_num - n_arrived
    print(f'{MD=}, {MN=}')
    print(f'{n_arrived=}, {message_num=}, {T=}, {t=}, {M=}, {lam=}, {p_ab=}')
    la = n_arrived / T
    return MD, MN, la


def calculate(M, x, T, p_ab=0.3, optional=False):
    res = []
    for i in x:
        res.append(simulate(M, i, T, p_ab, optional))
    md = []
    mn = []
    la = []
    for i in res:
        md.append(i[0])
        mn.append(i[1])
        la.append(i[2])
    return md, mn, la


if __name__ == "__main__":
    x = [i / 10 for i in range(1, 10)]
    #x += [2, 3, 5, 10]

    plt.figure(1)
    md, mn, la = calculate(10, x, 1000, 0.32, False)
    plt.plot(x, md)
    plt.title("ALOHA M[D]")
    plt.xlabel("lambda")
    plt.ylabel("Среднее время задержки")
    plt.savefig("ALOHA_M_D.png")

    plt.figure(2)
    plt.title("ALOHA M[N]")
    plt.plot(x, mn)
    plt.grid()
    plt.xlabel("lambda")
    plt.ylabel("Среднее значение количество абонентов в очереди")
    plt.savefig("ALOHA_M_N.png")

    plt.figure(0)
    plt.title("lam выходной")
    plt.plot(x, la)
    plt.grid()
    plt.xlabel("Интенсивность входного потока")
    plt.ylabel("Интенсивность выходного потока")
    plt.savefig("lam_выходной.png")

    plt.figure(3)
    plt.title("Выходной от вероятности передачи")
    p = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
    la_v = []
    for i in p:
        _, _, la = simulate(1, 0.5, 1000, i, False)
        la_v.append(la)
    plt.plot(p, la_v)
    plt.grid()
    plt.xlabel("p передачи")
    plt.ylabel("Интенсивность выходного потока")
    plt.savefig("Выходной_от_вероятности_передачи.png")
'''
    plt.figure(3)
    md, mn, la = calculate(10, x, 1000, 0.32, True)
    plt.title("Optional ALOHA M[D]")
    plt.plot(x, md)
    plt.grid()
    plt.xlabel("lambda")
    plt.ylabel("Среднее время задержки")
    plt.savefig("Optional_ALOHA_M_D.png")

    plt.figure(4)
    plt.title("Optional ALOHA M[N]")
    plt.plot(x, mn)
    plt.grid()
    plt.xlabel("lambda")
    plt.ylabel("Среднее значение количество абонентов в очереди")
    plt.savefig("Optional_ALOHA_M_N.png")
'''