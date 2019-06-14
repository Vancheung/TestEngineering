from Errors import *
from Field import Field
from Location import Location, Orientation
from Rover import Rover


class Command:
    def __init__(self, cmds):
        self.cmds = cmds
        for i in self.cmds.split(';'):
            if i:
                self.Parse(i)

    def Parse(self, cmd):
        # "I 0,0 40,40
        if cmd.split(' ')[0] == 'I':
            self.ParseI(cmd)
            return

        # cmd = 'O 5,3;O 2,1'
        if cmd.split(' ')[0] == 'O':
            self.ParseO(cmd)
            return

        # cmd = 'V 2,1 "N"'
        if cmd.split(' ')[0] == 'V':
            self.ParseV(cmd)
            return

        self.ParseMove(cmd)



    def ParseMove(self, cmd):
        if self.field and self.rover:
            for i in cmd:
                try:
                    self.rover.movemap[i](self.field)
                except Exception:
                    raise WrongCommandError
        else:
            raise InitError

    def ParseV(self, cmd):
        try:
            x = int(cmd.split(' ')[1].split(',')[0])
            y = int(cmd.split(' ')[1].split(',')[1])
            self.rover = Rover(Location(x, y), Orientation(cmd.split(' ')[2]))
        except:
            raise WrongIndexError

    def ParseO(self, cmd):
        try:
            x = int(cmd.split(' ')[1].split(',')[0])
            y = int(cmd.split(' ')[1].split(',')[1])
            self.field.setObstacles((x, y))
        except:
            raise WrongIndexError

    def ParseI(self, cmd):
        try:
            marginbeginx = int(cmd.split(' ')[1].split(',')[0])
            marginbeginy = int(cmd.split(' ')[1].split(',')[1])
            marginendx = int(cmd.split(' ')[2].split(',')[0])
            marginendy = int(cmd.split(' ')[2].split(',')[1])
            self.field = Field(Location(marginbeginx, marginbeginy), Location(marginendx, marginendy))
        except:
            raise WrongIndexError

