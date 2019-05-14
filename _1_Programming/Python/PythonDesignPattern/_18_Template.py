from cowpy import cow

# 默认风格
def dots_style(msg):
    msg = msg.capitalize()
    msg = '.' * 10 + msg + '.' * 10
    return msg

# 自定义风格1
def admire_style(msg):
    msg = msg.upper()
    return '!'.join(msg)

# 自定义风格2
def cow_style(msg):
    msg = cow.milk_random_cow(msg)
    return msg

# 模板函数 （通过参数传入具体执行哪个函数）
def generate_banner(msg, style=dots_style):
    print('-- start of banner --')
    print(style(msg))
    print('-- end of banner --\n\n')


def main():
    msg = 'happy coding'
    [generate_banner(msg, style) for style in (dots_style, admire_style, cow_style)]


if __name__ == '__main__':
    main()
