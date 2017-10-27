import multiprocessing
import time
import os
import random

    
def aaa(q,finish):
    for i in range(100):
        time.sleep(0.1)
        print('//////',i)
        q.put(i)
    #print(1)
    finish.value=True

def bbb(q,finish,l):
    print('++++++',os.getpid())
    while not (finish.value and q.empty()):
        try:
            x=q.get(block=True,timeout=1)
            time.sleep(random.random())
            with l:
                print(x ,os.getpid(),finish.value)
        except:
            pass
    print('-----',os.getpid(),finish.value)
    

if __name__=='__main__':
    q=multiprocessing.Queue()
    lock=multiprocessing.Lock()
    finish=multiprocessing.Value('b',False,lock=False)
    w=multiprocessing.Process(target=aaa,args=(q,finish))
    
    w.start()
    #print(2)
    #print(q.get())
    a=[]
    for i in range(3):
        a.append(multiprocessing.Process(target=bbb,args=(q,finish,lock)))
    
    for i in a:
        i.start()
    w.join()
    for i in a:
        i.join()