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
# ======================���õı��� begin=============================
CHANNEL_SUB = 'socket'
CHANNEL_PUB = 'standard-py'
REDIS_HOST='117.78.35.174'
REDIS_PORT=sys.argv[1]
REDIS_PASSWORD=123456
REDIS_DB=0
# alnum_to_chises       ����ת����
# delPunctuae           ȥ������������
# chises_to_alnum       ����ת����
# remove_emotion        Emoji���鴦��
method_list = ['delPunctuae', 'chises_to_alnum', 'remove_emotion']  # ���ñ�׼���������Ⱥ�˳������
 
# ======================���õı��� end=============================
 
current_path =  os.getcwd()
log =  current_path + os.path.sep + 'log'
if not os.path.exists(log):
    os.mkdir(log)
 
def getLogger():
    logger = logging.getLogger(__name__)
    logger.setLevel(level=logging.INFO)
    handler = logging.FileHandler("{0}standard{1}.log".format(log + os.path.sep, sys.argv[1]))
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
 
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
 
    logger.addHandler(handler)
    # logger.addHandler(console)
    return logger
 
logger = getLogger()
 
class StandardHandler(threading.Thread):
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
            logger.info('��{0}Ƶ��ȡ����������:{1}'.format(CHANNEL_SUB, message['data']))
            pushData = self.handler(message['data'])
            StandardHandler.redisClient.publish(CHANNEL_PUB, pushData)
            logger.info('����{0}Ƶ������:{1}'.format(CHANNEL_PUB, pushData))
            logger.info('Python��׼���������')
 
 
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
                logger.info("Python����һ�б�׼�����ŵ�Chatboddy��message������Ϊ:%s"%chatbody_newMessage)
                break
        return jsonObjs
 
 
    def handler(self, data):
        nlp = self.get_chatbody_message(data)
        nlp['operation'] = "python��׼��"
        nlp = json.dumps(nlp, ensure_ascii=False).replace(': ', ':')
        push_data = nlp.decode('utf-8').encode('utf-8')
        return push_data
 
# --------------------------------ȥ�������� begin-----------------------
 
 
def delPunctuae(text_str):
    # ȥ��������
    r = """[������������������!"��#$%&\'()*+,-./:;<=>?��@[\\]^_`{|}~����������������������������|]+""".decode('utf-8')
    text = re.sub(r, '', text_str)
    return text.encode('utf-8').strip()
# ---------------------------------ȥ�������� end -----------------------------------
 
 
# ---------------------------------����ת���� begin---------------------
 
import types
import random
 
 
class NotIntegerError(Exception):
    pass
 
 
class OutOfRangeError(Exception):
    pass
 
 
_MAPPING = (u'��', u'һ', u'��', u'��', u'��', u'��', u'��', u'��', u'��', u'��',)
_P0 = (u'', u'ʮ', u'��', u'ǧ',)
_S4, _S8, _S16 = 10 ** 4, 10 ** 8, 10 ** 16
_MIN, _MAX = 0, 9999999999999999
 
 
def num_to_chinese4(num):
    '''ת��[0, 10000)֮��İ���������
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
        c = len(lst)  # λ��
        result = u''
 
        for idx, val in enumerate(lst):
            if val != 0:
                result += _P0[idx] + _MAPPING[val]
                if idx < c - 1 and lst[idx + 1] == 0:
                    result += u'��'
 
        return result[::-1].replace(u'һʮ', u'ʮ')
 
 
def _to_chinese8(num):
    assert (num < _S8)
    to4 = num_to_chinese4
    if num < _S4:
        return to4(num)
    else:
        mod = _S4
        high, low = num / mod, num % mod
        if low == 0:
            return to4(high) + u'��'
        else:
            if low < _S4 / 10:
                return to4(high) + u'����' + to4(low)
            else:
                return to4(high) + u'��' + to4(low)
 
 
def _to_chinese16(num):
    assert (num < _S16)
    to8 = _to_chinese8
    mod = _S8
    high, low = num / mod, num % mod
    if low == 0:
        return to8(high) + u'��'
    else:
        if low < _S8 / 10:
            return to8(high) + u'����' + to8(low)
        else:
            return to8(high) + u'��' + to8(low)
 
 
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
 
 
# ----------------------------------------------------------����ת���� end------------------
 
 
# ---------------------------------------------����ת���� begin---------------------------
common_used_numerals_tmp ={
                            '��':0, 'һ':1, '��':2, '��':2, '��':3, '��':4, '��':5, '��':6, '��':7, '��':8, '��':9, 'ʮ':10,'��':100,'ǧ':1000, '��':10000, '��':100000000,
                            'Ҽ' : 1, '��' : 2, '��' : 3, '��' : 4, '��' : 5, '½' : 6, '��' : 7, '��' : 8, '��' : 9, '�@' : 2, '��' : 2, '��' : 0,
}
common_used_numerals = {}
for key in common_used_numerals_tmp:
    common_used_numerals[key.decode('utf-8')] = common_used_numerals_tmp[key]
# print common_used_numerals
 
 
def chinese2digits(uchars_chinese):
    uchars_chinese = uchars_chinese.decode('utf-8')
    total = 0
    r = 1              #��ʾ��λ����ʮ��ǧ...
    for i in range(len(uchars_chinese) - 1, -1, -1):
      val = common_used_numerals.get(uchars_chinese[i])
      if val >= 10 and i == 0:  #Ӧ�� ʮ�� ʮ�� ʮ*֮��
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
 
 
# ����ƥ���ٽ�ƥ������ת�ɺ���
def to_chinese_two(matched):
    value = matched.group('value')
    # print value
    # print type(value)
    # print value.encode('utf-8')
    # print to_chinese(value)
    return str(chinese2digits(value.encode('utf-8')))
 
 
# ��ת���ĺ����滻������
def chises_to_alnum(text_str):
    text_str = re.sub(u"(?P<value>[һ�����������߰˾�ʮҼ��������½��ƾ�ʰ�@����ǧ����]+)", to_chinese_two, text_str)
    return text_str
 
# ----------------------------------------------����ת���� end -------------------------------------------
 
# -----------------------------------Emoji���鴦�� begin -----------------------
highpoints = re.compile(u'[\uD800-\uDBFF][\uDC00-\uDFFF]')
def remove_emotion(a):
    nickname = highpoints.sub(u'', a)
    return nickname
 
# -----------------------------------Emoji���鴦�� end -----------------------
 
 
# =========================���ñ�׼����������������  begin =============================
result = ""
def dispatcher(result, messageType):
    for method in method_list:
        if '11' == str(messageType):
            break
        result = eval(method)(result)
        if unicode == type(result):
            result = result.encode("utf-8")
        logger.info("Python���÷���%s��׼������:%s"%(eval(method).func_code.co_name, result))
 
    return result
 
# =========================���ñ�׼����������������  end =============================
 
class ThreadDispatcher(object):
    def __init__(self):
        pass
 
    def start(self):
        s = StandardHandler()
        s.start()
        s.join()
 
 
if __name__ == '__main__':
    ThreadDispatcher().start()