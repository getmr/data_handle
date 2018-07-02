#!/usr/bin/env python

import uuid
import os
import re
from scene.application import get
from scene.logger import logger
# dataset_test_path = "D:/dataset/train_corpus/"
dataset_test_path = "/data/ai/aiworking/testbayes/dataset-use"
uuidStr = str(uuid.uuid4()).replace("-", '')  

count = 0
count_tag = 0
class CircleDir(object):
    file_list = []

    def circle_dir(self, filepath):
        files = os.listdir(filepath)
        for fi in files:
            fi_d = os.path.join(filepath, fi)
            if os.path.isdir(fi_d):
                self.circle_dir(fi_d)
            else:
                CircleDir.file_list.append(os.path.join(filepath, fi_d))

        return CircleDir.file_list

circledir = CircleDir()
files = circledir.circle_dir(dataset_test_path)
for f in files:
    try:
        with open(f, 'rb') as fr:
            content = fr.read().decode('utf-8')
            logger.info("从{0}中读取出来的数据是:{1}".format(f, content))
            content_reverse = content[::-1].strip()
            if content_reverse:
                tag = re.match(r"\d", content_reverse).group()
                logger.info("获取到的tag信息:{0}".format(tag))
                count_tag += 1
                chatbody_message = content_reverse[1::][::-1]
                logger.info("获取到的message信息:{0}".format(chatbody_message))
                scene =  get(uuidStr,chatbody_message)
                if str(scene) == str(tag):
                    count += 1
    except Exception as e:
        logger.error(e)
                
print(count)
print(count_tag)
print(count/count_tag)
logger.info("统计的count信息:{0}".format(count))
logger.info("统计的文本数量信息:{0}".format(count_tag))
logger.info("统计的bayes准确率:{0}".format(count/count_tag))
                

    
