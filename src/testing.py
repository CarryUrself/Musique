import pygame
from app import PartitionUI, D, Partition

pygame.mixer.init(size=32)
part = Partition("partitions/horrible.part")
part.load()
player = PartitionUI(part, D(900, 600))
player.play()