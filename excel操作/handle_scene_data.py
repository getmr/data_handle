# /usr/bin/python
# coding=utf-8
# file_name : scene_tags.py
# author    : zhangjintao
# date      : 2018/7/9
# desc      : json样本过滤
import re
import json
import os
import time


path = "/Users/zhangjintao/Desktop/标签文本/scene_data"
file_list = os.listdir("/Users/zhangjintao/Desktop/标签文本/file_json")
# print(file_list)
for file in file_list:
    with open("/Users/zhangjintao/Desktop/标签文本/file_json/%s" % file, 'r', encoding='utf-8') as f:
        json_data = f.read()
        # print(json_data)
        data_list = json.loads(json_data)
        # print(data_list)

    # 写入文件
    for dic in data_list:
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
