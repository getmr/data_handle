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
����:��dirvalueĿ¼���ж����ȡ����������   ÿ���������ݶ���һ�в��������� ������4���ո�Ȼ������������������б�ǩ(��ǩ֮���ÿո����)
    Ҫ���ľ��ǿ���Щ�����ļ��б�ǩ�����tag_str�е���Щ��ô��Щ�����ļ��������õ�Ҫ��dirvalueĿ¼�н���Щ���õ��ļ���ȡ��һ����Ŀ¼��dirvalue414�в���ԭ��Ŀ¼dirvalue��ɾ��
 
    ��ȡ�����ļ� ��û�н���ǩת��Ϊ��Ӧ������
"""
 
dirValue = '/root/Data/Data5'
circleObj = circleDir.CircleDir()
dir_list = circleObj.circle_dir(dirValue)
 
# dir_list = os.listdir(dirValue)
taglists = []
tag_str = """
��   ��Ʊ   ��վ  ����  ����  Ӳ��  Ӳ��  ����  ���� ����  ����   ̨��
���� ��Ʊ  ������  ���� �ǻ���  ����  ����  ��λ  �����  �Ǽ�ʱ��  �ǻ���  �ǻ���  ����  �ܵ�  ��˾  ����ת��  ����� ���ò�  ��˰��  ���� ת�� �ɻ� ���չ�˾ �� �տ�
�Ƶ�  ����  ���˼�  ����  ˫�˼� ��ͳ�׼�   ���� ס��  �󴲷�  ��������  ��ס  ��� ���Ƶ� �Ƶ�Ԥ��ll
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