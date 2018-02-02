#-*- coding:UTF-8 -*-

'''
Created on 2016年4月22日

@author: dailipo
'''
import unittest
import time
import hashlib
import httplib
import xml.etree.ElementTree as Etree
import common
#linux must open
# import sys
# reload(sys)
# sys.setdefaultencoding('utf8')
#***************************************************************************

APPKEY = "ac5d5452"
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
        '''检测能力正确,各配置串默认的情况'''
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
    
    def testTTSfunctioncase2111(self):
        '''2.1.1.1检测能力正确,各配置串默认的情况,返回16K16bit的pcm'''
        config = "capkey=tts.cloud.synth,property=cn_wangjing_common"
#         body = open(TEST_DATA + "1.txt", "r").read()
        body="就是乘客我现在把乘客送到了刚才手机关机了现在就是这个费用现在降不下来怎么办手机关机"
        voice,xml,resCode,resMessage = tts_post(APPKEY, DEVKEY,config, body)
        with open(TEST_RESULT+'testTTSfunctioncase1000_16K16bit.pcm','wb') as v_file:
            v_file.write(voice)
        self.assertEqual(resCode, "Success")
        self.assertEqual(resMessage, "Success")
        pass


    def testTTSfunctioncase2112(self):
        '''2.1.1.2 检测http头中task-config中能力字段为不存在的能力，调用合成请求协议的情况'''
        config = ["capkey=tts.cloud.test,property=cn_wangjing_common",
                  "capkey=abc123!@#,property=cn_wangjing_common",
                  "",
                  "property=cn_wangjing_common",                  
                  ]
        file=open("../Data/TestData/case1.txt","rb").read()
        body=file        
        for i  in config:
            voice,xml,resCode,resMessage = tts_post(APPKEY, DEVKEY,i, body,)
            with open(TEST_RESULT+'testTTSfunctioncase112_16K16bit.pcm','wb') as v_file:
                v_file.write(voice)
            self.assertEqual(resCode, "Failed")
            self.assertEqual(resMessage, "CommitRequest jetcl_commit_request failed")
            pass

    def testTTSfunctioncase2121(self):
        ''''2.1.2.1 检测http头中task-config中pitch基频1-10和min、max字段同时验证min=o和max=10，等于5时和不填写pitch的MD5值调用合成请求协议的情况'''
        for i in ['0','1','2','3','4','5','6','7','8','9','9.7','10',]:
            config = "capkey=tts.cloud.synth,property=cn_wangjing_common,pitch="+str(i)
            file=open("../Data/TestData/case1.txt","rb").read()
            body=file
            voice,xml,resCode,resMessage = tts_post(APPKEY, DEVKEY,config, body,)
            with open(TEST_RESULT+str(i)+'_pitch_'+'testTTSfunctioncase114_16K16bit.pcm','wb') as v_file:
                v_file.write(voice)
            self.assertEqual(resCode, "Success")
            self.assertEqual(resMessage, "Success")            

        for i  in ['min','max']:
            config = "capkey=tts.cloud.synth,property=cn_wangjing_common,pitch="+str(i)
            file=open("../Data/TestData/case1.txt","rb").read()
            body=file
            voice,xml,resCode,resMessage = tts_post(APPKEY, DEVKEY,config, body,)
            with open(TEST_RESULT+str(i)+'_pitch_'+'testTTSfunctioncase114_16K16bit.pcm','wb') as v_file:
                v_file.write(voice)
            self.assertEqual(resCode, "Success")
            self.assertEqual(resMessage, "Success")
        md5file=open(TEST_RESULT+'10'+'_pitch_'+'testTTSfunctioncase114_16K16bit.pcm',"rb").read()
        md5file2=open(TEST_RESULT+'max'+'_pitch_'+'testTTSfunctioncase114_16K16bit.pcm',"rb").read()
        md5file3=open(TEST_RESULT+'0'+'_pitch_'+'testTTSfunctioncase114_16K16bit.pcm',"rb").read()
        md5file4=open(TEST_RESULT+'min'+'_pitch_'+'testTTSfunctioncase114_16K16bit.pcm',"rb").read()
        md5file5=open(TEST_RESULT+'5'+'_pitch_'+'testTTSfunctioncase114_16K16bit.pcm',"rb").read()
        md5file6=open(TEST_RESULT+'testTTSfunctioncase111_16K16bit.pcm',"rb").read()      
        self.assertEqual(hashlib.md5(md5file).hexdigest(), hashlib.md5(md5file2).hexdigest())
        self.assertEqual(hashlib.md5(md5file3).hexdigest(), hashlib.md5(md5file4).hexdigest())
        self.assertEqual(hashlib.md5(md5file5).hexdigest(), hashlib.md5(md5file6).hexdigest())   
        pass
    def testTTSfunctioncase2122(self):
        ''''2.1.2.2 检测http头中task-config中pitch基频在0，11，负数，字段调用合成请求协议的情况'''
        for i in [11,-10]:
            config = "capkey=tts.cloud.synth,property=cn_wangjing_common,pitch="+str(i)
            file=open("../Data/TestData/case1.txt","rb").read()
            body=file
            voice,xml,resCode,resMessage = tts_post(APPKEY, DEVKEY,config, body,)
            v_file=open(TEST_RESULT+str(i)+'_pitch_'+'testTTSfunctioncase115_16K16bit.pcm','wb')
            if voice!=None:
                v_file.write(voice)
            self.assertEqual(resCode, "Failed")
            self.assertEqual(resMessage, "ParseTtsParams failed")
        pass
    def testTTSfunctioncase2123(self):
        ''''2.1.2.3 检测http头中task-config中volume基频在1-10和min、max字段同时验证min=o和max=10 volume=5和不填写volume的MD5调用合成请求协议的情况'''
        for i in ['0','1','2','3','4','5','6','7','8','9','9.7','10',]:
            config = "capkey=tts.cloud.synth,property=cn_wangjing_common,volume="+str(i)
            file=open("../Data/TestData/case1.txt","rb").read()
            body=file
            voice,xml,resCode,resMessage = tts_post(APPKEY, DEVKEY,config, body,)
            v_file=open(TEST_RESULT+str(i)+'_volume_'+'testTTSfunctioncase116_16K16bit.pcm','wb')
            if voice!=None:
                v_file.write(voice)
            self.assertEqual(resCode, "Success")
            self.assertEqual(resMessage, "Success")
        for i  in ['min','max']:
            config = "capkey=tts.cloud.synth,property=cn_wangjing_common,volume="+str(i)
            file=open("../Data/TestData/case1.txt","rb").read()
            body=file
            voice,xml,resCode,resMessage = tts_post(APPKEY, DEVKEY,config, body,)
#             v_file=open(TEST_RESULT+str(i)+'_pitch_'+'testTTSfunctioncase116_16K16bit.pcm','wb')
            with open(TEST_RESULT+str(i)+'_volume_'+'testTTSfunctioncase116_16K16bit.pcm','wb') as v_file:
                v_file.write(voice)
            self.assertEqual(resCode, "Success")
            self.assertEqual(resMessage, "Success")                    
        md5file=open(TEST_RESULT+'10'+'_volume_'+'testTTSfunctioncase116_16K16bit.pcm',"rb").read()
        md5file2=open(TEST_RESULT+'max'+'_volume_'+'testTTSfunctioncase116_16K16bit.pcm',"rb").read()
        md5file3=open(TEST_RESULT+'0'+'_volume_'+'testTTSfunctioncase116_16K16bit.pcm',"rb").read()
        md5file4=open(TEST_RESULT+'min'+'_volume_'+'testTTSfunctioncase116_16K16bit.pcm',"rb").read()
        md5file5=open(TEST_RESULT+'5'+'_volume_'+'testTTSfunctioncase116_16K16bit.pcm',"rb").read()
        md5file6=open(TEST_RESULT+'testTTSfunctioncase111_16K16bit.pcm',"rb").read()        
        self.assertEqual(hashlib.md5(md5file).hexdigest(), hashlib.md5(md5file2).hexdigest())
        self.assertEqual(hashlib.md5(md5file3).hexdigest(), hashlib.md5(md5file4).hexdigest())
        self.assertEqual(hashlib.md5(md5file5).hexdigest(), hashlib.md5(md5file6).hexdigest())
        pass
    def testTTSfunctioncase2124(self):
        ''''2.1.2.4 检测http头中task-config中speed语速在1-10和min、max字段同时验证min=o和max=10的MD5调用合成请求协议的情况'''
        for i in ['0','1','2','3','4','5','6','7','8','9','9.7','10',]:
            config = "capkey=tts.cloud.synth,property=cn_wangjing_common,speed="+str(i)
            file=open("../Data/TestData/case1.txt","rb").read()
            body=file
            voice,xml,resCode,resMessage = tts_post(APPKEY, DEVKEY,config, body,)
            with open(TEST_RESULT+str(i)+'_pitch_'+'testTTSfunctioncase2124_16K16bit.pcm','wb') as v_file:
                v_file.write(voice)
            self.assertEqual(resCode, "Success")
            self.assertEqual(resMessage, "Success")
        for i  in ['min','max']:
            config = "capkey=tts.cloud.synth,property=cn_wangjing_common,speed="+str(i)
            file=open("../Data/TestData/case1.txt","rb").read()
            body=file
            voice,xml,resCode,resMessage = tts_post(APPKEY, DEVKEY,config, body,)
