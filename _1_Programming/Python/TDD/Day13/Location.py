class Location:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

class Orientation:
    def __init__(self,orien):
        self.name = orien
        self.moveMap = {
            'N': (yPlus, yMinus),
            'W': (xMinus, xPlus),
            'S': (yMinus, yPlus),
            'E': (xPlus, xMinus)
        }

    def __eq__(self, other):
        return self.name == other.name
    def moveF(self,loc):
        return self.moveMap[self.name][0](loc)
    def moveB(self,loc):
        return self.moveMap[self.name][1](loc)

def xPlus(loc):
    return Location(loc.x + 1, loc.y)


def xMinus(loc):
    return Location(loc.x - 1, loc.y)


def yPlus(loc):
    return Location(loc.x, loc.y + 1)


def yMinus(loc):
    return Location(loc.x, loc.y - 1)

def turnPlus(ori):
    mm = ['N','W','S','E']
    ori.name = mm[mm.index(ori.name)+1] if mm.index(ori.name)+1<len(mm) else mm[mm.index(ori.name)+1-len(mm)]
    return ori

def turnMinus(ori):
    mm = ['N','W','S','E']
    ori.name = mm[mm.index(ori.name)-1]
    return ori
