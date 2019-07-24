class Scroller:
    def __init__(self, sprite, vel, WINDOW_WIDTH):
        self.sprite = sprite
        self.spriteWidth = sprite.get_width()
        self.imageOne = 0
        self.imageTwo = self.spriteWidth
        self.velocity = vel
        self.WINDOW_WIDTH = WINDOW_WIDTH
    
    def updatePositions(self):
        self.imageOne -= self.velocity
        self.imageTwo -= self.velocity

        if self.imageTwo <= 0:
            self.imageOne = self.imageTwo + self.spriteWidth
            temp = self.imageOne
            self.imageOne = self.imageTwo
            self.imageTwo = temp

        return (self.imageOne, self.imageTwo)
    
