#coding=utf-8
'''
Created on 2016-11-29

@author: libin
'''
import time
import datetime
import threading
from .logger import Logger
from .hci_helper import HttpHelper

class HttpStressFrame():
    
    def __init__(self, 
                 http_helper, 
                 thread_num=1, 
                 cycle_time=datetime.timedelta(weeks=0,days=3,hours=00,minutes=00,seconds=0,microseconds=0,milliseconds=0), 
                 need_analyze_response=True
                 ):
        
        if not isinstance(http_helper, HttpHelper):
            raise Exception("http_helper must be a instance of hci_http_test_kit.hci_helper.HttpHelper")
        self._http_helper = http_helper
        self._logger = self._http_helper._logger
        self._thread_num = thread_num
        self._cycle_time = cycle_time
        self._need_analyze_response = need_analyze_response
        
    def main_thread(self):
        self.setup()
        
        #create thread
        thread_list=[]
        
        if self._logger is None:
            self._logger = Logger("StressTest_"+str(time.strftime("%Y_%m_%d_%H_%M_%S"))+".log")
        
        for i in range(self._thread_num):
            thread_name = 'thread-' + str(i)
            new_thread = threading.Thread(target = self.stress_thread, args = (), name = thread_name)
            thread_list.append(new_thread)
            new_thread.start()

        # join
        for thread_obj in thread_list:
            thread_obj.join()
             
        self.teardown()
        
    def setup(self):
        '''
        This method is executed at the beginning of the main_thread() method is called
        '''
        pass
    
    def teardown(self):
        '''
        This method is executed at the ending of the main_thread() method is called
        '''
        pass
    
    def config(self):
        '''
        
        '''
        return "this is parent config"
    
    def body(self):
        return "this is parent body"
    
    def config_and_body(self):
        return self.config() , self.body()
    
    def stress_thread(self):
        #loop
        start_time = datetime.datetime.today()
        while (datetime.datetime.today()-start_time)<=self._cycle_time:
            self.run()
        self._logger.info("Thread end")
        
    def run(self):
        config,body = self.config_and_body()
        response = self._http_helper.do_request(config,body)[1]
        if self._need_analyze_response:
            return response, self._http_helper.analyze_result(response)
        return response
        
    def start(self):
        return self.main_thread()
        
    def sstart(self):
        newthread = threading.Thread(target = self.main_thread, args = (), name = "main_thread")
        newthread.start()
        return newthread
    
    def set_thread_num(self, thread_num):
        self._thread_num = thread_num
        
    def get_thread_num(self):
        return self._thread_num
        
    def set_cycle_time(self, cycle_time):
        self._cycle_time = cycle_time
        
    def get_cycle_time(self):
        return self._cycle_time
    