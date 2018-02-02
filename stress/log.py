#!/usr/bin/python
#coding=utf-8

#import logging
from logging import handlers
import logging
import os
import random


class Logger:        
    def __init__(self, logName):
        self._logger = logging.getLogger(logName)# 获取名为logName的logger 
        handler = logging.handlers.TimedRotatingFileHandler(logName,when="D",interval=1, backupCount=0, encoding=None, delay=False, utc=False)
        formatter = logging.Formatter('%(asctime)s ********* %(message)s')
        handler.setFormatter(formatter)
        self._logger.addHandler(handler)
        self._logger.setLevel(logging.INFO)
        
    def log(self, msg):
        if self._logger is not None:
            self._logger.info(msg)
            
    def get_test_list(self):
        init_chars = 'abcdefghijklmnopqrstuvwxzyABCDEFGHIJKLMNOPQRSTUVWXYZ'
        test_list=[]
        for i in range(0, 100000):
            random_char = random.sample(init_chars, 15)
            dst_char = ''.join(random_char)
            test_list.append(dst_char)
        return test_list
    
if __name__ == "__main__":
    log1 = Logger("log1.txt")
    test_chars = log1.get_test_list()
    for item in test_chars:
        log1.log(str(item)) 
    log2 = Logger("log2.txt")
    log2.log("hdfaad,fdas")