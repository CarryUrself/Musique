# Fichier permettant de transformer des array numpy en sons

from enum import Enum
from numpy import sin, ndarray


def violon(arr: ndarray):
    return sin(arr)


def piano(arr: ndarray):
    return sin(arr)


class Instrument(Enum):
    violon = violon
    piano = piano