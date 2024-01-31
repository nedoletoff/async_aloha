import random
import math
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
    while n_arrived != message_num:
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
    MD = sum(delay) / len(delay)
    MN = n_arrived / T
    print(f'{MD=}, {MN=}')
    print(f'{n_arrived=}, {message_num=}, {T=}, {t=}, {M=}, {lam=}, {p_ab=}')
    return MD, MN


def calculate(M, x, T, p_ab=0.3, optional=False):
    res = []
    for i in x:
        res.append(simulate(M, i, T, p_ab, optional))
    md = []
    mn = []
    for i in res:
        md.append(i[0])
        mn.append(i[1])
    return md, mn


if __name__ == "__main__":
    x = [i / 20 for i in range(1, 20)]

    plt.figure(1)
    md, mn = calculate(10, x, 1000, 0.32, False)
    plt.plot(x, md)
    plt.title("ALOHA M[D]")
    plt.xlabel("lambda")
    plt.ylabel("Среднее время задержки")
    plt.savefig("ALOHA_M_D.png")

    plt.figure(2)
    plt.title("ALOHA M[N]")
    plt.plot(x, mn)
    plt.xlabel("lambda")
    plt.ylabel("M[N]")
    plt.savefig("ALOHA_M_N.png")

    plt.figure(3)
    md, mn = calculate(10, x, 1000, 0.32, True)
    plt.title("Optional ALOHA M[D]")
    plt.plot(x, md)
    plt.xlabel("lambda")
    plt.ylabel("Среднее время задержки")
    plt.savefig("Optional_ALOHA_M_D.png")

    plt.figure(4)
    plt.title("Optional ALOHA M[N]")
    plt.plot(x, mn)
    plt.xlabel("lambda")
    plt.ylabel("M[N]")
    plt.savefig("Optional_ALOHA_M_N.png")
