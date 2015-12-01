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


def build_weight(size):
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


def build_pi_start(weights, size):
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


def build_dist(weights, size):
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


def build_pi(weights, size):
    d = list(build_pi_start(weights, size))

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


def floydSerial(weights, size):
    d = build_dist(weights, size)
    p = build_pi(weights, size)

    for k in range(1, size):
        for i in range(size):
            for j in range(size):
                d[k][i][j] = min(d[k-1][i][j], d[k-1][i][k] + d[k-1][k][j])
                if d[k-1][i][j] <= d[k-1][i][k] + d[k-1][k][j]:
                    p[k][i][j] = p[k-1][i][j]
                else:
                    p[k][i][j] = p[k-1][k][j]

    return d, p


if __name__ == "__main__":
    n = 10000
    start = time.process_time()
    w = build_weight(n)
    # dist, pi = floydSerial(w, n)
    end = time.process_time()
    # print(dist)
    # print(pi)
    print('Elapsed time: %ss' % str(end-start))
