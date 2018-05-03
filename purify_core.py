#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/4/16 17:34
# @Author  : BLKStone
# @Site    : http://blkstone.github.io
# @File    : purify_core.py
# @Software: PyCharm

import re
import StringIO
import datetime


# 计时器类
# 用于对一段代码进行计时
class TimeKeeper(object):
    def __init__(self):
        self.start_time = None
        self.stop_time = None
        self.elapsed_time = None

    def start(self):
        self.start_time = datetime.datetime.now()

    def stop(self):
        self.stop_time = datetime.datetime.now()

    def elapsed(self):
        self.elapsed_time = self.stop_time - self.start_time
        message = '[*] elapsed ' + str(self.elapsed_time) + '...'
        print(message)
        return self.elapsed_time


class Purifier(object):
    def __init__(self):
        self.debug = False

    # 匹配是否存在身份证信息
    def identity(self, content):

        pattern = r"(\d{6}\d{4}\d{2}\d{2}\d{3}[0-9]|X)"
        p = re.compile(pattern)
        iterator = p.finditer(content)

        new_string = list(content)

        for idx, m in enumerate(iterator):

            if self.debug:
                print idx,
                print m.span(),    # 索引组合
                print m.start(),    # 起始索引
                print m.end(),    # 终止索引
                print m.group(),    # 匹配内容
                print ''

            original = m.group()
            # 前面和后面各保留3位
            for idx in range(m.start() + 2, m.end() - 2):
                new_string[idx] = '*'

        masked = ''.join(new_string)

        if self.debug:
            print masked

        return masked

    def email(self, content):

        pattern = r"[\w!#$%&'*+/=?^_`{|}~-]+(?:\.[\w!#$%&'*+/=?^_`{|}~-]+)*@(?:[\w](?:[\w-]*[\w])?\.)+[\w](?:[\w-]*[\w])?"
        p = re.compile(pattern)
        iterator = p.finditer(content)

        new_string = list(content)

        for idx, m in enumerate(iterator):

            if self.debug:
                print idx,
                print m.span(),    # 索引组合
                print m.start(),    # 起始索引
                print m.end(),    # 终止索引
                print m.group(),    # 匹配内容
                print ''

            original = m.group()
            email_idx = original.find('@')
            for idx in range(m.start() + 1, m.start() + email_idx):
                new_string[idx] = '*'

        masked = ''.join(new_string)

        if self.debug:
            print masked

        return masked

    def mobile_phone(self, content):

        pattern = r"0?(13|14|15|17|18|19)[0-9]{9}"
        p = re.compile(pattern)
        iterator = p.finditer(content)

        new_string = list(content)

        for idx, m in enumerate(iterator):

            if self.debug:
                print idx,
                print m.span(),    # 索引组合
                print m.start(),    # 起始索引
                print m.end(),    # 终止索引
                print m.group(),    # 匹配内容
                print ''

            original = m.group()
            for idx in range(m.start() + 3, m.end() - 2):
                new_string[idx] = '*'

        masked = ''.join(new_string)

        if self.debug:
            print masked

        return masked

    def ip(self, content):

        pattern = "(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)"
        p = re.compile(pattern)
        iterator = p.finditer(content)

        new_string = list(content)

        for idx, m in enumerate(iterator):

            if self.debug:
                print idx,
                print m.span(),    # 索引组合
                print m.start(),    # 起始索引
                print m.end(),    # 终止索引
                print m.group(),    # 匹配内容
                print ''
            original = m.group()
            for idx in range(m.start() + 1, m.end() - 1):
                if new_string[idx] == '.':
                    continue
                else:
                    new_string[idx] = '*'

        masked = ''.join(new_string)

        if self.debug:
            print masked

        return masked

    def de_sensitive(self, content):

        res = self.identity(content)
        res = self.email(res)
        res = self.mobile_phone(res)
        res = self.ip(res)
        return res

    def file_de_sensitive(self, input_path, output_path):

        with open(input_path, 'r') as f:
            with open(output_path, 'w') as fw:
                for line in f.readlines():
                    new_line = self.de_sensitive(line)
                    fw.write(new_line)

        f.close()
        fw.close()


# ===================================================================================
# 以下为测试函数
def test_case_1():
    test_sentence_1 = '''李星（身份证：510722195412248414），董事长，邮箱：23786720@qq.com，1954年出生于军人家庭，1979年毕业于北京上海学院摄影系，手机:18134761224, 在创建公司前曾在多家国内外大型广告公司任职，以拍摄广告为主业。1984年成立广告有限公司,公司银行卡账号：62177892145000588476，开始独立运作，李星在完成人生的第一桶金后，从1990年起开始做自己感兴趣的事———拍摄电视剧，20009年国内电影产业慢慢成型，李星将公司影视投资核心转移到电影方面。'''

    p = Purifier()
    p.identity(test_sentence_1)
    p.email(test_sentence_1)
    p.mobile_phone(test_sentence_1)


def test_case_2():
    test_sentence_1 = '''李星（身份证：510722195412248414），董事长，邮箱：23786720@qq.com，1954年出生于军人家庭，1979年毕业于北京上海学院摄影系，手机:18134761224, 在创建公司前曾在多家国内外大型广告公司任职，以拍摄广告为主业。1984年成立广告有限公司,公司银行卡账号：62177892145000588476，开始独立运作，李星在完成人生的第一桶金后，从1990年起开始做自己感兴趣的事———拍摄电视剧，20009年国内电影产业慢慢成型，李星将公司影视投资核心转移到电影方面。'''

    p = Purifier()
    print test_sentence_1
    print p.de_sensitive(test_sentence_1)


def test_case_3():
    input_path = 'data/dbapp_waf.txt'
    output_path = 'data/dbapp_waf_desensitive.txt'
    p = Purifier()
    p.file_de_sensitive(input_path, output_path)


def test_case_4():
    test_sentence_1 = '''李星（身份证：510722195412248414），董事长，他的IP地址是192.168.12.5，邮箱：23786720@qq.com，1954年出生于军人家庭，1979年毕业于北京上海学院摄影系，手机:18134761224, 在创建公司前曾在多家国内外大型广告公司任职，以拍摄广告为主业。1984年成立广告有限公司,公司银行卡账号：62177892145000588476，开始独立运作，李星在完成人生的第一桶金后，从1990年起开始做自己感兴趣的事———拍摄电视剧，20009年国内电影产业慢慢成型，李星将公司影视投资核心转移到电影方面。'''

    p = Purifier()
    p.debug = True
    p.ip(test_sentence_1)


# 脱敏
# https://www.alibabacloud.com/help/zh/doc-detail/64590.htm
if __name__ == '__main__':
    tk = TimeKeeper()
    tk.start()
    test_case_1()
    msg = 'Test Case 1 FINISH.'
    print(msg)
    test_case_2()
    msg = 'Test Case 2 FINISH.'
    print(msg)
    test_case_3()
    msg = 'Test Case 3 FINISH.'
    print(msg)
    test_case_4()
    msg = 'Test Case 4 FINISH.'
    print(msg)
    tk.stop()
    print tk.elapsed()