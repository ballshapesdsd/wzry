#coding:gbk
import math
import cv2
import numpy as np

#判断逻辑,d为两帧的帧数差，x1,y1为前面那一帧的位置，x2,y2为后面那一帧的位置，t为后面那一帧的帧数，tp为记录每一帧的上一次tp时间（也是帧数），dazhao是每一帧的哪吒大招上一次施放时间（帧数）
def judge_position(d,x1,y1,x2,y2,t,tp,dazhao):
    #if math.sqrt((x2-x1)**2+(y2-y1)**2)/d>0.35 and (abs(x2-x1)>2 or abs(y2-y1)>2) and not(x2<=28 and y2>=171 and t>200):
    #一秒移动0.59像素以外，且x，y像素差有一个大于3-->不可能是正常的移动
    if math.sqrt((x2-x1)**2+(y2-y1)**2)/d>0.59 and (abs(x2-x1)>3 or abs(y2-y1)>3):
        #x2,y2处于红方老家区域（回城回家了），且和上一次回城时间相差7秒以上（回城时间7秒）
        if x2>=246 and y2<=91 and t>200 and t-tp[t-d]>7*25:# and t<23200:
            return True,t,dazhao[t-d]
        #哪吒大招判断逻辑：冷却70秒-施放时间5秒=65秒；施放时间5秒；25是fps
        #elif t-dazhao[t-d]>65*25 and d>=5*25 and t<23000:
        #    return True,tp[t-d],t
        else:
            return False,0,0
    else:
        return True,tp[t-d],dazhao[t-d]

#本场比赛的英雄代码
hh=[134, 154, 180, 132, 190, 157, 107, 189, 111, 171]

heroes=[]
for hero in hh:
    heroes.append(cv2.imread('.\\heroes_thumbnail_xiaoditu_1080\\test_'+str(hero)+'.png',cv2.IMREAD_COLOR))

#为避免位置定位到其他英雄上面，位置所在的截图必须和本英雄最相似，且相似度<0.25
def judge_hero(idx,pic):
    sim=[]
    for i,hero in enumerate(heroes):
        #值越大越匹配
        res = cv2.matchTemplate(pic,hero,cv2.TM_CCOEFF_NORMED)
        res = cv2.minMaxLoc(res)[1]
        sim.append((1-res,i))

    sim.sort()
    for idx1,(_,j) in enumerate(sim):
        #本英雄是heroes里第4个英雄
        if j==4:
            break
    #sim[0][0]>0.25可视情况注掉
    if idx1>0 or sim[0][0]>0.25:
        return False
    else:
        return True

#判断是否可能从老家走到此位置（比赛最开始的位置过滤，超过830帧就没有意义了）
def judge_position_start(idx,x,y):
    if math.sqrt((x-380)**2+y**2)/idx>0.59 and (abs(x-380)>2 or y>2):
        return False
    else:
        return True

filet=open('weizhi.txt','r')
t=0
weizhi=[]
for i in filet.readlines():

    weizhi.append(eval(i))
    t+=1

filet.close()
weizhi=[weizhi[0]]+weizhi
#ma保存以这一帧为结尾，最多能连多少帧数
ma=[0]
tp=[0]
dazhao=[0]
#1660的意思是在1660帧内一个英雄可以从蓝方老家移动到红方老家再回来，因此只需要有1660个位置保存连接帧数的信息
bb=list([] for i in range(1660))
result=[]

g=0

#用动态规划处理数据，因为位置数据有大量噪声（因为压盖），处理办法是把每一帧通过judge_positon的判断逻辑和接下来的某一帧连接起来
#能够连出的最长帧数为最终的结果
for idx,(x,y) in enumerate(weizhi[1:][:40000],1):
    print(idx)
    frame=cv2.imread('d:\\ttt\\jietu\\temp_'+str(idx).zfill(5)+'.png',cv2.IMREAD_COLOR)
    st=0 if idx<1660 else idx-1660
    #m保存以idx帧为结尾最多连接多少帧
    m=0
    tp_1=0
    dazhao_1=0
    
    if judge_hero(idx,frame) and (idx>840 or judge_position_start(idx,x,y)):
        for j in range(st,idx):
            
            temp_result=judge_position(idx-j,weizhi[j][0],weizhi[j][1],x,y,idx,tp,dazhao)
            #j帧和idx帧可以相连
            if temp_result[0] and ma[j]+1>m:
                
                m=ma[j]+1
                tp_1=temp_result[1]
                dazhao_1=temp_result[2]
                
                #bb的每一项都是这个格式[[a],[b,c],[d],[e,f]]，代表连接了a帧，b到c帧，d帧，e到f帧
                if not bb[j%1660]:
                    bb[idx%1660]=[[idx]]
                elif len(bb[j%1660][-1])==1:
                    if bb[j%1660][-1][0]+1==idx:
                        bb[idx%1660]=bb[j%1660][:-1]+[bb[j%1660][-1]+[idx]]
                    else:
                        bb[idx%1660]=bb[j%1660]+[[idx]]
                else:
                    if bb[j%1660][-1][1]+1==idx:
                        bb[idx%1660]=bb[j%1660][:-1]+[[bb[j%1660][-1][0]]+[idx]]
                    else:
                        bb[idx%1660]=bb[j%1660]+[[idx]]
    #和之前的所有帧都连接不上
    if m==0:
        
        tp.append(0)
        dazhao.append(0)
        #此帧为无效帧
        if idx<=840 and not judge_position_start(idx,x,y) or not judge_hero(idx,frame):
            ma.append(0)
            bb[idx%1660]=[]
        #此帧为有效帧
        else:
            ma.append(1)
            bb[idx%1660]=[[idx]]
    #记录信息
    else:
        ma.append(m)
        tp.append(tp_1)
        dazhao.append(dazhao_1)
        #g代表总共能连接的最长帧数
        if m>g:
            g=m
            #result是能连接的最长帧数信息
            result=bb[idx%1660]

fff=open('frames.txt','w')
fff.write(str(result))
fff.close()
