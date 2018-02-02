#coding=utf-8
'''
Created on 2017��11��8��

@author: wuchaojie
'''
import json
import time
import httplib
from hci_http_func_kit.logger import Logger
from hci_http_func_kit.hci_helper import HttpHelper, HttpHeadModel
from hci_http_func_kit import xls_helper
from hci_http_tts.func_frame import HttpFuncFrame
import hashlib
import chardet



TEST_DATA = "../Data/TestData/"
TEST_RESULT = "../Data/test/"
TEST_TXT = "../Data/TestData/"
MD5 = {}
md5_list = []

class TTSFuncTest():
    
    def SynthText(self,case_name, params):
        
        body = open(TEST_TXT + params['body'],'rb').read()
        print chardet.detect(body)
        voice,ErrorNo,resMessage = func_helper.do_request(params['config'],body, http_path = params['httppath'])    
        with open(TEST_RESULT+ params['voice_result'],'wb') as v_file:
            v_file.write(voice)
        params['actual1']  = ErrorNo
        params['actual2']  = resMessage

    def SynthMD5(self,case_name, params):
        
        body = open(TEST_TXT + params['body'],'rb').read()
        if(len(MD5) == 0):
            MD5['config1'] = params['config'] 
            voice1,ErrorNo,resMessage = func_helper.do_request(MD5['config1'],body, http_path = params['httppath'])   
            with open(TEST_RESULT+ params['voice_result'],'wb+') as v_file:
                v_file.write(voice1) 
                
            md5file1 = open(TEST_RESULT+ params['voice_result'],'rb').read()
            md5_1 = hashlib.md5(md5file1).hexdigest()
            md5_list.append(md5_1)
    
            params['actual1']  = ErrorNo
            params['actual2']  = resMessage
            params['result']  = "Audio is the default value !"
        else:
            MD5['config2'] = params['config'] 
            json_md5 = json.dumps(MD5)
            print json_md5
            voice2,ErrorNo,resMessage = func_helper.do_request(MD5['config2'],body, http_path = params['httppath'])   
            with open(TEST_RESULT+ params['voice_result'],'wb+') as v_file:
                v_file.write(voice2)
                
            md5file2 = open(TEST_RESULT+ params['voice_result'],'rb').read()
            md5_2 = hashlib.md5(md5file2).hexdigest()
            #md5_list.append(md5_2+"1")
            md5_list.append(md5_2)
                
            params['actual1']  = ErrorNo
            params['actual2']  = resMessage
            #将两个音频的MD5值做对比
        if(len(md5_list) == 2):
            if (cmp(md5_list[0],md5_list[1]) == 0):
                params['result']  = "The md5 of the audio is equal!"
                print "The md5 of the audio is equal !"
            else:
                params['result']  = "The md5 of the audio is not equal!"
                print "The md5 of the audio is not equal !"
#             if(len(md5_list) == 2):
            global md5_list
            global MD5
            print md5_list           
            md5_list = []
            MD5 = {}
            
        
#     def dispose_result(headers, response, params, add = False):
#         separator = ""
#         if add:
#             separator = ";"
#         else:
#             params['actual1'] = ""
#             params['actual2'] = ""
#             params['time_used'] = ""
#             params['result'] = ""
#     
#     
#         try:
#             
#             params['actual1'] += separator + response_res['ResCode']
#             params['actual2'] += separator + response_res['ResMessage']
#             params['time_used'] += separator + head_res['time_used']
#             #添加result要分为两行,才可以在没有结果的时候也加上";"符号
#             params['result'] += separator
#             params['result'] += response_res['Result']
#         except:
#             pass
#         finally:
#             return head_res, response_res
            
            



if __name__ == "__main__":

    func_helper = HttpHelper(url='10.0.1.117', 
                             port='8880', 
                             http_path="", 
                             head_model=None, 
                             logger=Logger("../log/Func_tts.log"), 
                             record_analyze_error = False,
                             timeout = 40)


    func_test = HttpFuncFrame("functest_test_tts.xls",
                              func_helper,
                              TTSFuncTest(),
                              write_result=True,
                              #write_result=False,
                              ) 
    case_filter = [] #全用例   
 #   case_filter = ["TestCase1001"]#正常情况
 #   case_filter = ["TestCase2104"] #md5不相等
 #   case_filter = ["TestCase1017"]   #md5相等
 #   case_filter = ["TestCase1146"]
    func_test.set_filter(case_filter)
    
    func_test.run()