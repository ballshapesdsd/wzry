#coding:gbk
import cv2
from PIL import Image
from bifen_baidu import OCR
import time
import os


#������ɱ��Ϣ�ľ��ο�
a=[(595,135,760,175),(630,135,721,175),(637,135,714,175),(578,134,772,180)]
b=[]
for i in a:
    b.append((int(i[0]/750*1080),int(i[1]/750*1080),int(i[2]/750*1080),int(i[3]/750*1080)))
b.append((858,197,1083,253))
print(b)


#˫���ȷ�
bifen1=0
bifen2=0

jisha=[]


for i in os.listdir('.\\jisha'):
    #t:[��ɱͼ�񣬻�ɱ��𣬾��ο�
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
tt=None

#��ɱ���ͣ�1Ϊ���ܣ�2Ϊ����
jisha_type=0
#ʶ����
result=[]
#�ٶ�ocr
ocr=OCR()

while ret:
    ret,frame = cap.read()
    if not ret or bb:
        break
    for idx,jisha_t in enumerate(jisha):
        #��ȡ���ο�
        temp=frame[jisha_t[2][1]:jisha_t[2][3],jisha_t[2][0]:jisha_t[2][2]]
        #ƥ��ֵԽСԽ����
        res=cv2.matchTemplate(temp,jisha_t[0],cv2.TM_SQDIFF_NORMED)[0][0]
        #��ֵ����Ϊ0.15
        if res<0.15:
            
            #�ðٶ�apiʶ��ȷ֣��ж��Ƿ��ǻطţ���ʱע����һ�����������api2000������
            
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
            
            #ttΪ��һ�λ�ɱ������֡����i�����ڵ�֡����i-tt����100�ж�Ϊ��ͬ�Ļ�ɱ��Ϣ
            if not tt or i-tt>100:
                tt=i
                if jisha_t[1]== 'jisha.png':
                    jisha_type=1
                else:
                    jisha_type=2
            elif jisha_type==1:
                #���ܣ����ֻ������ֺ��12֡ͷ��λ�ù̶��������ڵ�������ʶ��
                if i-tt==12:
                    #��ɱ�ߣ�������Ϊ��ɫ
                    yingxiong=frame[174:248,738:837]
                    for i1 in range(74):
                        for j1 in range(99):
                            if (i1-49)**2+(j1-49)**2>49*49:
                                yingxiong[i1,j1]=0
                    #����ɱ�ߣ�������Ϊ��ɫ
                    yingxiong1=frame[174:248,1107:1206]
                    for i1 in range(74):
                        for j1 in range(99):
                            if (i1-49)**2+(j1-49)**2>49*49:
                                yingxiong1[i1,j1]=0
                    #[��ɱ�ߣ���ɱ��𣬱���ɱ�ߣ����ֻ�ɱ��Ϣ��֡��]
                    #result.append([match_heroes(yingxiong),jisha_t[1],match_heroes(yingxiong1),tt])
                    result.append([match_heroes(yingxiong),jisha_t[1],match_heroes(yingxiong1),tt,huifang])
            else:
                #������ɱ��𣺳��ֻ������ֺ��4֡ͷ��λ�ù̶��������ڵ�������ʶ��
                if i-tt==4:
                    #ͬ��
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

