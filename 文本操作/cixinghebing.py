from jieba import posseg
import jieba
from threading import Thread


jieba.load_userdict("./userdict.txt")


def hebing(word_list):
    x = len(word_list) - 1
    try:
        for i in range(0, x):
            if word_list[i].flag in ['m', 't'] and word_list[i+1].flag in ['m', 't']:
                print(word_list[i+1].flag)
                if word_list[i].flag == word_list[i+1].flag:
                    word_list[i].word = word_list[i].word + \
                        word_list[i + 1].word
                    del word_list[i + 1]
                elif word_list[i+1].flag == 't' and word_list[i].flag == 'm':
                    word_list[i].word = word_list[i].word + \
                        word_list[i + 1].word
                    if word_list[i + 1].flag == 't':
                        word_list[i].flag = 't'
                    del word_list[i + 1]
                x = len(word_list) - 1
        return word_list
    except:
        return hebing(word_list)


while True:
    s = input("请输入切词")
    word_list = posseg.lcut(s)
    print(word_list)
    hebing(word_list)
    print(word_list)
