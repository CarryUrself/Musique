# Fichier permettant créer une interface utilisateur pour gérer une partition
# Sera probablement réfactorisé pour faire de l'async mais flemme

import pygame
from numpy import arange, float32, pi, ndarray, array, sin
from typing import Union, Callable, Any
from music import Note, Silence, retirerAlteration
from partition import Partition
from ui_elements import C, D, Asset, KeyEvent, Button, Showable, MouseEvent, PlacementFrequence, PlacementOctave, TAILLE_OCTAVE

TEMPO_BLANCHE = 5
class PartitionUI:
    """
    Classe possédant une interface graphique et un lecteur audio intégré pour les Partition
    """
    stop = False
    stop_playing = False
    assets: list[Asset] = []
    MovablePartition = Asset("partition")
    Noire = Asset("noire")


    def __init__(self, partition: Partition, dimensions: D) -> None:
        self.partition = partition
        self.dimensions = dimensions
        self.window = pygame.display.set_mode((dimensions.w, dimensions.h))
        self.playButton = Button("playButton", C(0, 0), lambda e: self.play())
        # self.pauseButton = Button("pauseButton", C(0, 0), lambda e: self.play())
        self.assets = [
            Button("popLastButton", C(dimensions.w - 25, 0),
                   lambda e: print(e)), 
            self.playButton
                   ]

    def quit(self):
            self.partition.save()
            self.stop_playing = True
            self.stop = True
        
    def build_partition(self):
        n = len(self.partition.notes) // 4 + 1
        coos = C(80, 80)
        xMAX = self.dimensions.w - self.MovablePartition.dimensions.w
        for _ in range(n):
            self.place(self.MovablePartition, coos)
            new_x = coos.x + self.MovablePartition.dimensions.w
            if new_x > xMAX:
                coos.x = self.MovablePartition.dimensions.w
                coos.y += int(self.MovablePartition.dimensions.h * 1.5)
            else:
                coos.x += self.MovablePartition.dimensions.w
                
    def place_notes(self):
        x = 0
        l = 136
        c = 80
        for note in self.partition.notes:
            y = 4
            x += self.Noire.dimensions.w
            if x > 1:##TODO
                i = 0
                x = 0
                l = l + int(self.MovablePartition.dimensions.h * 1.5)
            if isinstance(note, Note):
                y = PlacementFrequence[retirerAlteration(note.frequence)].value
                y += TAILLE_OCTAVE * PlacementOctave[note.hauteur.name].value
            self.place(self.Noire, C(c + x, l + y * int(1 + self.Noire.dimensions.h / 2)))
            

    def create_sound(self, frequency: float,
                     instrument: Callable[..., Any]) -> ndarray:
        #!
        #!
        #!
        #TODO
        coef = frequency / 440
        return array([])

    def fade_out(self, sound: ndarray) -> ndarray:
        """
        takes a sound as an array for input
        outputs the same sound but with fade out at the end
        """
        #!
        #!
        #!
        #TODO
        return sound

    def play_note(self, frequency: float, duration: float):
        # TODO:
        # - utiliser la transformation de fourrier pour recréer un motif pour chaque instrument
        # - l'utiliser pour ajuster la hauteur du son sans perdre le timbre
        # - scale ensuite le son par une courbe de bezier pour donne un "fade out"
        # - profit
        buffer = sin(2 * pi * arange(0, 44100, duration) * frequency /
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
            self.check_events()
            if self.stop_playing:
                break
            if isinstance(i, Note):
                self.play_note(i.frequence.value * i.hauteur.value,
                               i.rythme.value / TEMPO_BLANCHE)
            if isinstance(i, Silence):
                self.play_silence(i.rythme.value / TEMPO_BLANCHE)

    def collision(self, pos: C, elt: Showable) -> bool:
        x, y = pos.xy
        g, h = elt.coos.xy
        b, d = h + elt.dimensions.h, g + elt.dimensions.h
        return g < x < d and h < y < b

    def get_clicked_asset(self, e: MouseEvent) -> Union[Showable, None]:
        for i in self.assets:
            if isinstance(i, Button):
                if self.collision(e.pos, i):
                    return i
        return None

    def handleKeyDown(self, e: KeyEvent):
        if e.key == pygame.K_ESCAPE:
            self.quit()

    def handleMouseDown(self, e: MouseEvent):
        elt = self.get_clicked_asset(e)
        if isinstance(elt, Button):
            elt.onClick(e)
        pass

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                e = KeyEvent(event)
                self.handleKeyDown(e)
            if event.type == pygame.MOUSEBUTTONDOWN:
                e = MouseEvent(event)
                self.handleMouseDown(e)
            if event.type == pygame.QUIT:
                self.quit()

    def place(self, asset: Asset, coos: C):
        self.window.blit(asset.surface, coos.xy)

    def show(self, asset: Showable):
        self.window.blit(asset.surface, asset.coos.xy)

    def render(self):
        for asset in self.assets:
            if isinstance(asset, Showable):
                self.show(asset)
        pygame.display.flip()

    def __call__(self): # main loop
        while not self.stop:
            self.check_events()
            self.window.fill("black")
            self.build_partition()
            self.place_notes()
            self.render()
        return self
