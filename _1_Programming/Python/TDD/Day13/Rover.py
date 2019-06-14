from Location import *
class Rover:
    def __init__(self,location,orientation):
        self.location = location
        self.orientation = orientation
        self.movemap = {
            'F': self.moveForward,
            'B': self.moveBack,
            'L': self.turnLeft,
            'R': self.turnRight
        }

    def moveForward(self,field):
        newlocation = self.orientation.moveF(self.location)
        # if meet or out: return Exception
        if field.isObstacle(newlocation):
            raise Exception
        if not field.isInField(newlocation):
            raise Exception
        else:
            self.location = newlocation
        return self


    def moveBack(self,field):
        newlocation = self.orientation.moveB(self.location)
        if field.isObstacle(newlocation) or not field.isInField(newlocation):
            raise Exception
        else:
            self.location = newlocation
        return self

    def turnLeft(self,field):
        turnPlus(self.orientation)
        return self

    def turnRight(self,field):
        turnMinus(self.orientation)
        return self

    def __eq__(self, other):
        return self.location == other.location and self.orientation==other.orientation
