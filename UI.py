from dataclasses import dataclass
import os
import pygame
import numpy as np
from typing import Union, Callable, Any
from music import Note, Silence, Frequence, Hauteur, Rythme

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
        self.pos = (event.pos[1], event.pos[0])        # button
        assert isinstance(event.button, int)
        self.button = event.button
        self.event = event

GeneralEvent = Union[KeyEvent, MouseEvent]

@dataclass
class Asset:

    def __init__(self, name: str, dimensions: tuple[int, int]) -> None:
        self.name = name
        path = f"images/{name}.png"
        assert os.path.exists(path)
        self.surface = pygame.image.load(path)
        self.width = dimensions[0]
        self.height = dimensions[1]

class Showable(Asset):

    def __init__(self, name: str, dimensions: tuple[int, int], coos: tuple[int, int]) -> None:
        super().__init__(name, dimensions)
        self.coos = coos

class Button(Showable):

    def __init__(self, name: str, dimensions: tuple[int, int], coos: tuple[int, int], onClick: Callable[[MouseEvent], Any]) -> None:
        super().__init__(name, dimensions, coos)
        self.onClick = onClick

class Partition:
    """
    Classe permettant de gérer une partition. 
    S'utilise manuellement avec PartitionPlayer.
    Possède un parser intégré (parse_data, parse_note, parse_silence)
    """

    notes: list[Union[Note, Silence]] = []

    def __init__(self, path: str):
        assert path.endswith(".part")
        assert os.path.exists(path)
        self.path = path

    def __str__(self):
        s = ""
        for i in self.notes:
            if isinstance(i, Silence):
                s += f"(Silence {i.rythme.name})"
            elif isinstance(i, Note):
                s += f"(Note {i.frequence.name}, {i.hauteur.name}, {i.rythme.name})"
        return s

    def __repr__(self) -> str:
        return str(self)

    def parse_note(self, data: list[str]):
        f, h, r = data
        return Note(Frequence[f], Hauteur[h], Rythme[r])

    def parse_silence(self, data: list[str]):
        r = data[0]
        return Silence(Rythme[r])

    def parse_data(self, noteData: str):
        if noteData.startswith("//"):
            return None
        data = list(i.removesuffix("\n") for i in noteData.split(" "))
        TYPE, *DATA = data
        if TYPE == "note":
            return self.parse_note(DATA)
        if TYPE == "silence":
            return self.parse_silence(DATA)
        raise KeyError

    def load(self):
        with open(self.path, "r") as partition:
            for noteData in partition.readlines():
                try:
                    elt = self.parse_data(noteData)  # parsing data
                    if (elt):
                        self.notes.append(elt)
                except KeyError:
                    print("Fichier Partition corrompu")

    def save(self):
        #! TODO
        pass

class PartitionPlayer:
    """
    Classe possédant une interface graphique et un lecteur audio intégré pour les Partition
    """

    stop = False
    assets: list[Asset] = []

    def __init__(self, partition: Partition, dimensions: tuple[int,
                                                               int]) -> None:
        self.partition = partition
        self.dimensions = dimensions
        self.window = pygame.display.set_mode(dimensions)
        self.assets.append(Button("popLastButton", (25, 25), (dimensions[0] - 25, 0), lambda e: print(e)))

    def play_note(self, frequency: float, duration: float):
        buffer = np.sin(2 * np.pi * np.arange(0, 44100, duration) * frequency /
                        (44100 * duration)).astype(np.float32)
        sound = pygame.mixer.Sound(buffer)
        sound.play()
        pygame.time.wait(int(sound.get_length() * 1000))

    def play_silence(self, duration: float):
        # simulate sound but don't fire it
        buffer = np.arange(0, 44100, duration).astype(np.float32)
        sound = pygame.mixer.Sound(buffer)
        pygame.time.wait(int(sound.get_length() * 1000))

    def play(self):
        for i in self.partition.notes:
            if isinstance(i, Note):
                self.play_note(i.frequence.value * i.hauteur.value,
                               i.rythme.value / TEMPO_BLANCHE)
            if isinstance(i, Silence):
                self.play_silence(i.rythme.value / TEMPO_BLANCHE)

    def collision(self, pos: tuple[int, int], elt: Showable) -> bool:
        x, y = pos
        h, g = elt.coos
        b, d = h + elt.height, g + elt.width
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
        self.window.blit(asset.surface, asset.coos)

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