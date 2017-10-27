#coding:gbk
import math
import cv2
import numpy as np

#�ж��߼�,dΪ��֡��֡���x1,y1Ϊǰ����һ֡��λ�ã�x2,y2Ϊ������һ֡��λ�ã�tΪ������һ֡��֡����tpΪ��¼ÿһ֡����һ��tpʱ�䣨Ҳ��֡������dazhao��ÿһ֡����߸������һ��ʩ��ʱ�䣨֡����
def judge_position(d,x1,y1,x2,y2,t,tp,dazhao):
    #if math.sqrt((x2-x1)**2+(y2-y1)**2)/d>0.35 and (abs(x2-x1)>2 or abs(y2-y1)>2) and not(x2<=28 and y2>=171 and t>200):
    #һ���ƶ�0.59�������⣬��x��y���ز���һ������3-->���������������ƶ�
    if math.sqrt((x2-x1)**2+(y2-y1)**2)/d>0.59 and (abs(x2-x1)>3 or abs(y2-y1)>3):
        #x2,y2���ں췽�ϼ����򣨻سǻؼ��ˣ����Һ���һ�λس�ʱ�����7�����ϣ��س�ʱ��7�룩
        if x2>=246 and y2<=91 and t>200 and t-tp[t-d]>7*25:# and t<23200:
            return True,t,dazhao[t-d]
        #��߸�����ж��߼�����ȴ70��-ʩ��ʱ��5��=65�룻ʩ��ʱ��5�룻25��fps
        #elif t-dazhao[t-d]>65*25 and d>=5*25 and t<23000:
        #    return True,tp[t-d],t
        else:
            return False,0,0
    else:
        return True,tp[t-d],dazhao[t-d]

#����������Ӣ�۴���
hh=[134, 154, 180, 132, 190, 157, 107, 189, 111, 171]

heroes=[]
for hero in hh:
    heroes.append(cv2.imread('.\\heroes_thumbnail_xiaoditu_1080\\test_'+str(hero)+'.png',cv2.IMREAD_COLOR))

#Ϊ����λ�ö�λ������Ӣ�����棬λ�����ڵĽ�ͼ����ͱ�Ӣ�������ƣ������ƶ�<0.25
def judge_hero(idx,pic):
    sim=[]
    for i,hero in enumerate(heroes):
        #ֵԽ��Խƥ��
        res = cv2.matchTemplate(pic,hero,cv2.TM_CCOEFF_NORMED)
        res = cv2.minMaxLoc(res)[1]
        sim.append((1-res,i))

    sim.sort()
    for idx1,(_,j) in enumerate(sim):
        #��Ӣ����heroes���4��Ӣ��
        if j==4:
            break
    #sim[0][0]>0.25�������ע��
    if idx1>0 or sim[0][0]>0.25:
        return False
    else:
        return True

#�ж��Ƿ���ܴ��ϼ��ߵ���λ�ã������ʼ��λ�ù��ˣ�����830֡��û�������ˣ�
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
#ma��������һ֡Ϊ��β�������������֡��
ma=[0]
tp=[0]
dazhao=[0]
#1660����˼����1660֡��һ��Ӣ�ۿ��Դ������ϼ��ƶ����췽�ϼ��ٻ��������ֻ��Ҫ��1660��λ�ñ�������֡������Ϣ
bb=list([] for i in range(1660))
result=[]

g=0

#�ö�̬�滮�������ݣ���Ϊλ�������д�����������Ϊѹ�ǣ�������취�ǰ�ÿһ֡ͨ��judge_positon���ж��߼��ͽ�������ĳһ֡��������
#�ܹ��������֡��Ϊ���յĽ��
for idx,(x,y) in enumerate(weizhi[1:][:40000],1):
    print(idx)
    frame=cv2.imread('d:\\ttt\\jietu\\temp_'+str(idx).zfill(5)+'.png',cv2.IMREAD_COLOR)
    st=0 if idx<1660 else idx-1660
    #m������idx֡Ϊ��β������Ӷ���֡
    m=0
    tp_1=0
    dazhao_1=0
    
    if judge_hero(idx,frame) and (idx>840 or judge_position_start(idx,x,y)):
        for j in range(st,idx):
            
            temp_result=judge_position(idx-j,weizhi[j][0],weizhi[j][1],x,y,idx,tp,dazhao)
            #j֡��idx֡��������
            if temp_result[0] and ma[j]+1>m:
                
                m=ma[j]+1
                tp_1=temp_result[1]
                dazhao_1=temp_result[2]
                
                #bb��ÿһ��������ʽ[[a],[b,c],[d],[e,f]]������������a֡��b��c֡��d֡��e��f֡
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
    #��֮ǰ������֡�����Ӳ���
    if m==0:
        
        tp.append(0)
        dazhao.append(0)
        #��֡Ϊ��Ч֡
        if idx<=840 and not judge_position_start(idx,x,y) or not judge_hero(idx,frame):
            ma.append(0)
            bb[idx%1660]=[]
        #��֡Ϊ��Ч֡
        else:
            ma.append(1)
            bb[idx%1660]=[[idx]]
    #��¼��Ϣ
    else:
        ma.append(m)
        tp.append(tp_1)
        dazhao.append(dazhao_1)
        #g�����ܹ������ӵ��֡��
        if m>g:
            g=m
            #result�������ӵ��֡����Ϣ
            result=bb[idx%1660]

fff=open('frames.txt','w')
fff.write(str(result))
fff.close()
