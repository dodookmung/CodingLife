import ctypes

# 라이브러리 불러오기
example = ctypes.CDLL('./example.so')

# C 함수 호출
result = example.add(10, 20)

# 결과 출력
print("결과:", result)