#             v_file=open(TEST_RESULT+str(i)+'_pitch_'+'testTTSfunctioncase116_16K16bit.pcm','wb')
            with open(TEST_RESULT+str(i)+'_pitch_'+'testTTSfunctioncase2124_16K16bit.pcm','wb') as v_file:
                v_file.write(voice) 
            self.assertEqual(resCode, "Success")
            self.assertEqual(resMessage, "Success")               
        md5file=open(TEST_RESULT+'10'+'_pitch_'+'testTTSfunctioncase2124_16K16bit.pcm',"rb").read()
        md5file2=open(TEST_RESULT+'max'+'_pitch_'+'testTTSfunctioncase2124_16K16bit.pcm',"rb").read()
        md5file3=open(TEST_RESULT+'0'+'_pitch_'+'testTTSfunctioncase2124_16K16bit.pcm',"rb").read()
        md5file4=open(TEST_RESULT+'min'+'_pitch_'+'testTTSfunctioncase2124_16K16bit.pcm',"rb").read()
        md5file5=open(TEST_RESULT+'5'+'_pitch_'+'testTTSfunctioncase2124_16K16bit.pcm',"rb").read()
        md5file6=open(TEST_RESULT+'testTTSfunctioncase111_16K16bit.pcm',"rb").read()
        self.assertEqual(hashlib.md5(md5file).hexdigest(), hashlib.md5(md5file2).hexdigest())
        self.assertEqual(hashlib.md5(md5file3).hexdigest(), hashlib.md5(md5file4).hexdigest())
        self.assertEqual(hashlib.md5(md5file5).hexdigest(), hashlib.md5(md5file6).hexdigest())

        pass
    def testTTSfunctioncase2125(self):
        ''''2.1.2.5 检测http头中task-config中volume基频在11，负数，字段调用合成请求协议的情况'''
        for i in [11,-10]:
            config = "capkey=tts.cloud.synth,property=cn_wangjing_common,volume="+str(i)
            file=open("../Data/TestData/case1.txt","rb").read()
            body=file
            voice,xml,resCode,resMessage = tts_post(APPKEY, DEVKEY,config, body,)
            with open(TEST_RESULT+str(i)+'_volume_'+'testTTSfunctioncase2125_16K16bit.pcm','wb') as v_file:
                v_file.write(voice)
            self.assertEqual(resCode, "Failed")
            self.assertEqual(resMessage, "ParseTtsParams failed")
        pass
    def testTTSfunctioncase2126(self):
        ''''2.1.2.6 检测http头中task-config中speed基频在0，11，负数，字段调用合成请求协议的情况'''
        for i in [11,-10]:
            config = "capkey=tts.cloud.synth,property=cn_wangjing_common,speed="+str(i)
            file=open("../Data/TestData/case1.txt","rb").read()
            body=file
            voice,xml,resCode,resMessage = tts_post(APPKEY, DEVKEY,config, body,)
            v_file=open(TEST_RESULT+str(i)+'_speed_'+'testTTSfunctioncase2126_16K16bit.pcm','wb')
            if voice!=None:
                v_file.write(voice)
            self.assertEqual(resCode, "Failed")
            self.assertEqual(resMessage, "ParseTtsParams failed")
        pass

    def testTTSfunctioncase2127(self):
        ''''2.1.2.7 检测http头中task-config中puncmode为off能否合成功且无回车符或换行的MD5调用合成请求协议的情况'''
#         for i in ['off','on','off_rtn','on_rtn',]:
        #回车符号
        #off不合成标点符号，自动判断回车换行是否分隔符，缺省值,不读回车换行符
        config = "capkey=tts.cloud.synth,property=cn_wangjing_common,puncmode=off"
        file=open("../Data/TestData/case120.txt","rb").read()
        body=file
        voice,xml,resCode,resMessage = tts_post(APPKEY, DEVKEY,config, body,)
        with open(TEST_RESULT+'off'+'_puncmode_'+'testTTSfunctioncase120_16K16bit.pcm','wb') as v_file:
            v_file.write(voice)
        self.assertEqual(resCode, "Success")
        self.assertEqual(resMessage, "Success")
        md5file=open(TEST_RESULT+'off'+'_puncmode_'+'testTTSfunctioncase120_16K16bit.pcm',"rb").read()
        file=open("../Data/TestData/case120_hc.txt","rb").read()
        voice,xml,resCode,resMessage = tts_post(APPKEY, DEVKEY,config, file,)
        with open(TEST_RESULT+"off"+'_puncmode_'+'testTTSfunctioncase120_hc_16K16bit.pcm','wb') as v_file:
                v_file.write(voice)
        self.assertEqual(resCode, "Success")
        self.assertEqual(resMessage, "Success")                
        md5file2=open(TEST_RESULT+'off'+'_puncmode_'+'testTTSfunctioncase120_hc_16K16bit.pcm',"rb").read()
        ##换行符比较
        file=open("../Data/TestData/case1201.txt","rb").read()
        body=file
        voice,xml,resCode,resMessage = tts_post(APPKEY, DEVKEY,config, body,)
        with open(TEST_RESULT+'off'+'_puncmode_'+'testTTSfunctioncase1201_16K16bit.pcm','wb') as v_file:
            v_file.write(voice)
        self.assertEqual(resCode, "Success")
        self.assertEqual(resMessage, "Success")            
        md5file3=open(TEST_RESULT+'off'+'_puncmode_'+'testTTSfunctioncase1201_16K16bit.pcm',"rb").read()
        file=open("../Data/TestData/case1201_hh.txt","rb").read()
        voice,xml,resCode,resMessage = tts_post(APPKEY, DEVKEY,config, file,)
        with open(TEST_RESULT+"off"+'_puncmode_'+'testTTSfunctioncase1201_hh_16K16bit.pcm','wb') as v_file:
                v_file.write(voice)        
        self.assertEqual(resCode, "Success")
        self.assertEqual(resMessage, "Success")

        md5file4=open(TEST_RESULT+'off'+'_puncmode_'+'testTTSfunctioncase1201_hh_16K16bit.pcm',"rb").read()    
        self.assertEqual(hashlib.md5(md5file).hexdigest(), hashlib.md5(md5file2).hexdigest())
        self.assertEqual(hashlib.md5(md5file3).hexdigest(), hashlib.md5(md5file4).hexdigest())
        pass
    
    def testTTSfunctioncase2128(self):
        ''''2.1.2.8 检测http头中task-config中puncmode为on、能否合成功且有无回车符的MD5调用合成请求协议的情况'''
#         for i in ['off','on','off_rtn','on_rtn',]:
        #回车符MD5值比较
        config = "capkey=tts.cloud.synth,property=cn_wangjing_common,puncmode=on"
        file=open("../Data/TestData/case121.txt","rb").read()
        body=file
        voice,xml,resCode,resMessage = tts_post(APPKEY, DEVKEY,config, body,)
        with open(TEST_RESULT+'on'+'_puncmode_'+'testTTSfunctioncase121_16K16bit.pcm','wb') as v_file:
            v_file.write(voice)        
        self.assertEqual(resCode, "Success")
        self.assertEqual(resMessage, "Success")
        md5file=open(TEST_RESULT+'on'+'_puncmode_'+'testTTSfunctioncase121_16K16bit.pcm',"rb").read()
        config = "capkey=tts.cloud.synth,property=cn_wangjing_common,puncmode=on"
        file=open("../Data/TestData/case121_hc.txt","rb").read()
        voice,xml,resCode,resMessage = tts_post(APPKEY, DEVKEY,config, file,)
        with open(TEST_RESULT+"on"+'_puncmode_'+'testTTSfunctioncase121_hc_16K16bit.pcm','wb') as v_file:
                v_file.write(voice)        
        self.assertEqual(resCode, "Success")
        self.assertEqual(resMessage, "Success")
        with open(TEST_RESULT+"on"+'_puncmode_'+'testTTSfunctioncase121_hc_16K16bit.pcm','wb') as v_file:
                v_file.write(voice)
        md5file2=open(TEST_RESULT+'on'+'_puncmode_'+'testTTSfunctioncase121_hc_16K16bit.pcm',"rb").read()
             
        self.assertEqual(hashlib.md5(md5file).hexdigest(), hashlib.md5(md5file2).hexdigest())
        pass

    def testTTSfunctioncase2129(self):
        ''''2.1.2.9 检测http头中task-config中puncmode为off_rtn能否合成功、回车和换行结果对比,调用合成请求协议的情况'''
#         for i in ['off','on','off_rtn','on_rtn',]:
        #回车符  
        #off_rtn不读符号，强制将回车换行作为分隔符 
        config = "capkey=tts.cloud.synth,property=cn_wangjing_common,puncmode=off_rtn"
        file=open("../Data/TestData/case120.txt","rb").read()
        body=file
        voice,xml,resCode,resMessage = tts_post(APPKEY, DEVKEY,config, body,)
        with open(TEST_RESULT+'off_rtn'+'_puncmode_'+'testTTSfunctioncase122_16K16bit.pcm','wb') as v_file:
            v_file.write(voice)
        md5file=open(TEST_RESULT+'off_rtn'+'_puncmode_'+'testTTSfunctioncase122_16K16bit.pcm',"rb").read()
#         config = "capkey=tts.cloud.synth,property=cn_wangjing_common,puncmode=off_rtn"
#         file=open("../Data/TestData/case120_hc.txt","rb").read()
#         voice,xml,resCode,resMessage = tts_post(APPKEY, DEVKEY,config, file,)
#         with open(TEST_RESULT+"off_rtn"+'_puncmode_'+'testTTSfunctioncase122_hc_16K16bit.pcm','wb') as v_file:
#                 v_file.write(voice)
#         md5file2=open(TEST_RESULT+'off_rtn'+'_puncmode_'+'testTTSfunctioncase122_hc_16K16bit.pcm',"rb").read()
        #换行符
        self.assertEqual(resCode, "Success")
        self.assertEqual(resMessage, "Success")
        file=open("../Data/TestData/case1201.txt","rb").read()  #使用的测试数据和120case相同
        body=file
        voice,xml,resCode,resMessage = tts_post(APPKEY, DEVKEY,config, body,)
        with open(TEST_RESULT+'off_rtn'+'_puncmode_'+'testTTSfunctioncase1221_16K16bit.pcm','wb') as v_file:
            v_file.write(voice)
        md5file3=open(TEST_RESULT+'off_rtn'+'_puncmode_'+'testTTSfunctioncase1221_16K16bit.pcm',"rb").read()
#         file=open("../Data/TestData/case1201_hh.txt","rb").read()
#         voice,xml,resCode,resMessage = tts_post(APPKEY, DEVKEY,config, file,)
#         with open(TEST_RESULT+"off_rtn"+'_pitch_'+'testTTSfunctioncase1221_hh_16K16bit.pcm','wb') as v_file:
#                 v_file.write(voice)        
#         md5file4=open(TEST_RESULT+'off_rtn'+'_pitch_'+'testTTSfunctioncase1221_hh_16K16bit.pcm',"rb").read()
#        不读符号，强制将回车换行作为分隔符 ,所以比较两者的MD5值是否一致性
        self.assertEqual(hashlib.md5(md5file).hexdigest(), hashlib.md5(md5file3).hexdigest())
