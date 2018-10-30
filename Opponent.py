# A* ALGORITHM USED FOR RUNNING AWAY AND FINDING SHORTEST PATH FROM:
# https://www.redblobgames.com/pathfinding/a-star/introduction.html
# Implemented to fit the game.

# This file is for the opponent, which inherits from Player. Contains all the functions to make
# the AI run such as finding the path, the level it is, changing the self.x and self.y to move, etc.

import pygame
import math
import random
from WaterBalloon import WaterBalloon
from Player import Player
from queue import PriorityQueue, Queue

class Opponent(Player):
    
    @staticmethod
    def init():
        Player.playerImage = pygame.image.load("images/characters/stand1_0.png").convert_alpha() # Change this later!

    def __init__(self, row, col, numBalloons, powerLevel, lives):
        super(Opponent, self).__init__(row, col, numBalloons, powerLevel, lives)
        self.level = 1
        self.timeTrack = 0
        self.route = []
        self.done = True
        self.running = False
        
    ## General Funcitons:

    def gotHit(self):
        super(Opponent, self).gotHit()
        self.running = False
        self.route = []
        self.done = True

    def placeBalloon(self, balloons):
        if self.numBalloons > self.usedBalloons:
            balloons.add(WaterBalloon(self.row, self.col, "Computer"))
    
    def findItemPath(self, maze, item, balloons, other):
        if self.level == 1:
            return Opponent.findItemPathOne(self, maze, item)
        elif self.level == 2:
            return Opponent.findItemPathTwo(self, maze, item)
        elif self.level == 3:
            return Opponent.findItemPathThree(self, item, maze, balloons, other)
            
    def findPlayerPath(self, other, maze, balloons):
        if self.level == 1:
            pass # No such function...
        elif self.level == 2:
            return Opponent.findPlayerPathTwo(self, other, maze)
        elif self.level == 3:
            pass
    
    def findClosestItem(self, items):
        closestDistance = float("inf")
        closestItem = None
        for item in items:
            dist = Opponent.getDistance(self.row, self.col, item.row, item.col)
            if dist < closestDistance:
                closestItem = item
                closestDistance = dist
                
        return closestItem
    
    def findClosestBlock(self, maze):
        closestDistance = float("inf")
        closestBlock = None
        for block in maze:
            if block.type == 2: continue
            dist = Opponent.getDistance(self.row, self.col, block.row, block.col)
            if dist < closestDistance:
                closestBlock = block
                closestDistance = dist
                
        return closestBlock
    
    def getDistance(r1, c1, r2, c2):
        return abs(r1 - r2) + abs(c1 - c2)
        
    def getPossibleDirections(row, col, maze):
        directions = []
        canNorth, canSouth, canEast, canWest = True, True, True, True
        for wall in maze:
            if (row - 1 == wall.row) and (col == wall.col):
                canNorth = False
            
            if (row + 1 == wall.row) and (col == wall.col):
                canSouth = False
            
            if (col - 1 == wall.col) and (row == wall.row):
                canWest = False
            
            if (col + 1 == wall.col) and (row == wall.row):
                canEast = False
                
        if canNorth: directions.append((row-1, col))
        if canSouth: directions.append((row+1, col))
        if canEast: directions.append((row, col+1))
        if canWest: directions.append((row, col-1))
                
        return directions
                
    def runAway(self, other, balloons, maze):
        start = (self.row, self.col)
        mapping = Queue()
        mapping.put(start)
        cameFrom = dict()
        cameFrom[start] = None
        
        while not mapping.empty():
            current = mapping.get()

            if Opponent.outsideBalloonRadius(self, other, balloons, current):
                goal = (current[0], current[1])
                break
            for neighbor in Opponent.getMoves(self, current, maze):
                if neighbor not in cameFrom:
                    mapping.put(neighbor)
                    cameFrom[neighbor] = current

        if not Opponent.outsideBalloonRadius(self, other, balloons, current):
            return [(self.x, self.y)]
        current = goal
        path = []
        while current != start:
            path.append(current)
            current = cameFrom[current]

        path.append(start)
        path.reverse()
        return path
        
    def outsideBalloonRadius(self, other, balloons, current):
        r, c = current[0], current[1]
        for balloon in balloons:
            if balloon.owner == "Player":
                powerLevel = other.powerLevel
            elif balloon.owner == "Computer":
                powerLevel = self.powerLevel
            
            if abs(r - balloon.row) <= powerLevel and c == balloon.col: return False
            elif abs(c - balloon.col) <= powerLevel and r == balloon.row: return False
        
        return True
    
    def getMoves(self, current, maze, hasTarget = False, target = None):
        result = []
        row, col = current[0], current[1]
        
        for direction in ["N", "S", "E", "W"]: 
            canAppend = True
            for block in maze:
                if hasTarget:
                    if target == block: continue
                if direction == "N":
                    drow, dcol = -1, 0
                    if block.row == row + drow and block.col == col:
                        canAppend = False
                    if row + drow < 0: canAppend = False
                elif direction == "S":
                    drow, dcol = 1, 0
                    if block.row == row + drow and block.col == col:
                        canAppend = False
                    if row + drow > 10: canAppend = False
                elif direction == "E":
                    drow, dcol = 0, 1
                    if block.row == row and block.col == col + dcol:
                        canAppend = False
                    if col + dcol > 14: canAppend = False
                elif direction == "W":
                    drow, dcol = 0, -1
                    if block.row == row and block.col == col + dcol:
                        canAppend = False
                    if col + dcol < 0: canAppend = False
            if canAppend:
                newTuple = (row + drow, col + dcol)
                result.append(newTuple)
        return result

    ## Level One Algorithm and Functions:
    """ The level 1 AI has the following algorithm:
    --> First looks for an item, then goes randomly. If it is within the radius of a block or player, places
            a bomb then continues in a direction. """
    
    def findItemPathOne(self, maze, item, path = None): # Not necessarily the fastest path, but first one found.
        if path == None: path = [(self.row, self.col)]
        
        row, col = path[-1][0], path[-1][1]
        if row == item.row and col == item.col:
            return path

        for move in Opponent.getPossibleDirections(row, col, maze):
            if Opponent.inBoundaries(move) and move not in path:
                path.append(move)
                tempSolution = Opponent.findItemPathOne(self, maze, item, path)
                if tempSolution != None: return tempSolution
                path.append((row, col))

        return None
        
    def inBoundaries(move): # Helper Function
        row, col = move[0], move[1]
        left, right = 0, 14
        top, bottom = 0, 10
        
        if col < left or col > right: return False
        if row < top or row > bottom: return False

        return True
    
    def randomlyWalk(self, maze, other):
        path = [(self.row, self.col)]
        
        direction = ["N", "S", "E", "W"][random.randint(0, 3)]
        
        if direction == "N": drow, dcol = -1, 0
        elif direction == "S": drow, dcol = 1, 0
        elif direction == "E": drow, dcol = 0, 1
        elif direction == "W": drow,dcol = 0, -1
        conflict = False
        
        while True:
            r = path[-1][0]
            c = path[-1][1]
            newTuple = (r + drow, c + dcol)
            for wall in maze:
                if wall.row == newTuple[0] and wall.col == newTuple[1]:
                    conflict = True

            if newTuple[0] < 0 or newTuple[0] > 10 or newTuple[1] < 0 or newTuple[1] > 14:
                break
            
            if conflict: break
            
            path.append(newTuple)
            if newTuple[0] == other.row and newTuple[1] == other.col:
                break
        
        return path
        
    def algorithmOne(self, maze, other, items, balloons):

        w, h = 50, 50
        self.rect = pygame.Rect(self.x - 25, self.y - 50, w, h) 

        if self.done:

            nearest = Opponent.findClosestItem(self, items)
            if nearest != None:
                self.route = Opponent.findItemPath(self, maze, nearest, balloons, other)
                if self.route == None:
                    self.route = Opponent.randomlyWalk(self, maze, other)
            else: self.route = Opponent.randomlyWalk(self, maze, other)
            self.done = False
            
        if len(self.route) == 0: #End of going to where to place balloon
            self.running = True
            Opponent.placeBalloon(self, balloons)
            self.done = True
        
        elif len(self.route) > 0:
            
            self.row, self.col = self.route[0][0], self.route[0][1]
            self.route = self.route[1:]
            
    ## Level Two Algorithm and Functions:
    """
    The algorithm:
    --> First, check to see if there is a path to an item like before. v
    --> Then, check to see if there is a path to player. v
    --> Still won't be fastest route, but will go to player and try to hit them if there is an opportunity.
    --> If not, look for a block and drop balloon.
    --> Will run away from bombs.
    """
    
    def findPathToBlock(self, maze, block, path = None):
        if path == None: path = [(self.row, self.col)]

        currentRow, currentCol = path[-1][0], path[-1][-1]
        if Opponent.closeToBlock(self, currentRow, currentCol, block): return path
        
        for move in Opponent.getPossibleDirections(currentRow, currentCol, maze):
            if Opponent.inBoundaries(move) and move not in path:
                path.append(move)
                tempSolution = Opponent.findPathToBlock(self, maze, block, path)
                if tempSolution != None: return tempSolution
                path.append((currentRow, currentCol))

        return None

    def closeToBlock(self, r, c, block):
        if abs(r - block.row) <= self.powerLevel:
            if c == block.col: return True
        
        if abs(c - block.col) <= self.powerLevel:
            if r == block.row: return True
        
        return False
    
    def findItemPathTwo(self, maze, item, path = None):
        
        if path == None: path = [(self.row, self.col)]
        # The first path to look for an item works well, so just use it:
        return Opponent.findItemPathOne(self, maze, item, path)
        
    def findPlayerPathTwo(self, other, maze, path = None):
        
        if path == None: path = [(self.row, self.col)]
        
        currentRow, currentCol = path[-1][0], path[-1][1]
        if currentRow == other.row and currentCol == other.col:
            return path

        for move in Opponent.getPossibleDirections(currentRow, currentCol, maze):
            if Opponent.inBoundaries(move) and move not in path:
                path.append(move)
                tempSolution = Opponent.findPlayerPathTwo(self, other, maze, path)
                if tempSolution != None: return tempSolution
                path.append((currentRow, currentCol))
                
        return None
    
    def algorithmTwo(self, maze, other, items, balloons):
        w, h = 50, 50
        self.rect = pygame.Rect(self.x - 25, self.y - 50, w, h)

        if self.done:
            nearest = Opponent.findClosestItem(self, items)
            if nearest != None:
                self.route = Opponent.findItemPath(self, maze, nearest, balloons, other)
                if self.route == None:
                    self.route = Opponent.findPlayerPathTwo(self, other, maze)
                    if self.route == None:
                        targetBlock = Opponent.findClosestBlock(self, maze)
                        self.route = Opponent.findPathToBlock(self, maze, targetBlock)
            else:
                self.route = Opponent.findPlayerPathTwo(self, other, maze)
                if self.route == None:
                    targetBlock = Opponent.findClosestBlock(self, maze)
                    self.route = Opponent.findPathToBlock(self, maze, targetBlock)
            self.done = False
        
        if self.route == None:
            self.done = True
            return
        
        if len(self.route) == 0 and self.running == False:
            Opponent.placeBalloon(self, balloons)
            self.route = Opponent.runAway(self, other, balloons, maze)
            self.running = True
            
        if len(self.route) == 0 and self.running:
            self.timeTrack += 1
            if self.timeTrack % 5 == 0:
                self.done = True
                self.running = False
                self.timeTrack = 0
        
        elif len(self.route) > 0:
            
            self.row, self.col = self.route[0][0], self.route[0][1]
            self.route = self.route[1:]
             

    ## Level Three Algorithm and Functions:
    """
    The algorithm:
    --> First, check to see if there is a path to an item like before. This will be the
        fastest path to the item.
    --> Then, check to see if there is a path to a player, like before. This will be the
        fastest route.
    --> If not, look for a wall to drop a balloon.
    --> Will take into account things like how many balloons it has -- if the AI has more than
        one balloon, then will automatically look to drop another balloon somewhere, A.K.A. self.done is
        still true.
    --> Every path takes into account balloons, not just the run away one.
    """
    
    def algorithmThree(self, maze, other, items, balloons):
        
        w, h = 50, 50
        self.rect = pygame.Rect(self.x - 25, self.y - 50, w, h)
        
        if self.done:
            nearest = Opponent.findClosestItem(self, items)
            if nearest != None:
                self.route = Opponent.findItemPath(self, maze, nearest, balloons, other)
                if self.route == None:
                    self.route = Opponent.findPlayerPathThree(self, maze, balloons, other)
                    if self.route == None:
                        targetBlock = Opponent.findClosestBlock(self, maze)
                        self.route = Opponent.findBlockThree(self, targetBlock, balloons, other, maze)
            else:
                self.route = Opponent.findPlayerPathThree(self, maze, balloons, other)
                if self.route == None:
                    targetBlock = Opponent.findClosestBlock(self, maze)
                    self.route = Opponent.findBlockThree(self, targetBlock, balloons, other, maze)
            self.done = False
            
        if len(self.route) == 0 and self.running == False:
            Opponent.placeBalloon(self, balloons)
            self.route = Opponent.runAway(self, other, balloons, maze)
            self.running = True
            
        if len(self.route) == 0 and self.running:
            self.timeTrack += 1
            if self.timeTrack % 5 == 0:
                self.done = True
                self.running = False
                self.timeTrack = 0
        
        elif len(self.route) > 0:
            
            self.row, self.col = self.route[0][0], self.route[0][1]
            self.route = self.route[1:]
            
    def findPlayerPathThree(self, maze, balloons, other):
        start = ((self.row, self.col))
        goal = (other.row, other.col)
        mapping = PriorityQueue()
        mapping.put(start, 0)
        cameFrom = dict()
        costSoFar = dict()
        cameFrom[start] = None
        costSoFar[start] = 0
        
        while not mapping.empty():
            current = mapping.get()
            
            if current == goal:
                break
                
            for neighbor in Opponent.getMoves(self, current, maze):
                newCost = costSoFar[current] + Opponent.getCost(self, neighbor, maze, balloons, other)
                if neighbor not in costSoFar or newCost < costSoFar[neighbor]:
                    costSoFar[neighbor] = newCost
                    priority = newCost + Opponent.heuristic(goal, neighbor)
                    mapping.put(neighbor, priority)
                    cameFrom[neighbor] = current
        
        if mapping.empty() and not current == goal:
             return None # No solution
                    
        current = goal
        path = list()
        while current != start:
            path.append(current)
            current = cameFrom[current]
        
        path.append(start)
        path.reverse()
        return path
    
    def findBlockThree(self, block, balloons, other, maze):
        start = ((self.row, self.col))
        mapping = PriorityQueue()
        mapping.put(start, 0)
        cameFrom = dict()
        costSoFar = dict()
        cameFrom[start] = None
        costSoFar[start] = 0
        
        while not mapping.empty():
            current = mapping.get()
            
            r, c = current[0], current[1]
            if Opponent.closeToBlock(self, r, c, block):
                goal = r, c
                break
            
            for neighbor in Opponent.getMoves(self, current, maze):
                newCost = costSoFar[current] + Opponent.getCost(self, neighbor, maze, balloons, other)
                if neighbor not in costSoFar or newCost < costSoFar[neighbor]:
                    costSoFar[neighbor] = newCost
                    priority = newCost + Opponent.heuristic((block.row, block.col), neighbor)
                    mapping.put(neighbor, priority)
                    cameFrom[neighbor] = current
                    
        if mapping.empty() and not Opponent.closeToBlock(self, r, c, block):
             return None # No solution
             
        current = goal
        path = list()
        while current != start:
            path.append(current)
            current = cameFrom[current]
        
        path.append(start)
        path.reverse()
        return path
        
            
    def findItemPathThree(self, item, maze, balloons, other):
        start = ((self.row, self.col))
        mapping = PriorityQueue()
        mapping.put(start, 0)
        cameFrom = dict()
        costSoFar = dict()
        cameFrom[start] = None
        costSoFar[start] = 0
        
        while not mapping.empty():
            current = mapping.get()
            
            r, c = current[0], current[1]
            if r == item.row and c == item.col:
                goal = (current[0], current[1])
                break
            
            for neighbor in Opponent.getMoves(self, current, maze):
                newCost = costSoFar[current] + Opponent.getCost(self, neighbor, maze, balloons, other)
                if neighbor not in costSoFar or newCost < costSoFar[neighbor]:
                    costSoFar[neighbor] = newCost
                    priority = newCost + Opponent.heuristic((item.row, item.col), neighbor)
                    mapping.put(neighbor, priority)
                    cameFrom[neighbor] = current
                    
        if mapping.empty() and not (r == item.row and c == item.col):
             return None # No solution
             
        current = goal
        path = list()
        while current != start:
            path.append(current)
            current = cameFrom[current]
        
        path.append(start)
        path.reverse()
        return path
        
    def heuristic(goal, neighbor):
        return abs(goal[0] - neighbor[0]) + abs(goal[1] - neighbor[1])
        
    def getCost(self, neighbor, maze, balloons, other):
        for wall in maze:
            if wall.row == neighbor[0] and wall.col == neighbor[1]:
                return 10000000 # Arbitrary large number!!
        return 1
        
        for balloon in balloons:
            if balloon.owner == "Player":
                powerLevel = other.powerLevel
            else: powerLevel = self.powerLevel
            if abs(balloon.row - neighbor[0]) <= powerLevel and abs(balloon.col - neighbor[1]) <= powerLevel:
                return 500000
        return 1

    ## Update:
    
    def update(self, maze, other, items, balloons):
        if self.level == 1:
            Opponent.algorithmOne(self, maze, other, items, balloons)
        elif self.level == 2:
            Opponent.algorithmTwo(self, maze, other, items, balloons)
        elif self.level == 3:
            Opponent.algorithmThree(self, maze, other, items, balloons)
            
        self.x, self.y = (((self.col + 1) * 50), ((self.row + 1) * 50))