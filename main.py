import random
import sys
import time

__author__ = 'Nilson'

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


weights = []
dist = []


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


def pi_start_serial(size):
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


def dist_serial(size):
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


def pi_serial(size):
    d = list(pi_start_serial(size))

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


def min_serial(dd, i, j, k):
    return min(dd[i][j], dd[i][k] + dd[k][j])


def floyd_serial(size):
    p = pi_serial(size)

    for k in range(1, size):
        for i in range(size):
            for j in range(size):

                dist[k][i][j] = min(dist[k-1][i][j], dist[k-1][i][k] + dist[k-1][k][j])
                if dist[k-1][i][j] <= dist[k-1][i][k] + dist[k-1][k][j]:
                    p[k][i][j] = p[k-1][i][j]
                else:
                    p[k][i][j] = p[k-1][k][j]

    return dist, p


def floyd_parallel(size):
    p = pi_serial(size)

    for k in range(1, size):
        for i in range(size):
            for j in range(size):
                dist[k][i][j] = min(dist[k-1][i][j], dist[k-1][i][k] + dist[k-1][k][j])
                if dist[k-1][i][j] <= dist[k-1][i][k] + dist[k-1][k][j]:
                    p[k][i][j] = p[k-1][i][j]
                else:
                    p[k][i][j] = p[k-1][k][j]

    return p


if __name__ == "__main__":
    n = 10000
    weights = list(weight_serial(n))
    dist = list(dist_serial(n))

    fis = open('serial.txt', 'a')
    fip = open('parallel.txt', 'a')

    for n in [10, 100, 1000, 10000]:
        start = time.process_time()
        pi = floyd_serial(n)
        end = time.process_time()
        fis.write('For %s: Elapsed time: %ss\n' % (n, str(end-start)))
        print('For %s: Elapsed time: %ss' % (n, str(end-start)))

    # print(dist)
    # print(pi)
