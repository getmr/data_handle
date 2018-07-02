#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : segmentAndStandard_v3.py
# @Author: Zhangjintao
# @Date  : 2018/6/5
# @Desc  : 多线程标准化和切词处理


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


# ====================== 加载自定义词典==============================
# user_list = os.listdir("./word_dict")
# for file in user_list:
#     jieba.load_userdict("./word_dict/{}".format(file))

# ======================配置的变量 begin=============================
duplicate_words_flag = True  # 是否启动去掉重复词True启动
CHANNEL_SUB = 'socket'
CHANNEL_PUB = 'segment-standard'

REDIS_HOST = '117.78.35.174'
REDIS_PORT = 6001
REDIS_PASSWORD = 'aibot123456'
REDIS_DB=0

try:
    name = sys.argv[2]
except:
    pass


"""
alnum_to_chises       数字转汉字
delPunctuae           去除标点特殊符号
chises_to_alnum       汉字转数字
remove_emotion        Emoji表情处理
num_to_ch            数字一一转汉字
"""
method_list = ['delPunctuae', 'chises_to_alnum', 'remove_emotion']  # 配置标准化方法按先后顺序运行

# ======================配置的变量 end=============================

current_path =  os.getcwd()
log =  current_path + os.path.sep + 'log'
if not os.path.exists(log):
    os.mkdir(log)


def getLogger():
    logger = logging.getLogger(__name__)
    logger.setLevel(level=logging.INFO)
    handler = logging.FileHandler("{0}segment_standard{1}.log".format(log + os.path.sep, REDIS_PORT))
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    console = logging.StreamHandler()
    console.setLevel(logging.INFO)

    logger.addHandler(handler)
    logger.addHandler(console)
    return logger


logger = getLogger()


class StandardHandler():
    pool = redis.ConnectionPool(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD, db=REDIS_DB)
    redisClient = redis.StrictRedis(connection_pool=pool)

    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        p = StandardHandler.redisClient.pubsub()
        p.subscribe(CHANNEL_SUB)
        for message in p.listen():
            if message['type'] != 'message':
                continue
            logger.info('从{0}频道取出的数据是:{1}'.format(CHANNEL_SUB, message['data'].decode("utf-8")))
            pushData = self.handler_standard(message['data'])
            # 添加切词处理
            logger.info("--------开始切词--------{}".format(pushData))
            pushData, tf_idf = self.handler_segment(pushData)
            StandardHandler.redisClient.publish(CHANNEL_PUB, pushData)
            logger.info('放入{0}频道数据:{1}'.format(CHANNEL_PUB, pushData))
            logger.info('Python切词处理完成')

    def get_chatbody_message(self, message):
        # 转字典
        jsonObjs = json.loads(message.decode())

        if 'message' in jsonObjs:
            messageType = jsonObjs['messageType']
            value = jsonObjs['message']
            chatbody_newMessage = dispatcher(value, messageType)
            jsonObjs['message'] = chatbody_newMessage
            # logger.info("Python进过一列标准化最后放到Chatboddy中message的数据为:%s" %
            #             chatbody_newMessage)
        return jsonObjs

    def handler_standard(self, data):
        nlp = self.get_chatbody_message(data)
        nlp['operation'] = "python标准化"
        nlp = json.dumps(nlp, ensure_ascii=False).replace(': ', ':')
        push_data = nlp
        return push_data

    def cutWord(self, nlp0_data):
        jieba.load_userdict("userdict.txt")
        if duplicate_words_flag:
            seg = jieba.posseg.lcut(nlp0_data)
        logger.info("原声切词"+str(seg))
        # 相同词性临近词合并
        seg = hebing(seg)
        # 构造所需的存储格式
        # 1 顺序存储
        # l = [{i.word: i.flag} for i in seg if i.flag != 'x']
        # 去r, p
        l = [{i.word: i.flag} for i in seg if i.flag not in ['x', 'r', 'p', 'uj']]
        # 2 针对TF计数存储
        # {"2018":2, "年": 1}
        # 词性过滤
        dis_list = ['c', 'e', 'nr', 'o', 'r', 'u', 'y', 'x', 'r', 'p']
        all_list = [i.word for i in seg if i.flag not in dis_list]
        num_dict = Counter(all_list)
        return l, num_dict

    def nlp_cut_word_one(self, nlp0_data):
        # 反序列化，转成字典
        jsonObjs = json.loads(nlp0_data)
        # 如果存在key值message，进行切词
        if 'message' in jsonObjs.keys():
            li, num_dict = self.cutWord(jsonObjs['message'])
            jsonObjs['segments'] = li
            dic = dict()
            dic["TF_IDF"] = num_dict
        return jsonObjs, dic

    def handler_segment(self, data):
        nlp, tf_idf = self.nlp_cut_word_one(data)
        # chattbody出模型时间
        nlp['timeHandleEnd'] = str(int(round(time.time() * 1000)))
        # logger.info("放入"+RedisHandler.redis_push_db+"数据"+json.dumps(nlp).decode('utf-8').encode('utf-8'))
        nlp['operation'] = "Python切词处理"
        nlp = json.dumps(nlp, ensure_ascii=False).replace(': ', ':')
        tf_idf['timeHandleEnd'] = str(int(round(time.time() * 1000)))
        return nlp, tf_idf


