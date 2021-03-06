# Gauss-Jordan-elimination
## 가우스 조던 소거법

행렬을 `기약 행 사다리꼴` 형태로 만드는 알고리즘.

mxn 행렬 E 가 다음 성질을 만족할 때, 행 사다리꼴(row echelon form)이라고 한다.

    (i) 성분이 모두 0인 행이 존재하면 그 행은 행렬의 맨 아래에 위치한다.
    
    (ii) 각 행에서 처음으로 나타나는 0이 아닌 성분은 1이다. 이때, 이 1을 그 행의 선행 성분(leading entry)이라고 한다.
    
    (iii) i 행과 i+1 행 모두에 선행성분이 존재하면 (i+1) 행의 선행성분은 i 행의 선행 성분보다 오른쪽에 위치한다.
    
      또, 행렬 E 가 행사다리꼴이고 아래의 성질도 만족하면 E를 기약 행 사다리꼴 (reduced row echelon form)이라고 한다.
    
    (iv) 어떤 행의 선행성분을 포함하는 열(column)의 다른 성분은 모두 0이다.
    
    (출처: http://matrix.skku.ac.kr/sglee/linear/ocu/20104.html )
          
## 실행 결과:  
Before:  
    `[[1, 3, -2, 0, 2, 0, 0],`  
     `[2, 6, -5, -2, 4, -3, -1],`  
     `[0, 0, 5, 10, 0, 15, 5],`  
     `[2, 6, 0, 8, 4, 18, 6]]`  
 
After Guess_Jordan:  
    `[[1, 3, 0, 4, 2, 0, 0],`  
     `[0, 0, 1, 2, 0, 0, 0],`  
     `[0, 0, 0, 0, 0, 1, Fraction(1, 3)],`  
     `[0, 0, 0, 0, 0, 0, 0]]`
     
이를 이용하면, 간단한 일차 방정식의 해를 구하는 것도 가능합니다.

## 예시 1
  
    연립방정식 입력: x+y=2
    연립방정식 입력: 3x+y=4
    
    방정식 행렬화 결과
    [1, 1, 2]
    [3, 1, 4]
    
    가우스 조던 소거 결과
    [1, 0, 1]
    [0, 1, 1]
    
    방정식 해 출력
    x = 1
    y = 1

## 예시 2
미지수의 갯수에 구애받지 않습니다.

    연립방정식 입력: x+y+z=4
    연립방정식 입력: 2x+2y+z=6
    연립방정식 입력: y+z=3
    
    방정식 행렬화 결과
    [1, 1, 1, 4]
    [2, 1, 2, 6]
    [1, 1, 0, 3]
    
    가우스 조던 소거 결과
    [1, 0, 0, 1]
    [0, 1, 0, 2]
    [0, 0, 1, 1]
    
    방정식 해 출력
    y = 1
    z = 2
    x = 1
    
## 예시 3

    연립방정식 입력: 3x^2=27
    연립방정식 입력: x^2+y=10
      
    방정식 행렬화 결과
    [3, 0, 27]
    [1, 1, 10]
    
    가우스 조던 소거 결과
    [1, 0, 9]
    [0, 1, 1]
    
    방정식 해 출력
    x^2 = 9
    y = 1

