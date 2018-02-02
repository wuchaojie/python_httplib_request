#coding=utf-8
'''
Created on 2014-12-26

@author: wangsiyu
'''
#-*- coding=UTF-8-*-
import hashlib
import httplib
import time
import TTS_HTTP.common
import os
import random

class TTS_ABILITIES(object):
    def __init__(self, dk, ak, url, cf, text, vs = 3.8,is_EX=False):
        self.url=url
        self.vs=vs
        self.dk=dk
        self.cf=cf
        self.ak=ak
        self.is_EX=is_EX
        self.body=text#.encode('utf-8')#repr(text)#decode('unicode-escape')#
        self.request_date=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        
        
        self.header={'x-app-key':self.ak,
                'x-sdk-version':self.vs,
                'x-request-date' : self.request_date,
                'x-task-config' : self.cf,
                'x-auth' : hashlib.md5( str(self.request_date) + self.dk).hexdigest(),
                "x-session-key" :  hashlib.md5(str(self.request_date) + self.dk).hexdigest(),
#                 "x-udid" : str(random.randint(0, 150))+":"+str(random.randint(0, 1500000000)),
                "x-udid" :"101:1234567890"
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
        httpClient = httplib.HTTPConnection(self.url+":8880",timeout=500)
        self.reset_header()
        #print self.body
        start_time=time.time()
        httpClient.request("POST", "/tts/SynthText", self.body, self.header)
#         httpClient.request("POST", "/tts/synthtextex", self.body, self.header)
        response = httpClient.getresponse()
        post_time = time.time()-start_time
        print '【post time 】:', post_time,"(s)"
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
            return post_time,xml
        else:
            return '','response status!=200'
         
    def synthEX(self):
        #https://casio.hcicloud.com:8879/tts/SynthText
        httpClient = httplib.HTTPConnection(self.url+":8880",timeout=500)#casio.hcicloud.com用https
#         httpClient = httplib.HTTPSConnection(self.url+":8880")#普通用http
        self.reset_header()
        #print self.body
        start_time=time.time()
        httpClient.request("POST", "/tts/SynthTextEx", self.body, self.header)
#         httpClient.request("POST", "/tts/synthtextex", self.body, self.header)
        response = httpClient.getresponse()
        post_time = time.time()-start_time
        print '【post time】%s '%str(post_time),"(s)"
        if response.status==200:
            response_body = response.read()
            xml_position=response_body.find('</ResponseInfo>')
            if response_body.find('</ResponseInfo>')!=-1:
                voice=response_body[response_body.find('</ResponseInfo>')+len('</ResponseInfo>'):]
                xml=response_body[:response_body.find('</ResponseInfo>')+len('</ResponseInfo>')]
#                 synth_position=self.get_position(xml)
#                 print synth_position
#                 self.body=self.body[synth_position:]
            return post_time,xml
 
 
 
 