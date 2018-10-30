# Code taken from: https://stackoverflow.com/questions/28005641/how-to-add-a-background-image-into-pygame
# This file holds the backgrounds.
import pygame

class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location
        