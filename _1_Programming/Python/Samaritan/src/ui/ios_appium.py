# -*- coding: UTF-8 -*-

"""
-------------------------------------------------------------------------------
Describe: appium基础操作
Created At: 2020-08-27,  16:47
Author: 
-------------------------------------------------------------------------------
"""
from re import search
from subprocess import Popen, PIPE
from time import sleep
from json import dumps

from appium import webdriver
from selenium.common.exceptions import WebDriverException

from common.indicators import ParamInfo
from src import logger


class AppiumOperator:
    """
    Appium底层操作，不需要调用这个类，建议使用AppiumApi
    """

    def __init__(self, host='127.0.0.1', port=4723, wda_port=8100, udid=None):
        # self._stop()
        self.host = host
        self.server_port = port
        self.bootstrap_port = port + 1
        self.wda_port = wda_port
        self.udid = udid
        self._start()
        self.driver = None

    def _start(self):
        """
        启动appium服务
        :return:
        """
        cmd = 'appium -a %s -p %s -bp %s --webdriveragent-port %s' % (
            self.host, self.server_port, self.bootstrap_port, self.wda_port)
        if self.udid:
            cmd += ' --device-name %s' % self.udid
        logger.info(cmd)
        Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)

    def start_app(self, dev_info: dict):
        """
        启动指定app
        :param dev_info: 传入启动appium所需参数，格式为一个字典，等同于appium-desktop启动时的session配置
        :return:
        """
        try:
            logger.info('start %s at port %d' % (dev_info.get('bundleId'), self.server_port))
            logger.info('URL = http://127.0.0.1:%s/wd/hub' % self.server_port)
            self.driver = webdriver.Remote('http://127.0.0.1:%s/wd/hub' % self.server_port, dev_info)
        except Exception as e:
            logger.error(e)
            raise e

    def smart_find(self, name, retry_time=5):
        """
        智能查找元素，可以设置重试次数
        :param name:
        :param retry_time:
        :return:
        """
        start = 0
        while start < retry_time:
            try:
                element = self.driver.find_element_by_xpath(name)
                return element
            except WebDriverException:
                start += 1
                continue
        return None

    def click_button(self, button_name: str):
        """
        根据button的xpath定位元素并点击
        :param button_name:
        :return:
        """
        logger.info('try to find element %s and click' % button_name)
        btn = self.smart_find(button_name)
        if btn:
            btn.click()
        else:
            logger.error('No such element')
            raise WebDriverException('No such element')

    def click_location(self, position_x, position_y):
        pass

    def input(self, field_name: str, info: str):
        """
        根据输入框的xpath定位元素，并输入内容
        :param field_name:
        :param info:
        :return:
        """
        logger.info('try to find element %s' % field_name)
        text_field = self.smart_find(field_name)
        if text_field:
            text_field.clear()
            text_field.send_keys(str(info))
        else:
            logger.error('No such element')
            raise WebDriverException('No such element')

    @staticmethod
    def stop():
        """
        终止appium进程
        :return:
        """
        proc1 = Popen(['ps', '-A'], stdout=PIPE)
        proc2 = Popen(['grep', '/bin/appium'], stdin=proc1.stdout,
                      stdout=PIPE, stderr=PIPE)
        proc1.terminate()
        proc1.stdout.close()  # Allow proc1 to receive a SIGPIPE if proc2 exits.
        out, err = proc2.communicate()
        proc2.terminate()
        process_id = out.decode('utf-8').strip()
        p = Popen(['kill', '-9', search("(?sm)\w*\s*(\d*)", process_id).group(0).strip()])
        p.terminate()

    def quit(self):
        """
        关闭应用
        :return:
        """
        self.driver.quit()

    def screen_shot(self, screen_save_path):
        """
        屏幕截图
        :param screen_save_path:
        :return:
        """
        self.driver.get_screenshot_as_file(screen_save_path)


class AppiumApi:
    """
    用例层调用Appium的操作
    """

    def __init__(self, dev_info: dict, port=4723, wda_port=8100, udid=None):
        """

        :param dev_info:
        """
        self.appium = AppiumOperator(port=port, wda_port=wda_port, udid=udid)
        sleep(5)
        self.appium.start_app(dev_info)
        sleep(5)


    def operate(self, op: dict, param_info: ParamInfo):
        """
        根据配置进行操作
        :param op: eg:
        :param param_info: 调用update更新预配置
        :return:
        """
        logger.info("case:  " + op.get('description'))
        for i in op.get('operation'):
            if isinstance(i, dict):
                param_info.update(**i.get('update'))
                self.start(dumps(param_info.params))
            elif isinstance(i, str):
                getattr(self, i, None)()

    def screen_shot(self, screen_save_path):
        """
        屏幕截图
        :param screen_save_path:
        :return:
        """
        self.appium.screen_shot(screen_save_path)
