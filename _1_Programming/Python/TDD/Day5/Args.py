WRONG_FORMAT_ERROR = "Wrong format of argument!"


class Args():
    def __init__(self):
        self.logging = False
        self.port = 0
        self.directory = ''
        self.paras = {}  # 其他扩展参数

    def setLogging(self, log):
        if log in (True, False):
            self.logging = log
        else:
            return WRONG_FORMAT_ERROR

    def setPort(self, port):
        if type(port) == int:
            self.port = port
            return self
        if type(port) == str and port.isdigit():
            self.port = int(port)
            return self
        return WRONG_FORMAT_ERROR

    def setDir(self, dir):
        if type(dir) == str:
            self.directory = dir
            return self
        return WRONG_FORMAT_ERROR

    def Query(self, arg):
        if (arg == 'l'):
            return self.logging
        if (arg == 'p'):
            return self.port
        if (arg == 'd'):
            return self.directory
        return WRONG_FORMAT_ERROR

    def Parse(self,cmd):
        for i in cmd.strip().split('-'):
            key = i.split(' ')[0]
            value = i.strip().split(' ')[1:]
            # print('key = {},value = {}'.format(key, value))
            if key and value:
                # print('key = {},value = {}'.format(key,value))
                self.paras[key] = value
            elif key:
                self.paras[key] = None
        return self.paras

    def genArgs(self):
        if self.paras.get('l'):
            self.setLogging(True)
        if self.paras.get('p'):
            self.setPort(self.paras['p'])
        if self.paras.get('d'):
            self.setDir(self.paras['d'])

