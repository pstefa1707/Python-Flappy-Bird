import random

class Pipe:
    def __init__(self, PIPE_SPEED, PIPE_GAP, PIPE_DISTANCE, PIPE_WIDTH, PIPE_HEIGHT, WINDOW_HEIGHT, WINDOW_WIDTH, BASE_HEIGHT, UL_MARGIN):
        self.PIPE_GAP = PIPE_GAP
        self.PIPE_SPEED = PIPE_SPEED
        self.BASE_HEIGHT = BASE_HEIGHT
        self.PIPE_WIDTH = PIPE_WIDTH
        self.PIPE_DISTANCE = PIPE_DISTANCE
        self.WINDOW_HEIGHT = WINDOW_HEIGHT
        self.WINDOW_WIDTH = WINDOW_WIDTH
        self.xPos = WINDOW_WIDTH + PIPE_DISTANCE
        self.yLower = random.randrange(int(UL_MARGIN + PIPE_GAP), int(BASE_HEIGHT - UL_MARGIN))
        self.yUpper = (self.yLower - PIPE_GAP) - PIPE_HEIGHT
        self.childPole = False
        self.enabled = True
    
    def getLowerPos(self):
        return (self.xPos, self.yLower)
    
    def getUpperPos(self):
        return (self.xPos, self.yUpper)
    
    def updatePos(self):
        if self.xPos < self.WINDOW_WIDTH and not self.childPole:
            self.childPole = True
            self.xPos -= self.PIPE_SPEED
            return False
        else:
            self.xPos -= self.PIPE_SPEED
            return True
    
    def collisionChecks(self, birdPos, birdSize):
        birdRight = birdPos[0] + birdSize[0]
        birdLeft = birdPos[0]
        birdBottom = birdPos[1] + birdSize[1]
        birdUpper = birdPos[1]
        pipeRight = self.xPos + self.PIPE_WIDTH
        pipeLeft = self.xPos
        if self.enabled:
            if birdLeft > pipeRight:
                self.enabled = False
                return "awardPoint"
            elif birdLeft <= pipeRight and birdRight >= pipeLeft:
                if birdUpper <= (self.yLower - self.PIPE_GAP) or birdBottom >= self.yLower:
                    self.enabled = False
                    return "collision"
        else:
            return None
