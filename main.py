import pygame
from UI import Partition, PartitionPlayer

if __name__ == "__main__":
    pygame.mixer.init(size=32)
    part = Partition("partitions/TEST.part")
    part.load()
    player = PartitionPlayer(part, (900, 600))
    player()