#         self.assertEqual(hashlib.md5(md5file3).hexdigest(), hashlib.md5(md5file4).hexdigest())
        pass

    def testTTSfunctioncase21210(self):
        ''''2.1.2.10 检测http头中task-config中puncmode为on_rtn能否合成功、回车和换行结果对比,调用合成请求协议的情况'''

        config = "capkey=tts.cloud.synth,property=cn_wangjing_common,puncmode=on_rtn"
        file=open("../Data/TestData/case120.txt","rb").read()
        body=file
        voice,xml,resCode,resMessage = tts_post(APPKEY, DEVKEY,config, body,)
        with open(TEST_RESULT+'on_rtn'+'_puncmode_'+'testTTSfunctioncase123_16K16bit.pcm','wb') as v_file:
            v_file.write(voice)
        self.assertEqual(resCode, "Success")
        self.assertEqual(resMessage, "Success")            
        md5file=open(TEST_RESULT+'on_rtn'+'_puncmode_'+'testTTSfunctioncase123_16K16bit.pcm',"rb").read()
        file=open("../Data/TestData/case1201.txt","rb").read()  #使用的测试数据和120case相同
        body=file
        voice,xml,resCode,resMessage = tts_post(APPKEY, DEVKEY,config, body,)
        with open(TEST_RESULT+'on_rtn'+'_puncmode_'+'testTTSfunctioncase1231_16K16bit.pcm','wb') as v_file:
            v_file.write(voice)
        self.assertEqual(resCode, "Success")
        self.assertEqual(resMessage, "Success")            
        md5file3=open(TEST_RESULT+'on_rtn'+'_puncmode_'+'testTTSfunctioncase1231_16K16bit.pcm',"rb").read()
#         file=open("../Data/TestData/case1201_hh.txt","rb").read()
#         voice,xml,resCode,resMessage = tts_post(APPKEY, DEVKEY,config, file,)
#         with open(TEST_RESULT+"off_rtn"+'_pitch_'+'testTTSfunctioncase1221_hh_16K16bit.pcm','wb') as v_file:
#                 v_file.write(voice)        
#         md5file4=open(TEST_RESULT+'off_rtn'+'_pitch_'+'testTTSfunctioncase1221_hh_16K16bit.pcm',"rb").read()
#        不读符号，强制将回车换行作为分隔符 ,所以比较两者的MD5值是否一致性
        self.assertEqual(hashlib.md5(md5file).hexdigest(), hashlib.md5(md5file3).hexdigest())
#         self.assertEqual(hashlib.md5(md5file3).hexdigest(), hashlib.md5(md5file4).hexdigest())
        pass

    def testTTSfunctioncase21211(self):
        ''''2.1.2.11 检测http头中task-config中digitmode数字阅读方式,同时比对数字、电报的自动与不自动的MD5值调用合成请求协议的情况'''
        for i in ["auto_number","telegram","number","auto_telegram"]:
            config = "capkey=tts.cloud.synth,property=cn_wangjing_common,digitmode="+str(i)
            file=open("../Data/TestData/case124.txt","rb").read()
            body=file
            voice,xml,resCode,resMessage = tts_post(APPKEY, DEVKEY,config, body,)
            with open(TEST_RESULT+str(i)+'_digitmode_'+'testTTSfunctioncase21211_16K16bit.pcm','wb') as v_file:
                v_file.write(voice)
            self.assertEqual(resCode, "Success")
            self.assertEqual(resMessage, "Success")
        md5file=open(TEST_RESULT+'auto_number'+'_digitmode_'+'testTTSfunctioncase21211_16K16bit.pcm',"rb").read()
        md5file2=open(TEST_RESULT+'number'+'_digitmode_'+'testTTSfunctioncase21211_16K16bit.pcm',"rb").read()
        md5file3=open(TEST_RESULT+'telegram'+'_digitmode_'+'testTTSfunctioncase21211_16K16bit.pcm',"rb").read()
        md5file4=open(TEST_RESULT+'auto_telegram'+'_digitmode_'+'testTTSfunctioncase21211_16K16bit.pcm',"rb").read()
        self.assertEqual(hashlib.md5(md5file).hexdigest(), hashlib.md5(md5file2).hexdigest())
        self.assertEqual(hashlib.md5(md5file3).hexdigest(), hashlib.md5(md5file4).hexdigest())         
       
        pass

    def testTTSfunctioncase21212(self):
        ''''2.1.2.12 检测http头中task-config中engmode英文阅读方式,同时对比auto和english返回结果的MD5值调用合成请求协议的情况'''
        for i in ["auto","english","letter"]:
            config = "capkey=tts.cloud.synth,property=cn_wangjing_common,engmode="+str(i)
            file=open("../Data/TestData/case125.txt","rb").read()
            body=file
            voice,xml,resCode,resMessage = tts_post(APPKEY, DEVKEY,config, body,)
            with open(TEST_RESULT+str(i)+'_engmode_'+'testTTSfunctioncase125_16K16bit.pcm','wb') as v_file:
                v_file.write(voice)
            self.assertEqual(resCode, "Success")
            self.assertEqual(resMessage, "Success")
        md5file=open(TEST_RESULT+'auto'+'_engmode_'+'testTTSfunctioncase125_16K16bit.pcm',"rb").read()
        md5file2=open(TEST_RESULT+'english'+'_engmode_'+'testTTSfunctioncase125_16K16bit.pcm',"rb").read()
        md5file3=open(TEST_RESULT+'letter'+'_engmode_'+'testTTSfunctioncase125_16K16bit.pcm',"rb").read()
#         md5file4=open(TEST_RESULT+'auto_telegram'+'_digitmode_'+'testTTSfunctioncase124_16K16bit.pcm',"rb").read()
        self.assertEqual(hashlib.md5(md5file).hexdigest(), hashlib.md5(md5file2).hexdigest())
#         self.assertEqual(hashlib.md5(md5file3).hexdigest(), hashlib.md5(md5file4).hexdigest())         
        config = "capkey=tts.cloud.synth,property=cn_wangjing_common,engmode=auto"
        file=open("../Data/TestData/case1251.txt","rb").read()
        body=file
        voice,xml,resCode,resMessage = tts_post(APPKEY, DEVKEY,config, body,)
        with open(TEST_RESULT+'4auto'+'_engmode_'+'testTTSfunctioncase125_16K16bit.pcm','wb') as v_file:
            v_file.write(voice)
        self.assertEqual(resCode, "Success")
        self.assertEqual(resMessage, "Success")
        md5file4=open(TEST_RESULT+'4auto'+'_engmode_'+'testTTSfunctioncase125_16K16bit.pcm',"rb").read()
        self.assertEqual(hashlib.md5(md5file3).hexdigest(), hashlib.md5(md5file4).hexdigest())
#         config = "capkey=tts.cloud.synth,property=cn_wangjing_common,digitmode=number"
#         body="一千"
#         voice,xml,resCode,resMessage = tts_post(APPKEY, DEVKEY,config, body,)
#         with open(TEST_RESULT+'一千'+'_digitmode_'+'testTTSfunctioncase124_16K16bit.pcm','wb') as v_file:
#             v_file.write(voice)
#         md5file5=open(TEST_RESULT+'一千'+'_digitmode_'+'testTTSfunctioncase124_16K16bit.pcm',"rb").read()
#         self.assertEqual(hashlib.md5(md5file5).hexdigest(), hashlib.md5(md5file2).hexdigest())        
        pass

    def testTTSfunctioncase21213(self): #tagmode设置方式
        ''''2.1.2.13 检测http头中task-config中tagmode=auto、s3ml标注处理方式,调用合成请求协议的情况'''
        config = "capkey=tts.cloud.synth,property=cn_wangjing_common,tagmode=s3ml"
        for i  in ['backaudio','break','domain','emphasis','mark','paragraph','phoneme','prosody','punctuation','header','say','speak','sub','voice','lang']:
            print  'tagmode=s3ml,style:',i
            if str(i)=="backaudio":
 
                file=open("../Data/TestData/case126_s3_backaudio.txt","rb").read()
            elif str(i)=="break":   
                file=open("../Data/TestData/case126_s3_break.txt","rb").read()
            elif str(i)=="domain": 
                file=open("../Data/TestData/case126_s3_domain.txt","rb").read() 
            elif str(i)=="emphasis": 
                file=open("../Data/TestData/case126_s3_emphasis.txt","rb").read()                
            elif str(i)=="mark": 
                file=open("../Data/TestData/case126_s3_mark.txt","rb").read()                
            elif str(i)=="paragraph": 
                file=open("../Data/TestData/case126_s3_paragraph.txt","rb").read()
            elif str(i)=="phoneme": 
                file=open("../Data/TestData/case126_s3_phoneme.txt","rb").read()
            elif str(i)=="prosody": 
                file=open("../Data/TestData/case126_s3_prosody.txt","rb").read()                
            elif str(i)=="punctuation": 
                file=open("../Data/TestData/case126_s3_punctuation.txt","rb").read() 
            elif str(i)=="header": 
                file=open("../Data/TestData/case126_s3_header.txt","rb").read()                
            elif str(i)=="say": 
                file=open("../Data/TestData/case126_s3_say.txt","rb").read()
            elif str(i)=="speak": 
                file=open("../Data/TestData/case126_s3_speak.txt","rb").read()
            elif str(i)=="sub": 
                file=open("../Data/TestData/case126_s3_sub.txt","rb").read()                                                
            elif str(i)=="voice": 
                file=open("../Data/TestData/case126_s3_voice.txt","rb").read()                
            elif str(i)=="lang": 
                file=open("../Data/TestData/case126_s3_sublang.txt","rb").read()                                                                                                 
            body=file
            voice,xml,resCode,resMessage = tts_post(APPKEY, DEVKEY,config, body,)
            with open(TEST_RESULT+'s3ml'+str(i)+'_tagmode_'+'testTTSfunctioncase126_s3ml_16K16bit.pcm','wb') as v_file:
                v_file.write(voice)
            self.assertEqual(resCode, "Success")
            self.assertEqual(resMessage, "Success")
        config = "capkey=tts.cloud.synth,property=cn_wangjing_common,tagmode=auto"   
        file=open("../Data/TestData/case126_s3_lang.txt","rb").read() 
        body=file
        voice,xml,resCode,resMessage = tts_post(APPKEY, DEVKEY,config, body,)
        with open(TEST_RESULT+'auto'+'_tagmode_'+'testTTSfunctioncase126_16K16bit.pcm','wb') as v_file:
            v_file.write(voice)
        self.assertEqual(resCode, "Success")
        self.assertEqual(resMessage, "Success")
        pass
