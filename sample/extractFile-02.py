#! /usr/bin/env python
# -*- coding:UTF-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
 
from shutil import copy
__author__ = 'wangg'
 
import os
import re
import circleDir
 
"""
需求:在dirvalue目录下有多个爬取的样本数据   每个样本数据都是一行并且是问题 后面是4个空格然后后面是这个问题的所有标签(标签之间用空格隔开)
    要做的就是看这些样本文件中标签如果是tag_str中的这些那么这些样本文件就是有用的要从dirvalue目录中将这些有用的文件提取到一个新目录中dirvalue414中并从原来目录dirvalue中删除
 
    提取有用文件 还没有将标签转换为对应的数字
"""
 
dirValue = '/root/Data/Data5'
circleObj = circleDir.CircleDir()
dir_list = circleObj.circle_dir(dirValue)
 
# dir_list = os.listdir(dirValue)
taglists = []
tag_str = """
火车   火车票   火车站  高铁  软卧  硬卧  硬座  软座  上铺 下铺  中铺   台铁
机场 机票  机建费  机建 登机牌  航班  航段  舱位  候机厅  登记时间  登机牌  登机口  廊桥  跑道  航司  行李转盘  商务舱 经济舱  免税店  海关 转机 飞机 航空公司 民航 空客
酒店  房间  单人间  包间  双人间 总统套间   连锁 住宿  大床房  房间数量  入住  快捷 订酒店 酒店预定ll
"""
os.mkdir(dirValue + '/' + "dataNew")
os.mkdir(dirValue + '/' + "others")
 
dirValue414 = dirValue + '/' + "dataNew"
dirvalueOthers = dirValue + "/" + "others"
 
txt_list = []
for dirone in dir_list:
    with open(dirone, 'r') as f:
        content = f.read().decode("utf-8").encode("utf-8")
        match = re.match(r".*?\s{4}(.*)", content)
        if(match):
            tag = match.group(1).strip()
            tag_terms_list = tag.split()
            # print tag_terms_list
 
            exit_flag = False
            for tag_terms in tag_terms_list:
                # taglists.append(tag_terms)
 
                tag_str_list = tag_str.split()
                for tagstr in tag_str_list:
                    if tagstr in tag_terms:
                        txt_list.append(dirone)
                        copy(dirone, dirValue414 + "/" + os.path.split(dirone)[1])
                        os.remove(dirone)
                        exit_flag = True
                        break
 
                if exit_flag:
                    break
 
            if not exit_flag:
                copy(dirone, dirvalueOthers + "/" + os.path.split(dirone)[1])
                os.remove(dirone)
 
                # if tag_terms in tag_str:
                #     txt_list.append(dirone)
                #     copy(dirValue + "/" + dirone, dirValue414+"/"+dirone)
                #     os.remove(dirValue + "/" + dirone)
                #     break
 
 
 
 
# print len(txt_list)