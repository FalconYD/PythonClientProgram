# Python Shared Memory
 파이썬과 공유메모리 통신을 하는 이기종 언어 (C++, C#) 예제.
 C#, C++은 MemoryMappedFile로 "FalconEyes"라는 이름의 공유메모리를 생성하여 데이터를 업로드(복사)하고,
 파이썬은 "FalconEyes"라는 공유메모리가 있을 때, 해당 구조체 데이터를 업데이트한다.
## C#, C++ Struct
struct SharedMem
{
  int size;
  int width;
  int height;
  int depth;
  int count;
  unsigned char* buff;
}
