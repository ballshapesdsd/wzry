#coding:gbk
import cv2
from PIL import Image
from bifen_baidu import OCR
import time
import os


#各个击杀信息的矩形框
a=[(595,135,760,175),(630,135,721,175),(637,135,714,175),(578,134,772,180)]
b=[]
for i in a:
    b.append((int(i[0]/750*1080),int(i[1]/750*1080),int(i[2]/750*1080),int(i[3]/750*1080)))
b.append((858,197,1083,253))
print(b)


#双方比分
bifen1=0
bifen2=0

jisha=[]


for i in os.listdir('.\\jisha'):
    #t:[击杀图像，击杀类别，矩形框】
    t=[cv2.imread('.\\jisha\\'+i,cv2.IMREAD_COLOR)]
    t.append(i)
    if i not in ('diyidixue.png','siliansha.png','wuliansha.png','zhongjie.png','jisha.png','zhongjie2.png'):
        t.append(b[0])
    elif i in ('zhongjie.png','zhongjie2.png'):
        t.append(b[1])
    elif i == 'jisha.png':
        t.append(b[2])
    elif i == 'diyidixue.png':
        t.append(b[4])
    else:
        t.append(b[3])
    jisha.append(t)
    

cap = cv2.VideoCapture('kog_00_19_25_00_33_30.mp4')

ret,frame = cap.read()


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

#击杀类型，1为击败，2为其他
jisha_type=0
#识别结果
result=[]
#百度ocr
ocr=OCR()

while ret:
    ret,frame = cap.read()
    if not ret or bb:
        break
    for idx,jisha_t in enumerate(jisha):
        #截取矩形框
        temp=frame[jisha_t[2][1]:jisha_t[2][3],jisha_t[2][0]:jisha_t[2][2]]
        #匹配值越小越相似
        res=cv2.matchTemplate(temp,jisha_t[0],cv2.TM_SQDIFF_NORMED)[0][0]
        #阈值设置为0.15
        if res<0.15:
            
            #用百度api识别比分，判断是否是回放，暂时注掉，一场比赛大概用api2000次左右
            
            cv2.imwrite('temp_baidu.jpg',frame[34:76,988:1041])
            temp_im=Image.open('temp_baidu.jpg').filter(ImageFilter.SHARPEN)
            temp_im.save('temp_baidu.jpg')
            result1 = ocr.ocr('temp_baidu.jpg')
             
            cv2.imwrite('temp_baidu.jpg',frame[34:76,881:941])
            temp_im=Image.open('temp_baidu.jpg').filter(ImageFilter.SHARPEN)
            temp_im.save('temp_baidu.jpg')
            result2 = ocr.ocr('temp_baidu.jpg')
            
            if result1['words_result_num']!=1:
                result1=bifen1
            else:
                result1=int(result1['words_result'][0]['words'])
                
            if result2['words_result_num']!=1:
                result2=bifen2
            else:
                result2=int(result2['words_result'][0]['words'])
            
            if result1<bifen1 or result2<bifen2:
                huifang=True
            else:
                huifang=False
                bifen1,bifen2=result1,result2
            
            #tt为上一次击杀暴君的帧数，i是现在的帧数，i-tt大于100判断为不同的击杀信息
            if not tt or i-tt>100:
                tt=i
                if jisha_t[1]== 'jisha.png':
                    jisha_type=1
                else:
                    jisha_type=2
            elif jisha_type==1:
                #击败：出现击败文字后第12帧头像位置固定并且无遮挡，用来识别
                if i-tt==12:
                    #击杀者，背景置为黑色
                    yingxiong=frame[174:248,738:837]
                    for i1 in range(74):
                        for j1 in range(99):
                            if (i1-49)**2+(j1-49)**2>49*49:
                                yingxiong[i1,j1]=0
                    #被击杀者，背景置为黑色
                    yingxiong1=frame[174:248,1107:1206]
                    for i1 in range(74):
                        for j1 in range(99):
                            if (i1-49)**2+(j1-49)**2>49*49:
                                yingxiong1[i1,j1]=0
                    #[击杀者，击杀类别，被击杀者，出现击杀信息的帧数]
                    #result.append([match_heroes(yingxiong),jisha_t[1],match_heroes(yingxiong1),tt])
                    result.append([match_heroes(yingxiong),jisha_t[1],match_heroes(yingxiong1),tt,huifang])
            else:
                #其他击杀类别：出现击败文字后第4帧头像位置固定并且无遮挡，用来识别
                if i-tt==4:
                    #同上
                    yingxiong=frame[174:248,721:820]
                    for i1 in range(74):
                        for j1 in range(99):
                            if (i1-49)**2+(j1-49)**2>49*49:
                                yingxiong[i1,j1]=0
                    yingxiong1=frame[174:248,1137:1236]
                    for i1 in range(74):
                        for j1 in range(99):
                            if (i1-49)**2+(j1-49)**2>49*49:
                                yingxiong1[i1,j1]=0
                    #result.append([match_heroes(yingxiong),jisha_t[1],match_heroes(yingxiong1),tt])
                    result.append([match_heroes(yingxiong),jisha_t[1],match_heroes(yingxiong1),tt,huifang])

        a[idx].append((res,i+1))
    i+=1
    print(i)
for t in result:
    print(t)

