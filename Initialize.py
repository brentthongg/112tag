# This file starts all the constants, loads all the iamges, etc... basically starts the game.

import pygame
import random
import copy
from Player import Player
from Maze import Maze
from WaterBalloon import WaterBalloon
from BalloonExplosion import BalloonExplosion
from Opponent import Opponent
from Background import Background
from ItemDrop import ItemDrop

def setBackground(self):
    
    self.bgColor = (255, 255, 255)
    self.backGround = Background("images/backgrounds/Start Background.png", (0,0))
    self.gameWon = False
    self.gameLost = False
    self.nextLevel = False
    
    self.starterScreen = True
    self.helpScreen = False
    self.inGame = False
    self.gameOver = False
    
    self.quitImage = pygame.image.load("images/buttons/quit.png").convert_alpha()
    self.map = pygame.image.load("images/backgrounds/map1.png").convert_alpha()
    
def setPlayer(self):
    
    # Constants:
    startRow = 10
    startCol = 0
    numLives = 3
    startingNumBalloons = 1
    startingPower = 1
    
    Player.init()
    player = Player(startRow, startCol, startingNumBalloons, startingPower, numLives)
    self.playerGroup = pygame.sprite.GroupSingle(player)
    
def setBalloons(self):
    
    WaterBalloon.init()
    self.waterBalloons = pygame.sprite.Group()
    BalloonExplosion.init()
    self.balloonExplosions = pygame.sprite.Group()

def initializeMaze(self):
    
    self.maze = pygame.sprite.Group()
    margin = 50
    Maze.init()

    mazeList = [ # 0's are tiles that you can go on, 1's are blocks.
    [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
    [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
    [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
    [2, 2, 2, 0, 0, 0, 1, 1, 1, 0, 0, 0, 2, 2, 2],
    [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
    [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
    [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0]
                    ]
                    
    board = randomizeMaze(mazeList)

    for row in range(len(board)):
        for col in range(len(board[row])):
            if board[row][col] == 1:
                self.maze.add(Maze(row, col, 1))
            elif board[row][col] == 2:
                self.maze.add(Maze(row, col, 2))
                
def randomizeMaze(previousBoard):
    
    #Just in case of aliasing:
    newBoard = copy.deepcopy(previousBoard)
    for i in range(len(previousBoard)):
        for j in range(len(previousBoard[i])):
            if i < 3 and j < 3: continue
            elif i < 3 and j > 11: continue
            elif i > 7 and j < 3: continue
            elif i > 7 and j > 11: continue
            
            if chance(40):
                if chance(60): newBoard[i][j] = 1
                else: newBoard[i][j] = 2
    
    return newBoard

def initializeOpponent(self):
    Opponent.init()
    numBalloons = 1
    startPower = 1
    startLives = 3
    startRow = 0
    startCol = 14
    
    opponent = Opponent(startRow, startCol, numBalloons, startPower, startLives)
    self.opponentGroup = pygame.sprite.GroupSingle(opponent)
    
def initializeItems(self):
    ItemDrop.init()
    self.items = pygame.sprite.Group()
    
def chance(n):
    return random.randint(0, 99) < n