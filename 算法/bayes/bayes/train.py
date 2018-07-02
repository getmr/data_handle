#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# version:python3.6
from scene.segment_train import corpus_segment
from scene.algorithm import MultinomialNB  # 导入多项式贝叶斯算法
from scene.bunch_train import corpus2Bunch
from scene.tools import readbunchobj
from scene.weight_space import vector_space
from scene.constant import *
from scene.constant import *
# from scene.constant import LinuxConstant

# step1: corpus_segment_mian.py
corpus_segment(corpus_path_train, seg_path_train)
# step2: corpus2Bunch.py
corpus2Bunch(wordbag_path_train, seg_path_train)
# step3: TFIDF_space.py
vector_space(stopword_path, wordbag_path_train, space_path_tfidf)
# step4:NBayes_Predict.py
train_set = readbunchobj(space_path_tfidf)
# 训练分类器：输入词袋向量和分类标签，alpha:0.001 alpha越小，迭代次数越多，精度越高
clf = MultinomialNB(alpha=0.001).fit(train_set.tdm, train_set.label)

print("训练完成")