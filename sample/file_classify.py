#! /usr/bin/env python
# -*- coding:UTF-8 -*-
import os
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
 
__author__ = 'wangg'
 
"""
需求:有多个txt文件 (每个txt文件是一行后面空格+标签数字)
    要将这多个txt文件合并成一个txt文件(需求:按标签数字分类存放比如标签为1的全部放在一个txt文件中标签为2的放一个文件....)
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
        """输出文件列表"""
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
    parent_dir = '/home/python/fh/txt3wan/demo'  # 文件目录位置
    out_file = "newdemo.txt"  # 将多个文件先合并到这个指定文件然后从这个文件进行根据标签分类
    fobj = FileClassify()
    fobj.output_file(parent_dir, out_file)
    fobj.classify_text(parent_dir, out_file)