####################
    def testTTSfunctioncase212132(self): #tagmode设置方式
        ''''2.1.2.132 检测http头中task-config中tagmode=auto、s3ml标注处理方式,调用合成请求协议的情况'''
        config = "capkey=tts.cloud.synth,property=cn_wangjing_common,tagmode=s3ml"
#         for i  in ['backaudio','break','domain','emphasis','mark','paragraph','phoneme','prosody','punctuation','header','say','speak','sub','voice','lang']:
        for i  in ['break']:
            print  'tagmode=s3ml,style:',i
            if str(i)=="backaudio":
 
                file=open("../Data/TestData/case126_s3_backaudio.txt","rb").read()
            elif str(i)=="break":   
                file=open("../Data/TestData/case126_s3_break.txt","rb").read()
            elif str(i)=="domain": 
                file=open("../Data/TestData/case126_s3_domain.txt","rb").read() 
            elif str(i)=="emphasis": 
                file=open("../Data/TestData/case126_s3_emphasis.txt","rb").read()                
            elif str(i)=="mark": 
                file=open("../Data/TestData/case126_s3_mark.txt","rb").read()                
            elif str(i)=="paragraph": 
                file=open("../Data/TestData/case126_s3_paragraph.txt","rb").read()
            elif str(i)=="phoneme": 
                file=open("../Data/TestData/case126_s3_phoneme.txt","rb").read()
            elif str(i)=="prosody": 
                file=open("../Data/TestData/case126_s3_prosody.txt","rb").read()                
            elif str(i)=="punctuation": 
                file=open("../Data/TestData/case126_s3_punctuation.txt","rb").read() 
            elif str(i)=="header": 
                file=open("../Data/TestData/case126_s3_header.txt","rb").read()                
            elif str(i)=="say": 
                file=open("../Data/TestData/case126_s3_say.txt","rb").read()
            elif str(i)=="speak": 
                file=open("../Data/TestData/case126_s3_speak.txt","rb").read()
            elif str(i)=="sub": 
                file=open("../Data/TestData/case126_s3_sub.txt","rb").read()                                                
            elif str(i)=="voice": 
                file=open("../Data/TestData/case126_s3_voice.txt","rb").read()                
            elif str(i)=="lang": 
                file=open("../Data/TestData/case126_s3_sublang.txt","rb").read()                                                                                                 
            body=file
            print len(body)
            voice,xml,resCode,resMessage = tts_post(APPKEY, DEVKEY,config, body,)
            with open(TEST_RESULT+'s3ml'+str(i)+'_tagmode_'+'testTTSfunctioncase126_s3ml_16K16bit.pcm','wb') as v_file:
                v_file.write(voice)
            self.assertEqual(resCode, "Success")
            self.assertEqual(resMessage, "Success")
        config = "capkey=tts.cloud.synth,property=cn_wangjing_common,tagmode=auto"   
        file=open("../Data/TestData/case126_s3_lang.txt","rb").read() 
        body=file
        voice,xml,resCode,resMessage = tts_post(APPKEY, DEVKEY,config, body,)
        with open(TEST_RESULT+'auto'+'_tagmode_'+'testTTSfunctioncase126_16K16bit.pcm','wb') as v_file:
            v_file.write(voice)
        self.assertEqual(resCode, "Success")
        self.assertEqual(resMessage, "Success")
        pass



#####################
#     def testTTSfunctioncase21214(self): #tagmode设置方式 vtml 宝维音库,本次测试不涉及
#         ''''2.1.2.14 检测http头中task-config中tagmode=s3ml标注处理方式,调用合成请求协议的情况'''
#         config = "capkey=tts.cloud.synth,property=cn_wangjing_common,tagmode=vtml"
#         file=open("../Data/TestData/case127_vt.txt","rb").read()                                                                                                         
#         body=file
#         voice,xml,resCode,resMessage = tts_post(APPKEY, DEVKEY,config, body,)
#         with open(TEST_RESULT+'vtml'+'_tagmode_'+'testTTSfunctioncase127_vtml_16K16bit.pcm','wb') as v_file:
#             v_file.write(voice)
#         self.assertEqual(resCode, "Success")
#         self.assertEqual(resMessage, "Success")
#         pass

#     def testTTSfunctioncase21215(self): #ssml设置方式 vtml 宝维音库,本次测试不涉及 ,测试时请编辑测试数据为ssml标记文件
#         ''''2.1.2.15 检测http头中task-config中tagmode=ssml标注处理方式,调用合成请求协议的情况'''
#         config = "capkey=tts.cloud.synth,property=cn_wangjing_common,tagmode=ssml"
#         file=open("../Data/TestData/case128_ss.txt","rb").read()                                                                                                         
#         body=file
#         voice,xml,resCode,resMessage = tts_post(APPKEY, DEVKEY,config, body,)
#         with open(TEST_RESULT+'vtml'+'_tagmode_'+'testTTSfunctioncase128_ssml_16K16bit.pcm','wb') as v_file:
#             v_file.write(voice)
#         self.assertEqual(resCode, "Success")
#         self.assertEqual(resMessage, "Success")
#         pass

    def testTTSfunctioncase21216(self): 
        ''''2.1.2.16 检测http头中task-config中voicestyle朗读风格方式,调用合成请求协议的情况'''
        for i  in ['normal','plain','clear','vivid']:
            config = "capkey=tts.cloud.synth,property=cn_wangjing_common,voicestyle="+str(i)
            file=open("../Data/TestData/case129.txt","rb").read()                                                                                                         
            body=file
            voice,xml,resCode,resMessage = tts_post(APPKEY, DEVKEY,config, body,)
            with open(TEST_RESULT+str(i)+'_voicestyle_'+'testTTSfunctioncase129_16K16bit.pcm','wb') as v_file:
                v_file.write(voice)
            self.assertEqual(resCode, "Success")
            self.assertEqual(resMessage, "Success")
        pass

    def testTTSfunctioncase21217(self): 
        ''''2.1.2.17 检测http头中task-config中audioformat音频格式方式,调用合成请求协议的情况'''
        for i  in ['auto','vox6k4bit','vox8k4bit','alaw8k8bit','ulaw8k8bit','pcm8k8bit','pcm8k16bit','pcm16k8bit','pcm16k16bit','pcm11k8bit','pcm11k16bit','mp3','mp3_24','mp3_16']:
            config = "capkey=tts.cloud.synth,property=cn_wangjing_common,audioformat="+str(i)
            file=open("../Data/TestData/case129.txt","rb").read()                                                                                                         
            body=file
            voice,xml,resCode,resMessage = tts_post(APPKEY, DEVKEY,config, body,)
            with open(TEST_RESULT+str(i)+'_audioformat_'+'testTTSfunctioncase130.pcm','wb') as v_file:
                v_file.write(voice)
            self.assertEqual(resCode, "Success")
            self.assertEqual(resMessage, "Success")
        pass

    def testTTSfunctioncase21218(self): 
        ''''2.1.2.18 检测http头中task-config中audioformat音频格式方式,调用合成请求协议的情况'''
        config = "capkey=tts.cloud.synth,property=cn_wangjing_common"
#         file=open("../Data/TestData/case129.txt","rb").read()                                                                                                         
        body=file
        body="12345678就是乘客我现在把乘客送到了刚才手机关机了现在关机了现在就是这个费用现在降不下来怎么办手机关机了现在就是这个费用现在降不下来怎么办手就是乘客我现在把乘客送到了刚才手机关机了现在就是这个费用现在降不下来怎么办手机关机了现在就是这个费用现在降不下来怎么办手机关机了现在就是这个费用现在降不下来怎么办手机关机了现在就是这个费用现在降不下来怎么办手就是乘客我现在把乘客送到了刚才手机关机了现在就是这个费用现在降不下来怎么办手机关机了现在就是这个费用现在降不下来怎么办手机关机了现在就是这个费用现在降不下来怎么办手机关机了现在就是这个费用现在降不下来怎么办手就是乘客我现在把乘客送到了刚才手机关机了现在就是这个费用现在降不下来怎么办手机关机了现在就是这个费用现在降不下来怎么办手机关机了现在就是这个费用现在降不下来怎么办手机关机了现在就是这个费用现在降不下来怎么办手就是乘客我现在把乘客送到了刚才手机关机了现在就是这个费用现在降不下来怎么办手机关机了现在就是这个费用现在降不下来怎么办手机关机了现在就是这个费用现在降不下来怎么办手机关机了现在就是这个费用现在降不下来怎么办手就是乘客我现在把乘客送到了刚才手机关机了现在就是这个费用现在降不下来怎么办手机关机了现在就是这个费用现在降不下来怎么办手机关机了现在就是这个费用现在降不下来怎么办手机关机了现在就是这个费用现在降不下来怎么办手机关机了现在就是这个费用现在降不下来怎么办手机关机了现在就是这个费用现在降不下来怎么办就是乘客我现在把乘客送到了刚才手机关机了现在就是这个费用现在降不下来怎么办手机关机了现在就是这个费用现在降不下来怎么办手机关机了现在就是这个费用现在降不下来怎么办手机关机了现在就是这个费用现在降不下来怎么办手就是乘客我现在把乘客送到了刚才手机关机了现在就是这个费用现在降不下来怎么办手机关机了现在就是这个费用现在降不下来怎么办手机关机了现在就是这个费用现在降不下来怎么办手机关机了现在就是这个费用现在降不下来怎么办手就是乘客我现在把乘客送到了刚才手机关机了现在就是这个费用现在降不下来怎么办手机关机了现在就是这个费用现在降不下来怎么办手机关机了现在就是这个费用现在降不下来怎么办手机关机了现在就是这个费用现在降不下来怎么办手就是乘客我现在把乘客送到了刚才手机关机了现在就是这个费用现在降不下来怎么办手机关机了现在就是这个费用现在降不下来怎么办手机关机了现在就是这个费用现在降不下来怎么办手机关机了现在就是这个费用现在降不下来怎么办手就是乘客我现在把乘客送到了刚才手机关机了现在就是这个费用现在降不下来怎么办手机关机了现在就是这个费用现在降不下来怎么办手机关机了现在就是这个费用现在降不下来怎么办手机关机了现在就是这个费用现在降不下来怎么办手就是乘客我现在把乘客送到了刚才手机关机了现在就是这个费用现在降不下来怎么办手机关机了现在就是这个费用现在降不下来怎么办手机关机了现在就是这个费用现在降不下来怎么办手机关机了现在就是这个费用现在降不下来怎么办手机关机了现在就是这个费用现在降不下来怎么办手机关机了现在就是这个费用现在降不下来怎么办么办手机关机了现在就是这个费用现在降不下来怎么办手机关机了现在就是这个费用现在降不下来怎么办手机关机了现在就是这个费用现在降不下来怎么办"
        print len(body)
        voice,xml,resCode,resMessage = tts_post(APPKEY, DEVKEY,config, body,)
        with open(TEST_RESULT+'audioformat_'+'testTTSfunctioncase21218.pcm','wb') as v_file:
            v_file.write(voice)
        self.assertEqual(resCode, "Failed")
        self.assertEqual(resMessage, "jtts audio data success, but audio data > 4096")
        pass



