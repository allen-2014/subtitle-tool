from io import TextIOWrapper
from typing import List

def base_time_bias(time_bias_list: List[int]) ->int:
    """
    compute avg of recent 5 time bias, as base time bias

    Parameters:
    --------
        List[int]:time bais list
    Returns:
    -------
        int:base time bias
    """
    l,res = 0,0
    for time_bias in time_bias_list:
        if abs(time_bias) > 0:
            res += time_bias
            l += 1
    return res / l if l > 0 else 0

def read_subtitle(fd: TextIOWrapper = 0) ->List[str]:
    if fd == 0:
        return None
    #read num
    one_line11 = fd.readline()
    if one_line11 == "":
        return None
    line11_num = one_line11
    #time
    one_line11 = fd.readline()
    line11_time = one_line11
    #subtitle
    subtitle11 = ""
    while(True):
        one_line11 = fd.readline()
        if one_line11 == "\n" or one_line11 == "":
            break
        subtitle11 += one_line11
    return [line11_num, line11_time, subtitle11]