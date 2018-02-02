#-*- coding:utf-8 -*-

'''
Created on 2017-1-10

@author: libin
'''

class AudioFliter():
    def __init__(self, audio_data=None, audio_file=None):
        self._audio_data = ""
        self._audio_file_path = "UnKnown"
        
        if audio_data == None and audio_file == None:
            raise TypeError("AudioFliter need construct by audio_data or audio_file")
        if audio_data != None and audio_file != None:
            raise TypeError("AudioFliter can only init by one of audio_data or audio_file")
        
        if audio_data != None:
            self._audio_data = audio_data
        elif audio_file != None:
            self._audio_file_path = audio_file
            with open(self._audio_file_path, "rb") as audio_file:
                self._audio_data = audio_file.read()
    
    def fliter(self, interval=3200):
        audio_list = []
        last_data = self._audio_data
        while len(last_data) > 0:
            if len(last_data) > interval:
                audio_list.append(last_data[:interval])
                last_data = last_data[interval:]
            else:
                audio_list.append(last_data)
                break
        
        return audio_list