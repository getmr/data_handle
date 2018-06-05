#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : segment201861_6001.py
# @Author: Zhangjintao
# @Date  : 2018/6/1
# @Desc  : ���̶߳�ȡ
import json
import redis
import jieba
# ��Ҫ�������һ�����Ա�עģ��
import jieba.posseg
from collections import OrderedDict,Counter
import sys
import time
import logging
import os
import re
import threading
__author__ = 'wangg'
 
# ======================���õı��� begin=============================
duplicate_words_flag = True  # �Ƿ�����ȥ���ظ���True����
CHANNEL_SUB = 'standard-py'
CHANNEL_PUB = 'segment'
REDIS_HOST = '117.78.35.174'
REDIS_PORT = sys.argv[1]
REDIS_PASSWORD = 123456
REDIS_DB = 0
# ======================���õı��� end=============================
 
current_path =  os.getcwd()
log =  current_path + os.path.sep + 'log'
if not os.path.exists(log):
    os.mkdir(log)
 
 
def getLogger():
    logger = logging.getLogger(__name__)
    logger.setLevel(level=logging.INFO)
    handler = logging.FileHandler("{0}segment{1}.log".format(log+os.path.sep, REDIS_PORT) )
 
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(filename)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
 
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
 
    logger.addHandler(handler)
    logger.addHandler(console)
    return logger
 
 
logger = getLogger()
 
 
class PubSubHandlerThread(threading.Thread):
    """��Redis�����ж�ȡ���ݲ����зִʺʹ��Ա�ע"""
    pool = redis.ConnectionPool(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD, db=REDIS_DB)
    redisClient = redis.StrictRedis(connection_pool=pool)
 
    def __init__(self):
        threading.Thread.__init__(self)
 
    def run(self):
        p = PubSubHandlerThread.redisClient.pubsub()
        # ��ȡ����
        p.subscribe(CHANNEL_SUB)
        for message in p.listen():
            if message['type'] != 'message':
                continue
            logger.info('��{0}Ƶ��ȡ����������:{1}'.format(CHANNEL_SUB, message['data']))
            pushData, tf_idf = self.handlerData(message['data'])
            PubSubHandlerThread.redisClient.publish(CHANNEL_PUB, pushData)
            logger.info('����{0}Ƶ������:{1}'.format(CHANNEL_PUB, pushData))
            logger.info('Python�дʴ������')
 
    def cutWord(self, nlp0_data):
        logger.debug("________message________{}".format(nlp0_data))
        if duplicate_words_flag:
            seg = jieba.posseg.lcut(nlp0_data)
        # ��������Ĵ洢��ʽ
        # 1 ˳��洢
        l = [{i.word: i.flag} for i in seg if i.flag != 'x']
        # 2 ���TF�����洢
        # {"2018":2, "��": 1}
        # ���Թ���
        dis_list = ['c', 'e', 'nr', 'o', 'r', 'u', 'y', 'x']
        all_list = [i.word for i in seg if i.flag not in dis_list]
        num_dict = Counter(all_list)
 
        logger.debug("in cutWord�����������������дʺ�ķ��ؽ��������������{0}+++++++{1}".format(l, json.dumps(num_dict)))
        return l, num_dict
 
    def nlp_cut_word_one(self, nlp0_data):
        # �����л���ת���ֵ�
        logger.debug("����������������json����ǰ������������{}".format(nlp0_data))
        jsonObjs = json.loads(nlp0_data)
        logger.debug(
            "in nlp_cut_word_one ������������josn.loads��Ľ��������������{0}+++++++++++++{1}".format(jsonObjs, type(jsonObjs)))
        # �������keyֵmessage�������д�
        if 'message' in jsonObjs.keys():
            li, num_dict = self.cutWord(jsonObjs['message'])
            jsonObjs['segments'] = li
            dic = dict()
            dic["TF_IDF"] = num_dict
        logger.debug("in nlp_cut_word_one�����������������дʴ���󡪡�������������:{0}------------{1}".format(jsonObjs, dic))
        return jsonObjs, dic
 
    def handlerData(self, data):
        nlp, tf_idf = self.nlp_cut_word_one(data)
        # chattbody��ģ��ʱ��
        nlp['timeHandleEnd'] = str(int(round(time.time() * 1000)))
        # logger.info("����"+RedisHandler.redis_push_db+"����"+json.dumps(nlp).decode('utf-8').encode('utf-8'))
        nlp['operation'] = "Python�дʴ���"
        nlp = json.dumps(nlp, ensure_ascii=False).replace(': ', ':')
        tf_idf['timeHandleEnd'] = str(int(round(time.time() * 1000)))
        return nlp, tf_idf
 
    # ȥ�ظ����ʹ���
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