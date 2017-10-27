#coding:gbk
from PIL import Image
from PIL import ImageFilter
from PIL import ImageOps
import cv2
import os
import numpy as np


#把头像处理为圆形并缩小
for pic in os.listdir(r'.\heroes'):
    im = Image.open('.\\heroes\\'+pic)
    print(im.size)
    r,g,b=im.split()
    temp_im_r=np.array(r)
    temp_im_g=np.array(g)
    temp_im_b=np.array(b)
    
    i_mi=None
    i_ma=None
    j_mi=None
    j_ma=None
    
    for i in range(im.size[0]):
        t=0
        for j in range(im.size[1]):
            t+=int(temp_im_r[i,j])+int(temp_im_g[i,j])+int(temp_im_b[i,j])
        t=float(t)/int(im.size[1])/3
        if i_mi is None and t<245:
            i_mi=i
        if i_mi is not None and i_ma is None and t>245:
            i_ma=i-1
    for j in range(im.size[0]):
        t=0
        for i in range(im.size[1]):
            t+=int(temp_im_r[i,j])+int(temp_im_g[i,j])+int(temp_im_b[i,j])
        t=float(t)/int(im.size[1])/3
        if j_mi is None and t<245:
            j_mi=j
        if j_mi is not None and j_ma is None and t>245:
            j_ma=j-1
    if j_ma-j_mi!=i_ma-i_mi:
        print('ffff',pic)
        if j_ma-j_mi>i_ma-i_mi:
            j_ma=j_ma-((j_ma-j_mi)-(i_ma-i_mi))
        else:
            i_ma=i_ma-((i_ma-i_mi)-(j_ma-j_mi))
        
    i_mid=float(i_mi+i_ma)/2
    j_mid=float(j_mi+j_ma)/2
    ro=float(i_ma-i_mi+j_ma-j_mi)/4+1
    
    for i in range(im.size[0]):
        for j in range(im.size[1]):
            if (i-i_mid)*(i-i_mid)+(j-j_mid)*(j-j_mid)>ro*ro:
                temp_im_r[i,j]=0
                temp_im_g[i,j]=0
                temp_im_b[i,j]=0
    r= Image.fromarray(np.uint8(temp_im_r))
    g= Image.fromarray(np.uint8(temp_im_g))
    b= Image.fromarray(np.uint8(temp_im_b))
    im=Image.merge('RGB', (r,g,b))
    im=im.crop((j_mi,i_mi,j_ma+1,i_ma+1))
    im.save('12345.png')
    im=cv2.imread('12345.png',cv2.IMREAD_COLOR)
    im=cv2.resize(im,(57,57),interpolation=cv2.INTER_CUBIC)
    cv2.imwrite('.\\heroes_thumbnail_1080\\test_'+pic[:3]+'.png',im)
