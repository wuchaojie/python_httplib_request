# -*- coding=UTF-8 -*-
'''
Created on 2016年4月22日

@author: dailipo
'''

# class MyClass(object):
#     '''
#     classdocs
#     '''
# 
# 
#     def __init__(selfparams):
#         '''
#         Constructor
#         '''

import hashlib
import httplib
import time
#import common
import os
import random

class TTS_ABILITIES(object):
    def __init__(self,APPKEY,DEVKEY,URL, config, body,is_EX=True):
        self.URL=URL
        self.DEVKEY=DEVKEY
        self.config=config
        self.APPKEY=APPKEY
        self.is_EX=is_EX
        self.body=body#.encode('utf-8')#repr(text)#decode('unicode-escape')#
        self.request_date=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        
        
        self.header={'x-app-key':self.APPKEY,
                'x-sdk-version':3.8,
                'x-request-date' : self.request_date,
                'x-task-config' : self.config,
                'x-auth' : hashlib.md5( str(self.request_date) + self.dk).hexdigest(),
                "x-session-key" :  hashlib.md5(str(self.request_date) + self.DEVKEY).hexdigest(),
#                 "x-udid" : str(random.randint(0, 150))+":"+str(random.randint(0, 1500000000)),
                "x-udid" : "101:1234567890"
                }
        self.reset_header()
        
    def run(self):
        '''tagMode一次性合成所有文本，长度达到4096'''
        voice=None
        body=self.body
        voice=''
        if self.is_EX:
            try:
                voice,xml=self.synth()
            except Exception,e:
                return '',e
        else:
            voice,xml=self.synthEX()
        return voice,xml
    
    def reset_header(self):
        if self.vs<3.5:
            if len(self.body)<=256:
                request_data=self.body
            else:
                request_data=self.body[len(self.body)/2-128:len(self.body)/2+128]
            self.header['x-auth']=hashlib.md5(self.dk + str(self.request_date) + self.cf + request_data).hexdigest()
            
    def get_position(self,xml):
        synth_position=xml[xml.find('<SynthTextPos>')+len('<SynthTextPos>'):xml.find('</SynthTextPos>')]        
        return int(synth_position)

    
    def synth(self):
        httpClient = httplib.HTTPConnection(self.URL+":8880",timeout=500)
        self.reset_header()

        start_time=time.time()
        httpClient.request("POST", "/tts/SynthText", self.body, self.header)
#         httpClient.request("POST", "/tts/synthtextex", self.body, self.header)
        response = httpClient.getresponse()
        print '【time interval is】:',time.time()-start_time
        if response.status==200:
            response_body = response.read()
            xml_position=response_body.find('</ResponseInfo>')
            if response_body.find('</ResponseInfo>')!=-1:
                voice=response_body[response_body.find('</ResponseInfo>')+len('</ResponseInfo>'):]
                xml=response_body[:response_body.find('</ResponseInfo>')+len('</ResponseInfo>')]
                #print xml
#                 synth_position=self.get_position(xml)
#                 print synth_position
#                 self.body=self.body[synth_position:]
            return voice,xml
        else:
            return '','response status!=200'
        
    def synthEX(self):
        httpClient = httplib.HTTPConnection(self.URL+":8880",timeout=500)
        self.reset_header()
        print self.body
        start_time=time.time()
        httpClient.request("POST", "/tts/SynthTextEx", self.body, self.header)
        response = httpClient.getresponse()
        print 'time interval is ',time.time()-start_time
        if response.status==200:
            response_body = response.read()
            xml_position=response_body.find('</ResponseInfo>')
            if response_body.find('</ResponseInfo>')!=-1:
                voice=response_body[response_body.find('</ResponseInfo>')+len('</ResponseInfo>'):]
                xml=response_body[:response_body.find('</ResponseInfo>')+len('</ResponseInfo>')]
#                 synth_position=self.get_position(xml)
#                 print synth_position
#                 self.body=self.body[synth_position:]
            return voice,xml     