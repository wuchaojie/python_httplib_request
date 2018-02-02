#coding=utf-8
'''
Created on 2016-9-23

@author: libin
'''
import time
import json
import hashlib
import httplib
import xml.etree.ElementTree as ETree
from hci_http_func_kit.logger import Logger
from xml import etree



TEST_DATA = "../Data/TestData/"
TEST_RESULT = "../Data/TestResult/"
developer_key = "developer_key"
appkey = "ac5d5452"


class HttpHelper():
    '''
    For Hcicloud 8.x , send Http Request and analyze response
    '''
    
    def __init__(self, 
                 url = None, 
                 port = "8880", 
                 timeout = 3, 
                 method = "POST", 
                 http_path = None, 
                 head_model = None, 
                 logger = None, 
                 record_analyze_error = False
                 ):
        '''
        Constructor
        '''
        self._url = url
        self._port = port
        self._timeout = timeout
        self._method = method
        self._http_path = http_path
        self._record_analyze_error = record_analyze_error
        
        #set HTTP Head Model

            
        #set Logger
        if logger == None:
            self._logger = Logger("StressTest_"+str(time.strftime("%Y_%m_%d_%H_%M_%S"))+".log")
        else:
            self._logger = logger

            
            
    def do_request(self, config=None, body=None, url = None, port = None, timeout = None, method = None, http_path = None, head_model=None):
        '''
        发送HTTP请求 ,返回response,可设置单独设置 url,端口,超时时间,方法,http路径
        '''
        if url == None:
            url = self._url
        if port == None:
            port = self._port
        if timeout == None:
            timeout = self._timeout
        if method == None:
            method = self._method
        if http_path ==None:
            http_path = self._http_path
        
        headers = None
        a = HttpHeadModel()
        print  "post body is : " + body
        a.get_date_and_session_key()
        request_date, session_key = a.get_date_and_session_key()
        #_developer_key = 'developer_key'
        session_key = hashlib.md5(str(request_date) + developer_key).hexdigest()
        
        headers = {
               'x-app-key':appkey,
               'x-sdk-version':"3.8",
               'x-request-date':request_date,
               'x-task-config':config,
               #'x-udid':"101:1234567890",
               'x-udid':"101:1234567890",
               'x-session-key':session_key,
               #'Accept':self.get_accept()
                }
        json_str = json.dumps(headers)
        print json_str
        self._logger.debug(headers)
        response_body = "empty response"
        response_headers = {}
        try:
            start_time = time.time()
            httpClient = httplib.HTTPConnection(url,port,False,timeout)
            if headers is None:
                httpClient.request(method,http_path, body)
            else:
                httpClient.request(method,http_path, body, headers)
            response = httpClient.getresponse()
            end_time = time.time()
            post_time = end_time - start_time
            print  "post time is : " ,str(post_time),"(s)"
            response_headers = response.getheaders()
            response_body = response.read()
            
            ErrorNo =""
            resMessage=""
            if response.status==200:
                
                #xml_position=response_body.find('</ResponseInfo>')
                if response_body.find('</ResponseInfo>')!=-1:
                   
                    voice= response_body[response_body.find('</ResponseInfo>')+len('</ResponseInfo>'):]
                     
                    xml= response_body[:response_body.find('</ResponseInfo>')+len('</ResponseInfo>')]
                    xml_str = ETree.fromstring(xml)
                    self._logger.debug(xml)
                    #xml_str = Etree.fromstring() 
#                 if 'ResCode' in response_body:
#                     resCode = xml_str.find("ResCode").text
                if 'ErrorNo' in response_body:
                    ErrorNo = xml_str.find("ErrorNo").text
                if 'ResMessage' in response_body:
                    resMessage=xml_str.find("ResMessage").text
                #return voice,xml,ErrorNo,resMessage
                return voice,ErrorNo,resMessage
            else: 
                print "#################failed#############"
        except:  
                self._logger.error("wrong")

        

