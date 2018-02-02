#coding=utf-8
'''
Created on 2016-7-27

@author: libin
'''

import sys
import os
import xlsxwriter
import re
import datetime
import getopt

#try to use win32com lib
have_win32com = False
try:
    import win32com.client
    xlApp = win32com.client.DispatchEx('Excel.Application')
    have_win32com = True
except Exception:
    print "import win32com.client failed"

#get file path
path = os.path.abspath(os.curdir)

def read_file_by_path(filePath):
    '''read log file to data[] , return data[]'''
    print " >> re match "+filePath.split("\\")[-1]
    logfile = open(filePath,'r')
    
    monitorPatten = re.compile(r'(\d{4}-\d{2}-\d{2})\s(\d{2}:\d{2}:\d{2})\s(\d{1,9})\s(\d{1,9})\s(\d{1,5}\.\d|\d{1,9})\s(\d{1,9})\s(\d{1,9})')

    data = []
    for line in logfile.readlines():
        #ignore illegal line
        if 'sz memory_check' not in line and 'sz ..' not in line and 'monitor' not in line:
            match = monitorPatten.match(line)
            if match:
                data.append(match.groups())
    return data


def do_chart_for_file(logfile, workbook):
#     print ">  " + logfile

    time_format = workbook.add_format({'num_format': "hh:mm:ss"})

    sheetCount = 0
    if ".log" in logfile:
        workSheetName = re.split('/|\\\\',logfile)[-1].split(".")[0].split("_")[1]
        workSheetName = workSheetName.upper()
        worksheet = workbook.add_worksheet(workSheetName)
        row = 0
        start_row = 1
#取消注释下面的代码添加表头
#         worksheet.write(row,0,"date")
#         worksheet.write(row,1,"time")
#         worksheet.write(row,2,"vmem(kb)")
#         worksheet.write(row,3,"mem(kb)")
#         worksheet.write(row,4,"cpu(%)")
#         worksheet.write(row,5,"lsof")
#         worksheet.write(row,6,"pstree")
#         row+=1
#         start_row+=1

#insert data
        for per in read_file_by_path(logfile):
            worksheet.write(row, 0, per[0])
            hour,minute,second = per[1].split(":")  
            worksheet.write_datetime(row, 1, datetime.time(int(hour),int(minute),int(second)), time_format)
            worksheet.write_number(row, 2, int(per[2]))
            worksheet.write_number(row, 3, int(per[3]))
            
            if '.' in per[4]:
                worksheet.write_number(row, 4, float(per[4]))
            else:
                worksheet.write_number(row, 4, int(per[4]))
                
            worksheet.write_number(row, 5, int(per[5]))
            worksheet.write_number(row, 6, int(per[6]))
            row += 1

#add chart
        '''mem chart'''
        chart0 = workbook.add_chart({'type': 'line'})
        chart0.add_series({
                          'values': '='+workSheetName+'!$D$'+str(start_row)+':$D$'+str(row),
                          'name':workSheetName+"(MEMORY)",
                        })
        chart0.set_title({"name":workSheetName+"(MEMORY)"})
        worksheet.insert_chart('I1', chart0)
        
        '''vmvm chart'''
        chart4 = workbook.add_chart({'type': 'line'})
        chart4.add_series({
                          'values': '='+workSheetName+'!$C$'+str(start_row)+':$C$'+str(row),
                          'name':workSheetName+"(VMEMORY)",
                        })
        chart4.set_title({"name":workSheetName+"(VMEMORY)"})
        worksheet.insert_chart('I17', chart4)
        
        
        '''cpu chart'''
        chart1 = workbook.add_chart({'type': 'line'})
        chart1.add_series({
                          'values': '='+workSheetName+'!$E$'+str(start_row)+':$E$'+str(row),
                          'name':workSheetName+"(CPU)",
                        })
        chart1.set_title({"name":workSheetName+"(CPU)"})
        worksheet.insert_chart('Q1', chart1)
        
        '''lsof chart'''
        chart2 = workbook.add_chart({'type': 'line'})
        chart2.add_series({
                          'values': '='+workSheetName+'!$F$'+str(start_row)+':$F$'+str(row),
                          'name':"lsof",
                        })
        chart2.set_title({"name":"lsof"})
        worksheet.insert_chart('I33', chart2)
        
        '''pstree chart'''
        chart3 = workbook.add_chart({'type': 'line'})
        chart3.add_series({
                          'values': '='+workSheetName+'!$G$'+str(start_row)+':$G$'+str(row),
                          'name':"pstree",
                        })
        chart3.set_title({"name":"pstree"})
        worksheet.insert_chart('Q33', chart3)
        
        sheetCount += 1
    else:
        pass

        
