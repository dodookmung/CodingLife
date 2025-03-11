# C언어 함수를 파이썬에 연동하기
속도나 하드웨어 디바이스 드라이버 접근 등을 위해서 C와 연결해서 Python을 사용해야 할 일들은 생기기 마련이다.

- ctypes방법은 파이썬 표준 라이브러리에 포함되어 있다.
    - C로 작성된 코드가 Shared object (*.so)형태로 컴파일 되어 있어야함.

</br>

### GCC 사용해 동적 라이브러리(.so 파일) 생성(컴파일) - DLL도 가능
```
$ gcc -shared -o example.so -fPIC example.c
```
- 동적 라이브러리의 경우 라이브러리를 교체하는 것만으로도 변경이 가능합니다.
- .o는 목적 파일, 2진수로 이루어진 기계어 코드
- -fPIC은 Position-Independent Code의 약자로 example.o 파일을 동적 라이브러리로 사용하도록 하는 컴파일 옵션
- 해당 명령을 실행하면 "example.so" 파일이 생성.

### python에서 ctypes를 이용해 라이브러리 불러오기

Python 스크립트에서 ctypes 모듈을 사용하여 C 라이브러리를 불러올 수 있습니다.

````python
import ctypes

# 라이브러리 불러오기
example = ctypes.CDLL('./example.so')

# C 함수 호출
result = example.add(10, 20)

# 결과 출력
print("결과:", result)
````

### python 스크립트 실행
이제 Python VS Code 또는 터미널에서 python 스크립트를 실행하면 10과 20을 더한 30이 출력됩니다.

<img src="./imgs/sc.png">


</br></br></br>

### Reference

https://movefun-tech.tistory.com/43#GCC%20%EC%82%AC%EC%9A%A9%ED%95%B4%20%EB%8F%99%EC%A0%81%20%EB%9D%BC%EC%9D%B4%EB%B8%8C%EB%9F%AC%EB%A6%AC(.so%20%ED%8C%8C%EC%9D%BC)%20%EC%83%9D%EC%84%B1%20-%20DLL%EB%8F%84%20%EA%B0%80%EB%8A%A5-1

https://goodtogreate.tistory.com/entry/Ctypes%EB%A5%BC-%EC%9D%B4%EC%9A%A9%ED%95%9C-Python%EA%B3%BC-C%EC%99%80%EC%9D%98-%EC%97%B0%EA%B2%B0


### 참고할만한 자료

https://velog.io/@kravi/%ED%8C%8C%EC%9D%B4%EC%8D%AC-ctypes-%ED%99%9C%EC%9A%A9%ED%95%98%EA%B8%B0-Python-with-ctypes

https://nomad-programmer.tistory.com/105