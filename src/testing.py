import pygame
from app import PartitionUI, D, Partition
if __name__ == "__main__":
    pygame.mixer.init(size=32)
    part = Partition("partitions/TEST.part")
    part.load()
    player = PartitionUI(part, D(900, 600))
    player().play()
