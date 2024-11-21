from multiprocessing import shared_memory

import numpy as np
import cv2
TARGET_WIDTH = 640
TAREGET_HEIGHT= 480
TARGET_DEPTH = 3

def RunRecive(shm_name):
    
    
    # Shared Memory 테스트용, shared 메모리로부터 배열을 받아서,
    # print('[arr_stream] getting ')
    existing_shm = shared_memory.SharedMemory(name=shm_name)


    shared_a = np.frombuffer(existing_shm.buf, dtype=np.int32)
    
    npArray = np.array([(shared_a[0], shared_a[1], shared_a[2], shared_a[3], shared_a[4], shared_a[5])], dtype=[('memsize','i4'),('width', 'i4'), ('height', 'i4'), ('depth', 'i4'), ('count', 'i4'), ('buff', 'a921600')])
    
    npArray[0]['buff'] = existing_shm.buf[20:].tobytes()
    
    c = np.ndarray(shape=(npArray[0]['height'], npArray[0]['width'], npArray[0]['depth']), dtype=np.uint8, buffer=existing_shm.buf[20:])
    #c = np.ndarray(shape=(TAREGET_HEIGHT, TARGET_WIDTH, TARGET_DEPTH), dtype=np.uint8, buffer=existing_shm.buf)
    
    
    

    print(type(c))
    print(shared_a.shape, c.shape)

    while True:
        cv2.imshow('Shm_Recive', c)
        if cv2.waitKey(int(1000 / 24)) == ord('q'):
            break

    existing_shm.unlink()
    existing_shm.close()
    # 영상 파일과 창 닫기
    cv2.destroyAllWindows()