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
��dirvalueĿ¼������ȡ���������ļ�(���� 4���ո� ��ǩ ��ǩ) ���ǿ���Щ�ļ��еı�ǩ����tag_str��Щ�ؼ��ֲ�����Щ�����ؼ��ֵ��ļ�ͳ��һ�¸���s
 
"""
dirValue = '/home/python/fh/datanew'
dir_list = os.listdir(dirValue)
taglists = []
tag_str = """
��   ��Ʊ   ��վ  ����  ����  Ӳ��  Ӳ��  ����  ���� ����  ����   ̨��
���� ��Ʊ  ������  ���� �ǻ���  ����  ����  ��λ  �����  �Ǽ�ʱ��  �ǻ���  �ǻ���  ����  �ܵ�  ��˾  ����ת��  ����� ���ò�  ��˰��  ���� ת�� �ɻ�
�Ƶ�  ����  ���˼�  ����  ˫�˼� ��ͳ�׼�   ���� ס��  �󴲷�  ��������  ��ס  ���
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
 
print '��ɻ�Ʊ' in '��Ʊ'
print string.rfind('��ɻ�Ʊ', '��Ʊʿ�����')
 
print '��ɻ�Ʊ'.find("���� ��Ʊ  ������")