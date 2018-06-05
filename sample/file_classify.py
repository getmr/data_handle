#! /usr/bin/env python
# -*- coding:UTF-8 -*-
import os
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
 
__author__ = 'wangg'
 
"""
����:�ж��txt�ļ� (ÿ��txt�ļ���һ�к���ո�+��ǩ����)
    Ҫ������txt�ļ��ϲ���һ��txt�ļ�(����:����ǩ���ַ����ű����ǩΪ1��ȫ������һ��txt�ļ��б�ǩΪ2�ķ�һ���ļ�....)
"""
 
 
class FileClassify(object):
    def proc(self, fp, tset):
        for line in fp:
            tset.append(line)
        return tset
 
    def dir_list(self, parent_dir):
        dir_list = os.listdir(parent_dir)
        nums = list()
        for txt_file in dir_list:
            with open(parent_dir + "/" + txt_file, 'r') as f:
                nums = self.proc(f, nums)
        temp = list(set(nums))
        temp.sort(key=nums.index)
        return temp
 
    def write_content(self, fw, line_list):
        for content in line_list:
            fw.write(content)
        fw.write(os.linesep)
        fw.close()
 
    def output_file(self, parent_dir, file_name):
        """����ļ��б�"""
        fp = open(parent_dir + '/' + file_name, "w")
        for num in self.dir_list(parent_dir):
            fp.write(num)
        fp.close()
 
    def classify_text(self, parent_dir, file_name):
        fr = open(parent_dir + '/' + file_name, 'r')
        for line in fr:
            line_list = line.split()
            if len(line_list) <= 1:
                continue
            if line_list[-1] == '1':
                with open(parent_dir + '/' + '1.txt', 'a+') as f:
                    self.write_content(f, line_list[:-1])
            elif line_list[-1] == '2':
                with open(parent_dir + '/' + '2.txt', 'a+') as f:
                    self.write_content(f, line_list[: -1])
 
            elif line_list[-1] == '3':
                with open(parent_dir + '/' + '3.txt', 'a+') as f:
                    self.write_content(f, line_list[: -1])
 
 
if __name__ == "__main__":
    parent_dir = '/home/python/fh/txt3wan/demo'  # �ļ�Ŀ¼λ��
    out_file = "newdemo.txt"  # ������ļ��Ⱥϲ������ָ���ļ�Ȼ�������ļ����и��ݱ�ǩ����
    fobj = FileClassify()
    fobj.output_file(parent_dir, out_file)
    fobj.classify_text(parent_dir, out_file)