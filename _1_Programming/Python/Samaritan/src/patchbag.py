from os import system

cmd = [
    'pyinstaller -F slave\client.py --distpath ..\Windows\Slave_win',
    'pyinstaller -F slave\slave_server.py --distpath ..\Windows\Slave_win',
    'pyinstaller -F master\master_server.py --distpath ..\Windows\Master_win',
    'pyinstaller -F master\client.py --distpath ..\Windows\Master_win'
]

if __name__ == '__main__':
    for i in cmd:
        system(i)
