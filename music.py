from dataclasses import dataclass
from enum import Enum

class Frequence(Enum):
    """
    Traduit les notes en fréquences (Hz), par défaut on admet que la note est médium
    A noter: {note}d correspond à la note dièse, {note}b correspond à la note bémole 
    """
    do = 261
    dod = 277
    reb = 277
    re = 293
    red = 311
    mib = 311
    mi = 329
    fa = 349
    fad = 369
    solb = 369
    sol = 392
    sold = 415
    lab = 415
    la = 440
    lad = 466
    sib = 466
    si = 493

class Hauteur(Enum):
    """
    représente une octave, la valeur de l'octave est un multiplicateur à la fréquence de base
    """
    grave = 0.5
    medium = 1
    aigu1 = 2
    aigu2 = 4
    aigu3 = 4

class Rythme(Enum):
    """
    Représente un temps musical, ou quand la valeur augmente la durée diminue
    """
    # BASE 12
    binaire_double_croche = 16
    binaire_croche = 8
    noire = 4
    blanche = 2
    ronde = 1

@dataclass(frozen=True)
class Note:
    """
    Représente une note, avec son nom (fréquence), son octave (hauteur) et sa durée (rythme)
    """

    frequence: Frequence
    hauteur: Hauteur
    rythme: Rythme

@dataclass(frozen=True)
class Silence:
    """
    Représente l'élément musical "silence"
    """
    rythme: Rythme
