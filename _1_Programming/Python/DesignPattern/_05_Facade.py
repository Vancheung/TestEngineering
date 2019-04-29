class Stock1():
    def __init__(self):
        pass

    def Buy(self):
        print('Buy in '+str(self))

    def Sold(self):
        print("Sold out"+str(self))


class Stock2():
    def __init__(self):
        pass

    def Buy(self):
        print('Buy in '+str(self))

    def Sold(self):
        print("Sold out"+str(self))

class Fund():
    def __init__(self):
        self.sto1 = Stock1()
        self.sto2 = Stock2()

    # 使用外观封装一组方法
    def BuyFonds(self):
        self.sto1.Buy()
        self.sto2.Buy()

    def SoldFunds(self):
        self.sto1.Sold()
        self.sto2.Sold()


def client():
    f = Fund()
    f.BuyFonds()
    f.SoldFunds()

if __name__ =='__main__':
    client()
