import random
import scipy.stats as stats
import matplotlib.pyplot as plt
import time


def mean(x):
    if len(x) == 0:
        return -1
    return sum(x) / len(x)


class Messages:
    def __init__(self, lam, T, M, r=0.2, o=0.01):
        """
        Initialize the messages and stations.

        Parameters:
            lam (float): the arrival rate of messages
            T (int): the number of time slots
            M (int): the number of stations
            r (float, optional): the range of variation in message generation time
            o (float, optional): the base message generation time

        Returns:
            None
        """
        self.lam = lam
        self.T = T
        self.M = M
        stations_messages = [[] for _ in range(self.M)]
        self.generated_time = [[] for _ in range(self.M)]
        self.arrival_time = [[] for _ in range(self.M)]
        self.message_num = 0
        for i in range(self.M):
            stations_messages[i] = stats.poisson.rvs(self.lam / self.M, size=self.T).tolist()
        for i in range(self.M):
            for j in range(self.T):
                for _ in range(stations_messages[i][j]):
                    self.generated_time[i].append(j * o + random.uniform(-r, r))
                    self.generated_time[i][-1] = max(self.generated_time[i][-1], random.uniform(0, o))
            self.generated_time[i].sort()
            self.message_num += len(self.generated_time[i])

    def __str__(self):
        return f'{self.M=} {self.T=}\n{self.generated_time=}\n{self.arrival_time=}\n'

    def get_generated_time(self, m):
        return self.generated_time[m]

    def add_arrival_time(self, m, t):
        self.arrival_time[m].append(t)

    def get_sent_num(self):
        return sum([len(i) for i in self.arrival_time])

    def get_delay(self):
        res = []
        for i in range(self.M):
            for j in range(len(self.arrival_time[i])):
                res.append(self.arrival_time[i][j] - self.generated_time[i][j])
        return res


class Channel:
    def __init__(self, M, time_interval):
        self.M = M
        self.time_interval = time_interval
        self.timeline = -1
        self.using = -1
        self.abonent_on_timeline = None

    def __str__(self):
        return f'{self.timeline=}'

    def new_message(self, m: int, t: float) -> list:
        if self.timeline <= t:
            res = [self.timeline, self.abonent_on_timeline, self.using == 1]
            self.timeline = t + self.time_interval
            self.using = 1
            self.abonent_on_timeline = m
        else:
            self.using += 1
            res = [self.timeline, self.abonent_on_timeline, self.using == 1]
            self.timeline = t + self.time_interval
            self.using = 2
            self.abonent_on_timeline = m
        return res


class Queue:
    def __init__(self, time_interval):
        self.time_interval = time_interval
        self.data = []

    def __str__(self):
        return f'{self.data=}'

    def add(self, i: float):
        self.data.append(i)

    def append(self, i: list):
        self.data.extend(i)
        self.optimize_queue()

    def add_move(self, i: float):
        self.data.append(i + random.uniform(0, self.time_interval * 10))
        self.data.sort()

    def pop(self):
        return self.data.pop(0)

    def get(self):
        if len(self.data) == 0:
            return 999_999_999
        return self.data[0]

    def optimize_queue(self):
        for i in range(len(self.data) - 1):
            if self.data[i + 1] - self.data[i] < self.time_interval:
                self.data[i + 1] = self.data[i] + self.time_interval
        self.data.sort()


class Simulation:
    def __init__(self, lam, T, M, r=0.2, time_interval=0.01):
        self.lam = lam
        self.T = T
        self.M = M
        self.r = r
        self.time_interval = time_interval

        self.messages = Messages(lam, T, M, r, time_interval)
        self.channel = Channel(M, time_interval)
        self.queues = [Queue(time_interval) for _ in range(M)]
        self.collisions = 0
        self.time = 0

    def __str__(self):
        return (f'{self.messages=}\n{self.channel=}\n{self.queues=}\n'
                f'\n{self.collisions=}\n{self.time=}\n')

    def run(self):
        for i in range(self.M):
            self.queues[i].append(self.messages.get_generated_time(i))
        while self.time < self.T * self.time_interval * 2:
            if self.messages.message_num == self.messages.get_sent_num():
                break

            # находим время, минимальное время из очередей
            t_min = min([i.get() for i in self.queues])
            if t_min < self.time + self.time_interval:
                self.time = t_min
            else:
                self.time += self.time_interval

            # добавляем сообщения из очереди готовые к отправке в канал
            data = []
            for i in range(self.M):
                if self.queues[i].get() <= self.time:
                    data.append(self.channel.new_message(i, self.time))
                    self.queues[i].pop()

            # проверяем можем ли отправить сообщение
            for el in data:
                if el[2]:
                    self.messages.arrival_time[el[1]].append(el[0])
                elif el[1] is not None:
                    self.queues[el[1]].add_move(self.time)
                    self.collisions += 1

        return (mean(self.messages.get_delay()), self.messages.get_sent_num(), self.time, self.collisions,
                self.messages.message_num)


def draw(T, M, lam, r=0.2, time_interval=0.01):
    x = [i / 100 for i in range(1, 35)]
    temp = []
    print("Simulation start")
    start_time = time.time()
    for i in x:

        print("\r", end="")
        print(f"Current progress: {int(x.index(i) / len(x) * 100)}%\ttime: {time.time() - start_time}", end="")
        s = Simulation(i, T, M, r, time_interval)
        temp.append(s.run())
    print("\r", end="")
    print(f"Current progress: 100%\ttime: {time.time() - start_time}", end="")
    print("\nSimulation end")

    plt.figure(0)
    plt.plot(x, [i[0] for i in temp], label=f"{M=}")
    plt.grid(True)
    plt.legend()
    plt.xlabel("Интенсивность входного потока")
    plt.ylabel("Среднее время задержки")
    plt.savefig(f"graphics/ALOHAas_M_D{M}.png")

    plt.figure(1)
    plt.plot(x, [i[1] for i in temp], label=f"{M=}")
    plt.grid(True)
    plt.legend()
    plt.xlabel("Интенсивность входного потока")
    plt.ylabel("Количество отправленных сообщений")
    plt.savefig(f"graphics/ALOHAas_sent{M}.png")

    plt.figure(2)
    plt.plot(x, [i[3] for i in temp], label=f"{M=}")
    plt.grid(True)
    plt.legend()
    plt.xlabel("Интенсивность входного потока")
    plt.ylabel("Количество коллизий")
    plt.savefig(f"graphics/ALOHAas_col{M}.png")

    plt.figure(3)
    plt.plot(x, [i[1] / T for i in temp], label=f"{M=}")
    plt.grid(True)
    plt.legend()
    plt.xlabel("Интенсивность входного потока")
    plt.ylabel("Интенсивность выходного потока")
    plt.savefig(f"graphics/ALOHAas_lam{M}.png")

    plt.figure(4)
    plt.plot(x, [i[4] for i in temp], label=f"{M=}")
    plt.grid(True)
    plt.legend()
    plt.xlabel("Интенсивность входного потока")
    plt.ylabel("Количество созданных сообщений")
    plt.savefig(f"graphics/ALOHAas_created{M}.png")


if __name__ == '__main__':
    for i in range(1, 17, 3):
        draw(1000, i, 0.5, 0.2, 0.1)
