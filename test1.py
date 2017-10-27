import multiprocessing
import os
import time

 
def reader_proc(q):
    while True:   
        try:         
            print(q.get(block = False),os.getpid())
            time.sleep(0.1)
        except:         
            break

def writer(q):
    for i in range(100):
        q.put(i)
        

if __name__ == "__main__":
    q = multiprocessing.Queue()
    w=multiprocessing.Process(target=writer,args=(q,))
    w.start()
    
    a=[]
    for i in range(3):
        a.append(multiprocessing.Process(target=reader_proc, args=(q,)) )
    for i in a:
        i.start()
    w.join()  
    for i in a:
        i.join()  
    