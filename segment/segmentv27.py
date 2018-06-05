#! /usr/bin/env python
# -*- coding:UTF-8 -*-
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import json
import redis
import jieba
import jieba.posseg #需要另外加载一个词性标注模块
from collections import OrderedDict
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
REDIS_HOST='117.78.35.174'
REDIS_PORT=sys.argv[1]
REDIS_PASSWORD=123456
REDIS_DB=0
# ======================配置的变量 end=============================
 
current_path =  os.getcwd()
log =  current_path + os.path.sep + 'log'
if not os.path.exists(log):
    os.mkdir(log)
 
def getLogger():
    logger = logging.getLogger(__name__)
    logger.setLevel(level=logging.INFO)
    handler = logging.FileHandler("{0}segment{1}.log".format(log+os.path.sep, sys.argv[1]) )
 
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
 
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
 
    logger.addHandler(handler)
    logger.addHandler(console)
    return logger
logger = getLogger()
 
 
 
class PubSubHandlerThread(threading.Thread):
    """从Redis队列中读取数据并进行分词和词性标注"""
    pool = redis.ConnectionPool(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD, db=REDIS_DB)
    redisClient = redis.StrictRedis(connection_pool=pool)
    def __init__(self):
        threading.Thread.__init__(self)
 
    def run(self):
        p = PubSubHandlerThread.redisClient.pubsub()
        p.subscribe(CHANNEL_SUB)
        for message in p.listen():
            if message['type'] != 'message':
                continue
            logger.info('从{0}频道取出的数据是:{1}'.format(CHANNEL_SUB, message['data']))
            pushData = self.handlerData(message['data'])
            PubSubHandlerThread.redisClient.publish(CHANNEL_PUB, pushData)
            logger.info('放入{0}频道数据:{1}'.format(CHANNEL_PUB, pushData))
            logger.info('Python切词处理完成')
 
 
    def cutWord(self, nlp0_data):
        if duplicate_words_flag:
            m = re.compile("\\d").search(nlp0_data)
            if m is None:
                nlp0_data = ''.join(PubSubHandlerThread.distincWord(nlp0_data))
        seg = jieba.posseg.cut(nlp0_data)
        l = []
        for i in seg:
            l.append((i.word, i.flag))
        return l
 
    def nlp_cut_word_one(self, nlp0_data):
        jsonObjs = json.loads(str(nlp0_data))
        if unicode == type(jsonObjs):
            jsonObjs = jsonObjs.encode('utf-8')
            jsonObjs = json.loads(jsonObjs)
        for key, value in jsonObjs.items():
            if 'message' == key:
                li = self.cutWord(jsonObjs[key])
                dic = OrderedDict()
                for w, b in li:
                    dic[w] = b
                    jsonObjs['segments'] = dic
                jsonObjs['timeHandleStart'] = str(int(round(time.time() * 1000))) # chattbody入模型时间
                break
        return jsonObjs
 
    def handlerData(self, data):
        nlp = self.nlp_cut_word_one(data)
        nlp['timeHandleEnd'] = str(int(round(time.time() * 1000)))# chattbody出模型时间
        # logger.info("放入"+RedisHandler.redis_push_db+"数据"+json.dumps(nlp).decode('utf-8').encode('utf-8'))
        nlp['operation'] = "Python切词处理"
        nlp = json.dumps(nlp, ensure_ascii=False).replace(': ', ':')
        push_data = nlp.decode('utf-8').encode('utf-8')
        return push_data
 
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