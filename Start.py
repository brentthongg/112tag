# Start screen functions, such as pressing the button to play the game and stuff.
import pygame
from Background import Background

def startScreen(self, screen):
    
    self.playRect = (self.width // 2 - 150, self.height // 2 - 30, 
                        300, 60)
                        
    pygame.draw.rect(screen, (20, 200, 255), self.playRect)
    
    # Next three lines taken from https://stackoverflow.com/questions/10077644/python-display-text-with-font-color
    font = pygame.font.SysFont("Helvetica", 25)
    text = font.render("Play Game!", 1, (0, 0, 0))
    screen.blit(text, (self.width / 2 - 65, self.height / 2 - 10))
    
    self.helpRect = (self.width // 2 - 150, self.height // 2 + 80,
                        300, 60)
                        
    pygame.draw.rect(screen, (20, 200, 255), self.helpRect)
    
    font = pygame.font.SysFont("Helvetica", 25)
    text = font.render("Instructions", 1, (0, 0, 0))
    screen.blit(text, (self.width / 2 - 65, self.height // 2 + 100))
    
def pressButton(self, x, y):

    if self.starterScreen:
        if x > (self.width // 2 - 150) and x < (self.width // 2 + 150):
            if y > (self.height // 2 - 30) and y < (self.height // 2 + 30):
                self.starterScreen = False
                self.inGame = True
                self.backGround = Background("images/backgrounds/layout.png", (0, 0))

            if y > (self.height // 2) + 80 and y < (self.height // 2 + 140):
                self.starterScreen = False
                self.helpScreen = True
                self.backGround = Background("images/backgrounds/help.png", (0, 0))

def checkIfQuit(self, x, y):
    if self.inGame:
        if x > 1065 and x < 1175 and y > 475 and y < 575:
            self.willQuit = True