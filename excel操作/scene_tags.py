# /usr/bin/python
# coding=utf-8
# file_name : scene_tags.py
# author    : zhangjintao
# date      : 2018/7/9
# desc      : excel转json
import xlrd
from collections import OrderedDict
import json
import codecs

wb = xlrd.open_workbook('/Users/zhangjintao/Desktop/标签文本/聊天记录标签.xlsx')

convert_list = []
sh = wb.sheet_by_index(0)
title = sh.row_values(0)
for rownum in range(1, sh.nrows):
    rowvalue = sh.row_values(rownum)
    single = OrderedDict()
    for colnum in range(0, len(rowvalue)):
        # print(title[colnum], rowvalue[colnum])
        single[title[colnum]] = rowvalue[colnum]
    print(single)
    convert_list.append(single)

j = json.dumps(convert_list, ensure_ascii=False)

with codecs.open('file3.json', "w", "utf-8") as f:
    f.write(j)
