# Interface entre un fichier .part et un PartitionUI

from music import Note, Silence, Rythme, Frequence, Hauteur
from typing import Union
import os


class Partition:
    """
    Classe permettant de gérer une partition. 
    S'utilise manuellement avec PartitionPlayer.
    Possède un parser intégré (parse_data, parse_note, parse_silence)
    """

    notes: list[Note | Silence] = []

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