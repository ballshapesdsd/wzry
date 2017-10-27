#coding:gbk
from PIL import Image,ImageFilter
from aip import AipOcr

import cv2

#矩形框
#355,20,394,81--左边大比分
#1541,20,1586,81--右边大比分
#881,34,941,76--左边人头比分
#988,34,1041,76--右边人头比分

im = Image.open('baojun_1080.png').crop((355,20,394,81)).filter(ImageFilter.SHARPEN)
im.save('12345.png')

class OCR():
    def __init__(self):
        
        self.APP_ID = '10253196'
        self.API_KEY = 'rHGiInWCSToEjuy5yK6PsnGI'
        self.SECRET_KEY = 'dknE6TYRHBzRHDg2FMIgHr4u9zb8HyEz'

        self.aipOcr = AipOcr(self.APP_ID, self.API_KEY, self.SECRET_KEY)



    def get_file_content(self,filePath):
        with open(filePath, 'rb') as fp:
            return fp.read()

    def ocr(self,file_name):
        result = self.aipOcr.basicGeneral(self.get_file_content(file_name))
        return result
o=OCR()
#print(o.ocr('12345.png'))
