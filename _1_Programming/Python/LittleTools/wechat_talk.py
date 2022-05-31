""" 安卓端微信摸鱼小工具 """ 

import uiautomator2

client = uiautomator2.connect("")

def send(context):
    client(resourceId="com.tencent.mm:id/b4a").send_keys(context)
    client(resourceId="com.tencent.mm:id/b8k").click()
    

def receive():
    return [i.get_text() for i in client(className="android.widget.TextView")]
