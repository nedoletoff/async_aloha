import math
import random
import statistics


class SyncSystem:
    def __init__(self, mu=1, lam=0.5, time_end=10000):
        self.lam = lam
        self.mu = mu
        self.t = []
        self.time_now = 0
        self.time_end = time_end
        self.n = 0

        self.queue = []
        self.mas = []
        # print(self.mas)

    def gen_m(self, n):
        for i in range(n):
            if random.random() < self.lam:
                self.mas.append(random.uniform(0, n))
        self.mas.sort()

    def step(self):
        self.time_now += self.mu
        if len(self.mas) > 0 and self.mas[0] <= self.time_now:
            self.queue.append(self.mas.pop(0))

        if len(self.queue) > 0:
            self.t.append(self.time_now - self.queue.pop(0) + self.mu)
            self.n += 1

    def run(self):
        self.gen_m(self.time_end)
        while self.time_now < self.time_end:
            self.step()
        return self.t, math.exp(statistics.mean(self.t) - self.mu)


if __name__ == '__main__':
    s = SyncSystem(mu=1, lam=0.4, time_end=10000)
    t, n_av = s.run()
    d_t = 0
    for i in t:
        d_t += i
    print('M[D] = ', d_t / len(t))
    print('M[N] = ', n_av)
