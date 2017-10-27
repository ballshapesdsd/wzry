#coding:gbk
import numpy as np
import cv2
import time
import heapq
import sys
from ctypes import *
import random

#��ƥ���С��ͼӢ��ͷ��
template = cv2.imread('.\\heroes_thumbnail_xiaoditu_1080\\test_134.png',cv2.IMREAD_COLOR)
#Ӣ��ͷ����Ұ��
template1 = template[:,16:]
#Ӣ��ͷ����°��
template2 = template[16:,:]
cap = cv2.VideoCapture('c:\\users\\zhengchao\\workspace\\wzry\\kog_00_19_25_00_33_30.mp4')
ret,frame = cap.read()

#(x,y)����д������ļ���
filet=open('weizhi.txt','w')

#Ӣ��ͼ��ı߿�
def make_biankuang_circle():
    t=[]
    pic = cv2.imread('1.png',0)
    for i in range(42):
        for j in range(42):
            if pic[i,j]==0:
                t.append([i,j])
    return t

biankuang=make_biankuang_circle()

#Ӣ��ͷ�����������
def make_circle():
    t=[]
    for i in range(32):
        for j in range(32):
            if (i-15.5)**2+(j-15.5)**2<=241:
                t.append([i,j])
    return t
circle=make_circle()

dll1 = cdll.LoadLibrary('got_idx.dll')
dll2 = cdll.LoadLibrary('check_biankuang.dll')
dll3 = cdll.LoadLibrary('matched_pixels.dll')
check_bk = dll2.display
m_pixels = dll3.display

result111=(c_int*900)()

def heappp(x):
    x=x.reshape(x.shape[0]*x.shape[1])
    
    #print('----',x[0])
    #print(1111,x.ctypes.data)
    tp1=np.copy(x)
    x.sort()
    r=c_float(x[899])
    #print(tp1.dtype,x.shape[0])
    #print(tp1,r)
    try:
        dll1.got_idx(tp1.ctypes.data,tp1.shape[0],r,result111,900)
    except:
        #print(list(tp1))
        raise
    #heap111(x.ctypes.data,x.shape[0]*x.shape[1],900,result)
    #print(list(result))
    return list(result111)

v=[]
for i in range(121801):
    if i<50000:
        v.append(0.1)
    else:
        v.append(0.2)
    #v.append(random.random())
u=np.array(v).astype(np.float32).reshape((349,349))
#print(heappp(u))

def matched_pixels_new(i,j,im1,im2):
    rgb=a=(c_double*3)()
    d=check_bk(i,j,im2.ctypes.data,1,rgb)
    if d:
        return m_pixels(i,j,im1.ctypes.data,im2.ctypes.data)
    else:
        return 0

def matched_pixels(i,j,im1,im2,biankuang):
    
    #���˵������߽������
    biankuang1=list(filter(lambda x:x[0]<380 and x[1]<380 and x[0]>=0 and x[1]>=0\
                       ,list([y[0]+i-5,y[1]+j-5] for y in biankuang)))
    temp=list(zip(*biankuang1))
    
    r1=im2[:,:,2][temp]
    g1=im2[:,:,1][temp]
    b1=im2[:,:,0][temp]
    #����ɫ��������
    p=(r1!=0)+(g1!=0)+(b1!=0)
    #��ɫ��ֵ
    r=np.average(r1[p])
    #��ɫ��ֵ
    g=np.average(g1[p])
    #��ɫ��ֵ
    b=np.average(b1[p])
    
    #<���������ɫ����֮��ɫ
    if (r-83)**2+(g+b-441)**2<(r-178)**2+(g+b-53)**2:
        pass
    else:
        return 0,(0,0,0)
    s=time.clock()
    temp=circle
    
    #����߽����
    if j<0:
        u1=-j
        u=32
    elif j+32>380:
        u1=0
        u=32-((j+32)-380)
    else:
        u1=0
        u=32
    if i<0:
        v1=-i
        v=32
    elif i+32>380:
        v1=0
        v=32-((i+32)-380)
    else:
        v1=0
        v=32
    if j<0:
        k=j+32
        j=0
    elif j+32>380:
        k=380
    else:
        k=j+32
    if i<0:
        l=i+32
        i=0
    elif i+32>380:
        l=380
    else:
        l=i+32
    if u-u1<32 or v-v1<32:
        temp=[[i[0]-(32-(v-v1)) if v1>0 else i[0],i[1]-(32-(u-u1)) if u1>0 else i[1]] for i in temp]
        
    temp=list(i for i in temp if i[0]>=0 and i[1]>=0 and i[0]<v-v1 and i[1]<u-u1)
    temp=list(zip(*temp))
    
    temp1=np.array(temp[0])
    temp2=np.array(temp[1])
    
    #ȡ����ƥ���Ӣ�۵�rgbֵ
    r1=im1[v1:v,u1:u,2][temp1,temp2]
    g1=im1[v1:v,u1:u,1][temp1,temp2]
    b1=im1[v1:v,u1:u,0][temp1,temp2]
    
    #ȡ��С��ͼӢ��ͷ���rgbֵ
    r2=im2[i:l,j:k,2][temp1,temp2]
    g2=im2[i:l,j:k,1][temp1,temp2]
    b2=im2[i:l,j:k,0][temp1,temp2]
    
    #����Ӧ����rgbֵ�ľ���ֵ��С��50������ƥ�������
    r_diff=abs(r1.astype(np.int16)-r2.astype(np.int16))
    g_diff=abs(g1.astype(np.int16)-g2.astype(np.int16))
    b_diff=abs(b1.astype(np.int16)-b2.astype(np.int16))
    t1=np.sum(((r_diff<50).astype(np.uint8)+(g_diff<50).astype(np.uint8)+\
              (b_diff<50).astype(np.uint8))==3)
    #print(time.clock()-s)
    #����ƥ������������߿��rgbֵ
    return t1,(r,g,b)

