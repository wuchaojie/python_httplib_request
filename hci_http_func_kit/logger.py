#coding=utf-8
'''
Created on 2016-7-14

@author: libin
'''

import traceback
from logging import handlers
import logging

def log_traceback(fn):
    '''
    修饰方法, 用以在记录日志的同时打印调用位置
    '''
    def wrapper(self, msg):
        try:
            file_path = traceback.extract_stack()[-2][0]
            line = traceback.extract_stack()[-2][1]
            fn(self, " (" + file_path.split("\\")[-1] + " : " + str(line) + ")\t" + str(msg))
        except:
            print "log err failed"
    return wrapper

class Logger():        
    def __init__(self, logName, loglevel=logging.DEBUG, consolelevel=logging.DEBUG, when="H", interval=2, backupCount=6):
        """
        Constructor
        """
        self._logger = logging.getLogger(logName)# 获取名为logName的logger 
        handler = handlers.TimedRotatingFileHandler(logName,when=when,interval=interval, backupCount=backupCount, encoding=None, delay=False, utc=False)
        formatter = logging.Formatter('%(asctime)s p:%(process)d t:%(thread)d %(levelname)s %(message)s')
        handler.setFormatter(formatter)
        handler.setLevel(loglevel)
        self._logger.addHandler(handler)
        
        console = logging.StreamHandler()
        console.setLevel(consolelevel)
        formatter = logging.Formatter('%(asctime)s t:%(thread)d %(levelname)s %(message)s')
        console.setFormatter(formatter)
        self._logger.addHandler(console)         
        self._logger.setLevel(logging.DEBUG)
        
    
    def debug(self, msg):
        """
        记录debug级别的日志
        """
        if self._logger is not None:
            self._logger.debug("> "+str(msg))
                     
    def info(self, msg):
        """
        记录info级别的日志
        """
        if self._logger is not None:
            self._logger.info("> "+str(msg))
            
    def warning(self, msg):
        """
        记录warning级别的日志
        """
        if self._logger is not None:
            self._logger.warning("> "+str(msg))
            
    @log_traceback
    def error(self, msg):
        """
        记录error级别的日志
        """
        if self._logger is not None:
            self._logger.error("> "+str(msg))
        
        return self._logger
              
    def critical(self, msg):
        """
        记录critical级别的日志
        """
        if self._logger is not None:
            self._logger.critical("> "+str(msg))
    