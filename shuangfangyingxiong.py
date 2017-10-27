#coding:gbk
import cv2
from PIL import Image
import os
from bifen_baidu import OCR
import time


#英雄头像
heroes=[]
for i in os.listdir('.\\heroes_thumbnail_1080'):
    heroes.append((cv2.imread('.\\heroes_thumbnail_1080\\'+i,cv2.IMREAD_COLOR),i))

def match_heroes(frame):
    #背景置为黑色
    for i in range(57):
        for j in range(57):
            if (i-28)**2+(j-28)**2>28*28:
                frame[i,j]=0
    
    t=[]
    for idx,hero in enumerate(heroes):
        
        res=cv2.matchTemplate(frame,hero[0],cv2.TM_CCOEFF_NORMED)[0][0]
        t.append((res,hero[1]))
    t.sort()#897,200,1048,253#871,200,1022,253
    t=t[::-1]
    return t[0][1]

im1=cv2.imread('heianbaojun.png',cv2.IMREAD_COLOR)

#a,b,c,d为矩形框,a:左边英雄头像，b:右边英雄头像,c:左边选手名字,d:右边选手名字
a=[[4,376,61,433],[4,470,61,527],[4,565,61,622],[4,659,61,716],[4,754,61,811]]
b=[[1859,376,1916,433],[1859,470,1916,527],[1859,565,1916,622],[1859,659,1916,716],[1859,754,1916,811]]
c=[[0,345,150,374],[0,439,150,468],[0,534,150,563],[0,628,150,657],[0,723,150,752]]
d=[[1770,345,1920,374],[1770,439,1920,468],[1770,534,1920,563],[1770,628,1920,657],[1770,723,1920,752]]


for i in a+b:
    print(match_heroes(im1[i[1]:i[3],i[0]:i[2]]))

o=OCR()
for i in c+d:
    cv2.imwrite('12345.png',im1[i[1]:i[3],i[0]:i[2]])
    time.sleep(1)
    print(o.ocr('12345.png'))

