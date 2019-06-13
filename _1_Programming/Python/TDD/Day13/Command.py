from Field import Field
from Rover import Rover


class Command:
    def __init__(self, cmds):
        self.rover = None
        self.field = None
        cmds = cmds.split(';')
        for i in cmds:
            self.Parse(i)


    def Parse(self, cmd):
        if cmd[0] == 'I':  # 初始化区域
            X = int(cmd.split(' ')[1])
            Y = int(cmd.split(' ')[2])
            self.setField(X, Y)
            return

        if cmd[0] == 'V':  # 初始化火星车
            x = int(cmd.split(' ')[1])
            y = int(cmd.split(' ')[2])
            ori = cmd.split(' ')[3]
            self.setRover(x, y, ori)
            return

        if cmd[0] == 'O':  # 初始化障碍
            x = int(cmd.split(' ')[1])
            y = int(cmd.split(' ')[2])
            self.field.setObstacle(x,y)
            return


        # 行走指令
        if self.rover and self.field:
            for i in cmd:
                try:
                    self.rover.func_map[i](self.field)
                except Exception as e:
                    raise e
        else:
            raise Exception('Need nessary information: Field and Rover Location!')


    def setField(self, X, Y):
        self.field = Field(X, Y)

    def setRover(self, x, y, ori):
        self.rover = Rover((x, y), ori)

