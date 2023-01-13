# Fichier permettant de transformer des array numpy en sons
from typing import Callable
from scipy.io.wavfile import read
from matplotlib import pyplot as plt
from enum import Enum
from numpy import sin, ndarray, array, int32, pi, cos, sin
from functools import partial


def integrate(function: Callable[[int], float], steps: range):
    s = 0
    for i in steps:
        s += function(i) * 1 / 368
    return s


def violon():
    sample_rate, arr = read("instruments/violon.wav")
    


class Instrument(Enum):
    violon = violon()
    piano = violon