#########
    
    def testTTSfunctioncase2131(self):
        '''2.1.3.1 对SynthTextEx接口测试大于1024字节数据情况'''
        config = "capkey=tts.cloud.synth,property=cn_wangjing_common"
#         body = open(TEST_DATA + "1.txt", "r").read()
        body="就是乘客我现在把乘客送到了刚才手机关机了现在就是这个费用现在降不下来怎么办手机关机了现在就是这个费用现在降不下来怎么办手机关机了现在就是这个费用现在降不下来怎么办手机关机了现在就是这个费用现在降不下来怎么办手就是乘客我现在把乘客送到了刚才手机关机了现在就是这个费用现在降不下来怎么办手机关机了现在就是这个费用现在降不下来怎么办手机关机了现在就是这个费用现在降不下来怎么办手机关机了现在就是这个费用现在降不下来怎么办手就是乘客我现在把乘客送到了刚才手机关机了现在就是这个费用现在降不下来怎么办手机关机了现在就是这个费用现在降不下来怎么办手机关机了现在就是这个费用现在降不下来怎么办手机关机了现在就是这个费用现在降不下来怎么办手就是乘客我现在把乘客送到了刚才手机关机了现在就是这个费用现在降不下来怎么办手机关机了现在就是这个费用现在降不下来怎么办手机关机了现在就是这个费用现在降不下来怎么办手机关机了现在就是这个费用现在降不下来怎么办手就是乘客我现在把乘客送到了刚才手机关机了现在就是这个费用现在降不下来怎么办手机关机了现在就是这个费用现在降不下来怎么办手机关机了现在就是这个费用现在降不下来怎么办手机关机了现在就是这个费用现在降不下来怎么办手就是乘客我现在把乘客送到了刚才手机关机了现在就是这个费用现在降不下来怎么办手机关机了现在就是这个费用现在降不下来怎么办手机关机了现在就是这个费用现在降不下来怎么办手机关机了现在就是这个费用现在降不下来怎么办手机关机了现在就是这个费用现在降不下来怎么办手机关机了现在就是这个费用现在降不下来怎么办"
#         body="就是乘客我现在把乘客送到了刚才手机关机了现在就是这个费用现在降不下来怎么办手机关机了现在就是这个费,用现在降不下来怎么办手机关机了现在就是这个费用现在降不下来怎么办手机关机了现在就是这个"
        print len(body)
#         resCode,resMessage,response = tts_post(APPKEY, DEVKEY, URL,config, body,version,is_EX=True)
        voice,xml,resCode,resMessage = tts_postEx(APPKEY, DEVKEY,config, body,)
        with open(TEST_RESULT+"1"+'testTTSfunctioncase1001_16K16bit.pcm','wb') as v_file:
                v_file.write(voice)
#         md5file=open(TEST_RESULT+"1"+'testTTSfunctioncase1001_16K16bit.pcm','rb').read()
                
        self.assertEqual(resCode, "Failed")
        self.assertEqual(resMessage, "jtTTS_GetSentencePos failed")
#         #检测不带Ex的接口
#         voice,xml,resCode,resMessage = tts_post(APPKEY, DEVKEY,config, body,)
#         with open(TEST_RESULT+"1"+'testTTSfunctioncase2131_2_16K16bit.pcm','wb') as v_file:
#                 v_file.write(voice)
#         md5file=open(TEST_RESULT+"1"+'testTTSfunctioncase2131_2_16K16bit.pcm','rb').read()
#                 
#         self.assertEqual(resCode, "Failed")
#         self.assertEqual(resMessage, "jtTTS_GetSentencePos failed")
#         body="就是乘客我现在把乘客送到了刚才手机关机了现在就是这个费用现在降不下来怎么办手机关机了现在就是你好费用"
#         voice,xml,resCode,resMessage = tts_postEx(APPKEY, DEVKEY,config, body,)
#         with open(TEST_RESULT+"1"+'testTTSfunctioncase10012_16K16bit.pcm','wb') as v_file:
#                 v_file.write(voice)
#         self.assertEqual(resCode, "Success")
#         self.assertEqual(resMessage, "Success")   
#         md5file2=open(TEST_RESULT+"1"+'testTTSfunctioncase10012_16K16bit.pcm','rb').read()      
#         self.assertEqual(hashlib.md5(md5file).hexdigest(), hashlib.md5(md5file2).hexdigest())
#         pass




############################暂不修改############################################

    def testTTSfunctioncase2140(self):#xiaokun音库多domain
        ''''2.1.4.0 检测设置能力为tts.cloud.xiaokun时，设置不同的domain的值的情况'''
        domain=['common','finance','weather','queue','insurance','voyage','revenue','elecpower','message',]
        for i in domain:
            print i
            config = "capkey=tts.cloud.synth,property=cn_xiaokun_"+i
            file=open("../Data/TestData/case1.txt","rb").read()
            body=file
    #         if len(body)<=1024:
            voice,xml,resCode,resMessage = tts_postEx(APPKEY, DEVKEY,config, body,)
            v_file=open(TEST_RESULT+str(i)+'testTTSfunctioncase2140_16K16bit.pcm','wb')
            if voice!=None:
                v_file.write(voice)
            self.assertEqual(resCode, "Success")
            self.assertEqual(resMessage, "Success")
        pass

    def testTTSfunctioncase2141(self):
        '''2.1.4.1 检测http头中task-config中能力字段为不存在的能力，调用合成请求协议的情况'''
        config = ["capkey=tts.cloud.test,property=cn_xiaokun_common",
                  "capkey=abc123!@#,property=cn_xiaokun_common",
                  "",
                  "property=cn_xiaokun_common",                  
                  ]
        file=open("../Data/TestData/case1.txt","rb").read()
        body=file        
        for i  in config:
            voice,xml,resCode,resMessage = tts_postEx(APPKEY, DEVKEY,i, body,)
            with open(TEST_RESULT+'testTTSfunctioncase2141_16K16bit.pcm','wb') as v_file:
                v_file.write(voice)
            self.assertEqual(resCode, "Failed")
            self.assertEqual(resMessage, "CommitRequest jetcl_commit_request failed")
            pass

    def testTTSfunctioncase2142(self):
        ''''2.1.4.2 检测http头中task-config中pitch基频1-10和min、max字段同时验证min=o和max=10，等于5时和不填写pitch的MD5值调用合成请求协议的情况'''
        for i in ['0','1','2','3','4','5','6','7','8','9','9.7','10',]:
            config = "capkey=tts.cloud.synth,property=cn_xiaokun_common,pitch="+str(i)
            file=open("../Data/TestData/case1.txt","rb").read()
            body=file
            voice,xml,resCode,resMessage = tts_postEx(APPKEY, DEVKEY,config, body,)
            with open(TEST_RESULT+str(i)+'_pitch_'+'testTTSfunctioncase2142_16K16bit.pcm','wb') as v_file:
                v_file.write(voice)
            self.assertEqual(resCode, "Success")
            self.assertEqual(resMessage, "Success")            

        for i  in ['min','max']:
            config = "capkey=tts.cloud.synth,property=cn_xiaokun_common,pitch="+str(i)
            file=open("../Data/TestData/case1.txt","rb").read()
            body=file
            voice,xml,resCode,resMessage = tts_postEx(APPKEY, DEVKEY,config, body,)
            with open(TEST_RESULT+str(i)+'_pitch_'+'testTTSfunctioncase2142_16K16bit.pcm','wb') as v_file:
                v_file.write(voice)
            self.assertEqual(resCode, "Success")
            self.assertEqual(resMessage, "Success")
        md5file=open(TEST_RESULT+'10'+'_pitch_'+'testTTSfunctioncase2142_16K16bit.pcm',"rb").read()
        md5file2=open(TEST_RESULT+'max'+'_pitch_'+'testTTSfunctioncase2142_16K16bit.pcm',"rb").read()
        md5file3=open(TEST_RESULT+'0'+'_pitch_'+'testTTSfunctioncase2142_16K16bit.pcm',"rb").read()
        md5file4=open(TEST_RESULT+'min'+'_pitch_'+'testTTSfunctioncase2142_16K16bit.pcm',"rb").read()
        md5file5=open(TEST_RESULT+'5'+'_pitch_'+'testTTSfunctioncase2142_16K16bit.pcm',"rb").read()
        md5file6=open(TEST_RESULT+'common'+'testTTSfunctioncase2140_16K16bit.pcm',"rb").read()      
        self.assertEqual(hashlib.md5(md5file).hexdigest(), hashlib.md5(md5file2).hexdigest())
        self.assertEqual(hashlib.md5(md5file3).hexdigest(), hashlib.md5(md5file4).hexdigest())
        self.assertEqual(hashlib.md5(md5file5).hexdigest(), hashlib.md5(md5file6).hexdigest())   
        pass
    
    def testTTSfunctioncase2143(self):
        ''''2.1.4.3 检测http头中task-config中pitch基频在0，11，负数，字段调用合成请求协议的情况'''
        for i in [11,-10]:
            config = "capkey=tts.cloud.synth,property=cn_xiaokun_common,pitch="+str(i)
            file=open("../Data/TestData/case1.txt","rb").read()
            body=file
            voice,xml,resCode,resMessage = tts_postEx(APPKEY, DEVKEY,config, body,)
            v_file=open(TEST_RESULT+str(i)+'_pitch_'+'testTTSfunctioncase2143_16K16bit.pcm','wb')
            if voice!=None:
                v_file.write(voice)
            self.assertEqual(resCode, "Failed")
            self.assertEqual(resMessage, "ParseTtsParams failed")
        pass
    def testTTSfunctioncase2144(self):
        ''''2.1.4.4 检测http头中task-config中volume基频在1-10和min、max字段同时验证min=o和max=10 volume=5和不填写volume的MD5调用合成请求协议的情况'''
        for i in ['0','1','2','3','4','5','6','7','8','9','9.7','10',]:
            config = "capkey=tts.cloud.synth,property=cn_xiaokun_common,volume="+str(i)
            file=open("../Data/TestData/case1.txt","rb").read()
            body=file
            voice,xml,resCode,resMessage = tts_postEx(APPKEY, DEVKEY,config, body,)
            v_file=open(TEST_RESULT+str(i)+'_volume_'+'testTTSfunctioncase2144_16K16bit.pcm','wb')
            if voice!=None:
                v_file.write(voice)
            self.assertEqual(resCode, "Success")
            self.assertEqual(resMessage, "Success")
        for i  in ['min','max']:
            config = "capkey=tts.cloud.synth,property=cn_xiaokun_common,volume="+str(i)
            file=open("../Data/TestData/case1.txt","rb").read()
            body=file
            voice,xml,resCode,resMessage = tts_postEx(APPKEY, DEVKEY,config, body,)
