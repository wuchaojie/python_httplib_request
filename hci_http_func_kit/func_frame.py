#coding=utf-8
'''
Created on 2016-11-1

@author: libin
'''
import re
import time
import json
import xls_helper
from .hci_helper import HttpHelper

class HttpFuncFrame():
    
    def __init__(self, 
                 excel_file, 
                 http_helper,
                 funcs,
                 write_result=True):
        self._excel_file = excel_file
        if not isinstance(http_helper, HttpHelper):
            raise Exception("http_helper must be a instance of hci_http_test_kit.hci_helper.HttpHelper")
        self._http_helper = http_helper
        self._write_result = write_result
        self._filter = []
        self._funcs = funcs
        
        self._func_test = xls_helper.load_data_by_excel_file(self._excel_file)
        
    
    def run(self):
        #读取Excel文件
        self._http_helper._logger.info(str(time.asctime()))
        self._http_helper._logger.info("---Read Excel File---")

        
        #初始化时间和计数器,打印日志
        start_time = time.time()
        self._http_helper._logger.info("--------Start--------")
        runcase_count = 0
        
        #执行方法
        for case in self._func_test['cases']:
            if len(self._filter) > 0 and len(self._filter[0])>0:
                if case['casename'] not in self._filter:
                    continue
            self._http_helper._logger.info("-----Run " + case['casename'] + "-----")
            for func in case['func']:
                self._http_helper._logger.debug(json.dumps(func))
                try:
                    getattr(self._funcs, func['funcname'])(case['casename'], func)
                except Exception,ex:
                    self._http_helper._logger.error(str(ex)+ " in get attr")
            runcase_count += 1
            self._http_helper._logger.info("-----------------------------------------------------------------------------------")
        end_time = time.time()
                
        pass_count = 0;
        #将结果写回Excel, 数据结构写入testcase_construction.txt , 统计失败case数量
        if self._write_result:
            self._http_helper._logger.info("---Write Result To Excel File---")
            pass_count = xls_helper.write_result_to_excel_file(self._excel_file, self._func_test)
            #数据
            test_case_file = open("testcase_construction.txt","wb")
            test_case_file.write(str(json.dumps(self._func_test, ensure_ascii=False, indent=4)))
            test_case_file.close
        failed_count = runcase_count - pass_count
    
        #打印结果
        self._http_helper._logger.info("--------Done--------")
        self._http_helper._logger.info("共运行  "+str(runcase_count)+" 个测试用例")
        if self._write_result:
            self._http_helper._logger.info("成功 : " + str(pass_count) + " 个")
            self._http_helper._logger.info("失败 : " + str(failed_count) + " 个")
        self._http_helper._logger.info("共耗时: " + str(end_time-start_time) + " 秒")
        self._http_helper._logger.info("--------End---------")
        
    def get_detail(self):
        return self._func_test
        
    def set_funcs(self, funcs):
        self._funcs = funcs
        
    def set_filter(self, case_filter):
        self._filter = case_filter
        
    def get_funcs(self):
        return self._funcs
        
    def get_runable_funcs(self):
        runable_funcs = dir(self._funcs)
        i = 0
        while i < (len(runable_funcs)):
            if re.match("\A__",runable_funcs[i]):
                del runable_funcs[i]
            else:
                i += 1
        return runable_funcs