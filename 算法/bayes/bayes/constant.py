#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import platform
plat = platform.system()

# # 对训练集进行分词
# corpus_path_train = None  # 未分词分类语料库路径
# seg_path_train = None  # 分词后分类语料库路径
# # Bunch存储路径
# wordbag_path_train = None  # Bunch存储路径
# # IDF训练
# space_path_tfidf = None
# # 停顿词
# stopword_path = None
# seg_path_test = None  # 分词后分类语料库路径
#
# wordbag_path_test = None  # Bunch存储路径
# # 测试
# space_path_test = None


if 'Windows' == plat:
     # 对训练集进行分词
    corpus_path_train = "D:/dataset/train_corpus/"  # 未分词分类语料库路径
    seg_path_train = "D:/dataset/train_corpus_seg/"  # 分词后分类语料库路径
    # Bunch存储路径
    wordbag_path_train = "D:/dataset/bunch/train_set.dat"  # Bunch存储路径
    # IDF训练
    space_path_tfidf = "D:/dataset/bunch/tfdifspace.dat"
    # 停顿词
    stopword_path = "D:/dataset/stop_word/hlt_stop_words.txt"
    seg_path_test = "D:/dataset/test_corpus_seg/"  # 分词后分类语料库路径
    
    wordbag_path_test = "D:/dataset/bunch/"  # Bunch存储路径 
    # 测试
    space_path_test = "D:/dataset/bunch/testspace.dat"
    
else:
     # 对训练集进行分词
    corpus_path_train = "/data/ai/dataset/scene/train-scene/"  # 未分词分类语料库路径
    seg_path_train = "/data/ai/dataset/scene/train/"  # 分词后分类语料库路径
    # Bunch存储路径
    wordbag_path_train = "/data/ai/dataset/scene/bunch/train_set.dat"  # Bunch存储路径
    # IDF训练
    space_path_tfidf = "/data/ai/dataset/scene/bunch/tfdifspace.dat"
    # 停顿词
    stopword_path = "/data/ai/dataset/stopworld/hlt_stop_words.txt"
    seg_path_test = "/data/ai/dataset/scene/test_corpus_seg/"  # 分词后分类语料库路径  有待 创建
    
    wordbag_path_test = "/data/ai/dataset/scene/bunch/"  # Bunch存储路径
    # 测试
    space_path_test = "/data/ai/dataset/scene/bunch/testspace.dat"
    
    