num=1     
#print('num')
while(1):
    ret ,frame = cap.read()
    start=time.clock()
    #print(num)
    if ret == True:

        M = np.float32([[1, 0, 17], [0, 1, 17]])
        
        frame=frame[:380,:380]
        #ƽ�ƣ�����ƥ��߽紦��ͷ��
        frame = cv2.warpAffine(frame, M, (frame.shape[1], frame.shape[0]))
        
        #ģ��ƥ��
        res = cv2.matchTemplate(frame,template,cv2.TM_SQDIFF_NORMED)
        
        #print(res.dtype,res[11,11])
        res = -res.reshape(349*349)
        #print(res.dtype,res[11,11],res.shape)
        #ȡ�����Ƶ�300������
        #print(num)
        #t=heappp(res)
        #print(t)
        t=heapq.nlargest(900, range(len(res)), res.take)
        
        #�Ұ�ͷ��ģ��ƥ��
        res = cv2.matchTemplate(frame,template1,cv2.TM_SQDIFF_NORMED)
        
        res = -res.reshape(res.shape[0]*res.shape[1])
        #print(res.shape)
        #ȡ�����Ƶ�300������
        #t1=heappp(res)
        t1=heapq.nlargest(900, range(len(res)), res.take)
        
        #�°�ͷ��ģ��ƥ��
        res = cv2.matchTemplate(frame,template2,cv2.TM_SQDIFF_NORMED)
        res = -res.reshape(res.shape[0]*res.shape[1])
        #ȡ�����Ƶ�300������
        #t2=heappp(res)
        t2=heapq.nlargest(900, range(len(res)), res.take)
        
        #ƥ��������������ֵ
        ma=-1
        
        for temp in t:
            result=matched_pixels(temp//349,temp%349,template,frame,biankuang)
            if result[0]>ma:
                ma=result[0]
                r,g,b=result[1]
                y,x=temp//349,temp%349
        for temp in t1:
            result=matched_pixels(temp//365,temp%365-10,template,frame,biankuang)
            if result[0]>ma:
                ma=result[0]
                r,g,b=result[1]
                y,x=temp//365,temp%365-10
        
        for temp in t2:
            result=matched_pixels(temp//349-10,temp%349,template,frame,biankuang)
            if result[0]>ma:
                ma=result[0]
                r,g,b=result[1]
                y,x=temp//349-10,temp%349
        
        img2 = cv2.rectangle(frame, (x,y), (x+32,y+32), 255,2)
        filet.write(str((x,y))+'\n')
        #��ʱ��ʾλ��
        #cv2.imshow('img2',frame)
        #ͼ��д��Ӳ�̣�����鿴
        cv2.imwrite('d:\\ttt\\video\\temp_'+str(num).zfill(4)+'.jpg',frame)
        num+=1
        
        k = cv2.waitKey(60) & 0xff
        if k == 27:
            break
        else:
            pass
        print(num-1,time.clock()-start)
    else:
        break
cv2.destroyAllWindows()
filet.close()
