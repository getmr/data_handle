#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@version: python3.6
@author: XiangguoSun
@contact: sunxiangguodut@qq.com
@file: corpus_segment.py
@time: 2018/1/23 16:12
@software: PyCharm
"""
import os
import jieba
import json

from scene.tools import savefile, readfile
from scene.constant import *

def corpus_segment_main(uid,message):
    print("玩儿命分词中...")
#         '''
    content = message.encode("utf-8")
    content = content.replace('\r\n'.encode('utf-8'), ''.encode('utf-8')).strip()  # 删除换行
    content = content.replace(' '.encode('utf-8'), ''.encode('utf-8')).strip()  # 删除空行、多余的空格
    content_seg = jieba.cut(content)  # 为文件内容分词
# 
    seg_path = seg_path_test
    
    if not os.path.exists(seg_path):
        os.makedirs(seg_path)
#     
    savefile(seg_path + uid +'.txt', ' '.join(content_seg).encode('utf-8'))  # 将处理后的文件保存到分词后语料目录

    print("中文语料分词结束！！！")
