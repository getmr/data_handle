# /usr/bin/python
# coding=utf-8
# file_name : handle_excel.py
# author    : zhangjintao
# date      : 2018/7/9
# desc      : excel表格数据处理
import xlrd
from collections import OrderedDict
import os
import time
import re


# excel文件的路径
excel_path = "/Users/zhangjintao/Desktop/标签文本/excel_file"
# 处理后数据存储路径
path = "/Users/zhangjintao/Desktop/标签文本/scene_data"
if not os.path.exists:
    os.mkdir(path)

# 获得所有excle的文件列表
excel_file_list = os.listdir(excel_path)
print(excel_file_list)
# 切换到Excel文件目录下操作excel
os.chdir("/Users/zhangjintao/Desktop/标签文本/excel_file")


convert_list = []
# 将excel数据转成键值对的格式
for excel_file in excel_file_list:
    wb = xlrd.open_workbook(excel_file)

    sh = wb.sheet_by_index(0)
    title = sh.row_values(0)
    for rownum in range(1, sh.nrows):
        rowvalue = sh.row_values(rownum)
        single = OrderedDict()
        for colnum in range(0, len(rowvalue)):
            # print(title[colnum], rowvalue[colnum])
            single[title[colnum]] = rowvalue[colnum]
        # print(single)
        # print(single.get("聊天内容"))
        convert_list.append(single)

for dic in convert_list:
    # print(dic)
    if str(dic.get("大场景")):
            if dic.get("小场景"):
                print(dic.get("大场景"), dic.get("小场景"))
                path_tag = path + os.path.sep + \
                    str(int(dic.get("大场景"))) + str(int(dic.get("小场景")))
                if not os.path.exists(path_tag):
                    os.mkdir(path_tag)
                os.chdir(path_tag)
            else:
                path_tag = path + os.path.sep + str(int(dic.get("大场景")))
                if not os.path.exists(path_tag):
                    os.mkdir(path_tag)
                os.chdir(path_tag)
            t = int(time.time() * 1000)
            with open("{}.txt".format(t), 'w') as f:
                text = re.sub(r"[\xa0 ]+", "", dic.get("聊天内容"))
                # print(text)
                f.write(text)
