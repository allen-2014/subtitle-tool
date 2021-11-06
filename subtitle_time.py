from io import StringIO
import os
from typing import List

def time_split(subtitle_time: str = "") -> List[int]:
    """
    one subtitle time is splitted into hour,miniute,seconed and millisecond, four values

    Returns
    -------
    List[int]
        including hour,miniute,seconed and millisecond

    """
    time_list = subtitle_time.strip().split(":")
    sec_list = time_list[2].split(",")
    return [int(time_list[0]), int(time_list[1]), int(sec_list[0]),int(sec_list[1])]


def line_time_split(one_line_time: str ="") -> List[str]:
    """
    one line subtitle time format:
        xxx:xxx:xxx,xxx --> xxx:xxx:xxx,xxx
        is splitted into two subtitle times

    Returns
    -------
    List[str]
        two subtitle times
    """
    two_time_list = one_line_time.strip().split("-->")
    return [two_time_list[0].strip(), two_time_list[1].strip()]


def time_bias(one_line_time1: str="", one_line_time2: str="", base_time_bias: int=0) ->List[int]:
    time11 = time_split(line_time_split(one_line_time1)[0])
    time12 = time_split(line_time_split(one_line_time1)[1])
    time21 = time_split(line_time_split(one_line_time2)[0])
    time22 = time_split(line_time_split(one_line_time2)[1])
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

def base_time_bias(time_bias_list: List[int]) ->int:
    l,res = 0,0
    for time_bias in time_bias_list:
        if abs(time_bias) > 0:
            res += time_bias
            l += 1
    return res / l