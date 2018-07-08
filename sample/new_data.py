#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : new_data.py
# @Author: Zhangjintao
# @Date  : 2018/6/1
# @Desc  : 修改文本标签
import re
import os
import time


class NewData(object):
    def __init__(self, base_path):
        self.base_path = base_path

    def read_data(self, file_name, dir):
        path = self.base_path + os.path.sep + dir + os.path.sep + file_name
        print(file_name)
        try:
            with open(path, 'r', encoding="utf-8") as f:
                # print(f)
                b = f.read()
                data = re.sub(r'\s{8}\d', '', b).strip()
        except:
            print("_____________")
            return None, 0
        s1 = re.search(r1, data)
        s2 = re.search(r2, data)
        s3 = re.search(r3, data)
        s4 = re.search(r4, data)
        if s1:
            new_data = "{0}        {1}".format(data, 1)
            return new_data, 1
        elif s2:
            new_data = "{0}        {1}".format(data, 2)
            return new_data, 2
        elif s3:
            new_data = "{0}        {1}".format(data, 3)
            return new_data, 3
        elif s4:
            new_data = "{0}        {1}".format(data, 4)
            return new_data, 4
        else:
            new_data = "{0}        {1}".format(data, 0)
            return new_data, 0

    def save_data(self, new_data, dir, data):
        bs_path = os.getcwd()
        path = bs_path + os.path.sep + dir + os.path.sep
        if not os.path.exists(path):
            os.mkdir(path)
        with open(path + os.path.sep + data, "w", encoding="utf-8") as f:
            f.write(new_data)

    def run(self):
        # 获取子目录
        dir_list = os.listdir(self.base_path)
        print(dir_list)
        # 读取子目录下的所有文件名，获得列表
        for dir in dir_list:
            # print(dir)
            print(self.base_path + os.sep + dir)
            time.sleep(2)
            files_list = [filename for a, b, filename in os.walk(
                self.base_path + os.sep + dir)]
            print("file_list", files_list[0])

            for data in files_list[0]:
                time.sleep(5)
                # 读取数据
                # print(data)
                new_data, num = self.read_data(data, dir)
                if new_data is None:
                    continue
                # 将新的数据存入到文件中
                self.save_data(new_data, str(num), data)


if __name__ == '__main__':
    base_path = "/Users/zhangjintao/Desktop/dataNew"
    classify_list1 = ['飞机', '机票', '买飞机票', '坐飞机', '机场',
                      '登机牌', '登机', '登机口', '航班', '仓位', '登机时间', '订机票']

    r1 = r"飞机|机票|买飞机票|坐飞机|机场|登机牌|登机|登机口|航班|仓位|登机时间|订机票"
    r2 = r"火车|坐火车|高铁|硬座|软卧|和谐号|复兴号|硬卧|火车站|火车票"
    r3 = r"酒店|住宿|大床房|单间|总统套房"
    r4 = r"出差单|出差|差单"

    classify_list2 = ['火车', '坐火车', '高铁', '硬座',
                      '软卧', '和谐号', '复兴号', '硬卧', '火车站', '火车票']
    classify_list3 = ['酒店', '住宿', '大床房', '单间', '总统套房']
    classify_list4 = ['出差单', '出差', '差单']
    newData = NewData(base_path)
    newData.run()
