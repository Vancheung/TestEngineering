from Location import Location
from Errors import *
class Field:
    def __init__(self,locationbegin,locationend):
        self.locationbegin = locationbegin
        self.locationend = locationend
        self.obstacles = []

    def setObstacles(self,*kwargs):
        for i in kwargs:
            if self.isInField(Location(i[0],i[1])):
                self.obstacles.append(i)
            else:
                raise OutFieldError

    def isObstacle(self,location):
        return (location.x,location.y) in self.obstacles

    def __eq__(self, other):
        return self.locationbegin==other.locationbegin and self.locationend == other.locationend

    def isInField(self,location):
        return self.locationbegin.x <= location.x <= self.locationend.x and self.locationbegin.y <= location.y <= self.locationend.y
