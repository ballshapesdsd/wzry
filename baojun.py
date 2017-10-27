#coding:gbk
import cv2
from PIL import Image
import os
import time

#im,im2,im3�Ǳ��������ף��ڰ���������ɱ��������Ϣ
im=cv2.imread('baojun_1080.png',cv2.IMREAD_COLOR)[196:253,818:1023]
im2=cv2.imread('zhuzai_1080.png',cv2.IMREAD_COLOR)[196:253,818:1023]
im3=cv2.imread('heianbaojun.png',cv2.IMREAD_COLOR)[196:253,871:1073]

cap = cv2.VideoCapture('c:\\users\\zhengchao\\workspace\\wzry\\kog_00_19_25_00_33_30.mp4')

ret,frame = cap.read()


#heroes���Ǵ������Ӣ��ͷ���С��ͷ����Ϣ��ȡ�ϰ벿�֣����ѱ�����ɺ�ɫ
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

#ƥ��Ӣ��
def match_heroes(frame):
    
    t=[]
    for idx,hero in enumerate(heroes):
        #resֵԽ��ƥ��̶�Խ��
        res=cv2.matchTemplate(frame,hero[0],cv2.TM_CCOEFF_NORMED)[0][0]
        t.append((res,hero[1]))
    t.sort()
    t=t[::-1]
    return t[0][1]

i=0
tt=0
while True:
    if not ret:
        break
    #������������Ϣ�ֱ����ƥ�䣬ƥ��ֵԽСԽ����
    temp=frame[196:253,818:1023]
    res=cv2.matchTemplate(temp,im,cv2.TM_SQDIFF_NORMED)[0][0]
    res1=cv2.matchTemplate(temp,im2,cv2.TM_SQDIFF_NORMED)[0][0]
    res2=cv2.matchTemplate(frame[196:253,871:1073],im3,cv2.TM_SQDIFF_NORMED)[0][0]
    #��ֵ����Ϊ0.1
    if res<0.1 or res1<0.1 or res2<0.1:
        #ttΪ��һ�λ�ɱ������֡����i�����ڵ�֡����i-tt����100�ж�Ϊ��ͬ�Ļ�ɱ������Ϣ
        if not tt or i-tt>100:
            tt=i
        #���ֱ�����Ϣ���4֡ƥ��ͷ�񣨷�ֹ�ճ���ʱͷ���б��Σ�
        elif i-tt==4:
            if res<0.1:
                print(str(int(i/25/60)).zfill(2)+':'+str(i/25-int(i/25/60)*60)[:5],'baojun')
            elif res1<0.1:
                print(str(int(i/25/60)).zfill(2)+':'+str(i/25-int(i/25/60)*60)[:5],'zhuzai')
            else:
                print(str(int(i/25/60)).zfill(2)+':'+str(i/25-int(i/25/60)*60)[:5],'heianbaojun')
            #���������׺ͺڰ�������Ӣ��ͷ��λ�ò�ͬ
            if res<0.1 or res1<0.1:
                yingxiong=frame[174:248,674:773]
            else:
                yingxiong=frame[174:248,635:734]
            #Ӣ��ͷ�񱳾���Ϊ��ɫ
            for i1 in range(74):
                for j1 in range(99):
                    if (i1-49)**2+(j1-49)**2>49*49:
                        yingxiong[i1,j1]=0
                        
            print('yingxiong:',match_heroes(yingxiong))
    ret,frame = cap.read()
    i+=1
