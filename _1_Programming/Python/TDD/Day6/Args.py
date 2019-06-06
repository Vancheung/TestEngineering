class Args:
    def __init__(self, cmd):
        self.cmd = self.cmdParse(cmd)
        self.logging = False
        self.port = None
        self.directory = None

    def cmdParse(self, cmd):
        d = {}
        for i in cmd.strip().split('-'):
            key = i.split(' ')[0]
            values = i.strip().split(' ')[1:]
            if key:
                d[key] = values
        return d

    def isMatch(self, schema):
        for i in self.cmd:
            if schema.schema[i] == bool:
                for j in self.cmd[i]:
                    if not schema.isBool(j):
                        raise TypeError('Wrong format,{} should be a boolean'.format(i))

            if schema.schema[i] == int:
                for j in self.cmd[i]:
                    if not schema.isInt(j):
                        raise TypeError('Wrong format,{} should be a int'.format(i))

            if schema.schema[i] == str:
                for j in self.cmd[i]:
                    if not schema.isString(j):
                        raise TypeError('Wrong format,{} should be a string'.format(i))
        return True

    def setProperty(self, schema):
        if self.isMatch(schema):
            if 'l' in self.cmd:
                self.logging = True
            self.port = int(self.cmd['p'][0])
            self.directory = self.cmd['d'][0]
        else:
            raise TypeError('Wrong args for this schema!')
