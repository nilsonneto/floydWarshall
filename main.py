import random
import sys
import time
from multiprocessing import Process, Array

__author__ = 'Nilson'
numThreads = 4
dist = []
pi = []

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
    # Declaring
    myw = []

    myi = []
    for i in range(size):
        myj = []
        for j in range(size):
            if i == j:
                myj.append(0)
            else:
                myj.append(random.randint(2, 30))
        myi.append(myj)
    myw.append(myi)

    return myw


def pi_start_serial(weights, size):
    d = []

    dd = []
    for i in range(size):
        ddd = []
        for j in range(size):
            if i == j or weights[0][i][j] == sys.maxsize:
                ddd.append(None)
            elif i != j and weights[0][i][j] < sys.maxsize:
                ddd.append(i)
            else:
                ddd.append(-1)  # Something is wrong
        dd.append(ddd)
    d.append(dd)

    return d


def dist_serial(weights, size):
    d = list(weights)
    for k in range(1, size):
        dd = []
        for i in range(size):
            ddd = []
            for j in range(size):
                if i == j:
                    ddd.append(0)
                else:
                    ddd.append(int(sys.maxsize))
            dd.append(ddd)
        d.append(dd)
    return d


def pi_serial(weights, size):
    d = list(pi_start_serial(weights, size))

    for k in range(1, size):
        dd = []
        for i in range(size):
            ddd = []
            for j in range(size):
                if i == j:
                    ddd.append(None)
                else:
                    ddd.append(0)
            dd.append(ddd)
        d.append(dd)

    return d


def floyd_serial(weights, size):
    d = dist_serial(weights, size)
    p = pi_serial(weights, size)

    for k in range(1, size):
        for i in range(size):
            for j in range(size):
                d[k][i][j] = min(d[k-1][i][j], d[k-1][i][k] + d[k-1][k][j])
                if d[k-1][i][j] <= d[k-1][i][k] + d[k-1][k][j]:
                    p[k][i][j] = p[k-1][i][j]
                else:
                    p[k][i][j] = p[k-1][k][j]

    return d, p


# ----------------------------------------------------------------------------------------------------------------- #
# ----------------------------------------------------------------------------------------------------------------- #
# ----------------------------------------------------------------------------------------------------------------- #
# ----------------------------------------------------------------------------------------------------------------- #
# ----------------------------------------------------------------------------------------------------------------- #
def min_p_parallel(k, iran):
    # print(k, i, j, d[i][k], d[k][j])]
    '''
    numd.append([j, min(d[i][j], d[i][k] + d[k][j])]

    if d[i][j] <= d[i][k] + d[k][j]:
        nump.append([j, p[i][j]])
    else:
        nump.append([j, p[k][j]])
    '''
    global dist
    global pi

    for i in iran:
        for j in range(len(iran)*numThreads):
            dist[k][i][j] = min(dist[k - 1][i][j], dist[k - 1][i][k] + dist[k - 1][k][j])
            if dist[k-1][i][j] <= dist[k-1][i][k] + dist[k-1][k][j]:
                pi[k][i][j] = pi[k - 1][i][j]
            else:
                pi[k][i][j] = pi[k - 1][k][j]


def floyd_parallel(weights, size):
    global dist
    dist = dist_serial(weights, size)
    global pi
    pi = pi_serial(weights, size)

    for k in range(1, size):
        thr = []
        for pro in range(numThreads):
            imin = int(pro * (size/numThreads))
            imax = int((pro + 1) * (size/numThreads))
            iran = range(imin, imax)
            t = Process(target=min_p_parallel, args=(k, iran))
            t.daemon = True
            thr.append(t)
            t.start()
        for t in thr:
            t.join()


if __name__ == "__main__":
    n = 10000

    fis = open('serial.txt', 'a')
    fip = open('parallel.txt', 'a')

    for n in [1*numThreads, 10*numThreads, 100*numThreads, 500*numThreads, 10000*numThreads]:
        w = weight_serial(n)

        start = time.process_time()
        #ds, ps = floyd_serial(w, n)
        end = time.process_time()
        fis.write('For %s: Elapsed time: %ss\n' % (n, str(end-start)))
        #print('S: For %s: Elapsed time: %ss' % (n, str(end-start)))

        start = time.process_time()
        floyd_parallel(w, n)
        end = time.process_time()
        fip.write('For %s: Elapsed time: %ss\n' % (n, str(end-start)))
        print('P: For %s: Elapsed time: %ss' % (n, str(end-start)))

        #print('Same dist matrix: %s' % (dist == ds))
        #print('Same pi matrix: %s' % (pi == ps))

    # print(dist)
    # print(pi)
