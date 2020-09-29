import json
import threading
from time import sleep
from selenium.webdriver.chrome.options import Options

from selenium import webdriver

ids = [3729, 3730]
URLS = ['https://shop.48.cn/tickets/item/%s' % i for i in ids]


def save_cookies():
    """
    手动登录，保存session
    :return:
    """
    driver = webdriver.Chrome(executable_path='./chromedriver')
    driver.get("https://shop.48.cn/home/index")
    sleep(20)
    # 获取list的cookies
    input()
    print('开始保存！')
    json_cookies = json.dumps(driver.get_cookies())  # 转换成字符串保存

    with open('cookies.txt', 'w') as f:
        f.write(json_cookies)
    print('cookies保存成功！')


class Ticket:
    def __init__(self, list_cookies, is_quiet=True):
        self.list_cookies = list_cookies
        if is_quiet:
            chrome_options = Options()
            chrome_options.add_argument('--headless')
            self.driver = webdriver.Chrome(executable_path='./chromedriver', options=chrome_options)
        else:
            self.driver = webdriver.Chrome(executable_path='./chromedriver')

    def buy_vip(self, url):
        """
        vip 1张
        :param url:
        :return:
        """
        self.driver.get(url)
        for cookie in self.list_cookies:
            self.driver.add_cookie(cookie)
        self.driver.refresh()
        self.driver.find_element_by_id('seattype2').click()
        while True:
            self.driver.find_element_by_id('buy').click()

    def buy_normal(self, url):
        """
        普通票 3张
        :param url:
        :return:
        """
        self.driver.get(url)
        for cookie in self.list_cookies:
            self.driver.add_cookie(cookie)
        self.driver.refresh()
        self.driver.find_element_by_id('seattype3').click()
        self.driver.find_element_by_id('num').clear()
        self.driver.find_element_by_id('num').send_keys(3)
        while True:
            try:
                self.driver.find_element_by_id('buy').click()
            except:
                self.driver.close()


class TicketThread(threading.Thread):
    """
    使用多线程方式运行
    """

    def __init__(self, url, list_cookies, buyv=True):
        threading.Thread.__init__(self)
        self.ticket = Ticket(list_cookies, is_quiet=True)
        self.url = url
        self.buyv = buyv

    def run(self):
        """
        执行性能测试的线程
        :return:
        """
        print('open %s' % self.url)
        if self.buyv:
            self.ticket.buy_vip(url=self.url)
        else:
            self.ticket.buy_normal(url=self.url)


if __name__ == '__main__':
    # save_cookies()
    with open('cookies.txt', 'r', encoding='utf8') as f:
        coe = json.loads(f.read())

    for u in URLS:
        threads = [TicketThread(u, coe) for i in range(10)]
        threads.extend([TicketThread(u, coe, buyv=False) for i in range(10)])
        for i, t in enumerate(threads):
            print('start thread %s' % i)
            sleep(3)
            t.start()
