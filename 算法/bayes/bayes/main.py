#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import sys
import threading
import redis
import os
import logging
import json
from scene.application import *

# ======================配置的变量 begin=============================
duplicate_words_flag = True  # 是否启动去掉重复词True启动
CHANNEL_SUB = 'standard'
CHANNEL_PUB = {0: "node", 1: "plane", 2: "node",
               3: "hotel", 4: "sheet", 5: "node", 6: "node", 7: "node"}
REDIS_HOST = '117.78.35.174'
REDIS_PORT = 6001
REDIS_PASSWORD = 'aibot123456'
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
        "{0}{1}.log".format(log+os.path.sep, "scene"))

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


class SceneHandlerThread(threading.Thread):

    pool = redis.ConnectionPool(
        host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD, db=REDIS_DB)
    redisClient = redis.StrictRedis(connection_pool=pool)

    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        p = SceneHandlerThread.redisClient.pubsub()
        # 读取数据
        p.subscribe(CHANNEL_SUB)
        # 场景分类字典
        scene_dict = {"0": "其他（默认）", "1": "订机票", "2": "订火车票",
                      "3": "订酒店", "4": "出差单", "5": "登录", "6": "用户基本信息", "7": "企业相关"}
        for message in p.listen():
            if message['type'] != 'message':
                continue
            # 读取数据
            # print(message['data'].decode('utf-8')["operation"])
            read_data = message.get("data").decode("utf-8")
            json_read_dict = json.loads(read_data)
            json_read_dict["operation"] = "开始场景估计"
            logger.info('从{0}频道取出的数据是:{1}'.format(CHANNEL_SUB, json_read_dict))
            # data = message.get("data").decode("utf-8")
            # json_dict = json.loads(data)
            uid = json_read_dict.get('uId')
            chatBody_message = json_read_dict.get('message').strip()
            messageType = json_read_dict.get('messageType')
            scene = get(uid, chatBody_message)
            messageType_first_num = list(str(messageType))[0]
            chatBody = json.loads(message['data'].decode('utf-8'))
            # if messageType_first_num != str(scene):
            #chatBody["messageType"] = "{}000".format(scene)
            if str(messageType) == "59":
                chatBody["scene"] = scene
            elif str(scene) in ['1', '2', '3']:
                if str(scene) == messageType_first_num:
                    chatBody["scene"] = messageType_first_num
                else:
                    chatBody["scene"] = scene
            elif str(messageType) != str(0):
                chatBody["scene"] = messageType_first_num
            else:
                chatBody["scene"] = scene
            scene = chatBody["scene"]
            chatBody["operation"] = "场景估计完成:{}".format(scene_dict.get(scene))
            if scene == '0':
                chatBody['messageType'] = scene
                CHANNEL_PUB_scene = CHANNEL_PUB.get(0)
            elif scene == '1':
                CHANNEL_PUB_scene = CHANNEL_PUB.get(1)
            elif scene == '2':
                CHANNEL_PUB_scene = CHANNEL_PUB.get(2)
            elif scene == '3':
                CHANNEL_PUB_scene = CHANNEL_PUB.get(3)
            elif scene == '4':
                CHANNEL_PUB_scene = CHANNEL_PUB.get(4)
            elif scene == '5':
                CHANNEL_PUB_scene = CHANNEL_PUB.get(5)
            elif scene == '6':
                CHANNEL_PUB_scene = CHANNEL_PUB.get(6)
            else:
                CHANNEL_PUB_scene = CHANNEL_PUB.get(7)
            chatBody = json.dumps(chatBody, ensure_ascii=False)
            SceneHandlerThread.redisClient.publish(CHANNEL_PUB_scene, chatBody)
            logger.info('放入{0}频道数据:{1}'.format(CHANNEL_PUB_scene, chatBody))


obj = SceneHandlerThread()
obj.start()
obj.join()
