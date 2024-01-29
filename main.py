import math
import random
import matplotlib.pyplot as plt


def fact(n):
    if n <= 1:
        return 1
    return n * fact(n - 1)


d = []
n = []
T = 10000
n_accuracy = 10
x = []
y_pract_MD = []
y_teor_MD = []

y_pract_MN = []
y_teor_MN = []

print("Sync")
for lam in range(1, n_accuracy):
    lambd = lam / n_accuracy
    x.append(lambd)
    w = [False for b in range(int(T))]
    d.clear()
    nn = 0
    n_ab_out_ar = [0 for k in range(int(T))]
    for i in range(int(T)):
        num_of_ab = 0
        rnd = random.uniform(0, 1)
        pr_j = 0
        for j in range(10):
            pr_j = pr_j + ((lambd ** j) * math.exp(-lambd)) / fact(j)
            if rnd < pr_j:
                num_of_ab = j
                break
        nn += (num_of_ab + n_ab_out_ar[i])
        n.append(nn)

        a = [random.uniform(0, 1) for k in range(num_of_ab)]
        a.sort()
        f = 0
        for k in a:
            if i + 1 >= T:
                break
            if not w[i + 1]:
                d.append(k + 1)
                n_ab_out_ar[i + 1] = -1
                w[i + 1] = True
            else:
                b = i + 2
                if b >= T:
                    break
                d_temp = k + 2
                f = 0
                while w[b]:
                    b += 1
                    if b >= T:
                        f = 1
                        break
                    d_temp += 1
                if f:
                    break
                d.append(d_temp)
                n_ab_out_ar[b] = -1
                w[b] = True

    MD = sum(d) / len(d)
    MD_teor = (2 - lambd) / (2 - 2 * lambd) + 0.5
    MN = sum(n) / T
    MN_teor = (2 * lambd - lambd ** 2) / (2 - 2 * lambd)
    y_pract_MD.append(MD)
    y_teor_MD.append(MD_teor)
    y_pract_MN.append(MN)
    y_teor_MN.append(MN_teor)
    print(lambd)
    print("pract M[D]=", MD)
    print("teor M[D]=", MD_teor)
    d.clear()
    n.clear()

plt.figure(1)
plt.title("Sync M[D]")
plt.plot(x, y_pract_MD, label="pract")
plt.plot(x, y_teor_MD, label="teor")
plt.legend()
plt.xlabel("lambda")
plt.ylabel("M[D]")
plt.savefig("Sync_M_D.png")

plt.figure(2)
plt.title("Sync M[N]")
plt.plot(x, y_pract_MN, label="pract")
plt.plot(x, y_teor_MN, label="teor")
plt.legend()
plt.xlabel("lambda")
plt.ylabel("M[N]")
plt.savefig("Sync_M_N.png")

y_pract_MD.clear()
y_teor_MD.clear()
y_pract_MN.clear()

#print("Async")
for lam in range(1, n_accuracy):
    lambd = lam / n_accuracy
    d.clear()
    n = [0 for k in range(T)]
    times = []
    in_ab = [0 for k in range(T)]
    out_ab = [0 for k in range(T)]
    for i in range(int(T)):
        num_of_ab = 0
        rnd = random.uniform(0, 1)
        pr_j = 0
        for j in range(10):
            pr_j = pr_j + ((lambd ** (j)) * math.exp(-lambd)) / fact(j)
            if rnd < pr_j:
                num_of_ab = j
                break
        a = [random.uniform(0, 1) for k in range(num_of_ab)]
        a.sort()
        in_ab[i] = num_of_ab
        for k in a:
            times.append(i + k)
    d.append(1)
    last = 1 + times[0]
    out_ab[math.floor(1 + times[0])] += 1
    for i in range(1, len(times)):
        if times[i] < last:
            service_time_i = last - times[i] + 1
            d.append(service_time_i)
            last = service_time_i + times[i]
            if math.floor(last) < T:
                out_ab[math.floor(last)] += 1
        else:
            d.append(1)
            last = times[i] + 1
            if math.floor(last) < T:
                out_ab[math.floor(last)] += 1
    n[0] = in_ab[0]
    #print(in_ab[0], out_ab[0], in_ab[1], out_ab[1])

    for i in range(1, T):
        n[i] = n[i - 1] + in_ab[i] - out_ab[i]
    y_pract_MD.append(sum(d) / len(d))
    y_teor_MD.append((2 - lambd) / (2 - 2 * lambd))
    y_pract_MN.append(sum(n) / T)

plt.figure(3)
plt.title("Async M[D]")
plt.plot(x, y_pract_MD, label="pract")
plt.plot(x, y_teor_MD, label="teor")
plt.legend()
plt.xlabel("lambda")
plt.ylabel("M[D]")
plt.savefig("Async M[D].png")

plt.figure(4)
plt.title("Async M[N]")
plt.plot(x, y_pract_MN, label="pract")
plt.plot(x, y_teor_MN, label="teor")
plt.legend()
plt.xlabel("lambda")
plt.ylabel("M[N]")
plt.savefig("Async M[N].png")