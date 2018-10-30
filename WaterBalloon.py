# This file initializes the water balloons, and once they're on screen for a certain amount of time they explode, though
# that is not shown in this file explicitly, that's what the self.timeOnScreen is for!

import pygame
from GameObject import GameObject

class WaterBalloon(GameObject):
    time = 50 
    
    @staticmethod
    def init():
        WaterBalloon.balloonImage = pygame.image.load("images/objects/WATER_BALLOON.png").convert_alpha()
        WaterBalloon.balloonImage = pygame.transform.scale(WaterBalloon.balloonImage, (35, 35))
        
    def __init__(self, row, col, owner):
        super(WaterBalloon, self).__init__(row, col, WaterBalloon.balloonImage)
        self.timeOnScreen = 0
        self.owner = owner
        w, h = WaterBalloon.balloonImage.get_size()
        self.rect = pygame.Rect(self.x - w / 2, self.y - h / 2, w, h)
    
    def update(self, screenWidth, screenHeight):
        super(WaterBalloon, self).update(screenWidth, screenHeight)
        self.timeOnScreen += 1