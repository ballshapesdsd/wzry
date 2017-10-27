#coding:gbk
import numpy as np
import os
import cv2
import time
import heapq
import sys
from ctypes import *
import random
import multiprocessing

#(x,y)����д������ļ����ʽ��֡�� (x,y)
filet=open('weizhi_temp.txt','w')
filet.close()




#Ӣ��ͼ��ı߿�
def make_biankuang_circle():
    t=[]
    pic = cv2.imread('1.png',0)
    for i in range(42):
        for j in range(42):
            if pic[i,j]==0:
                t.append([i,j])
    return t



#Ӣ��ͷ�����������
def make_circle():
    t=[]
    for i in range(32):
        for j in range(32):
            if (i-15.5)**2+(j-15.5)**2<=241:
                t.append([i,j])
    return t


def minimum_elements_idx(x,elements_idxs,dll_object):
    
    x=x.reshape(x.shape[0]*x.shape[1])
    
    #����һ��
    tp1=np.copy(x)
    #����
    x.sort()
    #��900С��Ԫ��
    r=c_float(x[899])
    try:
        #ȡǰ900С��Ԫ�ص�idx
        dll_object.got_idx(tp1.ctypes.data,tp1.shape[0],r,elements_idxs,900)
    except:
        raise
    return list(elements_idxs)


def matched_pixels_new(i,j,im1,im2,check_bk,m_pixels):
    rgb=(c_double*3)()
    #�����ڶ�������Ϊ1����check�߿��Ƿ�Ϊ��ɫ������check�Ƿ�Ϊ��ɫ
    d=check_bk(i,j,im2.ctypes.data,1,rgb)
    #�߿��������
    if d:
        #ƥ���������
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
    print(time.clock()-s)
    #����ƥ������������߿��rgbֵ
    return t1,(r,g,b)



def frames_process(q,l,finish,num,num1,l1):
    dll_object = cdll.LoadLibrary('wzry.dll')

    check_bk = dll_object.check_biankuang
    m_pixels = dll_object.matched_pixels
    elements_idxs=(c_int*900)()
    circle=make_circle()
    
    #��ƥ���С��ͼӢ��ͷ��
    template = cv2.imread('.\\heroes_thumbnail_xiaoditu_1080\\test_134.png',cv2.IMREAD_COLOR)
    #Ӣ��ͷ����Ұ��
    template1 = template[:,16:]
    #Ӣ��ͷ����°��
    template2 = template[16:,:]
    
    termi=False
    while True:
        try:
            while True:
                try:
                    frame,numx=q.get(block=True,timeout=0.1)
                    break
                except:
                    pass
                if finish.value and num.value==num1.value:
                    print('finish!',os.getpid())
                    termi=True
                    break
            if termi:
                break
            #�Ѵ����֡����num1
            with l1:
                num1.value=num1.value+1
            
            M = np.float32([[1, 0, 17], [0, 1, 17]])
                
            frame=frame[:380,:380]
            
            #ƽ�ƣ�����ƥ��߽紦��ͷ��
            frame = cv2.warpAffine(frame, M, (frame.shape[1], frame.shape[0]))
            
            #ģ��ƥ��
            res = cv2.matchTemplate(frame,template,cv2.TM_SQDIFF_NORMED)
            
            #ȡ�����Ƶ�900������
            t=minimum_elements_idx(res,elements_idxs,dll_object)

            
            #�Ұ�ͷ��ģ��ƥ��
            res = cv2.matchTemplate(frame,template1,cv2.TM_SQDIFF_NORMED)

            #ȡ�����Ƶ�900������
            t1=minimum_elements_idx(res,elements_idxs,dll_object)
            
            #�°�ͷ��ģ��ƥ��
            res = cv2.matchTemplate(frame,template2,cv2.TM_SQDIFF_NORMED)

            #ȡ�����Ƶ�900������
            t2=minimum_elements_idx(res,elements_idxs,dll_object)
            
            #ƥ��������������ֵ
            ma=-1
            for temp in t:
                result=matched_pixels_new(temp//349,temp%349,template,frame,check_bk,m_pixels)
                if result>ma:
                    ma=result
                    y,x=temp//349,temp%349
            for temp in t1:
                result=matched_pixels_new(temp//365,temp%365-10,template,frame,check_bk,m_pixels)
                if result>ma:
                    ma=result
                    y,x=temp//365,temp%365-10
            
            for temp in t2:
                result=matched_pixels_new(temp//349-10,temp%349,template,frame,check_bk,m_pixels)
                if result>ma:
                    ma=result
                    y,x=temp//349-10,temp%349
            
            img2 = cv2.rectangle(frame, (x,y), (x+32,y+32), 255,2)

            with l:
                #������д���ļ�
                filet=open('weizhi_temp.txt','a+')
                filet.write(str(numx)+' '+str((x,y))+'\n')
                filet.close()
            #��ʱ��ʾλ��
            #cv2.imshow('img2',frame)
            #ͼ��д��Ӳ�̣�����鿴
            #cv2.imwrite('d:\\ttt\\video\\temp_'+str(num).zfill(4)+'.jpg',frame)
            
            print(numx,os.getpid())
            
        except:
            raise
            print('end:',os.getpid())
            break
        

def reader(q,finish,num):
    cap = cv2.VideoCapture('c:\\users\\zhengchao\\workspace\\wzry\\kog_00_19_25_00_33_30.mp4')
    ret,frame = cap.read()

    while(1):
        
        ret ,frame = cap.read()
        
        if ret == True and num.value<300:
            #numΪ��֡��
            num.value+=1
            print('frames_num:',num.value)
            q.put((frame,num.value),block=True)
            
        else:
            break
    #����֡����
    finish.value=True
    

if __name__ == '__main__':
    start=time.clock()
    #д�ļ���
    lock = multiprocessing.Lock()
    #�Ѵ����֡����
    lock1 = multiprocessing.Lock()
    finish  = multiprocessing.Value('b',False)
    num = multiprocessing.Value('i',0)
    num1 = multiprocessing.Value('i',0) 
    biankuang=make_biankuang_circle()
    
    
    a=[]
    
    q = multiprocessing.Queue(200)
    

    rr=multiprocessing.Process(target=reader,args=(q,finish,num))
    #��ÿһ֡��ͼ��
    rr.start()
    
    for i in range(4):
        a.append(multiprocessing.Process(target=frames_process, args=(q,lock,finish,num,num1,lock1)))
    
    for i in a:
        i.start()
    
    rr.join()
    for i in a:
        print(i)
    
#     while a[0].is_alive() or a[1].is_alive() or a[2].is_alive() or a[3].is_alive():
#         time.sleep(1)
#         print(a[0].is_alive(),a[0],a[1].is_alive(),a[1],a[2].is_alive(),a[2],a[3].is_alive(),a[3])
    for i in a:
        i.join()
    print(num.value)
    print(time.clock()-start)
    
    #�����ݰ�֡������
    filet=open('weizhi_temp.txt','r')
    a=list(i[1] for i in sorted((int(i[:i.index('(')-1]),eval(i[i.index('('):])) for i in filet.readlines()))
    filet.close()
    filet=open('weizhi.txt','w')
    for w in a:
        filet.write(str(w)+'\n')
    filet.close()