import random
import scipy.stats as stats
import matplotlib.pyplot as plt


def mean(x):
    return sum(x) / len(x)


class Messages:
    def __init__(self, lam, T, M, r=0.2, o=0.01, time_interval=0.01):
        """
        Initialize the simulation environment with the given parameters.

        Parameters:
            lam (float): The arrival rate of messages at the system.
            T (int): The number of time slots in the simulation.
            M (int): The number of stations in the system.
            r (float, optional): The range of random variation in message generation time. Defaults to 0.2.
            o (float, optional): The time interval between message generation. Defaults to 0.01.
        """
        self.delay = []
        self.lam = lam
        self.T = T
        self.M = M
        self.stations_messages = [[] for _ in range(self.M)]
        self.generated_time = [[] for _ in range(self.M)]
        self.arrival_time = [[] for _ in range(self.M)]
        self.queue = [[] for _ in range(self.M)]
        self.counters = [0 for _ in range(self.M)]
        self.message_num = 0
        self.sent_num = 0
        self.time_interval = time_interval
        self.queue_added = [0 for _ in range(self.M)]
        for i in range(self.M):
            self.stations_messages[i] = stats.poisson.rvs(self.lam / self.M, size=self.T).tolist()
        for i in range(self.M):
            for j in range(self.T):
                for _ in range(self.stations_messages[i][j]):
                    self.generated_time[i].append(j * o + random.uniform(-r, r))
                    self.generated_time[i][-1] = max(self.generated_time[i][-1], random.uniform(0, o))
            self.generated_time[i].sort()
            self.message_num += len(self.generated_time[i])

    def __str__(self):
        return f'{self.M=} {self.T=}\n{self.arrival_time=}\n{self.queue=}\n{self.counters=}\n{self.generated_time=}\n'

    def send_message(self, m, t):
        self.arrival_time[m].append(t)
        self.queue[m].pop(0)
        self.queue_added[m] = 0
        self.sent_num += 1

    def add_to_queue(self, m, i):
        self.queue[m].append(self.generated_time[m][i])
        self.counters[m] += 1

    def get_queue(self, m):
        return self.queue[m]

    def get_queue_size(self, m):
        return len(self.queue[m])

    def get_message_time(self, m):
        return self.generated_time[m][self.counters[m]]

    def get_generated_time(self, m):
        return self.generated_time[m]

    def get_count(self, m):
        return self.counters[m]

    def is_end_count(self, m):
        return self.counters[m] == len(self.generated_time[m])

    def get_delay(self):
        res = []
        for i in range(self.M):
            for j in range(len(self.arrival_time[i])):
                res.append(self.arrival_time[i][j] - self.generated_time[i][j])
        return res

    def get_minimal_generated(self):
        res = []
        for i in range(self.M):
            res.append(self.generated_time[i][self.counters[i]])
        return min(res)

    def optimize_queue(self):
        for i in range(self.M):
            for j in range(len(self.queue[i]) - 1):
                if self.queue[i][j + 1] - self.queue[i][j] < self.time_interval:
                    self.queue[i][j + 1] = self.queue[i][j] + self.time_interval
            self.queue[i].sort()

    def move_queue(self):
        for i in range(self.M):
            if len(self.queue[i]):
                self.queue[i][0] += random.uniform(0, self.time_interval * 10)
                self.queue[i].sort()
                self.queue_added[i] = 0


class Channel:
    def __init__(self, M, time_interval):
        self.M = M
        self.time_interval = time_interval
        self.stations_time = [[-1, -1] for _ in range(self.M)]

    def __str__(self):
        return f'{self.stations_time=}'

    def use(self, m, t):
        self.stations_time[m] = [t, t + self.time_interval]

    def can_sent(self, t):
        # get collision
        for i in range(self.M):
            if t > self.stations_time[i][1] and self.stations_time[i][0] > -1:
                if self.not_collision(i):
                    r = self.stations_time[i][0]
                    self.stations_time[i] = [-1, -1]
                    return i, r

    def not_collision(self, m):
        for i in range(self.M):
            if i == m:
                continue
            if self.stations_time[i][0] <= self.stations_time[m][0] and self.stations_time[i][1] >= \
                    self.stations_time[m][1]:
                return False
        return True

    def is_use(self, t):
        for i in range(self.M):
            if self.stations_time[i][0] <= t <= self.stations_time[i][1]:
                return True
        return False


def async_simulate(lam, T, M, r=0.2, time_interval=0.01):
    m = Messages(lam, T, M, r, time_interval)
    channel = Channel(M, time_interval)
    collisions = 0
    print(m)
    time = 0
    for _ in range(T):
        if m.message_num == m.sent_num:
            break
        temp = []
        for i in range(m.M):
            if not m.is_end_count(i):
                temp.append(m.get_message_time(i))
        if len(temp) > 0:
            time = min(temp)
        else:
            time += time_interval * 1.01

        for i in range(m.M):  # добавляем сообщения в подходящем интервале в очередь
            for j in range(m.get_count(i), len(m.get_generated_time(i))):
                if m.get_generated_time(i)[j] <= time:
                    m.add_to_queue(i, j)
                else:
                    break
        m.optimize_queue()
        for i in range(m.M):  # если очередь не пуста, пытаемся отправить сообщение
            if m.get_queue_size(i) > 0 and m.queue_added[i] == 0:
                channel.use(i, time)
                m.queue_added[i] = 1
        res = channel.can_sent(time)
        if res:
            # print(f'{time=} {res=}')
            m.send_message(res[0], res[1])
        elif sum([m.queue_added[i] for i in range(m.M)]) > m.M:
            m.move_queue()
        elif channel.is_use(time):
            collisions += 1

    return mean(m.get_delay()), m.sent_num, time, collisions


def test():
    m = Messages(1.5, 1000, 5)
    print(f"{m.stations_messages=}\n{m.generated_time=}")
    print(f"{m.message_num=}")
    c = 0
    for j in range(m.M):
        c += len(m.generated_time[j])
    print(f"{c/1000=}")


def main():
    lam = 0.3
    T = 1000
    M = 3
    r = 0.2
    time_interval = 0.001
    x = [i / 10 for i in range(1, 15)]
    temp = []
    for i in x:
        temp.append(async_simulate(i, T, M, r, time_interval))

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
        temp.append(async_simulate(lam, T, i, r, time_interval))

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


if __name__ == '__main__':
    main()