#解析http response
    def analyze_response(self, response, accept = None):
        '''
        提供一个接收accept类型的函数来调用返回结果解析功能
        '''
        if accept == None:
            if self._head_model == None:
                _accept = "application/json"
            else:
                try:
                    _accept = self._head_model.get_accept()
                except:
                    _accept = "application/json"
                    self._logger.error("get accept from head_model failed, analyze http response with default type \"application/json\"")
        else:
            _accept = accept
        if _accept == "application/xml":
            response_res = self.analyze_xml_response(response)
        elif _accept == "application/json":
            response_res = self.analyze_json_response(response)
        elif _accept == 'plain/text':
            response_res = self.analyze_text_response(response)
        else:
            raise Exception("\"Accept\" must be one of \"application/xml\" , \"application/json\" or \"plain/text\" , not \"" + str(_accept) + "\"")
        
        return response_res
    


    def analyze_xml_response(self, response):
        ret = {}
        try:
            root = ETree.fromstring(response)
        except:
            if self._record_analyze_error:
                self._logger.error("Response is not a standard XML format string")
        try:
            ret = walk(root)['ResponseInfo']
        except:
            if self._record_analyze_error:
                self._logger.error("Not Found \"ResponseInfo\" Node in xml response")
        #记录ResCode和ResMessage
        try:
            self._logger.info("ResCode: " + ret['ResCode'] + "\tResmMessage: " + ret['ResMessage'])
            print "ret is :" + ret
            ResCode = ret['ResCode']
            ResMessage = ret['ResMessage']
            voice = ret['ResMessage']
        except:
            if self._record_analyze_error:
                self._logger.error("Not Found \"ResCode\" Node or \"ResMessage\" Node in xml response")
        return ResCode,ResMessage,voice

    def analyze_json_response(self, response):
        '''
        将json格式的response解析为字典
        '''
        response_info = {}
        try:
            json_obj = json.loads(response, encoding='utf-8')
            response_info = json_obj['ResponseInfo']
            self._logger.info("ResCode: " + response_info["ResCode"] + "  ResMessage: " + response_info["ResMessage"])
            
            response_info['Token'] = json.dumps(response_info['Token'], encoding="UTF-8", ensure_ascii=False).replace("\"", "")
            response_info['Result'] = json.dumps(response_info['Result'], encoding="UTF-8", ensure_ascii=False)
            response_info['ResultCount'] = json.dumps(response_info['ResultCount'])           
        except Exception,ex:
            if self._record_analyze_error:
                self._logger.error(repr(ex) + " in analyze json response")
        return response_info


    def analyze_text_response(self, response):
        response_info = {}
        for line in response.split("\n"):
            try:
                parrator = line.find(":")
                key = line[:parrator]
                value = line[parrator+1:]
                response_info[key] = value
            except Exception,ex:
                if self._record_analyze_error:
                    self._logger.error(repr(ex) + " in analyze text response")
            try:
                response_info['Result'] = response_info['Text']
            except Exception,ex:
                if self._record_analyze_error:
                    self._logger.error("missing "  + repr(ex) + " in analyze text response")
        try:
            self._logger.info("ResCode: " + response_info["ResCode"] + "  ResMessage: " + response_info["ResMessage"])
        except Exception,ex:
            if self._record_analyze_error:
                self._logger.error("missing " + repr(ex) + " in log text ResCode and ResMessage")
        return response_info


