from typing import List

def base_time_bias(time_bias_list: List[int]) ->int:
    l,res = 0,0
    for time_bias in time_bias_list:
        if abs(time_bias) > 0:
            res += time_bias
            l += 1
    return res / l