#             v_file=open(TEST_RESULT+str(i)+'_pitch_'+'testTTSfunctioncase116_16K16bit.pcm','wb')
            with open(TEST_RESULT+str(i)+'_volume_'+'testTTSfunctioncase2144_16K16bit.pcm','wb') as v_file:
                v_file.write(voice)
            self.assertEqual(resCode, "Success")
            self.assertEqual(resMessage, "Success")                    
        md5file=open(TEST_RESULT+'10'+'_volume_'+'testTTSfunctioncase2144_16K16bit.pcm',"rb").read()
        md5file2=open(TEST_RESULT+'max'+'_volume_'+'testTTSfunctioncase2144_16K16bit.pcm',"rb").read()
        md5file3=open(TEST_RESULT+'0'+'_volume_'+'testTTSfunctioncase2144_16K16bit.pcm',"rb").read()
        md5file4=open(TEST_RESULT+'min'+'_volume_'+'testTTSfunctioncase2144_16K16bit.pcm',"rb").read()
        md5file5=open(TEST_RESULT+'5'+'_volume_'+'testTTSfunctioncase2144_16K16bit.pcm',"rb").read()
        md5file6=open(TEST_RESULT+'common'+'testTTSfunctioncase2140_16K16bit.pcm',"rb").read()      
        self.assertEqual(hashlib.md5(md5file).hexdigest(), hashlib.md5(md5file2).hexdigest())
        self.assertEqual(hashlib.md5(md5file3).hexdigest(), hashlib.md5(md5file4).hexdigest())
        self.assertEqual(hashlib.md5(md5file5).hexdigest(), hashlib.md5(md5file6).hexdigest())
        pass
    def testTTSfunctioncase2145(self):
        ''''2.1.4.5 检测http头中task-config中speed语速在1-10和min、max字段同时验证min=o和max=10的MD5调用合成请求协议的情况'''
        for i in ['0','1','2','3','4','5','6','7','8','9','9.7','10',]:
            config = "capkey=tts.cloud.synth,property=cn_xiaokun_common,speed="+str(i)
            file=open("../Data/TestData/case1.txt","rb").read()
            body=file
            voice,xml,resCode,resMessage = tts_postEx(APPKEY, DEVKEY,config, body,)
            with open(TEST_RESULT+str(i)+'_pitch_'+'testTTSfunctioncase2145_16K16bit.pcm','wb') as v_file:
                v_file.write(voice)
            self.assertEqual(resCode, "Success")
            self.assertEqual(resMessage, "Success")
        for i  in ['min','max']:
            config = "capkey=tts.cloud.synth,property=cn_xiaokun_common,speed="+str(i)
            file=open("../Data/TestData/case1.txt","rb").read()
            body=file
            voice,xml,resCode,resMessage = tts_postEx(APPKEY, DEVKEY,config, body,)
#             v_file=open(TEST_RESULT+str(i)+'_pitch_'+'testTTSfunctioncase116_16K16bit.pcm','wb')
            with open(TEST_RESULT+str(i)+'_pitch_'+'testTTSfunctioncase2145_16K16bit.pcm','wb') as v_file:
                v_file.write(voice) 
            self.assertEqual(resCode, "Success")
            self.assertEqual(resMessage, "Success")               
        md5file=open(TEST_RESULT+'10'+'_pitch_'+'testTTSfunctioncase2145_16K16bit.pcm',"rb").read()
        md5file2=open(TEST_RESULT+'max'+'_pitch_'+'testTTSfunctioncase2145_16K16bit.pcm',"rb").read()
        md5file3=open(TEST_RESULT+'0'+'_pitch_'+'testTTSfunctioncase2145_16K16bit.pcm',"rb").read()
        md5file4=open(TEST_RESULT+'min'+'_pitch_'+'testTTSfunctioncase2145_16K16bit.pcm',"rb").read()
        md5file5=open(TEST_RESULT+'5'+'_pitch_'+'testTTSfunctioncase2145_16K16bit.pcm',"rb").read()
        md5file6=open(TEST_RESULT+'common'+'testTTSfunctioncase2140_16K16bit.pcm',"rb").read()
        self.assertEqual(hashlib.md5(md5file).hexdigest(), hashlib.md5(md5file2).hexdigest())
        self.assertEqual(hashlib.md5(md5file3).hexdigest(), hashlib.md5(md5file4).hexdigest())
        self.assertEqual(hashlib.md5(md5file5).hexdigest(), hashlib.md5(md5file6).hexdigest())

        pass
    def testTTSfunctioncase2146(self):
        ''''2.1.4.6 检测http头中task-config中volume基频在11，负数，字段调用合成请求协议的情况'''
        for i in [11,-10]:
            config = "capkey=tts.cloud.synth,property=cn_xiaokun_common,volume="+str(i)
            file=open("../Data/TestData/case1.txt","rb").read()
            body=file
            voice,xml,resCode,resMessage = tts_postEx(APPKEY, DEVKEY,config, body,)
            with open(TEST_RESULT+str(i)+'_volume_'+'testTTSfunctioncase2146_16K16bit.pcm','wb') as v_file:
                v_file.write(voice)
            self.assertEqual(resCode, "Failed")
            self.assertEqual(resMessage, "ParseTtsParams failed")
        pass
    def testTTSfunctioncase2147(self):
        ''''2.1.2.6 检测http头中task-config中speed基频在0，11，负数，字段调用合成请求协议的情况'''
        for i in [11,-10]:
            config = "capkey=tts.cloud.synth,property=cn_xiaokun_common,speed="+str(i)
            file=open("../Data/TestData/case1.txt","rb").read()
            body=file
            voice,xml,resCode,resMessage = tts_postEx(APPKEY, DEVKEY,config, body,)
            v_file=open(TEST_RESULT+str(i)+'_speed_'+'testTTSfunctioncase2147_16K16bit.pcm','wb')
            if voice!=None:
                v_file.write(voice)
            self.assertEqual(resCode, "Failed")
            self.assertEqual(resMessage, "ParseTtsParams failed")
        pass

    def testTTSfunctioncase2148(self):
        ''''2.1.4.8 检测http头中task-config中puncmode为off能否合成功且无回车符或换行的MD5调用合成请求协议的情况'''
#         for i in ['off','on','off_rtn','on_rtn',]:
        #回车符号
        #off不合成标点符号，自动判断回车换行是否分隔符，缺省值,不读回车换行符
        config = "capkey=tts.cloud.synth,property=cn_xiaokun_common,puncmode=off"
        file=open("../Data/TestData/case120.txt","rb").read()
        body=file
        voice,xml,resCode,resMessage = tts_postEx(APPKEY, DEVKEY,config, body,)
        with open(TEST_RESULT+'off'+'_puncmode_'+'testTTSfunctioncase2148_16K16bit.pcm','wb') as v_file:
            v_file.write(voice)
        self.assertEqual(resCode, "Success")
        self.assertEqual(resMessage, "Success")
        md5file=open(TEST_RESULT+'off'+'_puncmode_'+'testTTSfunctioncase2148_16K16bit.pcm',"rb").read()
        file=open("../Data/TestData/case120_hc.txt","rb").read()
        voice,xml,resCode,resMessage = tts_postEx(APPKEY, DEVKEY,config, file,)
        with open(TEST_RESULT+"off"+'_puncmode_'+'testTTSfunctioncase2148_hc_16K16bit.pcm','wb') as v_file:
                v_file.write(voice)
        self.assertEqual(resCode, "Success")
        self.assertEqual(resMessage, "Success")                
        md5file2=open(TEST_RESULT+'off'+'_puncmode_'+'testTTSfunctioncase2148_hc_16K16bit.pcm',"rb").read()
        ##换行符比较
        file=open("../Data/TestData/case1201.txt","rb").read()
        body=file
        voice,xml,resCode,resMessage = tts_postEx(APPKEY, DEVKEY,config, body,)
        with open(TEST_RESULT+'off'+'_puncmode_'+'testTTSfunctioncase2148_16K16bit.pcm','wb') as v_file:
            v_file.write(voice)
        self.assertEqual(resCode, "Success")
        self.assertEqual(resMessage, "Success")            
        md5file3=open(TEST_RESULT+'off'+'_puncmode_'+'testTTSfunctioncase2148_16K16bit.pcm',"rb").read()
        file=open("../Data/TestData/case1201_hh.txt","rb").read()
        voice,xml,resCode,resMessage = tts_postEx(APPKEY, DEVKEY,config, file,)
        with open(TEST_RESULT+"off"+'_puncmode_'+'testTTSfunctioncase2148_hh_16K16bit.pcm','wb') as v_file:
                v_file.write(voice)        
        self.assertEqual(resCode, "Success")
        self.assertEqual(resMessage, "Success")

        md5file4=open(TEST_RESULT+'off'+'_puncmode_'+'testTTSfunctioncase2148_hh_16K16bit.pcm',"rb").read()    
        self.assertEqual(hashlib.md5(md5file).hexdigest(), hashlib.md5(md5file2).hexdigest())
        self.assertEqual(hashlib.md5(md5file3).hexdigest(), hashlib.md5(md5file4).hexdigest())
        pass
    
    def testTTSfunctioncase2149(self):
        ''''2.1.4.9检测http头中task-config中puncmode为on、能否合成功且有无回车符的MD5调用合成请求协议的情况'''
