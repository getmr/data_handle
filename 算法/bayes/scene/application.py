#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from scene.constant import *
from scene.segment_main import corpus_segment_main
from scene.bunch_main import corpus2Bunch
from scene.tools import readbunchobj
from scene.weight_space import vector_space
from scene.train import clf
from scene.constant import *
import os
import logging

current_path =  os.getcwd()
log =  current_path + os.path.sep + 'log'
if not os.path.exists(log):
    os.mkdir(log)
 
 
def getLogger():
    logger = logging.getLogger(__name__)
    logger.setLevel(level=logging.INFO)
    handler = logging.FileHandler("{0}{1}.log".format(log+os.path.sep, "scene") )
 
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(filename)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
 
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
 
    logger.addHandler(handler)
    logger.addHandler(console)
    return logger
 
 
logger = getLogger()



def get(uid,massage):
    
    corpus_segment_main(uid,massage)
    
    corpus2Bunch(uid)
    
    vector_space(stopword_path, wordbag_path_test + uid +'.dat', space_path_test, space_path_tfidf)
    
    test_set = readbunchobj(space_path_test)
    
    predicted,mat = clf.predict(test_set.tdm)

    ecpect = predicted[0]
    logger.info("概率预测值矩阵"+str(predicted))
    return ecpect
