# 事件类
class Event():
    def __init__(self,name):
        self.name = name

    def __str__(self):
        return self.name

# 核心类
class Widget():
    # 每个控件（子类）都有一个到父对象的引用
    # 父类的实例则parent为None
    def __init__(self,parent=None):
        self.parent = parent

    # 动态分发
    def handle(self,event):
        handler = 'handle_{}'.format(event)
        # 控件支持该方法
        if(hasattr(self,handler)):
            method = getattr(self,handler)
            method(event)
        # 控件有parent 则执行parent的handle方法
        elif self.parent:
            self.parent.handle(event)
        # 控件无parent，但是有default
        elif hasattr(self,'handle_default'):
            self.handle_default(event)

# 子控件不需要都能处理相同事件
class MainWindow(Widget):
    def handle_close(self,event):
        print('MainWindow {}'.format(event))

    def handle_default(self,event):
        print('MainWindow Default: {}'.format(event))

class SendDialog(Widget):
    def handle_paint(self,event):
        print('SendDialog: {}'.format(event))

class MsgText(Widget):
    def handle_down(self,event):
        print('MsgText: {}'.format(event))

def client():
    mw = MainWindow()
    sd = SendDialog(mw)
    msg = MsgText(sd)

    for e in ('down','paint','unhandled','close'):
        evt = Event(e)
        print('\nSending event -{}- to MainWindow'.format(evt))
        mw.handle(evt)
        print('Sending event -{}- to SendDialog'.format(evt))
        sd.handle(evt)
        print('Sending event -{}- to MsgText'.format(evt))
        msg.handle(evt)

if __name__ == '__main__':
    client()
