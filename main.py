import pygame
from UI import PartitionUI, D
from partition import Partition
if __name__ == "__main__":
    pygame.mixer.init(size=32)
    part = Partition("partitions/TEST.part")
    part.load()
    player = PartitionUI(part, D(900, 600))
    player()