#解析http response头
    def analyze_response_headers(self, headers):
        """
        解析http_response头为字典
        """
        headers_dict = {}
        try:
            for head in headers:
                headers_dict[head[0]] = head[1]
        except Exception,ex:
            if self._record_analyze_error:
                self._logger.error(repr(ex) + "in analyze response headers")
        finally:
            return headers_dict
        
        
    def set_logger(self, logger):
        '''
        设置FuncHelper的内置logger,需要为hci_http_func_kit.logger类型,理论上python自带的logger也可以使用
        '''
        self._logger = logger
        
    def set_http_info(self, url, port, path, method="POST"):
        '''
        设置http信息 : url, port, http_path, method
        '''
        self._url = url
        self._port = port
        self._http_path = path
        self._method = method
        
    def set_url(self, url):
        '''
        设置http信息 : url
        '''
        self._url = url  
        
    def set_port(self, port):
        '''
        设置http信息 : port
        '''
        self._port = port
        
    def set_path(self, path):
        '''
        设置http信息 : path
        '''
        self._http_path = path

    def set_http_timeout(self , timeout):
        '''
        设置http信息 : timeout
        '''
        self._timeout = timeout
        
#Converts xml to json  
def walk(root_node, level=0):
    this_node = {}
    if level == 0:
        ret = {}
        ret[root_node.tag] = this_node
    else:
        ret = this_node
        
    child_nodes = root_node.getchildren()
    
    if len(child_nodes) == 0:
        return root_node.text

    
    exist_tags = []
    list_tags = []
    for child_node in child_nodes:
        if child_node.tag in exist_tags:
            list_tags.append(child_node.tag)
        else:
            exist_tags.append(child_node.tag)


            
    for child_node in child_nodes:
        node = walk(child_node, level+1)
        if child_node.tag not in list_tags:
            this_node[child_node.tag] = node
        else:
            if child_node.tag not in this_node.keys():
                this_node[child_node.tag] = []
            this_node[child_node.tag].append(node)
        
    return ret
        
    
class HttpHeadModel(object):
    '''
    HTTP头模型,For Hci 8.x
    '''

    def __init__(self, app_key = "ac5d5452", 
                 developer_key = 'developer_key',
                 sdk_version = '3.8',
                 udid = "101:1234567890",
                 accept = "application/json",
                 hci_version = 8
                 ):
        '''
        Constructor
        '''
        self._app_key = app_key
        self._developer_key = developer_key
        self._sdk_version = sdk_version
        self._udid = udid
        self._accept = accept
        self._hci_version = hci_version
        
    def set_accept(self, accept):
        self._accept = accept
        
    def get_app_key(self):
        '''
        get HTTPHeadModel._appkey
        '''
        return self._app_key
    
    def get_developer_key(self):
        '''
        get HTTPHeadModel._developer_key
        '''
        return self._developer_key
    
    def get_sdk_version(self):
        '''
        get HTTPHeadModel._sdk_version
        '''
        return self._sdk_version
    
    def get_udid(self):
        '''
        get HTTPHeadModel._udid
        '''
        return self._udid
    
    def get_accept(self):
        '''
        get HTTPHeadModel._accept
        '''
        return self._accept
    
    def get_date_and_session_key(self):
        '''
        get a session key 
        '''
        request_date = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        session_key = hashlib.md5(str(request_date) + self._developer_key).hexdigest()
        return request_date, session_key
    
    def get_head(self, config, hci_version=None):
        '''
        get HTTP head for Hcicloud 8.x
        '''
        if hci_version == None:
            if self._hci_version == None:
                _hci_version_ = 8
            else:
                _hci_version_ = self._hci_version
        else:
            _hci_version_ = hci_version
        print "hci_version:" + _hci_version_  
        request_date, session_key = self.get_date_and_session_key()
        if _hci_version_==7:
            header = {
               'x-app-key':self.get_app_key(),
               'x-sdk-version':self.get_sdk_version(),
               'x-request-date':request_date,
               'x-task-config':config,
               'x-udid':self.get_udid(),
               'x-session-key':session_key
               }
        elif _hci_version_==8:
            header = {
               'x-app-key':self.get_app_key(),
               'x-sdk-version':self.get_sdk_version(),
               'x-request-date':request_date,
               'x-task-config':config,
               'x-udid':self.get_udid(),
               'x-session-key':session_key,
               #'Accept':self.get_accept()
                }
            
        else:
            raise Exception("unsuppot hcicloud version")
        print header
        
        return header