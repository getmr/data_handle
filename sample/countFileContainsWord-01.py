#! /usr/bin/env python
# -*- coding:UTF-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
__author__ = 'wangg'
 
import os
import re
import string
 
 
"""
在dirvalue目录下有爬取到的样本文件(问题 4个空格 标签 标签) 就是看哪些文件中的标签包含tag_str这些关键字并将这些包含关键字的文件统计一下个数s
 
"""
dirValue = '/home/python/fh/datanew'
dir_list = os.listdir(dirValue)
taglists = []
tag_str = """
火车   火车票   火车站  高铁  软卧  硬卧  硬座  软座  上铺 下铺  中铺   台铁
机场 机票  机建费  机建 登机牌  航班  航班  舱位  候机厅  登记时间  登机牌  登机口  廊桥  跑道  航司  行李转盘  商务舱 经济舱  免税店  海关 转机 飞机
酒店  房间  单人间  包间  双人间 总统套间   连锁 住宿  大床房  房间数量  入住  快捷
"""
 
 
txt_list = []
for dirone in dir_list:
    with open(dirValue + '/' + dirone, 'r') as f:
        content = f.read().decode("utf-8").encode("utf-8")
        match = re.match(r".*?\s{4}(.*)", content)
        if(match):
            tag = match.group(1).strip()
            tag_terms_list = tag.split("    ")
            # print tag_terms_list
            exit_flag = False
            for tag_terms in tag_terms_list:
                # taglists.append(tag_terms)
                # if tag_terms in tag_str:
                #     txt_list.append(dirone)
                #     break
 
                tag_str_list = tag_str.split()
                for tagstr in tag_str_list:
                    if tagstr in tag_terms:
                        txt_list.append(dirone)
                        exit_flag = True
                        break
                if exit_flag:
                    break
 
 
print len(txt_list)
 
print '买飞机票' in '机票'
print string.rfind('买飞机票', '机票士大夫撒')
 
print '买飞机票'.find("机场 机票  机建费")