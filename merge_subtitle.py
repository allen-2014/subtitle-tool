"""
merging two subtitle files into one subtitle file, 
which belonging to the same video,including movie, 
or TV Series etc.
"""
import os
import sys
from subtitle_time import  SubtitleTime
import utils
from subtitle import Subtitle

if len(sys.argv) == 6:
    path1 = sys.argv[1]
    path2 = sys.argv[2]
    (file_path,file_name) = os.path.split(path1);
    acd1_subtitle_num = int(sys.argv[3])
    acd2_subtitle_num = int(sys.argv[4])
    acd = int(sys.argv[5])
    """
    srt file1 and srt file2 into new srt file,
    """
    fd1,fd2 = 0, 0
    try:
        fd1 = open(path1, mode='tr',buffering=-1,encoding="utf-8-sig")
        fd2 = open(path2, mode='tr',buffering=-1,encoding="utf-8-sig")
        fd_merge = open(file_path + "\\1.srt",mode='tw+',buffering=-1,encoding="utf8")
        merge_subtitle_num = acd1_subtitle_num if (acd == 1)  else acd2_subtitle_num
        #locate file
        while(True):
            one_line1 = fd1.readline()
            if one_line1.strip().isnumeric() and int(one_line1.strip()) == acd1_subtitle_num:
                break
            if acd == 1:
                fd_merge.write(one_line1)
                fd_merge.flush()
        while(True):
            one_line2 = fd2.readline()
            if one_line2.strip().isnumeric() and int(one_line2.strip()) == acd2_subtitle_num:
                break
            if acd == 2:
                fd_merge.write(one_line2)
                fd_merge.flush()
        #read the subtitle files and merge
        #time
        one_line1 = fd1.readline()
        one_line2 = fd2.readline()
        line1_time = one_line1
        line2_time = one_line2
        subtitle_time1 = SubtitleTime(one_line1)
        subtitle_time2 = SubtitleTime(one_line2)
        if acd == 1:
            base_line_time = one_line1
        elif acd == 2:
            base_line_time = one_line2
        #
        time_bias_list = [0,0,0,0,0]
        base_time_bias = 0
        if merge_subtitle_num == acd1_subtitle_num or merge_subtitle_num == acd2_subtitle_num:
            #bias:ms
            time12_bias = subtitle_time1.time_bias(subtitle_time2)
            time_bias_list[4] = time12_bias[0]
            base_time_bias = utils.base_time_bias(time_bias_list)
        #bias:ms
        time12_bias[2] = 0
        #subtitle
        subtitle1 = ""
        subtitle2 = ""
        while(True):
            one_line1 = fd1.readline()
            if one_line1 == "\n" or one_line1 == "":
                break
            subtitle1 += one_line1
        while(True):
            one_line2 = fd2.readline()
            if one_line2 == "\n" or one_line2 == "":
                break
            subtitle2 += one_line2

        while (True):
            if time12_bias[2] < 0:
                subtitle11_list = utils.read_subtitle(fd1)
                if subtitle11_list == None:
                    fd_merge.write(str(merge_subtitle_num) + "\n" + base_line_time + (subtitle2 + subtitle1) + "\n")
                    fd_merge.flush()
                    break
            if time12_bias[2] > 0:
                subtitle21_list = utils.read_subtitle(fd2)
                if subtitle21_list == None:
                    fd_merge.write(str(merge_subtitle_num) + "\n" + base_line_time + (subtitle2 + subtitle1) + "\n")
                    fd_merge.flush()
                    break         
            
            if time12_bias[2] == 0:
                subtitle11_list = utils.read_subtitle(fd1)
                if subtitle11_list == None:
                    fd_merge.write(str(merge_subtitle_num) + "\n" + base_line_time + (subtitle2 + subtitle1) + "\n")
                    fd_merge.flush()
                    break
                subtitle21_list = utils.read_subtitle(fd2)
                if subtitle21_list == None:
                    fd_merge.write(str(merge_subtitle_num) + "\n" + base_line_time + (subtitle2 + subtitle1) + "\n")
                    fd_merge.flush()
                    break  
                
            subtitle11 = Subtitle(subtitle11_list[0],subtitle11_list[1],subtitle11_list[2])
            subtitle21 = Subtitle(subtitle21_list[0],subtitle21_list[1],subtitle21_list[2])
            # subtitle_time11 = SubtitleTime(line11_time)
            # subtitle_time21 = SubtitleTime(line21_time)
            time12_bias = subtitle11.subtitle_time_inst().time_bias(subtitle21.subtitle_time_inst(), base_time_bias)
            
            #write to new file directly
            if abs(time12_bias[0]) < 1000:
                fd_merge.write(str(merge_subtitle_num) + "\n" + base_line_time + (subtitle2 + subtitle1) + "\n")
                fd_merge.flush()
                #update data
                #subtitle num
                merge_subtitle_num += 1
                #time
                line1_time = subtitle11.subtitle_time_inst().to_string()
                line2_time = subtitle21.subtitle_time_inst().to_string()
                #subtitle
                subtitle2 = subtitle21.subtitle_text()
                subtitle1 = subtitle11.subtitle_text()
                #base_time_bias
                time_bias_list.pop(0)
                time_bias_list.append(time12_bias[0] + base_time_bias)
                base_time_bias = utils.base_time_bias(time_bias_list)
                if acd == 1:
                    base_line_time = line1_time
                elif acd == 2:
                    base_line_time = line2_time
                
                time12_bias[2] = 0
            #subtitle of file1 need to be self merging,and then with file2 write to new file
            elif time12_bias[2] < 0:
                subtitle1 += subtitle11.subtitle_text()
                if acd == 1:
                    subtitle_time1 = SubtitleTime(line1_time)
                    subtitle_time11 = subtitle11.subtitle_time_inst()
                    base_line_time = SubtitleTime(subtitle_time1.get_begin_time(), subtitle_time11.get_end_time()).to_string()
                elif acd == 2:
                    base_line_time = line2_time
            #subtitle of file2 need to be self merging,and then with file1 write to new file    
            elif time12_bias[2] > 0:
                subtitle2 += subtitle21.subtitle_text()
                if acd == 1:
                    base_line_time = line1_time
                elif acd == 2:
                    subtitle_time2 = SubtitleTime(line2_time)
                    subtitle_time21 = subtitle21.subtitle_time_inst()
                    base_line_time = SubtitleTime(subtitle_time2.get_begin_time(), subtitle_time21.get_end_time()).to_string()
            
        print("merge finished.")
    except:
        print("exception raised.")
    finally:
        if fd1 != 0:
            fd1.close()
        if fd2 != 0:
            fd2.close()
else:
    print("wrong")
