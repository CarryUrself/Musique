# Fichier permettant créer une interface utilisateur pour gérer une partition

from dataclasses import dataclass
import os
import pygame
from numpy import arange, float32, pi, ndarray, array
from typing import Union, Callable, Any
from music import Note, Silence
from instruments import Instrument
from partition import Partition
from functools import partial

@dataclass
class C: # Coordinates
    x: int
    y: int

    @property
    def xy(self):
        return (self.x, self.y)

@dataclass
class D: # Dimensions
    w: int
    h: int

    @property
    def wh(self):
        return (self.w, self.h)

TEMPO_BLANCHE = 5

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

    def __init__(self, name: str, dimensions: D) -> None:
        self.name = name
        path = f"images/{name}.png"
        assert os.path.exists(path)
        self.surface = pygame.image.load(path)
        self.dimensions = dimensions

class Showable(Asset):

    def __init__(self, name: str, dimensions: D,
                 coos: C) -> None:
        super().__init__(name, dimensions)
        self.coos = coos

class Button(Showable):

    def __init__(self, name: str, dimensions: D,
                 coos: C, onClick: Callable[[MouseEvent],
                                                          Any]) -> None:
        super().__init__(name, dimensions, coos)
        self.onClick = onClick


class PartitionUI:
    """
    Classe possédant une interface graphique et un lecteur audio intégré pour les Partition
    """

    stop = False
    assets: list[Asset] = []

    def __init__(self, partition: Partition, dimensions: D) -> None:
        self.partition = partition
        self.dimensions = dimensions
        self.window = pygame.display.set_mode((dimensions.w, dimensions.h))
        self.assets.append(
            Button("popLastButton", D(25, 25), C(dimensions.w - 25, 0), 
            lambda e: print(e)))
    
    def create_sound(self, frequency: float, instrument: Callable[..., Any]) -> ndarray:
        #!
        #!
        #!
        #TODO
        coef = frequency/440
        return array([])

    def fade_out(self, sound: ndarray) -> ndarray:
        #!
        #!
        #!
        #TODO
        return sound

    def play_note(self, frequency: float, duration: float,
                  instrument: Callable[[ndarray], ndarray]):
        # TODO:
        # - utiliser la transformation de fourrier pour recréer un motif pour chaque instrument
        # - l'utiliser pour ajuster la hauteur du son sans perdre le timbre
        # - scale ensuite le son par une courbe de bezier pour donne un "fade out"
        # - profit
        buffer = instrument(2 * pi * arange(0, 44100, duration) * frequency /
                            (44100 * duration)).astype(float32)
        sound = pygame.mixer.Sound(buffer)
        sound.play()
        pygame.time.wait(int(sound.get_length() * 1000))

    def play_silence(self, duration: float):
        # simulate sound but don't fire it
        buffer = arange(0, 44100, duration).astype(float32)
        sound = pygame.mixer.Sound(buffer)
        pygame.time.wait(int(sound.get_length() * 1000))

    def play(self):
        for i in self.partition.notes:
            if isinstance(i, Note):
                self.play_note(i.frequence.value * i.hauteur.value,
                               i.rythme.value / TEMPO_BLANCHE,
                               Instrument.violon.value)
            if isinstance(i, Silence):
                self.play_silence(i.rythme.value / TEMPO_BLANCHE)

    def collision(self, pos: C, elt: Showable) -> bool:
        x, y = pos.xy
        g, h = elt.coos.xy
        b, d = h + elt.dimensions.h, g + elt.dimensions.h
        # print(f"{y}     {x}")
        # print(f"{h, b, g, d}")
        return g < x < d and h < y < b

    def get_clicked_asset(self, e: MouseEvent) -> Union[Showable, None]:
        for i in self.assets:
            if isinstance(i, Button):
                if self.collision(e.pos, i):
                    return i
        return None

    def handleKeyDown(self, e: KeyEvent):
        if e.key == pygame.K_ESCAPE:
            self.stop = True

    def handleMouseDown(self, e: MouseEvent):
        elt = self.get_clicked_asset(e)
        if isinstance(elt, Button):
            elt.onClick(e)
        pass

    def quit(self):
        self.partition.save()
        self.stop = True

    def show(self, asset: Showable):
        self.window.blit(asset.surface, (asset.coos.x, asset.coos.y))

    def render(self):
        self.window.fill("black")
        for asset in self.assets:
            if isinstance(asset, Showable):
                self.show(asset)
        pygame.display.flip()

    def __call__(self):
        clock = pygame.time.Clock()
        while not self.stop:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    e = KeyEvent(event)
                    self.handleKeyDown(e)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    e = MouseEvent(event)
                    self.handleMouseDown(e)
                if event.type == pygame.QUIT:
                    self.quit()
            clock.tick(60)
            self.render()
        return self