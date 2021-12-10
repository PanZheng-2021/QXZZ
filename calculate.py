# coding:utf-8
# @Time : 2021/11/28 15:57
# @Author : 郑攀
# @File ： calculate.py
# @Software : PyCharm
import csv
import os

file = '天猫+连花清瘟+处理完.csv'

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
dictionary = ['效果','正品','价格','味道','质量','品牌','物流','包装','发货','服务']

doc_set = []
with open(file, "r", encoding='utf-8') as f:  # 打开文件
    read = csv.reader(f)
    for line in read:
        doc_set.append(line)

print(file)
for i in range(0,len(dictionary)):
    sentiment = []
    for j in range(0,len(doc_set)):
        if dictionary[i]==doc_set[j][0]:
            sentiment.append(doc_set[j][7])
    sentiment_2 = sentiment.count('2')
    positive = sentiment_2/len(sentiment)
    print(dictionary[i],positive)