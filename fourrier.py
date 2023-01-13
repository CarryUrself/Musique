# Fichier permettant de transformer des array numpy en sons
# Ne marche pas
# Ne cours pas non plus
from typing import Callable
from scipy.io.wavfile import read
from scipy.integrate import quad
from matplotlib import pyplot as plt
from enum import Enum
from numpy import sin, ndarray, array, int32, pi, cos, sin
from functools import partial

f = lambda x: cos(x) + sin(x)
twopi = 2 * pi
P = twopi

def integrate(function: Callable[[float], float], steps: range):
    s = 0
    for i in steps:
        s += function(i)
    return s


def a(func, n: int):
    return (2/P)*integrate(lambda x: func(x)*cos(n*x), range(int(2*P)))
def b(func, n: int):
    return (2/P)*integrate(lambda x: func(x)*sin(n*x), range(int(P*2)))
def res(N: int, x: float):
    s = 0
    for n in range(N):
        s += cos(n*x) * a(f, n) + sin(x*n) * b(f, n)
    print(x)
    return s

def violon():
    # sample_rate, arr = read("instruments/violon.wav")
    arr = array(list(cos(i) for i in range(100)))
    s = [0 for i in range(100)]
    plt.plot(arr)
    plt.plot([res(20, x) for x in range(100)])
    plt.show()


class Instrument(Enum):
    violon = violon()
    piano = violon


print(integrate(cos, range(int(10000*twopi))))
