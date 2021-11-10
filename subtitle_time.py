from io import StringIO
import os
from typing import List
"""
"""
class SubtitleTime(object):
    begin_time = ""
    end_time = ""
    link_sig = " --> "
    line_sig = "\n"
    
    def __init__(self, begin_time: str="", end_time: str=""):
        if end_time == "" and begin_time == "":
            return None
        elif end_time == "":
            two_time_list = begin_time.strip().split(self.link_sig.strip())
            self.begin_time = two_time_list[0].strip()
            self.end_time = two_time_list[1].strip()
        else:
            self.begin_time = begin_time
            self.end_time = end_time

    def get_begin_time(self):
        return self.begin_time

    def get_end_time(self):
        return self.end_time

    def time_bias(self, subtitle_time, base_time_bias: int=0) -> List[int]:
        """
        time bias of two subtitle time

        Parameters
        ----------
        1.subtitle time,
        2.base time bias


        Returns
        -------
        List[int]
            [bias of begin time, bias of end time ,flag]

        """
        time11 = self.begin_time_split()
        time12 = self.end_time_split()
        time21 = subtitle_time.begin_time_split()
        time22 = subtitle_time.end_time_split()
        #translate to millisecond
        time11 = time11[1]*60*1000+time11[2]*1000+time11[3];
        time12 = time12[1]*60*1000+time12[2]*1000+time12[3];
        time21 = time21[1]*60*1000+time21[2]*1000+time21[3];
        time22 = time22[1]*60*1000+time22[2]*1000+time22[3];
        if time11 - base_time_bias == time21:
            fh = 0
        elif time11 - base_time_bias > time21:
            fh = 1
        elif time11 - base_time_bias < time21:
            fh = -1
        time11_21_bias = (time11-base_time_bias-time21)
        time12_22_bias = (time12-base_time_bias-time22)
        return [time11_21_bias, time12_22_bias, fh]

    def begin_time_split(self) -> List[int]:
        """
        one subtitle time is splitted into hour,miniute,seconed and millisecond, four values

        Returns
        -------
        List[int]
            including hour,miniute,seconed and millisecond

        """
        time_list = self.begin_time.strip().split(":")
        sec_list = time_list[2].split(",")
        return [int(time_list[0]), int(time_list[1]), int(sec_list[0]),int(sec_list[1])]

    def end_time_split(self) -> List[int]:
        """
        one subtitle time is splitted into hour,miniute,seconed and millisecond, four values

        Returns
        -------
        List[int]
            including hour,miniute,seconed and millisecond

        """
        time_list = self.end_time.strip().split(":")
        sec_list = time_list[2].split(",")
        return [int(time_list[0]), int(time_list[1]), int(sec_list[0]),int(sec_list[1])]

    def to_string(self) -> str:
        return self.begin_time + self.link_sig + self.end_time + self.line_sig


