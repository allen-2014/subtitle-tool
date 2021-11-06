"""
merging two subtitle files into one subtitle file, 
which belonging to the same video,including movie, 
or TV Series etc.
"""
import os
import sys
import subtitle_time

if len(sys.argv) == 6:
    path1 = sys.argv[1]
    path2 = sys.argv[2]
    (file_path,file_name) = os.path.split(path1);
    acd1_subtitle_num = int(sys.argv[3])
    acd2_subtitle_num = int(sys.argv[4])
    acd = int(sys.argv[5])
    """
    file1 merge into file2,
    """
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
    if acd == 1:
        base_line_time = one_line1.strip()
    elif acd == 2:
        base_line_time = one_line2.strip()
    #
    time_bias_list = [0,0,0,0,0]
    if merge_subtitle_num == acd1_subtitle_num or merge_subtitle_num == acd2_subtitle_num:
        #bias:ms
        time12_bias = subtitle_time.time_bias(one_line1,one_line2)
        time_bias_list[4] = time12_bias[0]
        base_time_bias = subtitle_time.base_time_bias(time_bias_list)
    #bias:ms
    #time12_bias = subtitle_time.time_bias(one_line1,one_line2,base_time_bias)
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
            #read num
            one_line11 = fd1.readline()
            #time
            one_line11 = fd1.readline()
            if one_line11 == "":
                fd_merge.write(str(merge_subtitle_num) + "\n" + base_line_time + "\n" + (subtitle2 + subtitle1) + "\n")
                fd_merge.flush()
                break
            line11_time = one_line11
            #subtitle
            subtitle11 = ""
            while(True):
                one_line11 = fd1.readline()
                if one_line11 == "\n" or one_line11 == "":
                    break
                subtitle11 += one_line11
        if time12_bias[2] > 0:
            #read num
            one_line21 = fd2.readline()
            #time
            one_line21 = fd2.readline()
            if one_line21 == "":
                fd_merge.write(str(merge_subtitle_num) + "\n" + base_line_time + "\n" + (subtitle2 + subtitle1) + "\n")
                fd_merge.flush()
                break
            line21_time = one_line21
            #subtitle
            subtitle21 = ""
            while(True):
                one_line21 = fd2.readline()
                if one_line21 == "\n" or one_line21 == "":
                    break
                subtitle21 += one_line21
            # if acd == 1:
            #     base_line_time = one_line11.strip();
            # elif acd == 2:
            #     base_line_time = one_line21.strip();
            #bias:ms
        if time12_bias[2] == 0:
            #read num
            one_line11 = fd1.readline()
            one_line21 = fd2.readline()
            if one_line11 == "" or one_line21 == "":
                fd_merge.write(str(merge_subtitle_num) + "\n" + base_line_time + "\n" + (subtitle2 + subtitle1) + "\n")
                fd_merge.flush()
                break
            #time
            one_line11 = fd1.readline()
            one_line21 = fd2.readline()
            line11_time = one_line11
            line21_time = one_line21
            #subtitle
            subtitle11 = ""
            subtitle21 = ""
            while(True):
                one_line11 = fd1.readline()
                if one_line11 == "\n" or one_line11 == "":
                    break
                subtitle11 += one_line11
            while(True):
                one_line21 = fd2.readline()
                if one_line21 == "\n" or one_line21 == "":
                    break
                subtitle21 += one_line21

        time12_bias = subtitle_time.time_bias(line11_time,line21_time,base_time_bias)

        #write to new file directly
        if abs(time12_bias[0]) < 1000:
            fd_merge.write(str(merge_subtitle_num) + "\n" + base_line_time + "\n" + (subtitle2 + subtitle1) + "\n")
            fd_merge.flush()
            #update data
            #subtitle num    
            merge_subtitle_num += 1
            #time
            line1_time = line11_time
            line2_time = line21_time
            #subtitle
            subtitle2 = subtitle21
            subtitle1 = subtitle11
            #base_time_bias
            time_bias_list.pop(0)
            time_bias_list.append(time12_bias[0] + base_time_bias)
            base_time_bias = subtitle_time.base_time_bias(time_bias_list)
            if acd == 1:
                base_line_time = line1_time.strip()
            elif acd == 2:
                base_line_time = line2_time.strip()
            
            time12_bias[2] = 0
        #subtitle of file1 need to be self merging,and then with file2 write to new file
        elif time12_bias[2] < 0:
            subtitle1 += subtitle11
            if acd == 1:
                begin_time = subtitle_time.line_time_split(line1_time)[0]
                end_time = subtitle_time.line_time_split(line11_time)[1]
                base_line_time = begin_time + " --> " + end_time
            elif acd == 2:
                base_line_time = line2_time.strip()
        #subtitle of file2 need to be self merging,and then with file1 write to new file    
        elif time12_bias[2] > 0:
            subtitle2 += subtitle21
            if acd == 1:
                base_line_time = line1_time.strip()
            elif acd == 2:
                begin_time = subtitle_time.line_time_split(line2_time)[0]
                end_time = subtitle_time.line_time_split(line21_time)[1]
                base_line_time = begin_time + " --> " + end_time
        

    fd1.close()
    fd2.close()
    print("good job^_^")
else:
    print("wrong^-^")
