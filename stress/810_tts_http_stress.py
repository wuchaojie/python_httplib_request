# coding=utf-8
'''
Created on 2017年11月22日

@author: wuchaojie
'''
import unittest
import os
import time
import random
import threading
import TTS_class
import datetime


class Test(unittest.TestCase):
    # 设置账号
    appKey = "ac5d5452"
    url = "10.0.1.152"
    devKey = "developer_key"
    THREAD_MAX = 300
    CYCLE_TIME = datetime.timedelta(weeks=1, days=0, hours=00, minutes=00, seconds=10, microseconds=0, milliseconds=0)  # 60*60*24
    mutex = threading.Lock()
    
    test_rightlog = open('./log/TTS-Right-log-' + str(time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(time.time()))) + '.txt', 'wb')
    test_errorlog = open('./log/TTS-Right-log-' + str(time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(time.time()))) + '.txt', 'wb')

    domain=['barron','cameal','cartoonjing','diaoxiong','jiangman','liangjiahe','shenxu','wangjingv9','xiaokunv9','xumengjuan','zhaqian','uyghur'] #领域
    #domains=["common","finance","weather","queue","insurance","voyage","revenue","elecpower","message"] #ihear9.0 中已经去掉此项
    pitch_speed_vol_range_arry = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '9.7','10', 'max', 'min']
    puncmode_range_arry = ['off', 'off_rtn', 'on_rtn','on']
    engmode_range_arry = ['auto', 'english', 'letter']
    digitmode_range_arry = ['auto_number', 'telegram', 'number', 'auto_telegram']
    voicestyle_range_arry = ['normal', 'plain', 'clear', 'vivid']
    #tagmode_range_arry = ['auto','s3ml','none'] #ihear9.0 中已经去掉此项
    audioformat_range_arry = ['ulaw8k8bit', 'pcm8k8bit', 'pcm8k16bit', 'pcm16k8bit', 'pcm16k16bit', 'pcm11k8bit', 'pcm11k16bit', 'mp3', 'mp3_24', 'mp3_16', 'vox8k4bit', 'vox6k4bit', 'alaw8k8bit']
    
    StressDataDir = "../Data/TestData/StressData/"
    wangyuData = "../Data/StressData_fix/wangyuData/"
    #StressDataList = os.listdir(StressDataDir)
    StressDataList = os.listdir(wangyuData)
 
    def setUp(self):
        pass

    def tearDown(self):
        pass
    
    def GetRandomConfig(self):
        ttscfg = "capkey=tts.cloud.synth"
        ttscfg=ttscfg+',property=cn_'+random.choice(self.domain)+'_common'
        if ttscfg=="capkey=tts.cloud.synth,property=cn_uyghur_common":
            ttscfg='capkey=tts.cloud.synth,property=usy_uyghur_common'
        if random.uniform(0,1) > 0.5:
            ttscfg+=',pitch='+random.choice(self.pitch_speed_vol_range_arry)
        if random.uniform(0,1) > 0.5:
            ttscfg+=',speed='+random.choice(self.pitch_speed_vol_range_arry)
        if random.uniform(0,1) > 0.5:
            ttscfg+= ',volume='+random.choice(self.pitch_speed_vol_range_arry)
        if random.uniform(0,1) > 0.5:
            ttscfg+=',digitmode='+random.choice(self.digitmode_range_arry)
        if random.uniform(0,1) > 0.5:
            ttscfg+=',engmode='+random.choice(self.engmode_range_arry)
        if random.uniform(0,1) > 0.5:
            ttscfg+=',puncmode='+random.choice(self.puncmode_range_arry)
        if random.uniform(0,1) > 0.5:                       
            ttscfg+=',voicestyle='+random.choice(self.voicestyle_range_arry)  
        if random.uniform(0,1) > 0.5:
            ttscfg+=',audioformat='+random.choice(self.audioformat_range_arry)
        print ttscfg
        return ttscfg


    def testText_ihear9_tressCase(self):
#         mutex_post=threading.Lock()
#         mutex_fail=threading.Lock()
#         mutex_success=threading.Lock()
#         locks={'post':mutex_post,
#                 'fail':mutex_fail,
#                 'success':mutex_success,
#                 'post_fail':0,
#                 'fail_times':0,
#                  'success_times':0
#                 }
            
        thread_list=[]
            
        for i in range(self.THREAD_MAX):
            thread_name = 'thread-' + str(i)
            new_thread = threading.Thread(target = self.text_tts_process_main, args = (thread_name,i), name = thread_name)
            thread_list.append(new_thread)
            new_thread.start()    
        for thread_obj in thread_list:
            thread_obj.join()

    def text_tts_process_main(self, thread_name, thread_index):
        cycle_time=0
        #request_date = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        start_time=datetime.datetime.today()
        #thread_info=''
        runTime = str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
        while (True):
            cycle_time = cycle_time + 1
            print "【thread_name】 :" ,thread_name
            print '【cycle_time】:' , str(cycle_time)
            print "【START TIME】：",str(start_time) +'\n'+"【Stress'times】:" ,str(datetime.datetime.today()-start_time)
            if ((datetime.datetime.today()-start_time)>self.CYCLE_TIME):
                break
            else:
                #TestDataPath = self.StressDataDir + random.choice(self.StressDataList) 
                TestDataPath = self.wangyuData + random.choice(self.StressDataList)
                print TestDataPath
                file = open(TestDataPath, "rb").read()
                ttscfg = self.GetRandomConfig()
                if random.randint(0, 1) == 1:
                    is_Ex = True
                else:
                    is_Ex = False   
                try:
                    post_time, xml = TTS_class.TTS_ABILITIES(self.devKey, self.appKey, self.url, ttscfg, file, '3.8', is_Ex).run()
                    print str(xml)
                except Exception, e:
                    print e
                    self.mutex.acquire()                
                    self.test_errorlog.write('\n' + '【ERROR】\t【time】:' + runTime + '\n')
                    self.test_errorlog.write('【ERROR】\t【info】:' + e + '\n')
                    self.mutex.release()
                    continue
                self.mutex.acquire() 
                self.test_rightlog.write('【RIGHT】\t【thread_name】:' + thread_name  +'\n' + '【run time】:'+runTime +'\n【file】:'+str(TestDataPath)+ '\n【XML】' +xml+'\n')
                self.test_rightlog.write("【post time】  :" + str(post_time) +'\n')
                self.mutex.release()

        pass
    
if __name__ == '__main__':
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
