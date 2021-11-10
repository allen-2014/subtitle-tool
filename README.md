# subtitle-tool
merging two subtitle files(.srt) into one subtitle file(.srt), which belonging to the same video,including movie, or TV Series etc.<br>
merging rule: two subtitles having the most adjacent begin times are merged.

# Usage
the way of calling is command line. open the cmd in windows or others, input the following command:  

**python merge_subtitle.py "./eng.srt" "./chn.srt" 2 10 2** <br>

## Options
|Argument     |Description                                                                               |
|-------------|------------------------------------------------------------------------------------------|
|eng.srt      |first file to be merged                                                                   |
|chn.srt      |second file to be merged                                                                  |
|2 and 10     |the 2nd line in eng.srt and the 10th line in chn.srt are matching subtitles.              |
|2            |2 means the merging result format is the second file subtitle is up,the other is down.<br>|
|             |1 means the merging result format is the first file subtitle is up,the other is down. <br>|


the merging result is a new srt file,named "1.srt" default, or you can rename it.<br>


# Problems encountered and Solutions
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
is a problem.<br>
this program use the following solution:<br>

step 1:time_biase_list = [time_bias1,time_bias2,time_bias3,time_bias4,time_bias5]<br>
time_biasi = begin timei(of one subtitle file) - begin timei(of the other subtitle file)<br>
i = 1,2,3,...<br>

step 2:base_time_bias = avg(time_biase_list[1:5])

step 3:<br>
time_biase_list.pop(0)<br>
time_biase_list.append(new_time_bias)<br>

step4:goto step 2

as we can see, the base_time_bias changing with time_biase_list updating. That can improve the merging result dramatically.

## PS3
when we get base time bias, then how to know which subtitles should be merged. the way is to compute the begin time of two subtitles, and if the bias less than a two subtitles, then two subtitles will be merged,so how to the select threshold? just test more srt files.this program adopt the threshold of 1000ms.

# Version
|date     |version |
|---------|--------|
|20211110 |1.0.0   |

