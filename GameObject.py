#This was basically taken from Lukas's GameObject file, except adjusted slightly. 
#Main class for most game objects.

import pygame

class GameObject(pygame.sprite.Sprite): 
    
    def __init__(self, row, col, image):
        super(GameObject, self).__init__()
        self.row, self.col = row, col
        marginSize = 25
        w, h = image.get_size()
        self.x, self.y, self.image = (col * 50) + (w / 2) + marginSize, (row * 50) + (h / 2) + marginSize, image
        self.drow, self.dcol = 0, 0
        self.rect = pygame.Rect(self.x - w / 2, self.y - h / 2, w, h)

    def update(self, screenWidth, screenHeight):
        self.row += self.drow
        self.col += self.dcol
        marginSize = 25
        self.x, self.y = (self.col * 50) + marginSize + 25, (self.row * 50) + marginSize + 25
        self.drow, self.dcol = 0, 0