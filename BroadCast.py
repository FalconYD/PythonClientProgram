from multiprocessing import shared_memory
import numpy as np
import cv2

TARGET_WIDTH = 640
TAREGET_HEIGHT= 480
TARGET_DEPTH = 3
video_path = '1.mp4'




#if __name__ == '__main__' or __name__ == 'run':
def RunBroadCast():
    imgsize = TARGET_WIDTH * TAREGET_HEIGHT * TARGET_DEPTH
    memsize = imgsize + 20
    stream_shm = shared_memory.SharedMemory(name ='FalconEyes',create=True, size=memsize)
    npArray = np.array([(memsize, TARGET_WIDTH, TAREGET_HEIGHT, TARGET_DEPTH, 0, None)], dtype=[('memsize','i4'),('width', 'i4'), ('height', 'i4'), ('depth', 'i4'), ('count', 'i4'), ('buff', 'a921600')])
    
    
    #cap = cv2.VideoCapture(video_path)
    cap = cv2.VideoCapture(0)

    # 영상 파일이 정상적으로 열렸는지 확인
    if not cap.isOpened():
        print("영상 파일을 열 수 없습니다.")
        exit()

    # 영상의 프레임 너비와 높이 가져오기
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # 출력할 창 생성
    cv2.namedWindow('Broadcasting', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('Broadcasting', frame_width, frame_height)

    while True:
        # 영상에서 프레임 읽기
        ret, frame = cap.read()

        # 프레임을 제대로 읽지 못한 경우 종료
        if not ret:
            break

        # 프레임 출력
        cv2.imshow('Broadcasting', frame)

        cvMat = np.ndarray(frame.shape, dtype=frame.dtype, buffer=frame.data)
        #cvMat = cvMat.reshape(-1,cvMat.nbytes)
        #cvMat = cvMat.ravel()
        #npArray['buff'] = frame.data
        #npArray.dtype = [('memsize','i4'),('width', 'i4'), ('height', 'i4'), ('depth', 'i4'), ('count', 'i4'), ('buff', cvMat.dtype)]
        npArray[0]['buff'] = cvMat.data.tobytes()
        #npArray[0]['buff'] = cvMat[:]

        shmem = np.ndarray(npArray.shape, dtype=npArray.dtype, buffer=stream_shm.buf)
        shmem[:] = npArray

        #stream_shm.buf = struct.pack('iiiiiP', stMem.Memsize, stMem.width, stMem.height, stMem.channel, stMem.count, stMem.buff)
        #shared_a = np.ndarray(npArray.shape, dtype=npArray.dtype, buffer=npArray.buf)
        #shared_a[:] = frame.data
        
        if(cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT)):
            cap.open(video_path)

        # 'q' 키를 누르면 종료
        if cv2.waitKey(1) == ord('q'):
            break

    stream_shm.unlink()
    stream_shm.close()
    cap.release()
    cv2.destroyAllWindows()