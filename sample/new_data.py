#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : new_data.py
# @Author: Zhangjintao
# @Date  : 2018/6/1
# @Desc  : �޸��ı���ǩ
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
            return None,0
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
        # ��ȡ��Ŀ¼
        dir_list = os.listdir(self.base_path)
        print(dir_list)
        # ��ȡ��Ŀ¼�µ������ļ���������б�
        for dir in dir_list:
            # print(dir)
            print(self.base_path + os.sep + dir)
            time.sleep(2)
            files_list = [filename for a, b, filename in os.walk(self.base_path + os.sep + dir)]
            print("file_list", files_list[0])
 
            for data in files_list[0]:
                time.sleep(5)
                # ��ȡ����
                # print(data)
                new_data, num = self.read_data(data, dir)
                if new_data is None:
                    continue
                # ���µ����ݴ��뵽�ļ���
                self.save_data(new_data, str(num), data)
 
 
if __name__ == '__main__':
    base_path = "/Users/zhangjintao/Desktop/dataNew"
    classify_list1 = ['�ɻ�', '��Ʊ', '��ɻ�Ʊ', '���ɻ�', '����', '�ǻ���', '�ǻ�', '�ǻ���', '����', '��λ', '�ǻ�ʱ��', '����Ʊ']
 
    r1 = r"�ɻ�|��Ʊ|��ɻ�Ʊ|���ɻ�|����|�ǻ���|�ǻ�|�ǻ���|����|��λ|�ǻ�ʱ��|����Ʊ"
    r2 = r"��|����|����|Ӳ��|����|��г��|���˺�|Ӳ��|��վ|��Ʊ"
    r3 = r"�Ƶ�|ס��|�󴲷�|����|��ͳ�׷�"
    r4 = r"���|����|�"
 
    classify_list2 = ['��', '����', '����', 'Ӳ��', '����', '��г��', '���˺�', 'Ӳ��', '��վ', '��Ʊ']
    classify_list3 = ['�Ƶ�', 'ס��', '�󴲷�', '����', '��ͳ�׷�']
    classify_list4 = ['���', '����', '�']
    newData = NewData(base_path)
    newData.run()