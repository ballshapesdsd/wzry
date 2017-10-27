#coding:gbk
import math
import cv2
import numpy as np

cap = cv2.VideoCapture('c:\\users\\zhengchao\\workspace\\wzry\\kog_00_19_25_00_33_30.mp4')

ret,frame = cap.read()

filet=open('weizhi.txt','r')
t=0

#��ȡλ����Ϣ
weizhi=[]
for i in filet.readlines():
    weizhi.append(eval(i))
    t+=1

filet.close()

weizhi=[weizhi[0]]+weizhi

for idx,(x,y) in enumerate(weizhi[1:][:40000],1):
    print(idx)
    ret ,frame = cap.read()

    #ƽ��
    M = np.float32([[1, 0, 17], [0, 1, 17]])
    frame=frame[:380,:380]
    frame = cv2.warpAffine(frame, M, (frame.shape[1], frame.shape[0]))
    
    img2=frame[y:y+32,x:x+32]
    
    #����հ�ͼ��case
    if not (img2.shape[0]>0 and img2.shape[1]>0):
        ttemp=np.zeros((96,96))
        cv2.imwrite('d:\\ttt\\jietu\\temp_'+str(idx).zfill(5)+'.png',ttemp) 
        continue
    
    #��ͼ����Χ���ڿ�ƥ����
    M = np.float32([[1, 0, 32], [0, 1, 32]])
    img2 = cv2.warpAffine(img2, M, (96, 96))
    
    #Ӣ��ͷ��ı�����Ϊ��ɫ
    for i in range(img2.shape[0]):
        for j in range(img2.shape[0]):
            if not (i>=32 and j>=32 and i<64 and j<64) or (i-47.5)**2+(j-47.5)**2>240:
                img2[i,j]=0
                
    cv2.imwrite('d:\\ttt\\jietu\\temp_'+str(idx).zfill(5)+'.png',img2)