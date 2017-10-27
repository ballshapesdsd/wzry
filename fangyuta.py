#coding:gbk
import cv2
from PIL import Image
import os
import time

#im是摧毁敌方防御塔的文字，im2是我方摧毁防御塔的文字
im=cv2.imread('fangyuta_difang.png',cv2.IMREAD_COLOR)[200:253,897:1048]
im2=cv2.imread('fangyuta_wofang.png',cv2.IMREAD_COLOR)[200:253,871:1022]

cap = cv2.VideoCapture('kog_00_19_25_00_33_30.mp4')
ret,frame = cap.read()

fps=20361/(13*60+53)

#heroes里是处理过的英雄头像和小兵头像信息，取上半部分，并把背景变成黑色
heroes=[]
for i in os.listdir('.\\heroes_thumbnail_jisha_1080'):
    heroes.append((cv2.imread('.\\heroes_thumbnail_jisha_1080\\'+i,cv2.IMREAD_COLOR)[:74],i))
xiaobing=cv2.imread('xiaobingfangyuta.jpg',cv2.IMREAD_COLOR)[104:147,381:440]
xiaobing=cv2.resize(xiaobing,(99,74),interpolation=cv2.INTER_CUBIC)
for i1 in range(74):
    for j1 in range(99):
        if (i1-49)**2+(j1-49)**2>49*49:
            xiaobing[i1,j1]=0
heroes.append((xiaobing,'xiaobing.png'))

#匹配英雄
def match_heroes(frame):
    
    t=[]
    for idx,hero in enumerate(heroes):
        #res值越大匹配程度越高
        res=cv2.matchTemplate(frame,hero[0],cv2.TM_CCOEFF_NORMED)[0][0]
        t.append((res,hero[1]))
    t.sort()
    t=t[::-1]
    return t[0][1]


i=0
tt=None
while(1):
    if not ret:
        break
    #和二个文字信息分别进行匹配，匹配值越小越相似
    temp=frame[200:253,897:1048]
    res=cv2.matchTemplate(temp,im,cv2.TM_SQDIFF_NORMED)[0][0]
    temp=frame[200:253,871:1022]
    res1=cv2.matchTemplate(temp,im2,cv2.TM_SQDIFF_NORMED)[0][0]
    #阈值设置为0.2
    if res1<0.2 or res<0.2:
        #tt为上一次击杀暴君的帧数，i是现在的帧数，i-tt大于100判断为不同的推塔信息
        if not tt or i-tt>100:
            tt=i
        #出现推塔信息后第4帧匹配头像（防止刚出现时头像有变形）
        elif i-tt==4:
            if res<0.2:
                print(str(int(i/fps/60)).zfill(2)+':'+str(i/fps-int(i/fps/60)*60)[:5],'cuihuidifangfangyuta')
                
            if res1<0.2:
                print(str(int(i/fps/60)).zfill(2)+':'+str(i/fps-int(i/fps/60)*60)[:5],'wofangfangyutabeicuihui')
            yingxiong=frame[174:248,643:742]
            #英雄头像背景变为黑色
            for i1 in range(74):
                for j1 in range(99):
                    if (i1-49)**2+(j1-49)**2>49*49:
                        yingxiong[i1,j1]=0
            print('yingxiong:',match_heroes(yingxiong))

    ret,frame = cap.read()
    i+=1
