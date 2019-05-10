# View 实现还不够优雅

# Model
class QuoteModel():
    def __init__(self):
        self.quotes = []
    # 创建
    def check_num(self,n):
        # 把校验从Controller移到model
        try:
            n = int(n)
            if (n < 1):  # 让索引变为从1开始
                print("Index can't be less than 1!")
                return False
        except ValueError as err:
            print("Incorrect index '{}'".format(n))
            return False
        return True

    def create(self,quote):
        try:
            self.quotes.append(quote)
            value = 'Insert success! New quote is "{}".'.format(quote)
        except ValueError:
            value = 'Insert Fail! Please check your input'
        return value

    # 读取
    def read(self,n):
        if self.check_num(n):
            try:
                n = int(n)
                value = self.quotes[n - 1]
            except IndexError as err:
                value =  'Not found!'
        else:
            value = 'Wrong index'
        return value


    # 更新
    def update(self,n,quote):
        if self.check_num(n):
            try:
                n = int(n)
                self.quotes[n - 1] = quote
                value = 'Update numbe {} to {} success!'.format(n,self.quotes[n-1])
            except IndexError as err:
                value =  'Not found!'
        else:
            value = 'Wrong index'
        return value
    # 删除
    def delete(self,n):
        if self.check_num(n):
            n = int(n)
            self.quotes.pop(n-1)


# View
class QuoteTerminalView():
    # 不包含业务逻辑和数据，只做显示
    def show(self,quote):
        print('And the quote is "{}"'.format(quote))

    def error(self,msg):
        print('Error: {}'.format(msg))

    def select_quote(self):
        return input('Which quote number would you like to see? ')

    def select_operation(self):
        return input('What do you want to do? ')

    def add_quote(self):
        return input('Input your new quote: ')



# Controller
class QuoteTerminalController():
    def __init__(self):
        self.model = QuoteModel()
        self.view = QuoteTerminalView()
        self.op_pool = {'c':self.model.create, 'r':self.model.read, 'u':self.model.update, 'd': self.model.delete}

    def run(self):
        valid_input = False
        while not valid_input:
            op = self.view.select_operation()
            op = op.lower()
            if(op not in ('c','r','u','d')):
                self.view.error('Wrong operation')
                continue
            elif op=='c':
                n = self.view.add_quote()
                valid_input = True
            elif op =='u':
                n = self.view.select_quote()
                q = self.view.add_quote()
                valid_input = True
            else:
                n = self.view.select_quote()
                valid_input = True

        if op=='u':
            result = self.op_pool[op](n,q)
        else:
            result = self.op_pool[op](n)
        # quote = self.model.get_quote(n)
        self.view.show(result)

def main():
    controller = QuoteTerminalController()
    while True:
        controller.run()

if __name__ == '__main__':
    main()
