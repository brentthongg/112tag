# Basic layout from Lukas Peraza's ship part of the demo. This file basically creates the palyer and all of their attributes such as things like how many balloons, power, has armor, row and col, etc. Also moves the player and things like that.

import pygame
from GameObject import GameObject

class Player(GameObject):
    
    @staticmethod
    def init():
        Player.playerImage = pygame.image.load("images/characters/standing_1.png").convert_alpha()

    def __init__(self, row, col, numBalloons, powerLevel, lives):
        super(Player, self).__init__(row, col, Player.playerImage)
        self.startRow = row
        self.startCol = col
        self.numBalloons = numBalloons
        self.usedBalloons = 0
        self.powerLevel = powerLevel
        self.goingRight = False
        self.goingLeft = True
        self.lives = lives
        self.isArmored = False
        self.timer = 0
        self.speed = 1
        self.canMove = True
        w, h = 50, 50
        self.rect = pygame.Rect(self.x - 25, self.y - 50, w, h) 
        
    def update(self, keysDown, screenWidth, screenHeight, maze):
        self.timer += 1
        
        if self.timer % (5 - self.speed) == 0:
            self.canMove = True
            self.timer = 0
        
        if self.canMove:
            
            w, h = 50, 50
            self.rect = pygame.Rect(self.x - 25, self.y - 50, w, h) 
    
            Player.checkPlayerCollision(self, maze, keysDown)
    
            if self.col > 0 and keysDown(pygame.K_LEFT) and self.l:
                self.drow, self.dcol = 0, -1
                if self.goingRight:
                    self.goingRight = False
                    self.goingLeft = True
                    self.image = pygame.transform.flip(self.image, True, False)
                
            if self.col < 14 and keysDown(pygame.K_RIGHT) and self.r:
                self.drow, self.dcol = 0, 1
                if self.goingLeft:
                    self.goingLeft = False
                    self.goingRight = True
                    self.image = pygame.transform.flip(self.image, True, False)
            
            if self.row > 0 and keysDown(pygame.K_UP) and self.t:
                self.drow, self.dcol = -1, 0
                
            if self.row < 10 and keysDown(pygame.K_DOWN) and self.b:
                self.drow, self.dcol = 1, 0
                
            self.canMove = False
        
        super(Player, self).update(screenWidth, screenHeight)
        
    def checkPlayerCollision(self, maze, keysDown):
        self.t, self.b, self.l, self.r = True, True, True, True
        for wall in maze:
            wallRow, wallCol = wall.row, wall.col
            
            if keysDown(pygame.K_UP):
                if self.row - 1 == wallRow and self.col == wallCol:
                    self.t = False
            if keysDown(pygame.K_DOWN):
                if self.row + 1 == wallRow and self.col == wallCol:
                    self.b = False
            if keysDown(pygame.K_RIGHT):
                if self.row == wallRow and self.col + 1 == wallCol:
                    self.r = False
            if keysDown(pygame.K_LEFT):
                if self.row == wallRow and self.col - 1 == wallCol:
                    self.l = False
    
    def gotHit(self):
        if not self.isArmored:
            self.lives -= 1
            self.row, self.col = self.startRow, self.startCol
        else: 
            self.isArmored = False