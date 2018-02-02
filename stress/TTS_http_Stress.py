# coding=utf-8
'''
Created on 2015-1-14

@author: wangsiyu
'''
import unittest
import hashlib
import httplib
import datetime
import time
import os
import TTS_class
import sys
import threading
import random
import xml.etree.ElementTree as Etree
from xml.etree import ElementTree  


####linux must open###

# import sys
# reload(sys)
# sys.setdefaultencoding('utf8')


class Test(unittest.TestCase):

    # 设置账号
    appKey = "ac5d5452"
    url = "10.0.1.117"
    devKey = "developer_key"

    CYCLE_TIME = datetime.timedelta(weeks=0, days=0, hours=00, minutes=00, seconds=10, microseconds=0, milliseconds=0)  # 60*60*24
    THREAD_MAX = 100

#     test_errorlog = open('./log/TTS-Error-log-' + str(time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(time.time()))) + '.txt', 'wb')
    test_rightlog = open('./log/TTS-Right-log-' + str(time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(time.time()))) + '.txt', 'wb')
    domain=['wangjing','xiaokun'] #领域
    domains=["common","finance","weather","queue","insurance","voyage","revenue","elecpower","message"] 
    pitch_speed_vol_range_arry = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '9.7','10', 'max', 'min']
    puncmode_range_arry = ['off', 'off_rtn', 'on_rtn', 'on']
    engmode_range_arry = ['auto', 'english', 'letter']
    digitmode_range_arry = ['auto_number', 'telegram', 'number', 'auto_telegram']
#     tagmode_range_arry = ['auto', 'vtml', 's3ml', 'ssml', 'none']#含宝维和nuance音库时
    tagmode_range_arry = ['auto','s3ml','none'] #去掉宝维和nuance音库
    audioformat_range_arry = ['ulaw8k8bit', 'pcm8k8bit', 'pcm8k16bit', 'pcm16k8bit', 'pcm16k16bit', 'pcm11k8bit', 'pcm11k16bit', 'mp3', 'mp3_24', 'mp3_16', 'vox8k4bit', 'vox6k4bit', 'alaw8k8bit']
    
    StressDataDir = "../Data/TestData/StressData/"
    StressDataList = os.listdir(StressDataDir)
   
    mutex = threading.Lock()
    
    def setUp(self):
        pass


    def tearDown(self):
        pass
    
    def GetRandomConfig(self):
        ttscfg = "capkey=tts.cloud.synth"
        ttscfg=ttscfg+',property=cn_'+random.choice(self.domain)
        if ttscfg=="capkey=tts.cloud.synth,property=cn_wangjing":
            ttscfg=ttscfg+',property=cn_'+random.choice(self.domain)+'_common'
        else:            
            ttscfg=ttscfg+',property=cn_'+random.choice(self.domain)+'_'+random.choice(self.domains)
        ttscfg=ttscfg+',pitch='+random.choice(self.pitch_speed_vol_range_arry)+',speed='+random.choice(self.pitch_speed_vol_range_arry)+',volume='+random.choice(self.pitch_speed_vol_range_arry)
        ttscfg=ttscfg+',digitmode='+random.choice(self.digitmode_range_arry)
        ttscfg=ttscfg+',engmode='+random.choice(self.engmode_range_arry)
        ttscfg=ttscfg+',puncmode='+random.choice(self.puncmode_range_arry)
        ttscfg=ttscfg+',tagmode='+random.choice(self.tagmode_range_arry)
        ttscfg=ttscfg+',audioformat='+random.choice(self.audioformat_range_arry)
#         ttscfg = "capkey=tts.cloud.synth"
        return ttscfg


    def testName(self):
        mutex_post = threading.Lock()
        mutex_fail = threading.Lock()
        mutex_success = threading.Lock()
        
        thread_list = []

        config = ''
        
        for i in range(self.THREAD_MAX):
            thread_name = 'thread-' + str(i)
            log_content = thread_name
            print thread_name
            new_thread = threading.Thread(target=self.TTS_Thread, args=([thread_name]), name=thread_name)
            thread_list.append(new_thread)
            new_thread.start()
        for thread_obj in thread_list:
            thread_obj.join()
        
        print "over"
        pass

    def TTS_Thread(self, thread_name):
        cycle_time = 0
        error_test_case = 0
#         success_time = 0
        start_time = datetime.datetime.today()        
        runTime = str(time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(time.time())))
        while (True):
            cycle_time = cycle_time + 1
            print '【cycle_time】:' + str(cycle_time)
#             print '【success_time】:' + str(success_time)            
            print "【START TIME】：",str(start_time) +'\t'+"【Stress'times】:" ,str(datetime.datetime.today()-start_time)
            if ((datetime.datetime.today()-start_time)>self.CYCLE_TIME):
                break
#             cycle_time = cycle_time + 1
#             print '【cycle_time】:' + str(cycle_time)
#             print '【success_time】:' + str(success_time)
            else:
                TestDataPath = self.StressDataDir + random.choice(self.StressDataList)
                file = open(TestDataPath, "rb").read()
                ttscfg = self.GetRandomConfig()
                
                if random.randint(0, 1) == 1:
                    is_Ex = True
                else:
                    is_Ex = False
                
                try:
                    voice, xml = TTS_class.TTS_ABILITIES(self.devKey, self.appKey, self.url, ttscfg, file, '3.8', is_Ex).run()
                except Exception, e:
                    print e
                    self.mutex.acquire()                
                    self.test_errorlog.write('\n' + '【ERROR】\t【time】:' + runTime + '\n')
                    self.test_errorlog.write('【ERROR】\t【info】:' + e + '\n')
                    self.mutex.release()
                    continue
                self.mutex.acquire() 
                self.test_rightlog.write('【RIGHT】\t【thread_name】:' + thread_name  +'\n' + '【time】:'+runTime +'\n【file】:'+str(TestDataPath)+ '\n【XML：】' +xml+'\n')
                self.mutex.release()

        pass
    


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
