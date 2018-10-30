# Taken from Explosion.py from Asteroid Game by Lukas Peraza, makes the sprites for the balloon splashing.

import pygame
from GameObject import GameObject

class BalloonExplosion(pygame.sprite.Sprite):
    
    @staticmethod
    def init():
        image = pygame.image.load("images/objects/splashes.gif").convert_alpha()
        row, col = 2, 2
        width, height = image.get_size()
        cellWidth, cellHeight = width / col, height / row
        BalloonExplosion.frames = []
        for i in range(row):
            for j in range(col):
                subImage = image.subsurface(
                    (j * cellWidth, i * cellHeight, cellWidth, cellHeight))
                BalloonExplosion.frames.append(subImage)
        
    def __init__(self, row, col, angle): 
        newFrames = []
        for image in BalloonExplosion.frames:
            image = pygame.transform.rotate(image, angle)
            newFrames.append(image)
        BalloonExplosion.frames = newFrames
            
        super(BalloonExplosion, self).__init__()

        self.row, self.col = row, col
        marginSize = 25
        self.x, self.y = (col * 50) + 25 + marginSize, (row * 50) + 25 + marginSize
        self.frame = 0
        self.frameRate = 20
        self.aliveTime = 0

        self.updateImage()

    def updateImage(self):
        self.image = BalloonExplosion.frames[self.frame]
        w, h = self.image.get_size()
        self.rect = pygame.Rect(self.x - w / 2, self.y - h / 2, w, h)

    def update(self, dt):
        self.aliveTime += dt
        self.frame = self.aliveTime // (1000 // self.frameRate)
        if self.frame < len(BalloonExplosion.frames):
            self.updateImage()
        else:
            self.kill()