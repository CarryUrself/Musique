# Fichier contenant tous les éléments relatifs à l'UI et aux events

from dataclasses import dataclass
import pygame
from typing import Union, Callable, Any
import os
from enum import Enum

@dataclass
class C:  # Coordinates
    x: int
    y: int

    @property
    def xy(self):
        return (self.x, self.y)


@dataclass
class D:  # Dimensions
    w: int
    h: int

    @property
    def wh(self):
        return (self.w, self.h)

class KeyEvent:

    def __init__(self, event: pygame.event.Event) -> None:
        assert isinstance(event.key, int)
        self.event = event
        self.key = event.key


class MouseEvent:

    def __init__(self, event: pygame.event.Event) -> None:
        # pos
        assert isinstance(event.pos, tuple)
        assert len(event.pos) == 2
        assert isinstance(event.pos[0], int) and isinstance(event.pos[1], int)
        self.pos = C(event.pos[1], event.pos[0])  # button
        assert isinstance(event.button, int)
        self.button = event.button
        self.event = event

GeneralEvent = Union[KeyEvent, MouseEvent]

@dataclass
class Asset:

    def __init__(self, name: str) -> None:
        self.name = name
        path = f"images/{name}.png"
        assert os.path.exists(path)
        self.surface = pygame.image.load(path)
        self.dimensions = D(self.surface.get_width(), self.surface.get_height())


class Showable(Asset):

    def __init__(self, name: str, coos: C) -> None:
        super().__init__(name)
        self.coos = coos


class Button(Showable):

    def __init__(self, name: str, coos: C,
                 onClick: Callable[[MouseEvent], Any]) -> None:
        super().__init__(name, coos)
        self.onClick = onClick


class PlacementFrequence(Enum):
    do = 6
    re = 5
    mi = 4
    fa = 3
    sol = 2
    la = 1
    si = 0

class PlacementOctave(Enum):
    aigu2 = -2
    aigu1 = -1
    medium = 0
    grave = 1

TAILLE_OCTAVE = 7