# --------------------------------------------合并相同临近词性的词 -------------------------------------------
def hebing(word_list):
    x = len(word_list) - 1
    try:
        for i in range(0, x):
            if word_list[i].flag in ['m', 't'] and word_list[i + 1].flag in ['m', 't']:
                print(word_list[i + 1].flag)
                if word_list[i].flag == word_list[i + 1].flag:
                    word_list[i].word = word_list[i].word + word_list[i + 1].word
                    del word_list[i + 1]
                elif word_list[i + 1].flag == 't' and word_list[i].flag == 'm':
                    word_list[i].word = word_list[i].word + word_list[i + 1].word
                    if word_list[i + 1].flag == 't':
                        word_list[i].flag = 't'
                    del word_list[i + 1]
                x = len(word_list) - 1
        return word_list
    except:
        return hebing(word_list)
# --------------------------------------------数字转汉字（单个一一转）begin------------------------------------


def num2chinese(num):
    num_list = list(num)
    num_dict = {
        '0': '零',
        '1': '一',
        '2': '二',
        '3': '三',
        '4': '四',
        '5': '五',
        '6': '六',
        '7': '七',
        '8': '八',
        '9': '九'
    }
    num_ch_list = [num_dict[i] for i in num_list if i in num_dict]
    str_num = ''.join(num_ch_list)
    return str_num


# 正则匹配再将匹配内容转成汉字
def num_2_ch(matched):
    value = matched.group('value')

    return str(num2chinese(value))


# 数字转文字
def num_to_ch(text_str):
    # print("________进入ch2num_______", text_str, type(text_str))
    text_str = re.sub(
        "(?P<value>\d+)", num_2_ch, text_str)
    # print("________chiese2alnum______", text_str)
    return text_str

# --------------------------------------------数字转汉字（单个一一转）end------------------------------------


# --------------------------------------------时间冒号问题 begin------------------------------------


def time_colon(text_str):
    bold = re.compile(r'(\d):(\d)')
    text_str = bold.sub(r'\1点\2', text_str)
    return text_str

# --------------------------------------------时间冒号问题 end------------------------------------

# --------------------------------去除标点符号 begin-----------------------


def delPunctuae(text_str):
    # 去除标点符号
    r = """[\s\n]+"""
    text = re.sub(r, '', text_str)
    # logger.debug("in delPunctuae ——————————去除标点符号后的数据————————{}".format(text))
    return text.strip()

# ---------------------------------去除标点符号 end -----------------------------------


# ---------------------------------数字转汉字 begin---------------------

import types


class NotIntegerError(Exception):
    pass


class OutOfRangeError(Exception):
    pass


_MAPPING = (u'零', u'一', u'二', u'三', u'四', u'五', u'六', u'七', u'八', u'九',)
_P0 = (u'', u'十', u'百', u'千',)
_S4, _S8, _S16 = 10 ** 4, 10 ** 8, 10 ** 16
_MIN, _MAX = 0, 9999999999999999


def num_to_chinese4(num):
    '''
    转换[0, 10000)之间的阿拉伯数字
    '''
    assert (0 <= num and num < _S4)
    if num < 10:
        return _MAPPING[num]
    else:
        lst = []
        while num >= 10:
            lst.append(num % 10)
            num = num / 10
        lst.append(num)
        c = len(lst)  # 位数
        result = u''

        for idx, val in enumerate(lst):
            if val != 0:
                result += _P0[idx] + _MAPPING[val]
                if idx < c - 1 and lst[idx + 1] == 0:
                    result += u'零'

        return result[::-1].replace(u'一十', u'十')


def _to_chinese8(num):
    assert (num < _S8)
    to4 = num_to_chinese4
    if num < _S4:
        return to4(num)
    else:
        mod = _S4
        high, low = num / mod, num % mod
        if low == 0:
            return to4(high) + u'万'
        else:
            if low < _S4 / 10:
                return to4(high) + u'万零' + to4(low)
            else:
                return to4(high) + u'万' + to4(low)


def _to_chinese16(num):
    assert (num < _S16)
    to8 = _to_chinese8
    mod = _S8
    high, low = num / mod, num % mod
    if low == 0:
        return to8(high) + u'亿'
    else:
        if low < _S8 / 10:
            return to8(high) + u'亿零' + to8(low)
        else:
            return to8(high) + u'亿' + to8(low)


