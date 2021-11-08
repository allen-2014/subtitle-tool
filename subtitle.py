from os import linesep
from typing import Text
from subtitle_time import SubtitleTime

class Subtitle:
    num = ""
    subtitle_time = SubtitleTime()
    sub_text = ""
    line_sig = "\n"
    def __init__(self, num: str="",line_time: str="", sub_text: str=""):
        self.num = num
        self.subtitle_time = SubtitleTime(line_time)
        self.sub_text = sub_text
    
    def subtitle_time_inst(self):
        return  self.subtitle_time

    def subtitle_text(self):
        return self.sub_text

    def to_string(self) ->str:
        return self.num + \
                self.subtitle_time.to_string() + \
                self.sub_text + self.line_sig
                
                