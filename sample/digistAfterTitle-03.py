#! /usr/bin/env python
# -*- coding:UTF-8 -*-
__author__ = 'wangg'
 
import os
import re
 
keyword_lists = [{'2': '火车   火车票   火车站  高铁  软卧  硬卧  硬座  软座  上铺 下铺  中铺   台铁'}, {"1": '机场 机票  机建费  机建 登机牌  航班  航班  舱位  候机厅  登记时间  登机牌  登机口  廊桥  跑道  航司  行李转盘  商务舱 经济舱  免税店  海关 转机 飞机 航空公司 民航 空客'}, {'3': '酒店  房间  单人间  包间  双人间 总统套间   连锁 住宿  大床房  房间数量  入住  快捷 订酒店 酒店预定'}]
 
 
"""
需求:要将extractFile-02这一步提取出来的有用的样本文件  问题后面的标签 换成对应的数字   2代表火车  1 飞机  3 酒店相关
"""
# parent_dir = '/home/python/fh/aaa'
dirValue = '/root/Data/Data5/dataNew'
dir_list = os.listdir(dirValue)
 
 
 
 
 
taglists = []
 
txt_list = []
for dirone in dir_list:
    with open(dirValue + '/' + dirone, 'r') as f:
        content = f.read().decode("utf-8").encode("utf-8")
        match = re.match(r".*?\s{4}(.*)", content)
        if(match):
            tag = match.group(1).strip()
            tag_terms_list = tag.split()
            # print tag_terms_list
            for tag_terms in tag_terms_list:
                # taglists.append(tag_terms)
                # if tag_terms in tag_str:
                #     txt_list.append(dirone)
                #     break
 
                # tag_str_list = tag_str.split()
                # for tagstr in tag_str_list:
                #     if tagstr in tag_terms:
                #         txt_list.append(dirone)
                #         exit_flag = True
                #         break
                # if exit_flag:
                #     break
 
                for keyword_dict in keyword_lists:
                    exit_flag = False
                    for key,value in keyword_dict.items():
                        value_list = value.split()
                        for value in value_list:
                            if value in tag_terms:
                                with open(dirValue + "/" + dirone, "r") as f1, open(dirValue + "/" + dirone + ".bak", "w") as f2:
                                    for line in f1:
                                        f2.write(re.sub(tag, key, line))
                                os.remove(dirValue + '/' + dirone)
                                os.rename(dirValue + "/" + dirone + ".bak", dirValue + '/' + dirone)
                                exit_flag = True
                                break
                        if exit_flag:
                            break