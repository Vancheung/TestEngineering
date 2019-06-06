class Schema:
    def __init__(self, schema):
        self.schema = self.Parse(schema)

    def Parse(self, sch):
        d = {}
        types = {
            'int': int,
            'bool': bool,
            'boolean': bool,
            'float': float,
            'string': str,
            'str': str
        }
        for i in sch.strip().split(','):
            key = i.split(':')[0]
            value = i.split(':')[1].lower()
            if value in types:
                d[key] = types[value]
            else:
                raise TypeError('Wrong format, {} is not a legal type.'.format(value))
        return d

    def getSchema(self, key):
        try:
            return self.schema[key]
        except:
            ValueError('Wrong arg name!')

    def isBool(self, value):
        if value == None or isinstance(value, bool):
            return True
        return False

    def isInt(self, value):
        if isinstance(value, bool):
            return False
        if isinstance(value, str) and value.isdigit():
            return True
        return isinstance(value, int)

    def isString(self, value):
        return isinstance(value, str)
