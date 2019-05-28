class Args():
    def __init__(self, cmd):
        self.cmd = cmd
        self.paras = {}
        self.Parse()

    def Query(self, arg):
        return self.paras.get(arg, 'Arg name not found!')

    def Parse(self):
        for s in self.cmd.split('-'):

            # key : value
            s = s.split(' ')
            if s[0] and s[1]:
                if s[1].isdigit():
                    self.paras[s[0]] = int(s[1])
                    continue
                self.paras[s[0]] = s[1]  # 扩展时需要调整s.split(' ')[1]为列表解析

            # key without value
            elif s[0]:
                self.setDefault(s[0])

        return self.paras

    def setDefault(self, arg):
        self.paras[arg] = True
