import random
import sys
import time
from multiprocessing import Process, Array, Queue
from threading import Lock, Thread

import math

__author__ = 'Nilson'
numThreads = 4

"""
W = matriz de pesos (w(i,j))
n = |V|
V = {1, ..., n}
i = vertice inicial
j = vertice final
P = caminho minimo
d[k][i][j] = peso do caminho entre i e j, passando por k intermediários
se k = 0, então d[i][j][k] = w[i][j]
se k > 0, então min(d[i][j][k-1], (d[k-1][i][j], d[k-1][i][k] + d[k-1][k][j])


Para pi:
se d[k-1][i][j] <= d[k-1][i][k] + d[k-1][k][j], então pi[k][i][j] = pi[k-1][i][j]
se d[k-1][i][j] > d[k-1][i][k] + d[k-1][k][j], então pi[k][i][j] = pi[k-1][k][j]

"""


def weight_serial(size):
    dd = []
    for i in range(size):
        ddd = []
        for j in range(size):
            if i == j:
                ddd.append(0)
            else:
                ddd.append(random.randint(2, 30))
        dd.append(ddd)

    return dd


def pi_start_serial(weights, size):
    dd = []
    for i in range(size):
        ddd = []
        for j in range(size):
            if i == j or weights[i][j] == sys.maxsize:
                ddd.append(None)
            elif i != j and weights[i][j] < sys.maxsize:
                ddd.append(i)
            else:
                ddd.append(-1)
        dd.append(ddd)

    return dd


def dist_serial(weights, size):
    d = [[[(0 if __ == ___ else int(sys.maxsize)) for __ in range(size)] for __ in range(size)] for ___ in range(size)]
    d[0] = list(weights)

    return d


def pi_serial(weights, size):
    d = [[[(None if __ == ___ else 0) for __ in range(size)] for __ in range(size)] for ___ in range(size)]
    d[0] = list(pi_start_serial(weights, size))

    return d


def floyd_serial(weights, size):
    d = dist_serial(weights, size)
    p = pi_serial(weights, size)

    for k in range(1, size):
        for i in range(size):
            for j in range(size):
                d[k][i][j] = min(d[k - 1][i][j], d[k - 1][i][k] + d[k - 1][k][j])
                if d[k - 1][i][j] <= d[k - 1][i][k] + d[k - 1][k][j]:
                    p[k][i][j] = p[k - 1][i][j]
                else:
                    p[k][i][j] = p[k - 1][k][j]

    return d, p


# ----------------------------------------------------------------------------------------------------------------- #
# ----------------------------------------------------------------------------------------------------------------- #
# ----------------------------------------------------------------------------------------------------------------- #
# ----------------------------------------------------------------------------------------------------------------- #
# ----------------------------------------------------------------------------------------------------------------- #
def min_p_parallel(dist, pi, k, ir, size, queue):
    darr = []
    parr = []
    for i in ir:
        darr.append([(min(dist[i][j], dist[i][k] + dist[k][j])) for j in range(size)])
        parr.append([(pi[i][j] if dist[i][j] <= dist[i][k] + dist[k][j] else pi[k][j]) for j in range(size)])

    queue.put((ir, darr, parr))


def floyd_parallel(weights, size):
    dist = dist_serial(weights, size)
    pi = pi_serial(weights, size)

    for k in range(1, size):
        thr = []
        queue = Queue()

        for pro in range(numThreads):
            imin = math.floor(pro * (size / numThreads))
            imax = math.floor((pro + 1) * (size / numThreads))
            ir = range(imin, imax)
            t = Process(target=min_p_parallel, args=(dist[k - 1], pi[k - 1], k, ir, size, queue), daemon=True).start()
            thr.append(t)

        for t in thr:
            try:
                t.join()
            except AttributeError:
                pass

        for v in range(numThreads):
            veci, vecd, vecp = queue.get()
            ct = 0
            for i in veci:
                dist[k][i] = list(vecd[ct])
                pi[k][i] = list(vecp[ct])
                ct += 1

    return dist, pi


if __name__ == "__main__":
    n = 10000

    fis = open('serial.txt', 'a')
    fip = open('parallel.txt', 'a')

    for n in [1 * numThreads, 10 * numThreads, 100 * numThreads]:
        w = weight_serial(n)

        start = time.process_time()
        ds, ps = floyd_serial(w, n)
        end = time.process_time()
        fis.write('For %s: Elapsed time: %ss\n' % (n, str(end-start)))
        print('S: For %s: Elapsed time: %ss' % (n, str(end-start)))

        start = time.process_time()
        dp, pp = floyd_parallel(w, n)
        end = time.process_time()
        fip.write('For %s: Elapsed time: %ss\n' % (n, str(end-start)))
        print('P: For %s: Elapsed time: %ss' % (n, str(end - start)))

        print('Same dist matrix: %s' % (dp == ds))
        print('Same pi matrix: %s' % (pp == ps))

        # print(dist)
        # print(pi)
