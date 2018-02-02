#coding=utf-8
'''
Created on 2016-9-21

@author: libin
'''

import re
import xlrd
import xlwt
import types
import xlutils.copy


def open_excel_file(filename):
    """
    打开一个excel文件
    """
    try:
        workbook = xlrd.open_workbook(filename, formatting_info=True)
        return workbook
    except Exception,e:
        print str(e)
        
def load_data_by_excel_file(filename):
    '''
    从EXCEL中读取测试用例
    '''
    required_tags = set(["skip", "casename", "funcname", "config", "body"])
    basic_tags = re.compile(r"skip|casename|funcname|config|body|expect\d+|actual\d+|result")
    reserved_field = re.compile(r"atline|start_line|tag|expect\d+_at|actual\d+_at|count|cases|expect_count")
    
    #读取excel,并初始化行,列等信息
    workbook = open_excel_file(filename)
    test_case = {}
    cases = []
    case_count = 0
    sheet = workbook.sheet_by_index(0)
    nrows = sheet.nrows
    ncols = sheet.ncols
    
      
    #读取tag
    #读取第一行标记,记录所在列,存入tag
    tag = {}
    row = sheet.row_values(0)
    tag['start_line'] = int(row[0])-1
    for col in range(1,ncols):
        if len(row[col]) > 1:
            #检查是否和预留tag重复
            if reserved_field.match(row[col]):
                raise Exception("Please check custom tag ! It can't be the same as the reservation tag. Tag=\"" + row[col] +"\"")
            tag[row[col].decode('unicode-escape').encode('utf-8')] = col
            
    #必选tag检查
    if not required_tags.issubset(tag.keys()):
        need_tag = required_tags - set(tag.keys())
        raise Exception("Missing required tag(s): " + str(list(need_tag)).replace("[", "").replace("]", "") + " , please check Excel file !")
    
    #统计expect数量,存入tag
    expect_num = 0
    for key in tag.keys():
        if re.match('expect\d+',key):
            expect_num += 1
#     tag['expect_num'] = expect_num # 这行好像并没有什么用
    
    #将tag添加到test_case中
    test_case['tag'] = tag

  
    #读取测试用例   
    case = {}
    funcs = []
    func = {}
    pass_flag = False
    case_flag = True
    for nrow in range(tag['start_line'],nrows):
        #读取当前行
        row = sheet.row_values(nrow)
        #当pass标记列有值时跳过测试用例
        if len(str(row[tag['skip']]).strip()) > 0:
            pass_flag = True
            continue
        #若当前行的config列和body列为空,视为空行,跳过
        if len(row[tag['config']]) < 1 and len(row[tag['body']]) < 1:
            continue
        #识别casename,记录所在行,若casename为空,继续在该case中添加其他信息
        if len(row[tag['casename']]) < 1:
            if pass_flag:
                continue
            case_flag = False
        else:
            #当遇到下一个没有pass标记的新case时,继续读取
            pass_flag = False
            case['casename'] = row[tag['casename']]#.decode('unicode-escape').encode('utf-8')
            case['atline'] = nrow
            funcs = []
            case['func'] = funcs
            case_flag = True
        #处理func配置串和body,若无funcname则继承之前funname的值,否则读取当前行的funcname
        if len(row[tag['funcname']]) < 1 :
            func_name = func['funcname']
            func = {}
            func['funcname'] = func_name
        else:
            func = {}
            func['funcname'] = row[tag['funcname']]#.decode('unicode-escape').encode('utf-8')
        func['config'] = row[tag['config']]#.decode('unicode-escape').encode('utf-8')  # 并不好使
        func['body'] = row[tag['body']]
        func['func_at'] = nrow
        
        #在func中添加其他不属于basic_tag的标签
        for key in tag.keys():
            if not ( basic_tags.match(key) or reserved_field.match(key) ):
                if type(row[tag[key]]) not in (types.IntType, types.FloatType):
                    func[key] = row[tag[key]]#.decode('unicode-escape').encode('utf-8')
                else:
                    func[key] = row[tag[key]]
        
        #处理期待值
        n = 1
        i = 0
        #按expect[n]规则,寻找所有的期待值,并记录期待着所在格坐标
        while n < expect_num+1:
            expect_name = 'expect'+str(n)
            #若期待值为空,则视为当前行无更多期待值
            if len(str(row[tag[expect_name]])) < 1:
                break
            func[expect_name+"_at"] = (nrow,tag[expect_name])
            #若各种内容不为int和float,则更改编码为utf-8
            if type(row[tag[expect_name]]) not in (types.IntType, types.FloatType):
                func[expect_name] = row[tag[expect_name]]#.decode('unicode-escape').encode('utf-8')  # 并不好使
            else:
                func[expect_name] = row[tag[expect_name]]
            n += 1
            i += 1
        func['expect_count'] = i
        
        
   

        #将当前函数添加到funcs中
        funcs.append(func)
        
        #当当前行为新case时,将当前case添加到cases中
        if case_flag:
            case_count += 1
            cases.append(case)
            case = {}
            
    test_case['count'] = case_count
    test_case['cases'] = cases
    #print "test_case is :" + str(test_case)
    return test_case
           
            
