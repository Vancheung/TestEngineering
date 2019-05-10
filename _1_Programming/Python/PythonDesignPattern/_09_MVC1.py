quotes = ('A man is not complete until he is married. Then he is finished.',
 'As I said before, I never repeat myself.',
 'Behind a successful man is an exhausted woman.',
 'Black holes really suck...', 'Facts are stubborn things.')

# Model
class QuoteModel():
    def get_quote(self,n):
        # 把校验从Controller移到model
        try:
            n = int(n)
            if (n < 1):  # 让索引变为从1开始
                value = "Index can't be less than 0!"
            else:
                value = quotes[n-1]
        except ValueError as err:
            value = "Incorrect index '{}'".format(n)
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
        return input('Which quote number would you like to see? ')



# Controller
class QuoteTerminalController():
    def __init__(self):
        self.model = QuoteModel()
        self.view = QuoteTerminalView()

    def run(self):
        valid_input = False
        while not valid_input:
            n = self.view.select_quote()
            valid_input = True

        quote = self.model.get_quote(n)
        self.view.show(quote)

def main():
    controller = QuoteTerminalController()
    while True:
        controller.run()

if __name__ == '__main__':
    main()
