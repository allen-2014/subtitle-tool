# subtitle-tool
merging two subtitle files(.srt) into one subtitle file(.srt), which belonging to the same video,including movie, or TV Series etc.

# Problems encounted and Solution
## PS1
when using the end time of subtitle to compare, the result of emerging is bad,
because of the end time not matching the actual time in the video so much,so if 
want to merge exactly, this program hava to use and uses the begin time of 
subtitle, not the end time of it.
## PS2
time bias of two begin time of subtitle which belongs to different srt files,
can be the base time bias of the left begin time.That's meaning each two begin 
times corresponding the same subtitle in two files has the same time bias 
theoretically(if srt files are faultless), but actually not, they may have some 
little(or big) difference each other,so how to compute the base time bias reasonably 
is a problem.
this program use the following solution:

step 1:time_biase_list = [time_bias1,time_bias2,time_bias3,time_bias4,time_bias5]
time_biasi = begin timei(of one subtitle file) - begin timei(of the other subtitle file)
i = 1,2,3,...

step 2:base_time_bias = avg(time_biase_list[1:5])

step 3:
time_biase_list.pop(0)
time_biase_list.append(new_time_bias)

step4:goto step 2

as we can see, the base_time_bias changing with time_biase_list updating. That can improve the merging result dramatically.

## PS
when we get base time bias, the threshold


