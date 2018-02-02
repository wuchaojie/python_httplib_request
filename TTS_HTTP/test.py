# -*- coding= UTF-8 -*-
'''
Created on 2016年4月22日

@author: wuchaojie
'''
import random
import json

dict = {}

def is_chinese(uchar):
        """判断一个unicode是否是汉字"""
        if uchar >= u'\u4e00' and uchar<=u'\u9fa5':
            return True
        else:
            return False
            
def check_contain_chinese(check_str):
    for ch in check_str.decode('utf-8'):
        if u'\u4e00' <= ch <= u'\u9fff':
           return True
    return False

# def is_chinese(s):
#     rt = False
#     if s>= u"\u4e00" and s<= u"\u9fa6":
#         rt = True
#     return rt

# ss = "中文测试測試請說ha".decode("utf-8")
# for row in ss:
#     print row,is_chinese(row)

testdata = open("C:/Users/wuchaojie/Desktop/nlu_result.txt", "rb").read()
i = 0
for line in testdata.split("\n") :
    parrator = line.find(":")
    parratorend = line.find(",")
    if parrator != -1 :
        value = line[parrator+1:parratorend]
        if check_contain_chinese(value):
            i = i + 1
            print i
            print value
            dict["city"+str(i)] = value

            
print json.dumps(dict, encoding='UTF-8', ensure_ascii=False)
with open("test1.txt", "a") as mjsn_file:
    #mjsn_file.write(json.dumps(content, ensure_ascii=False) + "\n")
    #for key,value in dict.items(): #无序
    for key,value in sorted(dict.items()): #有序
        mjsn_file.write(key + ":" + str(value) + "\n")
        pass
    
    
#     i+=1
#     if (i % 2) == 0:
#         #content.append(line.replace("\n", "")) 
#         with open("test.txt", "a") as mjsn_file:
#             #mjsn_file.write(json.dumps(content, ensure_ascii=False) + "\n")
#             mjsn_file.write(newline[1]+ "\n")
    


    