import json

def write_result_to_excel_file(filename, func_test, is_print_exceptions = False):
    """
    将运行结果写回excel,并判断测试用例是否通过,期望值和实际值是否匹配,并返回通过的case数
    """
    #打开workbook,获取第一个sheet
    workbook = open_excel_file(filename)
    wb = xlutils.copy.copy(workbook)
    sheet = wb.get_sheet(0)
    
    #初始化计数量
    pass_count = 0
    
    for case in func_test['cases']:
        #设置单元格字体格式,该格式在写入测试用例是否通过时使用
        font = xlwt.Font()
        res_style = xlwt.XFStyle()
        res_style.font = font
        font.bold = True
        res = True
        
        #设置结果字体
        result_font = xlwt.Font()
        result_style = xlwt.XFStyle()
        result_style.font = result_font
        result_font.name = 'SimSun'
        #统计actual返回值数量
        actual_count = 0
        for func in case['func']:
            #在期望值个数内进行循环
            except_count = func['expect_count']
            if "result" in func_test['tag'].keys():
                
                try:
                    res_result = True
                    if(str(func['result']) == "The md5 of the audio is equal!"):
                        res_result = True
                    elif(str(func['result']) == "Audio is the default value !"):
                        res_result = True
                    else :
                        res_result = False
                    try:
                        
                        sheet.write(func['func_at'], func_test['tag']['result'], json.dumps(json.loads(func['result']), ensure_ascii=False), result_style)
                    except Exception,ex:
                        if is_print_exceptions:
                            print repr(ex)
                        try:
                            sheet.write(func['func_at'], func_test['tag']['result'], func['result'].decode('utf-8'), result_style) 
                        except:
                            sheet.write(func['func_at'], func_test['tag']['result'], func['result'], result_style)                    
                except Exception,ex:
                    if is_print_exceptions:
                        print "read params[",repr(ex),"] error"
            
            for i in range(1, except_count+1):
                #设置单元格格式,在写入实际返回值时使用
                pattern = xlwt.Pattern()
                pattern.pattern = xlwt.Pattern.SOLID_PATTERN
                ret_style = xlwt.XFStyle()
                ret_style.pattern = pattern
            

                
                #尝试数字转化为excel可以识别的float类型,不可转换的非数字类型会在转换时抛出异常,并不改变原值.不处理异常
                try:
                    func['actual'+str(i)] = float(func['actual'+str(i)])
                except Exception:
                    pass    
                try:
                    #获取期望值所在单元坐标,并判断期望和实际值是否相等
                    except_at = func['expect'+str(i)+'_at']
                    e_res = str(func['expect'+str(i)]) == str(func['actual'+str(i)])

                    #当期望值和实际值相等,将背景色设为亮绿色
                    if e_res:
                        pattern.pattern_fore_colour = 0x2A #light green
                    #当期望值和实际值不等,将背景色设为玫瑰色
                    else:
                        pattern.pattern_fore_colour = 0x2D #rose
                    #将实际值写入Excel表格
                    sheet.write(except_at[0], except_at[1]+1, func['actual'+str(i)], ret_style)
                    #判断该测试用例是否通过
#                     print "res before :",res
#                     print "e_res before :",e_res
#                     print "res_result before :",res_result
                    res = res and e_res and res_result
                    actual_count += 1
                except Exception, ex:
                    if is_print_exceptions:
                        print repr(ex), " in write result to excel"
        
        #当该用例执行,并得到返回值时判断是否通过,写入结果
        if actual_count > 0:
            #当测试用例通过
#             print "res_result:",res_result
#             print "res:", res
            if res:
                result = 'PASS'
                font.colour_index = 0x11 #green
                pass_count += 1
            #当测试用例没有通过
            else:
                result = 'FAILED'
                font.colour_index = 0x0A #red
            #将测试结果写入该测试用例第一行的第一个单元格
            sheet.write(case['atline'], 0, result,res_style)

    #保存excel文件
    wb.save(filename)
    
    return pass_count
