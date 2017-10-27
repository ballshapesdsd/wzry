#coding:gbk
import numpy as np
import cv2
import time
import heapq
import math

cap = cv2.VideoCapture('c:\\users\\zhengchao\\workspace\\wzry\\kog_00_19_25_00_33_30.mp4')

ret,frame = cap.read()

def ccc(d,x1,y1,x2,y2,t):
    #判断是否tp回家
    if x2>=246 and y2<=91:
        return False
    else:
        return True
#插值,d为帧差，x是要插值的帧数和前一帧的帧差,x1,y1是前一帧的位置，x2,y2是后一帧的位置
def bbb(d,x,x1,y1,x2,y2):
    return int(x1+(x2-x1)*x/d),int(y1+(y2-y1)*x/d)

filet=open('weizhi.txt','r')
t=0
a=[]
for i in filet.readlines():

    a.append(eval(i))
    t+=1

filet.close()

filet=open('frames.txt','r')
frames=eval(filet.read())
filet.close()

idx=0
#每一帧的位置
loc=[]

#插值过程
temp=frames[0]
for i in range(1,temp[0]):
    loc.append(bbb(temp[0],i,205,0,a[temp[0]-1][0],a[temp[0]-1][1]))
for idxx,temp1 in enumerate(frames[:-1]):
    
    if len(temp1)==1:
        loc.append((a[temp1[0]-1][0],a[temp1[0]-1][1]))
    else:
        for v in range(temp1[0],temp1[1]+1):
            loc.append((a[v-1][0],a[v-1][1]))
    if ccc(frames[idxx+1][0]-temp1[-1],a[temp1[-1]-1][0],a[temp1[-1]-1][1],a[frames[idxx+1][0]-1][0],a[frames[idxx+1][0]-1][1],frames[idxx+1][0]):
        for jjj in range(temp1[-1]+1,frames[idxx+1][0]):
            loc.append(bbb(frames[idxx+1][0]-temp1[-1],jjj-temp1[-1],a[temp1[-1]-1][0],a[temp1[-1]-1][1],a[frames[idxx+1][0]-1][0],a[frames[idxx+1][0]-1][1]))
    else:
        for jjj in range(temp1[-1]+1,frames[idxx+1][0]):
            loc.append((a[temp1[-1]-1][0],a[temp1[-1]-1][1]))
if len(frames[-1])==1:
    loc.append((a[frames[-1][0]-1][0],a[frames[-1][0]-1][1]))
else:
    for v in range(frames[-1][0],frames[-1][1]+1):
        loc.append((a[v-1][0],a[v-1][1]))

for jjj in range(frames[-1][-1],24000):
    loc.append((a[frames[-1][-1]-1][0],a[frames[-1][-1]-1][1]))
num=1


#每一帧的位置画出来，把图片写入硬盘，可用ffmpeg生成视频
while(1):
    ret ,frame = cap.read()
    if ret == True:
        start=time.clock()
        
        M = np.float32([[1, 0, 17], [0, 1, 17]])
        
        frame=frame[:380,:380]
        frame = cv2.warpAffine(frame, M, (frame.shape[1], frame.shape[0]))

        img2 = cv2.rectangle(frame, loc[num-1], (loc[num-1][0]+32,loc[num-1][1]+32), 255,2)
        print(num,loc[num-1])

        cv2.imwrite('d:\\ttt\\video_chazhi\\temp_'+str(num).zfill(4)+'.jpg',img2)
        num+=1
       