import multiprocessing
from ctypes import *
import time
import random
import os


def aaa(dll_name):
    print(os.getpid(),dll_name)
    dll=cdll.LoadLibrary(dll_name)
    for i in range(20):
        time.sleep(0.5*random.random())
        print(i,os.getpid())

if __name__=='__main__':
#     dll=cdll.LoadLibrary('test.dll')
#     x=dll.p
#     print(x(1,2))
    a=[]
    dll_names=['test.dll']*3
    for i in range(3):
        a.append(multiprocessing.Process(target=aaa,args=(dll_names[i],)))
     
    for i in a:
        i.start()
    while a[0].is_alive() or a[1].is_alive() or a[2].is_alive():
        time.sleep(1)
        print(a[0].is_alive(),a[0],a[2].is_alive(),a[2],a[2].is_alive(),a[2])    
        pass
     
#     for i in a:
#         i.join()