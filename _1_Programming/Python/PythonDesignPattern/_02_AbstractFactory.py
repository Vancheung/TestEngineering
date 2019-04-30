# 根据不同的配置，使用抽象工厂实例化一组对象
class Frog:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

    def interact_with(self, obstacle):
        print('{} the Frog encounters {} and {}!'.format(self,obstacle, obstacle.action()))


class Bug:
    def __str__(self):
        return 'a bug'

    def action(self):
        return 'eats it'

# 工厂1：Frog-Bug 形式
class FrogWorld:
    def __init__(self, name):
        print(self)
        self.player_name = name

    def __str__(self):
        return '\n\n\t------ Frog World -------'

    def make_character(self):
        return Frog(self.player_name)

    def make_obstacle(self):
        return Bug()


class Wizard:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

    def interact_with(self, obstacle):
        print('{} the Wizard battles against {} and {}!'.format(self, obstacle,obstacle.action()))


class Ork:
    def __str__(self):
        return 'an evil ork'

    def action(self):
        return 'kills it'

# 工厂2： wizard-ork 形式
class WizardWorld:
    def __init__(self, name):
        print(self)
        self.player_name = name

    def __str__(self):
        return '\n\n\t------ Wizard World -------'

    def make_character(self):
        return Wizard(self.player_name)

    def make_obstacle(self):
        return Ork()


class GameEnvironment:
    def __init__(self, factory):
        self.hero = factory.make_character()
        self.obstacle = factory.make_obstacle()

    def play(self):
        self.hero.interact_with(self.obstacle)


def validate_age(name):
    try:
        age = input('Welcome {}. How old are you? '.format(name))
        age = int(age)
    except ValueError as err:
        print("Age {} is invalid, please try again...".format(age))
        return (False, age)
    return (True, age)


def client():
    name = input("Hello. What's your name? ")
    valid_input = False
    while not valid_input:
        valid_input, age = validate_age(name)  # 输入有效性判断
    if age < 18:
        game = FrogWorld
    else:
        game = WizardWorld
    environment = GameEnvironment(game(name))
    environment.play()


if __name__ == '__main__':
    client()