def do_workbook(inputPath, outputPath):
    
    if have_win32com and os.path.exists('./vbaProject.bin'):
        extension_name = ".xlsm"
    else:
        extension_name = ".xlsx"
    
    
    #文件夹内是否有日志文件
    haveLog = False
    if os.path.isfile(inputPath):
        if ".log" in inputPath:
            haveLog = True
    else:
        for logfile in os.listdir(inputPath):
            if ".log" in logfile:
                haveLog = True
    
    #当输出参数为路径时,补全输出文件名
    if not os.path.isfile(outputPath):
        outputPath = outputPath+"\\"+'Stress'+extension_name
    
    #当输出参数为文件时,判断是否以.xlsm结尾,如果文件夹内有log文件,创建workbook
    
    if haveLog:
        if extension_name in outputPath:
            outputPath = outputPath
        else:
            outputPath = outputPath+"Stress"+extension_name
        workbook = xlsxwriter.Workbook(outputPath)
    
    #为workbook中添加数据和图表
        if os.path.isfile(inputPath):
            do_chart_for_file(inputPath,workbook)
        else:
            for logfile in os.listdir(inputPath):
                do_chart_for_file(inputPath+"\\"+logfile,workbook)
       
    #尝试向workbook内添加vba宏
        have_vba = False
        if os.path.exists('./vbaProject.bin') and have_win32com:
            print "---"
            print ">> Add Macro ..."
            workbook.add_vba_project('./vbaProject.bin')
            have_vba = True
        
        
        workbook.close()

    #当有win32com库并且有vba宏二进制文件时,改变图表的X坐标
        if have_win32com and have_vba:
            print ">> Try Execute Macro ..."
            try:
                global xlApp
                xlBook = xlApp.workbooks.Open(outputPath)
                xlApp.Run("ChangeXValue".decode('utf-8'))
                xlBook.Save()
                xlApp.Quit()
            except:
                print "change x value failed"

        print "\n-> Do "+outputPath+" workbook done!"
        print "===\n"
    else:
        print "\n-> "+ inputPath+ "\\  not exist log File!\n"


def achelp():
    print "-i : input File or Path"
    print "     使用该参数以指定log文件夹路径或log文件"
    print "-o : output File or Path"    
    print "     使用该参数以指定输出的.xlsm文件或输出路径"
    print "-h : help"
    print "     使用该参数以获取此帮助"
    
def recursion_read(inputPath):
    if os.path.isdir(inputPath):
        for childpath in os.listdir(inputPath):
            recursion_read(inputPath+"\\"+childpath)
        do_workbook(inputPath,inputPath)
    else:
        pass

if __name__ == "__main__":
    
    opts, args = getopt.getopt(sys.argv[1:], "hi:o:")
    inputPath = path
    outputPath = path
    
    doChart = 2
    for op, value in opts:
        if op == "-i":
            inputPath = value;
            doChart = 1
        elif op == "-o":
            outputPath = value;
            doChart = 1
        elif op == "-h":
            achelp()
            doChart = 0
            
    if doChart == 1:
        do_workbook(inputPath,outputPath)
    elif doChart == 2:
        recursion_read(inputPath)
    
    
    print "\n>>> Done! <<<\n"
    os.system("pause") 