#         for i in ['off','on','off_rtn','on_rtn',]:
        #回车符MD5值比较
        config = "capkey=tts.cloud.synth,property=cn_xiaokun_common,puncmode=on"
        file=open("../Data/TestData/case121.txt","rb").read()
        body=file
        voice,xml,resCode,resMessage = tts_postEx(APPKEY, DEVKEY,config, body,)
        with open(TEST_RESULT+'on'+'_puncmode_'+'testTTSfunctioncase2149_16K16bit.pcm','wb') as v_file:
            v_file.write(voice)        
        self.assertEqual(resCode, "Success")
        self.assertEqual(resMessage, "Success")
        md5file=open(TEST_RESULT+'on'+'_puncmode_'+'testTTSfunctioncase2149_16K16bit.pcm',"rb").read()
        config = "capkey=tts.cloud.synth,property=cn_xiaokun_common,puncmode=on"
        file=open("../Data/TestData/case121_hc.txt","rb").read()
        voice,xml,resCode,resMessage = tts_postEx(APPKEY, DEVKEY,config, file,)
        with open(TEST_RESULT+"on"+'_puncmode_'+'testTTSfunctioncase2149_hc_16K16bit.pcm','wb') as v_file:
                v_file.write(voice)        
        self.assertEqual(resCode, "Success")
        self.assertEqual(resMessage, "Success")
        with open(TEST_RESULT+"on"+'_puncmode_'+'testTTSfunctioncase2149_hc_16K16bit.pcm','wb') as v_file:
                v_file.write(voice)
        md5file2=open(TEST_RESULT+'on'+'_puncmode_'+'testTTSfunctioncase2149_hc_16K16bit.pcm',"rb").read()
             
        self.assertEqual(hashlib.md5(md5file).hexdigest(), hashlib.md5(md5file2).hexdigest())
        pass

    def testTTSfunctioncase21410(self):
        ''''2.1.4.10 检测http头中task-config中puncmode为off_rtn能否合成功、回车和换行结果对比,调用合成请求协议的情况'''
#         for i in ['off','on','off_rtn','on_rtn',]:
        #回车符  
        #off_rtn不读符号，强制将回车换行作为分隔符 
        config = "capkey=tts.cloud.synth,property=cn_xiaokun_common,puncmode=off_rtn"
        file=open("../Data/TestData/case120.txt","rb").read()
        body=file
        voice,xml,resCode,resMessage = tts_postEx(APPKEY, DEVKEY,config, body,)
        with open(TEST_RESULT+'off_rtn'+'_puncmode_'+'testTTSfunctioncase21410_16K16bit.pcm','wb') as v_file:
            v_file.write(voice)
        md5file=open(TEST_RESULT+'off_rtn'+'_puncmode_'+'testTTSfunctioncase21410_16K16bit.pcm',"rb").read()
#         config = "capkey=tts.cloud.synth,property=cn_wangjing_common,puncmode=off_rtn"
#         file=open("../Data/TestData/case120_hc.txt","rb").read()
#         voice,xml,resCode,resMessage = tts_post(APPKEY, DEVKEY,config, file,)
#         with open(TEST_RESULT+"off_rtn"+'_puncmode_'+'testTTSfunctioncase122_hc_16K16bit.pcm','wb') as v_file:
#                 v_file.write(voice)
#         md5file2=open(TEST_RESULT+'off_rtn'+'_puncmode_'+'testTTSfunctioncase122_hc_16K16bit.pcm',"rb").read()
        #换行符
        self.assertEqual(resCode, "Success")
        self.assertEqual(resMessage, "Success")
        file=open("../Data/TestData/case1201.txt","rb").read()  #使用的测试数据和120case相同
        body=file
        voice,xml,resCode,resMessage = tts_postEx(APPKEY, DEVKEY,config, body,)
        with open(TEST_RESULT+'off_rtn'+'_puncmode_'+'testTTSfunctioncase21410_16K16bit.pcm','wb') as v_file:
            v_file.write(voice)
        md5file3=open(TEST_RESULT+'off_rtn'+'_puncmode_'+'testTTSfunctioncase21410_16K16bit.pcm',"rb").read()
#         file=open("../Data/TestData/case1201_hh.txt","rb").read()
#         voice,xml,resCode,resMessage = tts_post(APPKEY, DEVKEY,config, file,)
#         with open(TEST_RESULT+"off_rtn"+'_pitch_'+'testTTSfunctioncase1221_hh_16K16bit.pcm','wb') as v_file:
#                 v_file.write(voice)        
#         md5file4=open(TEST_RESULT+'off_rtn'+'_pitch_'+'testTTSfunctioncase1221_hh_16K16bit.pcm',"rb").read()
#        不读符号，强制将回车换行作为分隔符 ,所以比较两者的MD5值是否一致性
        self.assertEqual(hashlib.md5(md5file).hexdigest(), hashlib.md5(md5file3).hexdigest())
#         self.assertEqual(hashlib.md5(md5file3).hexdigest(), hashlib.md5(md5file4).hexdigest())
        pass

    def testTTSfunctioncase21411(self):
        ''''2.1.4.11 检测http头中task-config中puncmode为on_rtn能否合成功、回车和换行结果对比,调用合成请求协议的情况'''

        config = "capkey=tts.cloud.synth,property=cn_xiaokun_common,puncmode=on_rtn"
        file=open("../Data/TestData/case120.txt","rb").read()
        body=file
        voice,xml,resCode,resMessage = tts_postEx(APPKEY, DEVKEY,config, body,)
        with open(TEST_RESULT+'on_rtn'+'_puncmode_'+'testTTSfunctioncase21411_16K16bit.pcm','wb') as v_file:
            v_file.write(voice)
        self.assertEqual(resCode, "Success")
        self.assertEqual(resMessage, "Success")            
        md5file=open(TEST_RESULT+'on_rtn'+'_puncmode_'+'testTTSfunctioncase21411_16K16bit.pcm',"rb").read()
        file=open("../Data/TestData/case1201.txt","rb").read()  #使用的测试数据和120case相同
        body=file
        voice,xml,resCode,resMessage = tts_postEx(APPKEY, DEVKEY,config, body,)
        with open(TEST_RESULT+'on_rtn'+'_puncmode_'+'testTTSfunctioncase21411_16K16bit.pcm','wb') as v_file:
            v_file.write(voice)
        self.assertEqual(resCode, "Success")
        self.assertEqual(resMessage, "Success")            
        md5file3=open(TEST_RESULT+'on_rtn'+'_puncmode_'+'testTTSfunctioncase21411_16K16bit.pcm',"rb").read()
#         file=open("../Data/TestData/case1201_hh.txt","rb").read()
#         voice,xml,resCode,resMessage = tts_post(APPKEY, DEVKEY,config, file,)
#         with open(TEST_RESULT+"off_rtn"+'_pitch_'+'testTTSfunctioncase1221_hh_16K16bit.pcm','wb') as v_file:
#                 v_file.write(voice)        
#         md5file4=open(TEST_RESULT+'off_rtn'+'_pitch_'+'testTTSfunctioncase1221_hh_16K16bit.pcm',"rb").read()
#        不读符号，强制将回车换行作为分隔符 ,所以比较两者的MD5值是否一致性
        self.assertEqual(hashlib.md5(md5file).hexdigest(), hashlib.md5(md5file3).hexdigest())
#         self.assertEqual(hashlib.md5(md5file3).hexdigest(), hashlib.md5(md5file4).hexdigest())
        pass

    def testTTSfunctioncase21412(self):
        ''''2.1.4.12 检测http头中task-config中digitmode数字阅读方式,同时比对数字、电报的自动与不自动的MD5值调用合成请求协议的情况'''
        for i in ["auto_number","telegram","number","auto_telegram"]:
            config = "capkey=tts.cloud.synth,property=cn_xiaokun_common,digitmode="+str(i)
            file=open("../Data/TestData/case124.txt","rb").read()
            body=file
            voice,xml,resCode,resMessage = tts_postEx(APPKEY, DEVKEY,config, body,)
            with open(TEST_RESULT+str(i)+'_digitmode_'+'testTTSfunctioncase21412_16K16bit.pcm','wb') as v_file:
                v_file.write(voice)
            self.assertEqual(resCode, "Success")
            self.assertEqual(resMessage, "Success")
        md5file=open(TEST_RESULT+'auto_number'+'_digitmode_'+'testTTSfunctioncase21412_16K16bit.pcm',"rb").read()
        md5file2=open(TEST_RESULT+'number'+'_digitmode_'+'testTTSfunctioncase21412_16K16bit.pcm',"rb").read()
        md5file3=open(TEST_RESULT+'telegram'+'_digitmode_'+'testTTSfunctioncase21412_16K16bit.pcm',"rb").read()
        md5file4=open(TEST_RESULT+'auto_telegram'+'_digitmode_'+'testTTSfunctioncase21412_16K16bit.pcm',"rb").read()
        self.assertEqual(hashlib.md5(md5file).hexdigest(), hashlib.md5(md5file2).hexdigest())
        self.assertEqual(hashlib.md5(md5file3).hexdigest(), hashlib.md5(md5file4).hexdigest())         
       
        pass

    def testTTSfunctioncase21413(self):
        ''''2.1.4.13 检测http头中task-config中engmode英文阅读方式,同时对比auto和english返回结果的MD5值调用合成请求协议的情况'''
        for i in ["auto","english","letter"]:
            config = "capkey=tts.cloud.synth,property=cn_xiaokun_common,engmode="+str(i)
            file=open("../Data/TestData/case125.txt","rb").read()
            body=file
            voice,xml,resCode,resMessage = tts_postEx(APPKEY, DEVKEY,config, body,)
            with open(TEST_RESULT+str(i)+'_engmode_'+'testTTSfunctioncase21413_16K16bit.pcm','wb') as v_file:
                v_file.write(voice)
            self.assertEqual(resCode, "Success")
            self.assertEqual(resMessage, "Success")
        md5file=open(TEST_RESULT+'auto'+'_engmode_'+'testTTSfunctioncase21413_16K16bit.pcm',"rb").read()
        md5file2=open(TEST_RESULT+'english'+'_engmode_'+'testTTSfunctioncase21413_16K16bit.pcm',"rb").read()
        md5file3=open(TEST_RESULT+'letter'+'_engmode_'+'testTTSfunctioncase21413_16K16bit.pcm',"rb").read()
