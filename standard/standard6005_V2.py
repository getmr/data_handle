# -*- coding:utf-8 -*-

import logging
import json
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import re
import redis
import os
import threading
# ======================配置的变量 begin=============================
CHANNEL_SUB = 'socket'
CHANNEL_PUB = 'standard-py'
REDIS_HOST = '117.78.35.174'
REDIS_PORT = sys.argv[1]
REDIS_PASSWORD = 123456
REDIS_DB = 0
# alnum_to_chises       数字转汉字
# delPunctuae           去除标点特殊符号
# chises_to_alnum       汉字转数字
# remove_emotion        Emoji表情处理
method_list = ['delPunctuae', 'chises_to_alnum',
               'remove_emotion']  # 配置标准化方法按先后顺序运行

# ======================配置的变量 end=============================

current_path = os.getcwd()
log = current_path + os.path.sep + 'log'
if not os.path.exists(log):
    os.mkdir(log)


def getLogger():
    logger = logging.getLogger(__name__)
    logger.setLevel(level=logging.INFO)
    handler = logging.FileHandler(
        "{0}standard{1}.log".format(log + os.path.sep, sys.argv[1]))
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    console = logging.StreamHandler()
    console.setLevel(logging.INFO)

    logger.addHandler(handler)
    # logger.addHandler(console)
    return logger


logger = getLogger()


class StandardHandler(threading.Thread):
    pool = redis.ConnectionPool(
        host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD, db=REDIS_DB)
    redisClient = redis.StrictRedis(connection_pool=pool)

    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        p = StandardHandler.redisClient.pubsub()
        p.subscribe(CHANNEL_SUB)
        for message in p.listen():
            if message['type'] != 'message':
                continue
            logger.info('从{0}频道取出的数据是:{1}'.format(
                CHANNEL_SUB, message['data']))
            pushData = self.handler(message['data'])
            StandardHandler.redisClient.publish(CHANNEL_PUB, pushData)
            logger.info('放入{0}频道数据:{1}'.format(CHANNEL_PUB, pushData))
            logger.info('Python标准化处理完成')

    def get_chatbody_message(self, message):
        jsonObjs = json.loads(message)
        if unicode == type(jsonObjs):
            jsonObjs = jsonObjs.encode('utf-8')
            jsonObjs = json.loads(jsonObjs)

        for key, value in jsonObjs.items():
            if 'message' == key:
                messageType = jsonObjs['messageType']
                chatbody_newMessage = dispatcher(value, messageType)
                jsonObjs['message'] = chatbody_newMessage
                logger.info("Python进过一列标准化最后放到Chatboddy中message的数据为:%s" %
                            chatbody_newMessage)
                break
        return jsonObjs

    def handler(self, data):
        nlp = self.get_chatbody_message(data)
        nlp['operation'] = "python标准化"
        nlp = json.dumps(nlp, ensure_ascii=False).replace(': ', ':')
        push_data = nlp.decode('utf-8').encode('utf-8')
        return push_data

# --------------------------------去除标点符号 begin-----------------------


def delPunctuae(text_str):
    # 去除标点符号
    r = """[：，。、“”‘’’!"￥#$%&\'()*+,-./:;<=>?？@[\\]^_`{|}~，。（）《》【】‘’“”·、|]+""".decode(
        'utf-8')
    text = re.sub(r, '', text_str)
    return text.encode('utf-8').strip()
# ---------------------------------去除标点符号 end -----------------------------------


# ---------------------------------数字转汉字 begin---------------------

import types
import random


class NotIntegerError(Exception):
    pass


class OutOfRangeError(Exception):
    pass


_MAPPING = (u'零', u'一', u'二', u'三', u'四', u'五', u'六', u'七', u'八', u'九',)
_P0 = (u'', u'十', u'百', u'千',)
_S4, _S8, _S16 = 10 ** 4, 10 ** 8, 10 ** 16
_MIN, _MAX = 0, 9999999999999999


def num_to_chinese4(num):
    '''转换[0, 10000)之间的阿拉伯数字
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
common_used_numerals_tmp = {
    '零': 0, '一': 1, '二': 2, '两': 2, '三': 3, '四': 4, '五': 5, '六': 6, '七': 7, '八': 8, '九': 9, '十': 10, '百': 100, '千': 1000, '万': 10000, '亿': 100000000,
                            '壹': 1, '贰': 2, '叁': 3, '肆': 4, '伍': 5, '陆': 6, '柒': 7, '捌': 8, '玖': 9, '貮': 2, '两': 2, '〇': 0,
}
common_used_numerals = {}
for key in common_used_numerals_tmp:
    common_used_numerals[key.decode('utf-8')] = common_used_numerals_tmp[key]
# print common_used_numerals


def chinese2digits(uchars_chinese):
    uchars_chinese = uchars_chinese.decode('utf-8')
    total = 0
    r = 1  # 表示单位：个十百千...
    for i in range(len(uchars_chinese) - 1, -1, -1):
      val = common_used_numerals.get(uchars_chinese[i])
      if val >= 10 and i == 0:  # 应对 十三 十四 十*之类
        if val > r:
          r = val
          total = total + val
        else:
          r = r * val
          #total =total + r * x
      elif val >= 10:
        if val > r:
          r = val
        else:
          r = r * val
      else:
        total = total + r * val
    return total


# 正则匹配再将匹配内容转成汉字
def to_chinese_two(matched):
    value = matched.group('value')
    # print value
    # print type(value)
    # print value.encode('utf-8')
    # print to_chinese(value)
    return str(chinese2digits(value.encode('utf-8')))


# 将转换的汉字替换掉数字
def chises_to_alnum(text_str):
    text_str = re.sub(
        u"(?P<value>[一二三四五六七八九十壹贰叁肆伍陆柒捌玖拾貮两百千万亿]+)", to_chinese_two, text_str)
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
        if unicode == type(result):
            result = result.encode("utf-8")
        logger.info("Python调用方法%s标准化数据:%s" %
                    (eval(method).func_code.co_name, result))

    return result

# =========================调用标准化处理函数调度器  end =============================


class ThreadDispatcher(object):
    def __init__(self):
        pass

    def start(self):
        s = StandardHandler()
        s.start()
        s.join()


if __name__ == '__main__':
    ThreadDispatcher().start()
