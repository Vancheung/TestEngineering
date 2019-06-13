class Field:
    def __init__(self,X,Y):
        self.X = X
        self.Y = Y
        self.obstacles = []

    def setObstacle(self,x,y):
        self.obstacles.append((x,y))

    def getObstacle(self):
        return self.obstacles
