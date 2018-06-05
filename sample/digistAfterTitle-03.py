#! /usr/bin/env python
# -*- coding:UTF-8 -*-
__author__ = 'wangg'
 
import os
import re
 
keyword_lists = [{'2': '��   ��Ʊ   ��վ  ����  ����  Ӳ��  Ӳ��  ����  ���� ����  ����   ̨��'}, {"1": '���� ��Ʊ  ������  ���� �ǻ���  ����  ����  ��λ  �����  �Ǽ�ʱ��  �ǻ���  �ǻ���  ����  �ܵ�  ��˾  ����ת��  ����� ���ò�  ��˰��  ���� ת�� �ɻ� ���չ�˾ �� �տ�'}, {'3': '�Ƶ�  ����  ���˼�  ����  ˫�˼� ��ͳ�׼�   ���� ס��  �󴲷�  ��������  ��ס  ��� ���Ƶ� �Ƶ�Ԥ��'}]
 
 
"""
����:Ҫ��extractFile-02��һ����ȡ���������õ������ļ�  �������ı�ǩ ���ɶ�Ӧ������   2�����  1 �ɻ�  3 �Ƶ����
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