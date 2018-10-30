# This file handles all the item drops that one can obtain.

import pygame
from GameObject import GameObject
import random

class ItemDrop(GameObject):
    
    @staticmethod
    def init():
        image = pygame.image.load("images/objects/items.png")
        rows, cols = 2, 2
        width, height = image.get_size()
        cellWidth, cellHeight = width / cols, height / rows
        ItemDrop.itemList = []
        for row in range(rows):
            for col in range(cols):
                subImage = image.subsurface(
                    (col * cellWidth, row * cellHeight, cellWidth, cellHeight))
                ItemDrop.itemList.append(subImage)
        
    def __init__(self, row, col):
        itemNum = random.randint(0, 3)
        
        if itemNum == 0:
            self.itemType = "Speed"
        elif itemNum == 1:
            self.itemType = "Armor"
        elif itemNum == 2:
            self.itemType = "Power"
        elif itemNum == 3:
            self.itemType = "Balloon"
            
        itemImage = ItemDrop.itemList[itemNum]
        
        super(ItemDrop, self).__init__(row, col, itemImage)