#         md5file4=open(TEST_RESULT+'auto_telegram'+'_digitmode_'+'testTTSfunctioncase124_16K16bit.pcm',"rb").read()
        self.assertEqual(hashlib.md5(md5file).hexdigest(), hashlib.md5(md5file2).hexdigest())
#         self.assertEqual(hashlib.md5(md5file3).hexdigest(), hashlib.md5(md5file4).hexdigest())         
        config = "capkey=tts.cloud.synth,property=cn_xiaokun_common,engmode=auto"
        file=open("../Data/TestData/case1251.txt","rb").read()
        body=file
        voice,xml,resCode,resMessage = tts_postEx(APPKEY, DEVKEY,config, body,)
        with open(TEST_RESULT+'4auto'+'_engmode_'+'testTTSfunctioncase21413_16K16bit.pcm','wb') as v_file:
            v_file.write(voice)
        self.assertEqual(resCode, "Success")
        self.assertEqual(resMessage, "Success")
        md5file4=open(TEST_RESULT+'4auto'+'_engmode_'+'testTTSfunctioncase21413_16K16bit.pcm',"rb").read()
        self.assertEqual(hashlib.md5(md5file3).hexdigest(), hashlib.md5(md5file4).hexdigest())
#         config = "capkey=tts.cloud.synth,property=cn_wangjing_common,digitmode=number"
#         body="一千"
#         voice,xml,resCode,resMessage = tts_post(APPKEY, DEVKEY,config, body,)
#         with open(TEST_RESULT+'一千'+'_digitmode_'+'testTTSfunctioncase124_16K16bit.pcm','wb') as v_file:
#             v_file.write(voice)
#         md5file5=open(TEST_RESULT+'一千'+'_digitmode_'+'testTTSfunctioncase124_16K16bit.pcm',"rb").read()
#         self.assertEqual(hashlib.md5(md5file5).hexdigest(), hashlib.md5(md5file2).hexdigest())        
        pass

    def testTTSfunctioncase21414(self): #tagmode设置方式
        ''''2.1.4.14检测http头中task-config中tagmode=auto、s3ml标注处理方式,调用合成请求协议的情况'''
        config = "capkey=tts.cloud.synth,property=cn_xiaokun_common,tagmode=s3ml"
        for i  in ['backaudio','break','domain','emphasis','mark','paragraph','phoneme','prosody','punctuation','header','say','speak','sub','voice','lang']:
            print  'tagmode=s3ml,style:',i
            if str(i)=="backaudio":
 
                file=open("../Data/TestData/case126_s3_backaudio.txt","rb").read()
            elif str(i)=="break":   
                file=open("../Data/TestData/case126_s3_break.txt","rb").read()
            elif str(i)=="domain": 
                file=open("../Data/TestData/case126_s3_domain.txt","rb").read() 
            elif str(i)=="emphasis": 
                file=open("../Data/TestData/case126_s3_emphasis.txt","rb").read()                
            elif str(i)=="mark": 
                file=open("../Data/TestData/case126_s3_mark.txt","rb").read()                
            elif str(i)=="paragraph": 
                file=open("../Data/TestData/case126_s3_paragraph.txt","rb").read()
            elif str(i)=="phoneme": 
                file=open("../Data/TestData/case126_s3_phoneme.txt","rb").read()
            elif str(i)=="prosody": 
                file=open("../Data/TestData/case126_s3_prosody.txt","rb").read()                
            elif str(i)=="punctuation": 
                file=open("../Data/TestData/case126_s3_punctuation.txt","rb").read() 
            elif str(i)=="header": 
                file=open("../Data/TestData/case126_s3_header.txt","rb").read()                
            elif str(i)=="say": 
                file=open("../Data/TestData/case126_s3_say.txt","rb").read()
            elif str(i)=="speak": 
                file=open("../Data/TestData/case126_s3_speak.txt","rb").read()
            elif str(i)=="sub": 
                file=open("../Data/TestData/case126_s3_sub.txt","rb").read()                                                
            elif str(i)=="voice": 
                file=open("../Data/TestData/case126_s3_voice.txt","rb").read()                
            elif str(i)=="lang": 
                file=open("../Data/TestData/case126_s3_lang.txt","rb").read()                                                                                                 
            body=file
            voice,xml,resCode,resMessage = tts_postEx(APPKEY, DEVKEY,config, body,)
            with open(TEST_RESULT+'s3ml'+str(i)+'_tagmode_'+'testTTSfunctioncase21414_s3ml_16K16bit.pcm','wb') as v_file:
                v_file.write(voice)
#             self.assertEqual(resCode, "Failed")
#             self.assertEqual(resMessage, "jtTTS_GetSentencePos failed")
        config = "capkey=tts.cloud.synth,property=cn_xiaokun_common,tagmode=auto"   
        file=open("../Data/TestData/case126_s3_lang.txt","rb").read() 
        body=file
        voice,xml,resCode,resMessage = tts_postEx(APPKEY, DEVKEY,config, body,)
        with open(TEST_RESULT+'auto'+'_tagmode_'+'testTTSfunctioncase21414_16K16bit.pcm','wb') as v_file:
            v_file.write(voice)
        self.assertEqual(resCode, "Success")
        self.assertEqual(resMessage, "Success")
        pass

#####################
#     def testTTSfunctioncase21415(self): #tagmode设置方式 vtml 宝维音库,本次测试不涉及
#         ''''2.1.4.15 检测http头中task-config中tagmode=s3ml标注处理方式,调用合成请求协议的情况'''
#         config = "capkey=tts.cloud.synth,property=cn_xiaokun_common,tagmode=vtml"
#         file=open("../Data/TestData/case127_vt.txt","rb").read()                                                                                                         
#         body=file
#         voice,xml,resCode,resMessage = tts_postEx(APPKEY, DEVKEY,config, body,)
#         with open(TEST_RESULT+'vtml'+'_tagmode_'+'testTTSfunctioncase127_vtml_16K16bit.pcm','wb') as v_file:
#             v_file.write(voice)
#         self.assertEqual(resCode, "Success")
#         self.assertEqual(resMessage, "Success")
#         pass

#     def testTTSfunctioncase21416(self): #ssml设置方式 vtml 宝维音库,本次测试不涉及 ,测试时请编辑测试数据为ssml标记文件
#         ''''2.1.4.16 检测http头中task-config中tagmode=ssml标注处理方式,调用合成请求协议的情况'''
#         config = "capkey=tts.cloud.synth,property=cn_xiaokun_common,tagmode=ssml"
#         file=open("../Data/TestData/case128_ss.txt","rb").read()                                                                                                         
#         body=file
#         voice,xml,resCode,resMessage = tts_postEx(APPKEY, DEVKEY,config, body,)
#         with open(TEST_RESULT+'vtml'+'_tagmode_'+'testTTSfunctioncase128_ssml_16K16bit.pcm','wb') as v_file:
#             v_file.write(voice)
#         self.assertEqual(resCode, "Success")
#         self.assertEqual(resMessage, "Success")
#         pass

    def testTTSfunctioncase21417(self): 
        ''''2.1.4.17 检测http头中task-config中voicestyle朗读风格方式,调用合成请求协议的情况'''
        for i  in ['normal','plain','clear','vivid']:
            config = "capkey=tts.cloud.synth,property=cn_xiaokun_common,voicestyle="+str(i)
            file=open("../Data/TestData/case129.txt","rb").read()                                                                                                         
            body=file
            voice,xml,resCode,resMessage = tts_postEx(APPKEY, DEVKEY,config, body,)
            with open(TEST_RESULT+str(i)+'_voicestyle_'+'testTTSfunctioncase21417_16K16bit.pcm','wb') as v_file:
                v_file.write(voice)
            self.assertEqual(resCode, "Success")
            self.assertEqual(resMessage, "Success")
        pass

    def testTTSfunctioncase21418(self): 
        ''''2.1.4.18 检测http头中task-config中audioformat音频格式方式,调用合成请求协议的情况'''
        for i  in ['auto','vox6k4bit','vox8k4bit','alaw8k8bit','ulaw8k8bit','pcm8k8bit','pcm8k16bit','pcm16k8bit','pcm16k16bit','pcm11k8bit','pcm11k16bit','mp3','mp3_24','mp3_16']:
            config = "capkey=tts.cloud.synth,property=cn_xiaokun_common,audioformat="+str(i)
            file=open("../Data/TestData/case129.txt","rb").read()                                                                                                         
            body=file
            voice,xml,resCode,resMessage = tts_postEx(APPKEY, DEVKEY,config, body,)
            with open(TEST_RESULT+str(i)+'_audioformat_'+'testTTSfunctioncase21417.pcm','wb') as v_file:
                v_file.write(voice)
            self.assertEqual(resCode, "Success")
            self.assertEqual(resMessage, "Success")
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
    print '【time interval is】:',time.time()-start_time
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
            xml_1111 = response_body[:response_body.find('</ResponseInfo>')]
            print "voice:"+ voice,"xml_1111:"+xml_1111
            xml_str = Etree.fromstring(xml) 
        if 'ResCode' in response_body:
            resCode = xml_str.find("ResCode").text
        if 'ResMessage' in response_body:
            resMessage=xml_str.find("ResMessage").text
        print xml
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
    print '【time interval is】:',time.time()-start_time
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
        return voice,xml,resCode,resMessage
    else: 
        print "#################failed#############"           
 


if __name__ == "__main__":
    import sys;sys.argv = ['', 'Test.testTTSfunctioncase111']
    unittest.main()