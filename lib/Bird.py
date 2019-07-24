class Bird:
    def __init__(self, WINDOW_WIDTH, WINDOW_HEIGHT, FALL_VELOCITY, JUMP_VELOCITY, JUMP_HEIGHT, BASE_HEIGHT):
        self.counter = 0
        self.pos = (int(WINDOW_WIDTH * 0.2), int(WINDOW_HEIGHT * 0.5))
        self.aniIter = 0
        self.jumpState = False
        self.jumpOrigin = 0
        self.BASE_HEIGHT = BASE_HEIGHT
        self.JUMP_VELOCITY = JUMP_VELOCITY
        self.FALL_VELOCITY = FALL_VELOCITY
        self.JUMP_HEIGHT = JUMP_HEIGHT
    
    def getPos(self):
        return self.pos
    
    def getAniIter(self):
        return self.aniIter

    def updatePos(self):
        if self.jumpState:
            if (self.jumpOrigin - (self.pos[1] - self.JUMP_VELOCITY)) > self.JUMP_HEIGHT:
                self.jumpState = False
                self.setPos(self.jumpOrigin - self.JUMP_HEIGHT)
            else:
                self.setPos(self.pos[1] - self.JUMP_VELOCITY)
        else:
            self.setPos(self.pos[1] + self.FALL_VELOCITY)

    def setPos(self, newPos):
        lst = list(self.pos)
        lst[1] = newPos
        self.pos = tuple(lst)
    
    def incrementAniIter(self):
        self.aniIter += 1
        if self.aniIter > 2:
            self.aniIter = 0

    def incrementCounter(self):
        self.counter += 1
    
    def jump(self):
        self.jumpOrigin = self.pos[1]
        self.jumpState = True
    
    def uLCollision(self):
        if self.pos[1] <= 0 or (self.pos[1]+21) >= self.BASE_HEIGHT:
            return True
        return False