def to_chinese(num):
    if type(num) != types.IntType and type(num) != types.LongType:
        raise NotIntegerError(u'%s is not a integer.' % num)
    if num < _MIN or num > _MAX:
        raise OutOfRangeError(u'%d out of range[%d, %d)' % (num, _MIN, _MAX))

    if num < _S4:
        return num_to_chinese4(num)
    elif num < _S8:
        return _to_chinese8(num)
    else:
        return _to_chinese16(num)


def to_chinese_(matched):
    value = int(matched.group('value'))
    # print type(value)
    # print to_chinese(value)
    return str(to_chinese(value).encode('utf-8'))


def alnum_to_chises(text_str):
    text_str = re.sub('(?P<value>\d+)', to_chinese_, text_str)
    return text_str


# ----------------------------------------------------------数字转汉字 end------------------


# ---------------------------------------------汉字转数字 begin---------------------------
CN_NUM = {
    '〇': 0,
    '一': 1,
    '二': 2,
    '三': 3,
    '四': 4,
    '五': 5,
    '六': 6,
    '七': 7,
    '八': 8,
    '九': 9,

    '零': 0,
    '壹': 1,
    '贰': 2,
    '叁': 3,
    '肆': 4,
    '伍': 5,
    '陆': 6,
    '柒': 7,
    '捌': 8,
    '玖': 9,

    '貮': 2,
    '两': 2,
}
CN_UNIT = {
    '十': 10,
    '拾': 10,
    '百': 100,
    '佰': 100,
    '千': 1000,
    '仟': 1000,
    '万': 10000,
    '萬': 10000,
    '亿': 100000000,
    '億': 100000000,
    '兆': 1000000000000,
}


def cn2dig(cn):
    res = re.search(r'[十拾百佰千仟万萬亿億兆]', cn)

    # print(res)
    lcn = list(cn)
    if res is not None:
        if len(set(lcn)) == 1:
            return cn
        # print(lcn)
        unit = 0  # 当前的单位
        ldig = []  # 临时数组

        while lcn:
            cndig = lcn.pop()

            if CN_UNIT.get(cndig):
                unit = CN_UNIT.get(cndig)
                if unit == 10000:
                    ldig.append('w')  # 标示万位
                    unit = 1
                elif unit == 100000000:
                    ldig.append('y')  # 标示亿位
                    unit = 1
                elif unit == 1000000000000:  # 标示兆位
                    ldig.append('z')
                    unit = 1

                continue

            else:
                dig = CN_NUM.get(cndig)

                if unit:
                    dig = dig * unit
                    unit = 0

                ldig.append(dig)

        if unit == 10:  # 处理10-19的数字
            ldig.append(10)

        ret = 0
        tmp = 0

        while ldig:
            x = ldig.pop()

            if x == 'w':
                tmp *= 10000
                ret += tmp
                tmp = 0

            elif x == 'y':
                tmp *= 100000000
                ret += tmp
                tmp = 0

            elif x == 'z':
                tmp *= 1000000000000
                ret += tmp
                tmp = 0

            else:
                tmp += x

        ret += tmp
        return ret

    else:
        li = []
        if len(lcn) > 1:
            for i in lcn:
                if i in CN_NUM:
                    li.append(str(CN_NUM[i]))
            # print(li)
            return ''.join(li)
        else:
            if lcn[0] in CN_NUM:
                return CN_NUM[lcn[0]]


# 正则匹配再将匹配内容转成汉字
def to_chinese_two(matched):
    value = matched.group('value')
    # print value
    # print type(value)
    # print value.encode('utf-8')
    # print to_chinese(value)
    return str(cn2dig(value))


# 汉字转数字
def chises_to_alnum(text_str):
    # print("________进入ch2num_______",text_str)
    text_str = re.sub(
        "(?P<value>[一二三四五六七八九十壹贰叁肆伍陆柒捌玖拾貮两百千万亿零〇]+)", to_chinese_two, text_str)
    # print("________chiese2alnum______", text_str)
    return text_str


# ----------------------------------------------汉字转数字 end -------------------------------------------


# -----------------------------------Emoji表情处理 begin -----------------------

highpoints = re.compile(u'[\uD800-\uDBFF][\uDC00-\uDFFF]')


def remove_emotion(a):
    nickname = highpoints.sub(u'', a)
    return nickname

# -----------------------------------Emoji表情处理 end -----------------------


# =========================调用标准化处理函数调度器  begin =============================
result = ""


def dispatcher(result, messageType):
    for method in method_list:
        if '11' == str(messageType):
            break
        result = eval(method)(result)
        # logger.info("Python调用方法%s标准化数据:%s" %
        #             (eval(method).__name__, result))
    return result

# =========================调用标准化处理函数调度器  end =============================


class ThreadDispatcher(object):
    def __init__(self):
        pass

    def start(self):
        s = StandardHandler()
        s.run()
        logger.info("------------------- start is OK -----------------")
        # s.join()


if __name__ == '__main__':
    ThreadDispatcher().start()


