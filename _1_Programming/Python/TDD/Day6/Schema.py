class Schema():
    def __init__(self, schema):
        self.df = self.setSchema(schema)

    def setSchema(self, schema):
        dic = self.parseSchema(schema)
        newdic = {}
        types = {'bool': bool,
                 'str': str,
                 'int': int,
                 'float': float,
                 'list': list,
                 'dict': dict}
        for i in dic:
            if dic[i] in types:
                newdic[i] = types.get(dic[i])  # 'l':'bool' -> 'l':bool
            else:
                raise TypeError('Unsupported type {}, type should be in (bool,str,int,float,list,dict).'.format(dic[i]))
        return newdic

    def parseSchema(self, schema):
        d = {}
        for i in schema.strip().split(' '):
            d[i.split(':')[0]] = i.split(':')[1]
        return d

    def isBoolean(self, key, value):
        return isinstance(value, self.df[key])

    def isInt(self, key, value):
        # isinstance(False,int) = True
        if value == True or value == False:
            return False
        if isinstance(value, str) and value.isdigit():
            return True
        else:
            return isinstance(value, self.df[key])

    def isString(self, key, value):
        return isinstance(value, self.df[key])
