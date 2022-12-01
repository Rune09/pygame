import pygame

pygame.init()

# muziek eerst inladen en dan pas afspelen
pygame.mixer.music.load('music/main2.ogg')
pygame.mixer.music.play()

# while-lus om python te laten runnen
i = 0
while i == 0:
    i = 0
