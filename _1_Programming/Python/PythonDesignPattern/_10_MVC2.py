# quotes = ('A man is not complete until he is married. Then he is finished.',
#  'As I said before, I never repeat myself.',
#  'Behind a successful man is an exhausted woman.',
#  'Black holes really suck...', 'Facts are stubborn things.')

# Model
class QuoteModel():
    def __init__(self):
        self.quotes = []
    # 创建
    def create(self,quote):
        try:
            self.quotes.append(quote)
            value = 'Insert success! New quote is "{}".'.format(quote)
        except ValueError:
            value = 'Insert Fail! Please check your input'
        return value

    # 读取
    def read(self,n):
        try:
            n = int(n)
            value = self.quotes[n - 1]
        except IndexError as err:
            value = 'Not found!'
        return value


    # 更新
    def update(self,n,quote):
        try:
            self.quotes[n - 1] = quote
            value = 'Update numbe {} to {} success!'.format(n, self.quotes[n - 1])
        except IndexError as err:
            value = 'Not found!'

        return value

    # 删除
    def delete(self,n):
        try:
            quote = self.quotes.pop(n-1)
            value = 'Remove {} Success!'.format(quote)
        except IndexError as err:
            value = 'Not found!'
        return value


# View
class QuoteTerminalView():
    # 不包含业务逻辑和数据，只做显示
    def show(self,quote):
        print('And the quote is "{}"'.format(quote))

    def error(self,msg):
        print('Error: {}'.format(msg))

    def select_quote(self):
        return input('Which quote number would you like to process?(0 for none) ')

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

            n = self.view.select_quote()
            try:
                n = int(n)
                if (n < 0):  # 让索引变为从1开始
                    print("Index can't be less than 1!")
                    continue
                else:
                    valid_input = True
            except ValueError as err:
                print("Incorrect index '{}'".format(n))

            if op in ('c','u'):
                q = self.view.add_quote()
                valid_input = True

        if op =='c':
            result = self.op_pool[op](q)
        elif op=='u':
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
