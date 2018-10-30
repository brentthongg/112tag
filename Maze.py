# This class holds all the tiles/walls. 

import pygame
import random
from GameObject import GameObject

class Maze(GameObject):
    
    @staticmethod
    def init():
        Maze.orangeTile = pygame.image.load("images/objects/tiles/orange-tile.png").convert_alpha()
        Maze.blueTile = pygame.image.load("images/objects/tiles/blue-tile.png").convert_alpha()
        Maze.redTile = pygame.image.load("images/objects/tiles/red-tile.png").convert_alpha()
        Maze.tileList = [Maze.orangeTile, Maze.blueTile]
    
    def __init__(self, row, col, type):
        self.type = type
        if self.type == 1:
            self.image = Maze.tileList[random.randint(0,1)]
        elif self.type == 2: 
            self.image = Maze.redTile
            
        super(Maze, self).__init__(row, col, self.image)
        
    def __hash__(self):
        return hash((self.row, self.col))

    def __eq__(self, other):
        return (isinstance(other, Maze) and self.row == other.row and self.col == other.col)