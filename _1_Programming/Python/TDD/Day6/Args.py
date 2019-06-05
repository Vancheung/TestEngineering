class Args():
    def __init__(self, schema, cmd):

        self.dic = self.cmdParse(cmd)  # cmd解析为字典
        self.schema = schema

        self.logging = False
        self.port = None
        self.directory = None

    # 检查cmd字典与schema是否匹配
    def isMatch(self):
        for i in self.schema.df:
            if self.schema.df[i] == bool:
                for j in self.dic[i]:
                    if not self.schema.isBoolean(i, j):
                        raise TypeError('Wrong argment type, [{}]\'s type should be bool.'.format(i))
            if self.schema.df[i] == int:
                for j in self.dic[i]:
                    if not self.schema.isInt(i, j):
                        raise TypeError('Wrong argment type, [{}]\'s type should be int.'.format(i))
            if self.schema.df[i] == str:
                for j in self.dic[i]:
                    if not self.schema.isString(i, j):
                        raise TypeError('Wrong argment type, [{}]\'s type should be string.'.format(i))
        return True

    def cmdParse(self, cmd):
        cmdDic = {}
        for i in cmd.strip().split('-'):
            key = i.split(' ')[0]
            if key:
                cmdDic[i.split(' ')[0]] = i.strip().split(' ')[1:]
        return cmdDic

    def setProperty(self):
        if 'l' in self.dic:
            self.logging = True
        if 'p' in self.dic:
            self.port = int(self.dic['p'][0])
        if 'd' in self.dic:
            self.directory = self.dic['d'][0]

