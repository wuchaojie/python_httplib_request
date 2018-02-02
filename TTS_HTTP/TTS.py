#coding=utf-8
'''
Created on 2015-1-13

@author: wangsiyu
'''
import unittest
import hashlib
import httplib
import time
import common
import os
import TTS_class
import sys
import xml.etree.ElementTree as Etree
from xml.etree import ElementTree  


class Test(unittest.TestCase):
    
    #设置账号
    devKey=common.intranet82.devKey
    appKey=common.intranet82.appKey
    url=common.intranet82.url
    
    #初始化参数
    Case_is_Pass=True
    CasePass=u"""
                               ----------------------------------------
                                      Case Pass!!!!!!!!!!!!!!!!!
                               ----------------------------------------"""
    CaseFailed=u"""
                               ----------------------------------------
                                      Case Failed!!!!!!!!!!!!!!!
                               ----------------------------------------"""
    #生成日志
    test_log=open('./log/tts-log-'+str(time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(time.time())))+'.txt','wb')
    
    capkey='tts.cloud.xiaokun'
    caseName='case1.txt'
    
    def setUp(self):
        self.test_log.write("****************************************************************************************************\n")
        pass


    def tearDown(self):        
        if  self.Case_is_Pass:
            self.test_log.write("\n"+self.CasePass+"\n")
        else:
            self.test_log.write("\n"+self.CaseFailed+"\n")
        self.test_log.write("****************************************************************************************************\n")
        pass


    def test_TTS_Case100(self):    
        Notes="1.1.1 检测能力正确,各配置串默认的情况"
        
        self.test_log.write(str(sys._getframe().f_code.co_name)+"\n注释："+Notes)    
        #file=open("./Data/TestData/"+self.caseName,"rb").read()
        #file=open("./Data/TestData/case30-right.txt","rb").read()
        
        ttscfg='capkey=tts.cloud.misaki'
        voice,xml=TTS_class.TTS_ABILITIES('0e83c3acb47fd8ad2c537bce64d6a366','ac5d5431','api.hcicloud.com',ttscfg,'銀行から抽出した数百元','3.8').run()
        v_file=open('./Data/ResultData/test_TTS_Case1.pcm','wb')
        if voice!=None:
            v_file.write(voice)
        self.Case_is_Pass=self.get_info_from_response(xml, "Success", "Success", "0")
        pass
    
    def test_TTS_Case1(self):    
        Notes="1.1.1 检测能力正确,各配置串默认的情况"
        
        self.test_log.write(str(sys._getframe().f_code.co_name)+"\n注释："+Notes)    
        file=open("./Data/TestData/"+self.caseName,"rb").read()
        #file=open("./Data/TestData/case30-right.txt","rb").read()
        
        ttscfg='capkey='+self.capkey
        voice,xml=TTS_class.TTS_ABILITIES(self.devKey,self.appKey,self.url,ttscfg,file,'3.8').run()
        v_file=open('./Data/ResultData/test_TTS_Case1.pcm','wb')
        if voice!=None:
            v_file.write(voice)
        self.Case_is_Pass=self.get_info_from_response(xml, "Success", "Success", "0")
        pass
    
    def test_TTS_Case2(self):
        Notes="1.1.2 检测http头中task-config中能力字段为不存在的能力，调用合成请求协议的情况"
        
        self.test_log.write(str(sys._getframe().f_code.co_name)+"\n注释："+Notes)  
        file=open("./Data/TestData/"+self.caseName,"rb").read()
        
        ttscfg='capkey=tts.cloud.123'
        voice,xml=TTS_class.TTS_ABILITIES(self.devKey,self.appKey,self.url,ttscfg,file,'3.8').run()
        self.Case_is_Pass=self.get_info_from_response(xml, "FAILED", "CanUseContinue failed(8,kLicenseErrorCapkeyNotFound)", "17")        
        pass
    
    
    def test_TTS_Case3(self):
        Notes="1.1.3 检测http头中task-config中没有capkey字段调用合成请求协议的情况(failed)"
        
        self.test_log.write(str(sys._getframe().f_code.co_name)+"\n注释："+Notes)  
        file=open("./Data/TestData/"+self.caseName,"rb").read()
        
        ttscfg='domain=finance'
        voice,xml=TTS_class.TTS_ABILITIES(self.devKey,self.appKey,self.url,ttscfg,file,'3.8').run()
        v_file=open('./Data/ResultData/test_TTS_Case3.pcm','wb')
        if voice!=None:
            v_file.write(voice)
        self.Case_is_Pass=self.get_info_from_response(xml, "FAILED", "CanUseContinue failed(8,kLicenseErrorCapkeyNotFound)", "17")        
        pass
    
    
    def test_TTS_Case4(self):
        Notes="1.1.4 检测设置能力为tts.cloud.xiaokun时，设置不同的domain的值的情况"
        
        self.test_log.write(str(sys._getframe().f_code.co_name)+"\n注释："+Notes)  
        
        domain=['finance','weather','queue','voyage','revenue','elecpower','message','insurance']
        for i in domain:
            print i
            file=open("./Data/TestData/tts_text_domain_"+i+".txt","rb").read()
            ttscfg='capkey=tts.cloud.xiaokun,domain='+i
            voice,xml=TTS_class.TTS_ABILITIES(self.devKey,self.appKey,self.url,ttscfg,file,'3.8').run()
            v_file=open('./Data/ResultData/test_TTS_Case4-'+i+'.pcm','wb')
            if voice!=None:
                v_file.write(voice)
            self.Case_is_Pass=self.get_info_from_response(xml, "Success", "Success", "0")      
        pass
    
    def test_TTS_Case5(self):
        Notes="1.1.5 检测设置能力为非tts.cloud.xiaokun能力时，设置不同的domain的值的情况"
        
        domain=['finance','weather','queue','voyage','revenue','elecpower','message','insurance']
        for i in domain:
            print i
            file=open("./Data/TestData/tts_text_domain_"+i+".txt","rb").read()
            ttscfg='capkey=tts.cloud.wangjing,domain=weather'#+i
            print ttscfg
            voice,xml=TTS_class.TTS_ABILITIES(self.devKey,self.appKey,self.url,ttscfg,file,'3.9.5').run()
            v_file=open('./Data/ResultData/test_TTS_Case5-'+i+'.pcm','wb')
            if voice!=None:
                v_file.write(voice)
            self.Case_is_Pass=self.get_info_from_response(xml, "Success", "Success", "0")    
        pass
    
    
    def test_TTS_Case6(self):    
        Notes="1.1.6 检测能力pitch字段设置为不同值时的情况"
        
        self.test_log.write(str(sys._getframe().f_code.co_name)+"\n注释："+Notes)    
        file=open("./Data/TestData/"+self.caseName,"rb").read()
        range_arry=['1','2','3','4','5','6','7','8','9','10','max','min']
        
        for i in range_arry:
            ttscfg='capkey=tts.cloud.uyghur,pitch='+str(i)
            voice,xml=TTS_class.TTS_ABILITIES(self.devKey,self.appKey,self.url,ttscfg,file,'3.8').run()
            v_file=open('./Data/ResultData/test_TTS_Case6-pitch'+str(i)+'.pcm','wb')
            if voice!=None:
                v_file.write(voice)
            self.Case_is_Pass=self.get_info_from_response(xml, "Success", "Success", "0")
        pass
    
    def test_TTS_Case7(self):    
        Notes="1.1.7 检测能力speed字段设置为不同值时的情况"
        
        self.test_log.write(str(sys._getframe().f_code.co_name)+"\n注释："+Notes)    
        file=open("./Data/TestData/"+self.caseName,"rb").read()
        range_arry=['1','2','3','4','5','6','7','8','9','10','max','min']
        
        for i in range_arry:
            ttscfg='capkey=tts.cloud.uyghur,speed='+str(i)
            voice,xml=TTS_class.TTS_ABILITIES(self.devKey,self.appKey,self.url,ttscfg,file,'3.8').run()
            v_file=open('./Data/ResultData/test_TTS_Case7-speed'+str(i)+'.pcm','wb')
            if voice!=None:
                v_file.write(voice)
            self.Case_is_Pass=self.get_info_from_response(xml, "Success", "Success", "0")
        pass
    
    def test_TTS_Case8(self):    
        Notes="1.1.8 检测能力volume字段设置为不同值时的情况"
        
        self.test_log.write(str(sys._getframe().f_code.co_name)+"\n注释："+Notes)    
        file=open("./Data/TestData/"+self.caseName,"rb").read()
        range_arry=['1','2','3','4','5','6','7','8','9','10','max','min']
        
        for i in range_arry:
            ttscfg='capkey=tts.cloud.uyghur,volume='+str(i)
            voice,xml=TTS_class.TTS_ABILITIES(self.devKey,self.appKey,self.url,ttscfg,file,'3.8').run()
            v_file=open('./Data/ResultData/test_TTS_Case8-volume'+str(i)+'.pcm','wb')
            if voice!=None:
                v_file.write(voice)
            self.Case_is_Pass=self.get_info_from_response(xml, "Success", "Success", "0")
        ttscfg='capkey=tts.cloud.uyghur,volume=max'
        
        pass
    
    def test_TTS_Case9(self):    
        Notes="1.1.9 检测能力puncmode字段设置为不同值时的情况"
        
        self.test_log.write(str(sys._getframe().f_code.co_name)+"\n注释："+Notes)    
        file=open("./Data/TestData/case.txt","rb").read()
        range_arry=['off','off_rtn','on_rtn','on']
        
        for i in range_arry:
            ttscfg='capkey=tts.cloud.uyghur,puncmode='+str(i)
            voice,xml=TTS_class.TTS_ABILITIES(self.devKey,self.appKey,self.url,ttscfg,file,'3.8').run()
            v_file=open('./Data/ResultData/test_TTS_Case9-puncmode'+str(i)+'.pcm','wb')
            if voice!=None:
                v_file.write(voice)
            self.Case_is_Pass=self.get_info_from_response(xml, "Success", "Success", "0")
        pass
    
    def test_TTS_Case10(self):    
        Notes="1.1.10 检测能力digitmode字段设置为不同值时的情况"
        
        self.test_log.write(str(sys._getframe().f_code.co_name)+"\n注释："+Notes)    
        file='18667624667'#open("./Data/TestData/"+self.caseName,"rb").read()
        range_arry=['auto_number','telegram','number','auto_telegram']
        
        for i in range_arry:
            ttscfg='capkey=tts.cloud.uyghur,digitmode='+str(i)
            voice,xml=TTS_class.TTS_ABILITIES(self.devKey,self.appKey,self.url,ttscfg,file,'3.8').run()
            v_file=open('./Data/ResultData/test_TTS_Case10-digitmode'+str(i)+'.pcm','wb')
            if voice!=None:
                v_file.write(voice)
            self.Case_is_Pass=self.get_info_from_response(xml, "Success", "Success", "0")
        pass
    
    def test_TTS_Case11(self):    
        Notes="1.1.11 检测能力engmode字段设置为不同值时的情况"
        
        self.test_log.write(str(sys._getframe().f_code.co_name)+"\n注释："+Notes)    
        file='how old are you run you may live'#open("./Data/TestData/"+self.caseName,"rb").read()
        range_arry=['auto','english','letter']
        
        for i in range_arry:
            ttscfg='capkey=tts.cloud.uyghur,engmode='+str(i)
            voice,xml=TTS_class.TTS_ABILITIES(self.devKey,self.appKey,self.url,ttscfg,file,'3.8').run()
            v_file=open('./Data/ResultData/test_TTS_Case11-engmode'+str(i)+'.pcm','wb')
            if voice!=None:
                v_file.write(voice)
            self.Case_is_Pass=self.get_info_from_response(xml, "Success", "Success", "0")
        pass
    
    def test_TTS_Case12(self):    
        Notes="1.1.12 检测能力tagmode字段设置为不同值时的情况"
         
        self.test_log.write(str(sys._getframe().f_code.co_name)+"\n注释："+Notes)    
        file=open("./Data/TestData/"+self.caseName,"rb").read()
        range_arry=['auto','vtml','s3ml','ssml']
         
        for i in range_arry:
            ttscfg='capkey=tts.cloud.uyghur,tagmode='+str(i)
            voice,xml=TTS_class.TTS_ABILITIES(self.devKey,self.appKey,self.url,ttscfg,file,'3.8').run()
            self.Case_is_Pass=self.get_info_from_response(xml, "Success", "Success", "0")
            
        ttscfg='capkey=tts.cloud.uyghur,tagmode=none'
        voice,xml=TTS_class.TTS_ABILITIES(self.devKey,self.appKey,self.url,ttscfg,file,'3.8').run()
        v_file=open('./Data/ResultData/test_TTS_Case11-tagmode-none.pcm','wb')
        if voice!=None:
            v_file.write(voice)
        self.Case_is_Pass=self.get_info_from_response(xml, "Success", "Success", "0")
        pass

    def test_TTS_Case13(self):    
        Notes="1.1.13 检测能力audioformat字段设置为不同值时的情况"
        
        self.test_log.write(str(sys._getframe().f_code.co_name)+"\n注释："+Notes)    
        file=open("./Data/TestData/"+self.caseName,"rb").read()
        range_arry=['ulaw8k8bit','pcm8k8bit','pcm8k16bit','pcm16k8bit','pcm16k16bit','pcm11k8bit','pcm11k16bit','mp3','mp3_24','mp3_16','vox8k4bit','vox6k4bit','alaw8k8bit']
        
        for i in range_arry:
            ttscfg='capkey=tts.cloud.uyghur,audioformat='+str(i)
            voice,xml=TTS_class.TTS_ABILITIES(self.devKey,self.appKey,self.url,ttscfg,file,'3.8').run()
            v_file=open('./Data/ResultData/test_TTS_Case13-audioformat-'+str(i)+'.pcm','wb')
            if voice!=None:
                v_file.write(voice)
            self.Case_is_Pass=self.get_info_from_response(xml, "Success", "Success", "0")
        pass
    
    def test_TTS_Case14(self):    
        Notes="1.1.14 检测能力voicestyle字段设置为不同值时的情况"
        
        self.test_log.write(str(sys._getframe().f_code.co_name)+"\n注释："+Notes)    
        file=open("./Data/TestData/"+self.caseName,"rb").read()
        range_arry=['normal','plain','clear','vivid']
        
        for i in range_arry:
            ttscfg='capkey=tts.cloud.uyghur,voicestyle='+str(i)
            voice,xml=TTS_class.TTS_ABILITIES(self.devKey,self.appKey,self.url,ttscfg,file,'3.8').run()
            v_file=open('./Data/ResultData/test_TTS_Case14-voicestyle-'+str(i)+'.pcm','wb')
            if voice!=None:
                v_file.write(voice)
            self.Case_is_Pass=self.get_info_from_response(xml, "Success", "Success", "0")
        pass
    
    def test_TTS_Case15(self):    
        Notes="1.1.15 检测能力pitch字段设置为非法值时的情况"
        
        self.test_log.write(str(sys._getframe().f_code.co_name)+"\n注释："+Notes)    
        file=open("./Data/TestData/"+self.caseName,"rb").read()
        range_arry=['-1','0.5','11','abc']
        
        for i in range_arry:
            ttscfg='capkey=tts.cloud.uyghur,pitch='+str(i)
            voice,xml=TTS_class.TTS_ABILITIES(self.devKey,self.appKey,self.url,ttscfg,file,'3.8').run()
            self.Case_is_Pass=self.get_info_from_response(xml, "FAILED", "ParseTtsParams failed", "4")
        pass
    
    def test_TTS_Case16(self):    
        Notes="1.1.16 检测能力speed字段设置为非法值时的情况"
        
        self.test_log.write(str(sys._getframe().f_code.co_name)+"\n注释："+Notes)    
        file=open("./Data/TestData/"+self.caseName,"rb").read()
        range_arry=['-1','0.5','11','abc']
        
        for i in range_arry:
            ttscfg='capkey=tts.cloud.uyghur,speed='+str(i)
            voice,xml=TTS_class.TTS_ABILITIES(self.devKey,self.appKey,self.url,ttscfg,file,'3.8').run()
            self.Case_is_Pass=self.get_info_from_response(xml, "FAILED", "ParseTtsParams failed", "4")
        pass
    
    def test_TTS_Case17(self):    
        Notes="1.1.17 检测能力volume字段设置为非法值时的情况"
        
        self.test_log.write(str(sys._getframe().f_code.co_name)+"\n注释："+Notes)    
        file=open("./Data/TestData/"+self.caseName,"rb").read()
        range_arry=['-1','0.5','11','abc']
        
        for i in range_arry:
            ttscfg='capkey=tts.cloud.uyghur,volume='+str(i)
            voice,xml=TTS_class.TTS_ABILITIES(self.devKey,self.appKey,self.url,ttscfg,file,'3.8').run()
            self.Case_is_Pass=self.get_info_from_response(xml, "FAILED", "ParseTtsParams failed", "4")
        pass
    
    def test_TTS_Case18(self):    
        Notes="1.1.18 检测能力puncmode字段设置为非法值时的情况"
        
        self.test_log.write(str(sys._getframe().f_code.co_name)+"\n注释："+Notes)    
        file=open("./Data/TestData/"+self.caseName,"rb").read()
        range_arry=['-1','0.5','11','abc']
        
        for i in range_arry:
            ttscfg='capkey=tts.cloud.uyghur,puncmode='+str(i)
            voice,xml=TTS_class.TTS_ABILITIES(self.devKey,self.appKey,self.url,ttscfg,file,'3.8').run()
            self.Case_is_Pass=self.get_info_from_response(xml, "FAILED", "ParseTtsParams failed", "4")
        pass
    
    
    def test_TTS_Case19(self):    
        Notes="1.1.19 检测能力digitmode字段设置为非法值时的情况"
        
        self.test_log.write(str(sys._getframe().f_code.co_name)+"\n注释："+Notes)    
        file=open("./Data/TestData/"+self.caseName,"rb").read()
        range_arry=['-1','0.5','11','abc']
        
        for i in range_arry:
            ttscfg='capkey=tts.cloud.uyghur,digitmode='+str(i)
            voice,xml=TTS_class.TTS_ABILITIES(self.devKey,self.appKey,self.url,ttscfg,file,'3.8').run()
            self.Case_is_Pass=self.get_info_from_response(xml, "FAILED", "ParseTtsParams failed", "4")
        pass
    
    def test_TTS_Case20(self):    
        Notes="1.1.20 检测能力engmode字段设置为不同值时的情况"
        
        self.test_log.write(str(sys._getframe().f_code.co_name)+"\n注释："+Notes)    
        file=open("./Data/TestData/"+self.caseName,"rb").read()
        range_arry=['-1','0.5','11','abc']
        
        for i in range_arry:
            ttscfg='capkey=tts.cloud.uyghur,engmode='+str(i)
            voice,xml=TTS_class.TTS_ABILITIES(self.devKey,self.appKey,self.url,ttscfg,file,'3.8').run()
            self.Case_is_Pass=self.get_info_from_response(xml, "FAILED", "ParseTtsParams failed", "4")
        pass
    
    def test_TTS_Case21(self):    
        Notes="1.1.21 检测能力tagmode字段设置为不同值时的情况"
        
        self.test_log.write(str(sys._getframe().f_code.co_name)+"\n注释："+Notes)    
        file=open("./Data/TestData/"+self.caseName,"rb").read()
        range_arry=['-1','0.5','11','abc']
        
        for i in range_arry:
            ttscfg='capkey=tts.cloud.uyghur,tagmode='+str(i)
            voice,xml=TTS_class.TTS_ABILITIES(self.devKey,self.appKey,self.url,ttscfg,file,'3.8').run()
            self.Case_is_Pass=self.get_info_from_response(xml, "FAILED", "ParseTtsParams failed", "4")
        pass
    
    
    def test_TTS_Case22(self):    
        Notes="1.1.22 检测能力 audioformat字段设置为不同值时的情况"
        
        self.test_log.write(str(sys._getframe().f_code.co_name)+"\n注释："+Notes)    
        file=open("./Data/TestData/"+self.caseName,"rb").read()
        range_arry=['ulaw17k8bit','0.5','11','abc']
        
        for i in range_arry:
            ttscfg='capkey=tts.cloud.uyghur,audioformat='+str(i)
            voice,xml=TTS_class.TTS_ABILITIES(self.devKey,self.appKey,self.url,ttscfg,file,'3.8').run()
            self.Case_is_Pass=self.get_info_from_response(xml, "FAILED", "ParseTtsParams failed", "4")
        pass
    
    def test_TTS_Case23(self):    
        Notes="1.1.23 检测能力 voicestyle字段设置为不同值时的情况"
        
        self.test_log.write(str(sys._getframe().f_code.co_name)+"\n注释："+Notes)    
        file=open("./Data/TestData/"+self.caseName,"rb").read()
        range_arry=['ulaw17k8bit','0.5','11','abc']
        
        for i in range_arry:
            ttscfg='capkey=tts.cloud.uyghur,voicestyle='+str(i)
            voice,xml=TTS_class.TTS_ABILITIES(self.devKey,self.appKey,self.url,ttscfg,file,'3.8').run()
            self.Case_is_Pass=self.get_info_from_response(xml, "FAILED", "ParseTtsParams failed", "4")
        pass
    
    def test_TTS_Case24(self):    
        Notes="1.1.24 检测配置串超长的情况"
        
        self.test_log.write(str(sys._getframe().f_code.co_name)+"\n注释："+Notes)    
        file=open("./Data/TestData/"+self.caseName,"rb").read()
        ttscfg='capkey=tts.cloud.uyghur,asdsad'
        #ttscfg='capkey=tts.cloud.uyghur,capkey=tts.cloud.uyghur,capkey=tts.cloud.uyghur,capkey=tts.cloud.uyghur,capkey=tts.cloud.uyghur,capkey=tts.cloud.uyghur,capkey=tts.cloud.uyghur,capkey=tts.cloud.uyghur,capkey=tts.cloud.uyghur,capkey=tts.cloud.uyghur,capkey=tts.cloud.uyghur,capkey=tts.cloud.uyghur,capkey=tts.cloud.uyghur,capkey=tts.cloud.uyghur,capkey=tts.cloud.uyghur,capkey=tts.cloud.uyghur,capkey=tts.cloud.uyghur,capkey=tts.cloud.uyghur,capkey=tts.cloud.uyghur,capkey=tts.cloud.uyghur,capkey=tts.cloud.uyghur,capkey=tts.cloud.uyghur,capkey=tts.cloud.uyghur,capkey=tts.cloud.uyghur,capkey=tts.cloud.uyghur,capkey=tts.cloud.uyghur,capkey=tts.cloud.uyghur,capkey=tts.cloud.uyghur,capkey=tts.cloud.uyghur,capkey=tts.cloud.uyghur,capkey=tts.cloud.uyghur,capkey=tts.cloud.uyghur,capkey=tts.cloud.uyghur,capkey=tts.cloud.uyghur,capkey=tts.cloud.uyghur,capkey=tts.cloud.uyghur,capkey=tts.cloud.uyghur,capkey=tts.cloud.uyghur,capkey=tts.cloud.uyghur,capkey=tts.cloud.uyghur,capkey=tts.cloud.uyghur,capkey=tts.cloud.uyghur,capkey=tts.cloud.uyghur,capkey=tts.cloud.uyghur,capkey=tts.cloud.uyghur,capkey=tts.cloud.uyghur'
        #ttscfg='capkey=tts.cloud.uyghur,asdsadsadsadsadsadsadsadsdsadsadsadsadsadsadasd,asdsadsadsadsadsadsadsadsdsadsadsadsadsadsadasd,asdsadsadsadsadsadsadsadsdsadsadsadsadsadsadasd,asdsadsadsadsadsadsadsadsdsadsadsadsadsadsadasd,asdsadsadsadsadsadsadsadsdsadsadsadsadsadsadasd,asdsadsadsadsadsadsadsadsdsadsadsadsadsadsadasd,asdsadsadsadsadsadsadsadsdsadsadsadsadsadsadasd,asdsadsadsadsadsadsadsadsdsadsadsadsadsadsadasd,asdsadsadsadsadsadsadsadsdsadsadsadsadsadsadasd,asdsadsadsadsadsadsadsadsdsadsadsadsadsadsadasd'
        voice,xml=TTS_class.TTS_ABILITIES(self.devKey,self.appKey,self.url,ttscfg,file,'3.8').run()
        self.Case_is_Pass=self.get_info_from_response(xml, "FAILED", "ParseTtsParams failed", "4")
        pass
    
    def test_TTS_Case25(self):    
        Notes="1.1.25 检测配置串为空"
        
        self.test_log.write(str(sys._getframe().f_code.co_name)+"\n注释："+Notes)    
        file=open("./Data/TestData/"+self.caseName,"rb").read()
        
        ttscfg=''
        voice,xml=TTS_class.TTS_ABILITIES(self.devKey,self.appKey,self.url,ttscfg,file,'3.8').run()
        self.Case_is_Pass=self.get_info_from_response(xml, "Success", "Success", "0")
        pass
    
    def test_TTS_Case26(self):    
        Notes="1.1.26 检测配置串中合成文本为空"
        
        self.test_log.write(str(sys._getframe().f_code.co_name)+"\n注释："+Notes)    
        file=open("./Data/TestData/case26.txt","rb").read()
        
        ttscfg=''
        voice,xml=TTS_class.TTS_ABILITIES(self.devKey,self.appKey,self.url,ttscfg,file,'3.8').run()
        self.Case_is_Pass=self.get_info_from_response(xml, "FAILED", "jtts audio data success, but audio data is 0", "2")
        pass
    
    def test_TTS_Case27(self):    
        Notes="1.1.27 检测配置串中合成文本为非UTF8文本（汉字）"
        
        self.test_log.write(str(sys._getframe().f_code.co_name)+"\n注释："+Notes)    
        file=open("./Data/TestData/case27.txt","rb").read()
        
        ttscfg='capkey='+self.capkey
        voice,xml=TTS_class.TTS_ABILITIES(self.devKey,self.appKey,self.url,ttscfg,file,'3.8').run()
        self.Case_is_Pass=self.get_info_from_response(xml, "FAILED", "Requesting text is not encoded with UTF8.", "4")
        pass
    
    def test_TTS_Case28(self):    
        Notes="1.1.28 检测配置串中合成文本超过1024字节"
        
        self.test_log.write(str(sys._getframe().f_code.co_name)+"\n注释："+Notes)    
        file=open("./Data/TestData/case28=1024.txt","rb").read()
        
        ttscfg='capkey='+self.capkey
        voice,xml=TTS_class.TTS_ABILITIES(self.devKey,self.appKey,self.url,ttscfg,file,'3.8').run()
        self.Case_is_Pass=self.get_info_from_response(xml, "Success", "Success", "0")
        
        file=open("./Data/TestData/case28bigerthan1024.txt","rb").read()
        voice,xml=TTS_class.TTS_ABILITIES(self.devKey,self.appKey,self.url,ttscfg,file,'3.8').run()
        self.Case_is_Pass=self.get_info_from_response(xml, "FAILED", "jtts audio data success, but audio data > 1024", "2")
        pass
    
    def test_TTS_Case29(self):    
        Notes="1.1.29 检测配置串中设置tagmode 为none，但合成文本为标记语言的情况"
        
        self.test_log.write(str(sys._getframe().f_code.co_name)+"\n注释："+Notes)    
        file=open("./Data/TestData/case29.txt","rb").read()
        
        ttscfg='capkey=tts.cloud.uyghur,tagmode=ssml'
        voice,xml=TTS_class.TTS_ABILITIES(self.devKey,self.appKey,self.url,ttscfg,file,'3.8').run()
        self.Case_is_Pass=self.get_info_from_response(xml, "Success", "Success", "0")
        v_file=open('./Data/ResultData/test_TTS_Case29.pcm','wb')
        if voice!=None:
            v_file.write(voice)
        pass
    
    def test_TTS_Case30(self):    
        Notes="1.1.30 检测配置串中设置tagmode 为ssml，但合成文本为非标记语言的情况(格式错误)"
        
        self.test_log.write(str(sys._getframe().f_code.co_name)+"\n注释："+Notes)    
        file=open("./Data/TestData/case30-false.txt","rb").read()
        
        ttscfg='capkey=tts.cloud.carol,tagmode=ssml'
        voice,xml=TTS_class.TTS_ABILITIES(self.devKey,self.appKey,self.url,ttscfg,file,'3.8').run()
        self.Case_is_Pass=self.get_info_from_response(xml, "Success", "Success", "0")
        v_file=open('./Data/ResultData/test_TTS_Case30-false.pcm','wb')
        if voice!=None:
            v_file.write(voice)
            
        file=open("./Data/TestData/case30-right.txt","rb").read()        
        voice,xml=TTS_class.TTS_ABILITIES(self.devKey,self.appKey,self.url,ttscfg,file,'3.8').run()
        self.Case_is_Pass=self.get_info_from_response(xml, "Success", "Success", "0")
        v_file=open('./Data/ResultData/test_TTS_Case30-right.pcm','wb')
        if voice!=None:
            v_file.write(voice)
        pass
    
    def test_TTS_Case31(self):    
        Notes="1.1.31 检测配置串中设置tagmode 为s3ml，但合成文本为非标记语言的情况(格式错误)"
        
        self.test_log.write(str(sys._getframe().f_code.co_name)+"\n注释："+Notes)    
        file=open("./Data/TestData/case31-false.txt","rb").read()
        
        ttscfg='capkey=tts.cloud.uyghur,tagmode=s3ml'
        voice,xml=TTS_class.TTS_ABILITIES(self.devKey,self.appKey,self.url,ttscfg,file,'3.8').run()
        self.Case_is_Pass=self.get_info_from_response(xml, "FAILED", "jTTS_SessionStart failed", "2010")
        v_file=open('./Data/ResultData/test_TTS_Case31-false.pcm','wb')
        if voice!=None:
            v_file.write(voice)
            
        file=open("./Data/TestData/case31-right.txt","rb").read()        
        voice,xml=TTS_class.TTS_ABILITIES(self.devKey,self.appKey,self.url,ttscfg,file,'3.8').run()
        self.Case_is_Pass=self.get_info_from_response(xml, "Success", "Success", "0")
        v_file=open('./Data/ResultData/test_TTS_Case31-right.pcm','wb')
        if voice!=None:
            v_file.write(voice)
        pass
    
    def test_TTS_Case32(self):    
        Notes="1.1.32 检测合成时间超过40s的情况"
        
        self.test_log.write(str(sys._getframe().f_code.co_name)+"\n注释："+Notes)    
        file=open("./Data/TestData/case32.txt","rb").read()
        
        ttscfg='capkey=tts.cloud.carol,tagmode=ssml'
        voice,xml=TTS_class.TTS_ABILITIES(self.devKey,self.appKey,self.url,ttscfg,file,'3.8').run()
        self.Case_is_Pass=self.get_info_from_response(xml, "Success", "Success", "0")
        pass
    
    def test_TTS_Case33(self):    
        Notes="1.1.33 验证[ServiceUrl]/tts/SynthTextEx 只合成50字节的情况"
        
        self.test_log.write(str(sys._getframe().f_code.co_name)+"\n注释："+Notes)    
        file='123456789012345678901234567890123456789012345678901'#open("./Data/TestData/case33.txt","rb").read()
        #file='ۋەھىمە بىلەن ھۆكۈمرانلىق قىلىش، خەلقنى قورقوتۇپ باشقۇرۇش'
       # ttscfg='capkey='+self.capkey
        ttscfg='capkey=tts.cloud.xiaokun'
        print 'file to be synth length is :'+str(len(file))
        voice,xml=TTS_class.TTS_ABILITIES(self.devKey,self.appKey,self.url,ttscfg,file,'3.8',False).run()
        self.Case_is_Pass=self.get_info_from_response(xml, "Success", "Success", "0")
        v_file=open('./Data/ResultData/test_TTS_Case33.pcm','wb')
        if voice!=None:
            v_file.write(voice)
        pass
    
    def test_TTS_Case34(self):    
        Notes="1.1.34 检测能力正确,tts.cloud.uyghur能力合成英文的情况"
        
        self.test_log.write(str(sys._getframe().f_code.co_name)+"\n注释："+Notes)    
        file='hello hello how are you'#open("./Data/TestData/"+self.caseName,"rb").read()
        #file=open("./Data/TestData/case30-right.txt","rb").read()
        
        ttscfg='capkey=tts.cloud.uyghur,engmode=english'
        voice,xml=TTS_class.TTS_ABILITIES(self.devKey,self.appKey,self.url,ttscfg,file,'3.8').run()
        v_file=open('./Data/ResultData/test_TTS_Case34.pcm','wb')
        if voice!=None:
            v_file.write(voice)
        self.Case_is_Pass=self.get_info_from_response(xml, "Success", "Success", "0")
        pass
    
    def test_TTS_Case35(self):    
        Notes="1.1.35 检测能力正确,tts.cloud.uyghur能力合成汉语的情况"
        
        self.test_log.write(str(sys._getframe().f_code.co_name)+"\n注释："+Notes)    
        file='合成汉语合成汉语合成汉语合成汉语合成汉语合成汉语合成汉语合成汉语合成汉语合成汉语合成汉语合成汉语'#open("./Data/TestData/"+self.caseName,"rb").read()
        #file=open("./Data/TestData/case30-right.txt","rb").read()
        
        ttscfg='capkey='+self.capkey
        voice,xml=TTS_class.TTS_ABILITIES(self.devKey,self.appKey,self.url,ttscfg,file,'3.8').run()
        v_file=open('./Data/ResultData/test_TTS_Case35.pcm','wb')
        if voice!=None:
            v_file.write(voice)
        self.Case_is_Pass=self.get_info_from_response(xml, "Success", "Success", "0")
        pass
    
    
    
    def get_info_from_response(self,response,expect_ResCode,expect_ResMessage,expect_ErrorNo,expect_Result=""):
        xml_str = Etree.fromstring(response) 
        all_is_same=True
        if 'ResCode' in response:
            self.ResCode = xml_str.find("ResCode").text
            if len(expect_ResCode)!=0:
                print 'Get_ResCode:'+self.ResCode+'\tExpect_ResCode:'+expect_ResCode
                self.test_log.write('\nGet_ResCode:'+self.ResCode+'\tExpect_ResCode:'+expect_ResCode)
                if self.ResCode!=expect_ResCode:
                    all_is_same=False
            
        if 'ResMessage' in response:
            self.ResMessage=xml_str.find("ResMessage").text
            if len(expect_ResMessage)!=0:
                print 'Get_ResMessage:'+self.ResMessage+'\tExpect_ResMessage:'+expect_ResMessage
                self.test_log.write('\nGet_ResMessage:'+self.ResMessage+'\tExpect_ResMessage:'+expect_ResMessage)
                if self.ResMessage!=expect_ResMessage:
                    all_is_same=False
                    
        if 'ErrorNo' in response:
            self.ErrorNo=xml_str.find("ErrorNo").text
            if len(expect_ErrorNo)!=0:
                print 'Get_ErrorNo:'+self.ErrorNo+'\tExpect_ErrorNo:'+expect_ErrorNo
                self.test_log.write('\nGet_ErrorNo:'+self.ErrorNo+'\tExpect_ErrorNo:'+expect_ErrorNo)
                if self.ErrorNo!=expect_ErrorNo:
                    all_is_same=False
        return all_is_same

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_TTS_Case1']
    unittest.main()