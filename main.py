import threading
import time

import cv2
import numpy as np
import dataclasses

import BroadCast
import Receive


@dataclasses.dataclass
class ST_THREAD:
    id:int = -1
    interval:float = 0.1
    flag:bool = False
    state:int = 0

def THREAD_TEST(id, param:ST_THREAD):
    count = 0
    param.state = 1
    while param.flag:
        time.sleep(param.interval)
        count += 1
        print(f"{param.id} : {count}")
        if count == 10:
            break
        pass
    
    param.state = 10
    pass

def THREAD_MODULERUN():
    #BroadCast.RunBroadCast()
    Receive.RunRecive("FalconEyes")
    pass

def mainloop():
    threading.Thread(target = THREAD_MODULERUN).start()
    
    
    stparam1 = ST_THREAD()
    stparam1.id = 0
    stparam1.flag = True
    stparam1.interval = 0.1
    
    thread1 = threading.Thread(target = THREAD_TEST, args = (0,stparam1))
    thread1.start()
    
    stparam2 = ST_THREAD()
    stparam2.id = 1
    stparam2.flag = True
    stparam2.interval = 1
    thread2 = threading.Thread(target = THREAD_TEST, args = (0,stparam2))
    thread2.start()
    
    thread1.join()
    
    #stparam2.flag = False
    thread2.join()
    
    print(f"End")
    pass

if __name__ == '__main__':
    mainloop()