#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@version: python3.6
@author: XiangguoSun
@contact: sunxiangguodut@qq.com
@file: corpus2Bunch.py
@time: 2018/1/23 16:12
@software: PyCharm
"""

import os
import pickle

from sklearn.datasets.base import Bunch
from scene.tools import readfile
from scene.constant import *

def corpus2Bunch(uid):
# space_path_tfidf = "D:/dataset/bunch/tfdifspace.dat" 

# wordbag_path_test = "/data/dataset/bunch/"  # Bunch存储路径 
    wordbag_path_test1 = wordbag_path_test
    if not os.path.exists(wordbag_path_test1):
        os.makedirs(wordbag_path_test1)
        
    fullname = seg_path_test + uid +'.txt'    # 分词后的文件
        
#     catelist = os.listdir(seg_path)  # 分词后的路径
    # 创建一个Bunch实例
    bunch = Bunch(target_name=[], label=[], filenames=[], contents=[])
#     bunch.target_name.extend(catelist)
    '''
    extend(addlist)是python list中的函数，意思是用新的list（addlist）去扩充
    原来的list
    '''
    # 获取每个目录下所有的文件
#     for mydir in catelist:
#         class_path = seg_path + mydir + "/"  # 拼出分类子目录的路径
#         file_list = os.listdir(class_path)  # 获取class_path下的所有文件
#         for file_path in file_list:  # 遍历类别目录下文件
#             fullname = class_path + file_path  # 拼出文件名全路径
#             bunch.label.append(mydir)
#             bunch.filenames.append(fullname)
#             bunch.contents.append(readfile(fullname))  # 读取文件内容
#             '''append(element)是python list中的函数，意思是向原来的list中添加element，注意与extend()函数的区别'''
            
    bunch.filenames.append(fullname)
    bunch.contents.append(readfile(fullname))  # 读取文件内容
    
    # 将bunch存储到wordbag_path路径中
    with open(wordbag_path_test + uid +'.dat', "wb") as file_obj:
        pickle.dump(bunch, file_obj)
    print("构建文本对象结束！！！")