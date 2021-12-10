# coding:utf-8
# @Time : 2021/11/19 14:46
# @Author : 郑攀
# @File ： conversion.py
# @Software : PyCharm
import csv
import os
import time

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# -*- coding: utf-8 -*-
# 加载自定义词
import synonyms
import jieba
import re
import warnings
warnings.filterwarnings("ignore")
from aip import AipNlp
APP_ID = '25241652'
API_KEY = 'AarC0lsmRrdrS2dIEGmpvDGK'
SECRET_KEY = 'MoFEfWdQadecVdqyIEFRGbqP4LxAKaZz'
client = AipNlp(APP_ID, API_KEY, SECRET_KEY)

stop_table = ['你', '了', '我', '啊', '是', '呢', '吧', '的', '地', '呀', '个', '哪', '在', '非常', '和', '好', '很', '又', '有', '还',
              '上', '都', '也', '起来', '不', '?', '选', '用', '大', '高', '就', '给',
              '着', '快', '买', '这',  '吗', '什么', '怎么', 'hellip',
              '!', '.', '？', '！', '。', '…', '，', ',', '、', '/', '+', '_', '-', '*', '-', '&', '@', '(', ')', '%', '$',
              '#', ' ', ':', '：', ';', '[', ']', "'", '\\', 'n', '~', '（', '）']
dictionary = ['效果','正品','价格','味道','质量','品牌','物流','包装','发货','服务']

def format1(list1):
    a = []
    for s in list1:
        a1 = list(jieba.cut(s))
        a.append(a1)
    for i in range(0, len(a)):
        for item in stop_table:
            while item in a[i]:
                a[i].remove(item)
    return a
doc_set = []
with open('天猫+复方氨酚烷胺片.csv', "r", encoding='utf-8') as f:  # 打开文件
    read = csv.reader(f)
    for line in read:
        doc_set.append(line[1])
sentences = format1(doc_set)

pattern = r',|\.|/|;|\'|`|\[|\]|<|>|\?|:|"|\{|\}|\~|!|@|#|\$|%|\^|&|\(|\)|-|=|\_|\+|，|。|、|；|‘|’|【|】|·|！| |…|（|）'

fp = open('天猫+复方氨酚烷胺片+处理完.csv', 'a+', newline='', encoding='utf-8')
write = csv.writer(fp)
# write.writerow(['字典属性','商品属性','相似性','商品属性所在短句','短句积极性','短句消极性','置信度','情感类别'])
for i in range(0,len(sentences)):
    result_list = re.split(pattern,doc_set[i])
    for word in sentences[i]:
        for dic in dictionary:
            result = synonyms.compare(word, dic, seg=False)
            if result>0.7:
                for short_sentence in result_list:
                    if word in short_sentence:
                        sentiment = client.sentimentClassify(short_sentence)
                        print(i,sentiment)
                        positive = str(sentiment['items'][0]['positive_prob'])
                        negative = str(sentiment['items'][0]['negative_prob'])
                        confidence = str(sentiment['items'][0]['confidence'])
                        emotion = str(sentiment['items'][0]['sentiment'])
                        string = [dic, word, result,short_sentence,positive,negative,confidence,emotion]
                        write.writerow(string)
                        time.sleep(1)

fp.close()