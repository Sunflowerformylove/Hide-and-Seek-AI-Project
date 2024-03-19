from Support import *
import random

# 2: Hider cell
# 6: anounced cell

class Hider:
    # Initialize a Hider
    def __init__(self, map, N, M):
        self.map = map
        self.N = N
        self.M = M
        self.posX = random.randint(0, M-1)
        self.posY = random.randint(0, N-1)
        # posY: row
        # posX: column
        while map[self.posY][self.posX] == 1 or map[self.posY][self.posX] == 2 or map[self.posY][self.posX] == 3:
            self.posX = random.randint(0, M)
            self.posY = random.randint(0, N)
        map[self.posY][self.posX] = 2
        self.announcePos = None
        self.step = 0

    # Funtion to get Seeker's position if Hider can observe him
    def observeSeeker(self, visions):
        for i in range(len(visions)):
            if self.map[visions[i][0]][visions[i][1]] == 3: return visions[i]
        return None

    # Function to get list visions of Hider
    def get_visions(self):
        return logic_vision(self.map, 2, self.posY, self.posX, self.N, self.M)
    
    # Function to randomly announce cell close to current position of Hider, in Hider's vision
    # 6: announced cell
    def announce(self, visions):
        if self.announcePos != None: 
            self.map[self.announcePos[0]][self.announcePos[1]] = 0
        pos = (random.randint(self.posY-2, self.posY+2), random.randint(self.posX2, self.posX+2))
        while self.map[pos[0]][pos[1]] == 1 or self.map[pos[0]][pos[1]] == 2 or self.map[pos[0]][pos[1]] == 3:
            pos = (random.randint(self.posY-2, self.posY+2), random.randint(self.posX2, self.posX+2))
        self.announcePos = pos
        self.map[pos[0]][pos[1]] = 6

    # Funtion to randomly move the Hider
    def move(self):
        visions = self.get_visions()
        self.step += 1
        if self.step % 6 == 0: 
            self.announce(visions)
        seekerPos = self.observeSeeker(visions)
        newPos = None

        if seekerPos == None:
            newPos = random.choice(visions)
            while self.map[self.newPosY][self.newPosX] == 1 or self.map[self.newPosY][self.newPosX] == 2 or self.map[self.newPosY][self.newPosX] == 3:
                newPos = random.choice(visions)
        else:
            maxDist = -math.inf
            for i in range(len(visions)):
                dist = manhattanDist(visions[i][0], visions[i][1], seekerPos[0], seekerPos[1])
                if dist > maxDist:
                    maxDist = dist
                    newPos = visions[i]

        self.posY = newPos[0]
        self.posX = newPos[1]
        self.map[self.posY][self.posX] = 2  
