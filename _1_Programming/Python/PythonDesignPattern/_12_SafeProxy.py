# 保护代理
class SensitiveInfo():
    def __init__(self):
        self.users = ['nick','tom','ben','mike']

    def read(self):
        print('There are {} users: {}'.format(len(self.users),' '.join(self.users)))

    def add(self,user):
        self.users.append(user)
        print('Add user {}'.format(user))

    def remove(self,index):
        s = self.users.pop(int(index))
        print('Remove user {}'.format(s))

# 保护代理
class Info():
    def __init__(self):
        self.protected = SensitiveInfo()
        self.secret = '0xdeadbeef'

    # 读取不需要权限
    def read(self):
        self.protected.read()

    # 添加新用户需要权限
    def add(self,user):
        sec = input('what is the secret? ')
        self.protected.add(user) if sec==self.secret else print('Wrong password!')

    # 删除新用户需要权限
    def remove(self,user):
        sec = input('what is the secret? ')
        self.protected.remove(user) if sec==self.secret else print('Wrong password!')

def client():
    info = Info()
    s = SensitiveInfo()
    while True:
        print('1. read list |==| 2. add user |==| 3. remove user')
        key = input('choose option: ')
        if key == '1':
            info.read()
        elif key == '2':
            name = input('choose username: ')
            info.add(name)
        elif key == '3':
            index = input('choose index: ')
            info.remove(index)
        else:
            print('unknown option: {}'.format(key))

if __name__ == '__main__':
    client()
