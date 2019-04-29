class PersonBuilder():
    def __init__(self):
        pass
    def BuildHead(self):
        raise NotImplementedError

    def BuildBody(self):
        raise NotImplementedError

    # def BuildArmleft(self):
    #     raise NotImplementedError
    #
    # def BuildArmRight(self):
    #     raise NotImplementedError
    #
    # def BuildLegLeft(self):
    #     raise NotImplementedError
    #
    # def BuildLegRight(self):
    #     raise NotImplementedError

    # def Build(self):
    #     self.BuildHead()
    #     self.BuildBody()

class PersonThinBuilder(PersonBuilder):
    def BuildHead(self):
        print('小头')

    def BuildBody(self):
        print('细身子')

class PersonFatBuilder(PersonBuilder):
    def BuildHead(self):
        print('大头')

    def BuildBody(self):
        print('胖身子')

class PersonDirector(object):
    # def __init__(self):
    #     self.pb = PersonBuilder()

    def CreatePerson(self,bulder):
        bulder.BuildHead()
        bulder.BuildBody()

def client():
    p = PersonDirector()
    p.CreatePerson(PersonThinBuilder())
    p.CreatePerson(PersonFatBuilder())


if __name__ == '__main__':
    client()
