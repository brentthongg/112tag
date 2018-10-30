# Main (starter) file - This file starts the game and runs it. Has the keypressed, timer fired, etc. functions that run the game itself.
# Layout taken from Lukas Peraza's Asteroid game demo!

import pygame
from pygamegame import PygameGame
from Initialize import *
from GameObject import GameObject
from Background import Background
from Updates import *
from Maze import Maze
from Player import Player
from Start import *
from ItemDrop import ItemDrop

class Main(PygameGame):
    
    ## Initializing Functions:
    
    def init(self):
        setBackground(self)
        setPlayer(self)
        setBalloons(self)
        initializeMaze(self)
        initializeOpponent(self)
        initializeItems(self)
        self.timer = 0
        self.willQuit = False

    ## Keyboard Functions:

    def keyPressed(self, code, mod):
        if self.gameLost or self.gameWon:
            if code == pygame.K_r: Main.init(self) # Restarts the game
        
        if code == pygame.K_SPACE:
            Main.placeBalloon(self)
            
        if self.helpScreen and code == pygame.K_b: 
            self.starterScreen = True
            self.helpScreen = False
            self.backGround = Background("images/backgrounds/Start Background.png", (0,0))
        
        opponent = self.opponentGroup.sprites()[0]
        if self.inGame and code == pygame.K_n and opponent.level < 3:
            self.nextLevel = True
            self.gameOver = True
            
        if self.inGame and code == pygame.K_l:
            opponent.gotHit()
            
    def placeBalloon(self):
        player = self.playerGroup.sprites()[0]
        if player.numBalloons > player.usedBalloons:
            self.waterBalloons.add(WaterBalloon(player.row, player.col, "Player"))
            player.usedBalloons += 1

    ## Mouse Functions:
    
    def mouseReleased(self, x, y):
        pressButton(self, x, y)
        checkIfQuit(self, x, y)
        if self.nextLevel:
            levelBefore = self.opponentGroup.sprites()[0].level
            self.nextLevel = False
            self.gameOver = False
            setPlayer(self)
            setBalloons(self)
            initializeMaze(self)
            initializeOpponent(self)
            initializeItems(self)
            self.timer = 0
            self.opponentGroup.sprites()[0].level = levelBefore + 1

    
    ## Timer (Update) Functions:
    
    def timerFired(self, dt):
        self.timer += 1
        if self.playerGroup.sprites()[0].lives <= 0: 
            self.gameLost = True
            self.gameOver = True
            return
        
        elif self.opponentGroup.sprites()[0].level == 3 and self.opponentGroup.sprites()[0].lives <= 0:
            self.gameWon = True
            self.gameOver = True
            return
        
        elif self.opponentGroup.sprites()[0].level < 3 and self.opponentGroup.sprites()[0].lives <= 0:
            self.nextLevel = True
            self.gameOver = True
            return
        
        if self.inGame and not self.gameOver:
            self.waterBalloons.update(self.width, self.height)
            explosions(self)
            updateBalloonCount(self)
            player = self.playerGroup.sprites()[0]
            player.update(self.isKeyPressed, self.width, self.height, self.maze)
            self.balloonExplosions.update(dt)
            checkItemGrabbed(self)
            compSpeed = self.opponentGroup.sprites()[0].speed
            if self.timer % (10 - compSpeed) == 0:
                self.opponentGroup.update(self.maze, player, self.items, self.waterBalloons)
    
    ## Drawing Functions:
    
    def drawScore(self, screen):
        playerLives = self.playerGroup.sprites()[0].lives
        enemyLives = self.opponentGroup.sprites()[0].lives
        font = pygame.font.SysFont("Avenir", 12)
        text = font.render("Your lives: %d     Enemy lives: %d" % (playerLives, enemyLives), 1, (0, 0, 0))
        screen.blit(text, (self.width // 2, self.height - 20))
    
    def countItems(self, screen):
        #Getting amount of power:
        player = self.playerGroup.sprites()[0]
        numSword = player.powerLevel - 1
        numBalloons = player.numBalloons - 1
        hasArmor = player.isArmored
        amountBoots = player.speed - 1
        
        font = pygame.font.SysFont("Avenir", 28)
        textSword = font.render(str(numSword), 1, (0, 0, 0))
        textBalloons = font.render(str(numBalloons), 1, (0, 0, 0))
        textSpeed = font.render(str(amountBoots), 1, (0, 0, 0))
        if hasArmor:
            textArmor = font.render("1", 1, (0, 0, 0))
        else: textArmor = font.render("0", 1, (0, 0, 0))
        screen.blit(textSword, (950, 100))
        screen.blit(textBalloons, (1100, 100))
        screen.blit(textArmor, (950, 170))
        screen.blit(textSpeed, (1100, 170))
    
    def redrawAll(self, screen):
        if self.starterScreen: 
            screen.blit(self.backGround.image, (0, 0)) #stackoverflow.com/questions/28005641/how-to-add-a-background-image-into-pygame
            startScreen(self, screen)
        
        if self.inGame:
            screen.blit(self.map, (25, 25))
            self.maze.draw(screen)
            self.waterBalloons.draw(screen)
            self.items.draw(screen)
            self.balloonExplosions.draw(screen)
            screen.blit(self.backGround.image, (0, 0))
            self.playerGroup.draw(screen)
            self.opponentGroup.draw(screen)
            screen.blit(self.quitImage, (1065, 475))
            Main.drawScore(self, screen)
            Main.countItems(self, screen)
            if self.willQuit: Main.init(self)
                
        if self.helpScreen:
            screen.blit(self.backGround.image, (0, 0))

        if self.gameWon:
            dimensions = (0, 150, 1200, 300)
            pygame.draw.rect(screen, (255, 50, 50), dimensions)
            font = pygame.font.SysFont("Helvetica", 40)
            text = font.render("You won! Press 'R' to play again!", 1, (0, 0, 0))
            screen.blit(text, (self.width // 2 - 300, self.height // 2))
        
        if self.gameLost:
            dimensions = (0, 150, 1200, 300)
            pygame.draw.rect(screen, (255, 50, 50), dimensions)
            font = pygame.font.SysFont("Helvetica", 40)
            text = font.render("Game Over! Press 'R' to play again!", 1, (0, 0, 0))
            screen.blit(text, (self.width // 2 - 300, self.height // 2))
            
        if self.nextLevel:
            dimensions = (0, 150, 1200, 300)
            pygame.draw.rect(screen, (50, 100, 255), dimensions)
            font = pygame.font.SysFont("Helvetica", 40)
            text = font.render("Click anywhere to start the next level!", 1, (0, 0, 0))
            screen.blit(text, (self.width // 2 - 330, self.height // 2))
            

Main(1200, 600).run()
    