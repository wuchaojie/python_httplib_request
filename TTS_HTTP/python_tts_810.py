#-*- coding:UTF-8 -*-
'''
Created on 2018��1��5��

@author: wuchaojie
'''

import unittest
import sys
import time
import hashlib
import httplib
import xml.etree.ElementTree as Etree

#***************************************************************************
#domain=['barron','cameal','cartoonjing','diaoxiong','jiangman','liangjiahe','shenxu','wangjingv9','xiaokunv9','xumengjuan','zhaqian','uyghur'] #音库
domain=['wangjingv9'] #音库
APPKEY = "4c5d548a"
URL = "10.0.1.117"
DEVKEY = "developer_key"
TEST_DATA = "../Data/TestData/"
TEST_RESULT = "../Data/TestResult/"

#****************************************************************************

class Test(unittest.TestCase):


    def setUp(self):
        print "******************************************************************************"
        print self._testMethodName
        pass


    def tearDown(self):
        pass

    def testTTSfunctioncase111(self):
        '''TTS810测试'''
        config = "capkey=tts.cloud.synth,property=cn_wangjingv9_common"
        file=open("../Data/TestData/case1.txt","rb").read()
        body=file
        voice,xml,resCode,resMessage = tts_post(APPKEY, DEVKEY,config, body,)
#         voice,xml,resCode,resMessage = tts_postEx(APPKEY, DEVKEY,config, body,)
        with open(TEST_RESULT+'testTTSfunctioncase111_16K16bit.pcm','wb') as v_file:
            v_file.write(voice)
        self.assertEqual(resCode, "Success")
        self.assertEqual(resMessage, "Success")
        voice,xml,resCode,resMessage = tts_postEx(APPKEY, DEVKEY,config, body,)
        with open(TEST_RESULT+'testTTSfunctioncase111_Ex_16K16bit.pcm','wb') as v_file:
            v_file.write(voice)
        pass

def tts_post(APPKEY, dev,config, body,is_EX=False,*filename):
    '''TTS POST'''
    
    request_date = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    print request_date   
    headers = {
                   "x-app-key" :APPKEY,
                   "x-sdk-version" : 3.8,
                   "x-request-date": request_date,
                   "x-task-config" : config,
                   "x-session-key" :  hashlib.md5(str(request_date) + DEVKEY).hexdigest(),
                   "x-udid" : "101:1234567890"
               }  
    print headers
      
    httpClient = httplib.HTTPConnection(URL+":8880",timeout=500)
    start_time=time.time()
    httpClient.request("POST", "/tts/SynthText", body ,headers)
    print '��time interval is��:',time.time()-start_time
    response = httpClient.getresponse()
    response_body = response.read()
#     print response_body
    print response.status
    print response.reason
    resCode =""
    resMessage=""
    if response.status==200:
        xml_position=response_body.find('</ResponseInfo>')
        if response_body.find('</ResponseInfo>')!=-1:
            voice=response_body[response_body.find('</ResponseInfo>')+len('</ResponseInfo>'):]
            xml=response_body[:response_body.find('</ResponseInfo>')+len('</ResponseInfo>')]
            xml_str = Etree.fromstring(xml) 
        if 'ResCode' in response_body:
            resCode = xml_str.find("ResCode").text
        if 'ResMessage' in response_body:
            resMessage=xml_str.find("ResMessage").text
        print xml
        print ">>>>>>Speech synthesis success<<<<<<<"
        return voice,xml,resCode,resMessage
    else: 
        print "#################failed#############"

def tts_postEx(APPKEY, dev,config, body,is_EX=True,*filename):
    '''TTS POSTEx'''
    
    request_date = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    print request_date   
    headers = {
                   "x-app-key" :APPKEY,
                   "x-sdk-version" : 3.8,
                   "x-request-date": request_date,
                   "x-task-config" : config,
                   "x-session-key" :  hashlib.md5(str(request_date) + DEVKEY).hexdigest(),
                   "x-udid" : "101:1234567850"
               }
    print headers
    httpClient = httplib.HTTPConnection(URL+":8880",timeout=500)
    start_time=time.time()
    httpClient.request("POST", "/tts/SynthTextEx", body ,headers)
    print '��time interval is��:',time.time()-start_time
    response = httpClient.getresponse()
    response_body = response.read()
#     print response_body
    print response.status
    print response.reason
    resCode =""
    resMessage=""
    if response.status==200:
        xml_position=response_body.find('</ResponseInfo>')
        if response_body.find('</ResponseInfo>')!=-1:
            voice=response_body[response_body.find('</ResponseInfo>')+len('</ResponseInfo>'):]
            xml=response_body[:response_body.find('</ResponseInfo>')+len('</ResponseInfo>')]
            xml_str = Etree.fromstring(xml) 
        if 'ResCode' in response_body:
            resCode = xml_str.find("ResCode").text
        if 'ResMessage' in response_body:
            resMessage=xml_str.find("ResMessage").text
        print xml
        print ">>>>>>Speech synthesis success(Ex)<<<<<<<"
        return voice,xml,resCode,resMessage
    else: 
        print "#################failed#############"     

if __name__ == "__main__":
    #sys.argv = ['', 'Test.testTTSfunctioncase111']
    unittest.main()