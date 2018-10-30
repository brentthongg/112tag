# This file handles a lot of the functions in timerFired, which I want to update regularly.

import pygame
import random
from WaterBalloon import WaterBalloon
from BalloonExplosion import BalloonExplosion
from ItemDrop import ItemDrop

def explosions(self):
    player = self.playerGroup.sprites()[0]
    compPlayer = self.opponentGroup.sprites()[0]
    for balloon in self.waterBalloons:
        if balloon.timeOnScreen > WaterBalloon.time:
            self.balloonExplosions.add(BalloonExplosion(balloon.row, balloon.col, 0))
            if balloon.owner == "Player":
                powerLevel = player.powerLevel
            else: powerLevel = compPlayer.powerLevel
            for power in range(powerLevel):
                power += 1
                self.balloonExplosions.add(BalloonExplosion(balloon.row, balloon.col - power, 270))
                self.balloonExplosions.add(BalloonExplosion(balloon.row, balloon.col + power, 90)) 
                self.balloonExplosions.add(BalloonExplosion(balloon.row - power, balloon.col, 0))
                self.balloonExplosions.add(BalloonExplosion(balloon.row + power, balloon.col, 180))
            balloon.kill()
            removal(self)   

def removal(self):
    for wall in self.maze:
        if wall.type == 2: continue
        for explosion in self.balloonExplosions:
            if explosion.row == wall.row and explosion.col == wall.col:
                if chance(30): # 30% chance
                    self.items.add(ItemDrop(wall.row, wall.col))
                wall.kill()

    player = self.playerGroup.sprites()[0]
    computer = self.opponentGroup.sprites()[0]

    for explosion in self.balloonExplosions:
        if explosion.row == player.row and explosion.col == player.col:
            player.gotHit()

        if explosion.row == computer.row and explosion.col == computer.col:
            computer.gotHit()

def chance(n):
    x = random.randint(0, 99)
    return x < n
    
def updateBalloonCount(self):
    player, comp = 0, 0
    for balloon in self.waterBalloons:
        if balloon.owner == "Player":
            player += 1
        elif balloon.owner == "Computer":
            comp += 1
    self.playerGroup.sprites()[0].usedBalloons = player
    self.opponentGroup.sprites()[0].usedBalloons = comp
    
def checkItemGrabbed(self):
    player = self.playerGroup.sprites()[0]
    computer = self.opponentGroup.sprites()[0]
    
    for item in self.items:
        if item.row == player.row and item.col == player.col:
            acquireBenefits(player, item)
        elif item.row == computer.row and item.col == computer.col:
            acquireBenefits(computer, item)

def acquireBenefits(person, item):
    if item.itemType == "Speed":
        if person.speed < 3:
            person.speed += 1
    elif item.itemType == "Armor":
        person.isArmored = True
    elif item.itemType == "Balloon":
        if person.numBalloons < 5:
            person.numBalloons += 1
    elif item.itemType == "Power":
        if person.powerLevel < 5:
            person.powerLevel += 1

    item.kill()
    