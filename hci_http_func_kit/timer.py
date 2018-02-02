#coding=utf-8
'''
Created on 2017-1-5

@author: libin
'''
import time

class Timer():

    def __init__(self, need_detail = False):
        self._need_detail = need_detail
        self._times = 0
        self._total_seconds = 0
        self._time_list = []
        
        self._start_time = None
        self._end_time = None

    
    def __add__(self, other_timer):
        newTimer = Timer(self._need_detail)
        newTimer += self
        newTimer += other_timer
        return newTimer
    
    def __iadd__(self, other_timer):
        self._times += other_timer._times
        self._total_seconds += other_timer._total_seconds
        if self._need_detail:
            self._time_list += other_timer._time_list
        return self
    
    def start(self):
        self._start_time = time.time()

    def end(self):
        self._end_time = time.time()
    
    def commit(self):
        delta_time = self._end_time - self._start_time
        self._times += 1
        self._total_seconds += delta_time
        if self._need_detail:
            self._time_list.append(delta_time)
    
    def get_delta_seconds(self):
        return self._end_time - self._start_time
    
    def get_total_seconds(self):
        return self._total_seconds
    
    def get_average_seconds(self):
        if self._times == 0:
            return 0
        else:
            return self._total_seconds / self._times
    
    def get_detail(self):
        return self._time_list
    
    def reset(self):
        self._times = 0
        self._total_seconds = 0
        self._time_list = []
        
        self._start_time = None
        self._end_time = None
    