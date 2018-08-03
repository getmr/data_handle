# coding:utf-8
'''
Created on 2018/7/11 上午9:08
@author: zhangjintao
'''
import jieba
import os
import jieba.posseg as pg


# 训练样本集路径
data_path = "/home[表情]otao/Desktop/1"

sentences = []
file_name = os.listdir(data_path)
for file in file_name:
    with open(data_path + os.path.sep + file, "r") as f:
        sentence = f.read()
    # seg = pg.lcut(sentence)
    # words = [i.word for i in seg if i.flag not in ["x", "r"]]
    sentences.append(jieba.lcut(sentence))


import numpy
# 将预处理过的"词库"保存到文件中，便于调试
numpy_array = numpy.array(sentences)
numpy.save('sentences.npy', numpy_array)

# 将预处理后的"词库"从文件中读出，便于调试
numpy_array = numpy.load('sentences.npy')
sentences = numpy_array.tolist()

num_features = 300
#　单词出现最少次数
min_word_count = 5
num_workers = 2
context = 5
downsampling = 1e-3

from gensim.models import word2vec

model = word2vec.Word2Vec(sentences, workers=num_workers, size=num_features, min_count=min_word_count, window=context,
                          sample=downsampling)

model.init_sims(replace=True)

# # 保存word2vec训练参数便于调试
# model.wv.save_word2vecmorning('word2vec_model.bin', binary=True)
# model.wv.load_word2vecmorning('word2vec_model.bin', binary=True)

print('词语相似度计算morning')
print('飞机 vs 机票:')
print(model.n_similarity('飞机', '机票'))
print('机场 vs 机票:')
print(model.n_similarity('机场', '机票'))
# # print('你好 vs 你好:')
# print(model.n_similarity('航班', '机票'))
print('行程 vs 机场:')
print(model.n_similarity('行程', '机场'))
print('住宿 vs 酒店:')
print(model.n_similarity('住宿', '酒店'))

print(model.wv.similarity("飞机", "机票"))
print(model.wv.similarity('住宿', '酒店'))
print(model.similar_by_word("飞机"))
print(model.similarity('住宿', '酒店'))
# 可以支持列表
print(model.n_similarity('住宿', '酒店'))
# 余弦相似度
print(model.wv.similarity('住宿', '酒店'))
