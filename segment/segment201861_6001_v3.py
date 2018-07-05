#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : segment201861_6001.py
# @Author: Zhangjintao
# @Date  : 2018/6/1
# @Desc  : 多线程读取
import json
import redis
import jieba
# 需要另外加载一个词性标注模块
import jieba.posseg
from collections import OrderedDict, Counter
import sys
import time
import logging
import os
import re
import threading
__author__ = 'wangg'

# ======================配置的变量 begin=============================
duplicate_words_flag = True  # 是否启动去掉重复词True启动
CHANNEL_SUB = 'standard-py'
CHANNEL_PUB = 'segment'
REDIS_HOST = '117.78.35.174'
REDIS_PORT = sys.argv[1]
REDIS_PASSWORD = 123456
REDIS_DB = 0
# ======================配置的变量 end=============================

current_path = os.getcwd()
log = current_path + os.path.sep + 'log'
if not os.path.exists(log):
    os.mkdir(log)


def getLogger():
    logger = logging.getLogger(__name__)
    logger.setLevel(level=logging.INFO)
    handler = logging.FileHandler(
        "{0}segment{1}.log".format(log+os.path.sep, REDIS_PORT))

    handler.setLevel(logging.INFO)
    formatter = logging.Formatter(
        '%(asctime)s - %(filename)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    console = logging.StreamHandler()
    console.setLevel(logging.INFO)

    logger.addHandler(handler)
    logger.addHandler(console)
    return logger


logger = getLogger()


class PubSubHandlerThread(threading.Thread):
    """从Redis队列中读取数据并进行分词和词性标注"""
    pool = redis.ConnectionPool(
        host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD, db=REDIS_DB)
    redisClient = redis.StrictRedis(connection_pool=pool)

    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        p = PubSubHandlerThread.redisClient.pubsub()
        # 读取数据
        p.subscribe(CHANNEL_SUB)
        for message in p.listen():
            if message['type'] != 'message':
                continue
            logger.info('从{0}频道取出的数据是:{1}'.format(
                CHANNEL_SUB, message['data']))
            pushData, tf_idf = self.handlerData(message['data'])
            PubSubHandlerThread.redisClient.publish(CHANNEL_PUB, pushData)
            logger.info('放入{0}频道数据:{1}'.format(CHANNEL_PUB, pushData))
            logger.info('Python切词处理完成')

    def cutWord(self, nlp0_data):
        logger.debug("________message________{}".format(nlp0_data))
        if duplicate_words_flag:
            seg = jieba.posseg.lcut(nlp0_data)
        # 构造所需的存储格式
        # 1 顺序存储
        l = [{i.word: i.flag} for i in seg if i.flag != 'x']
        # 2 针对TF计数存储
        # {"2018":2, "年": 1}
        # 词性过滤
        dis_list = ['c', 'e', 'nr', 'o', 'r', 'u', 'y', 'x']
        all_list = [i.word for i in seg if i.flag not in dis_list]
        num_dict = Counter(all_list)

        logger.debug(
            "in cutWord————————切词后的返回结果——————{0}+++++++{1}".format(l, json.dumps(num_dict)))
        return l, num_dict

    def nlp_cut_word_one(self, nlp0_data):
        # 反序列化，转成字典
        logger.debug("————————json处理前——————{}".format(nlp0_data))
        jsonObjs = json.loads(nlp0_data)
        logger.debug(
            "in nlp_cut_word_one ——————josn.loads后的结果——————{0}+++++++++++++{1}".format(jsonObjs, type(jsonObjs)))
        # 如果存在key值message，进行切词
        if 'message' in jsonObjs.keys():
            li, num_dict = self.cutWord(jsonObjs['message'])
            jsonObjs['segments'] = li
            dic = dict()
            dic["TF_IDF"] = num_dict
        logger.debug(
            "in nlp_cut_word_one————————切词处理后————————:{0}------------{1}".format(jsonObjs, dic))
        return jsonObjs, dic

    def handlerData(self, data):
        nlp, tf_idf = self.nlp_cut_word_one(data)
        # chattbody出模型时间
        nlp['timeHandleEnd'] = str(int(round(time.time() * 1000)))
        # logger.info("放入"+RedisHandler.redis_push_db+"数据"+json.dumps(nlp).decode('utf-8').encode('utf-8'))
        nlp['operation'] = "Python切词处理"
        nlp = json.dumps(nlp, ensure_ascii=False).replace(': ', ':')
        tf_idf['timeHandleEnd'] = str(int(round(time.time() * 1000)))
        return nlp, tf_idf

    # 去重复单词功能
    @staticmethod
    def distincWord(text_str):
        seg = list(set(text_str))
        seg.sort(key=text_str.index)
        return seg


class ThreadDispatcher(object):
    def __init__(self):
        pass

    def start(self):
        s = PubSubHandlerThread()
        s.start()
        s.join()


if __name__ == '__main__':
    ThreadDispatcher().start()