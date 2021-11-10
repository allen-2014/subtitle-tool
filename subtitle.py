from os import linesep
from typing import Text
from subtitle_time import SubtitleTime

class Subtitle(object):
    __num = ""
    __subtitle_time = SubtitleTime()
    __sub_text = ""
    __line_sig = "\n"
    def __init__(self, num: str="",line_time: str="", sub_text: str=""):
        self.__num = num
        self.__subtitle_time = SubtitleTime(line_time)
        self.__sub_text = sub_text

    @property
    def subtitle_time(self):
        return  self.__subtitle_time
    
    @property
    def subtitle_text(self):
        return self.__sub_text

    def to_string(self) ->str:
        return self.__num + \
                self.__subtitle_time.to_string() + \
                self.__sub_text + self.__line_sig
                
                