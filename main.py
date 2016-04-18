# 선도 원소의 index 를 찾아줌
def find_first_element_index(line):
    for index in range(len(line)):
        if line[index] != 0:
            return index

    # 선도 원소가 없을 경우
    return None


# 선도 원소를 1에 맞춰주는 함수
def change_line(line):
    try:
        first_one = line[find_first_element_index(line)]
    except TypeError:
        # 선도 원소가 없을 경우
        # (find_first_element_index 에서 None 이 넘어왔을 경우)
        return line

    else:
        # 모든 원소에 1/first_one 을 곱한 행을 반환
        return [data * (1 / first_one) for data in line]


# 가우스 소거
def guess(matrix):
    # line 행
    # row 열

    # 직접적인 matrix 값을 변경하기 위해 index 로 반복
    for index in range(len(matrix)):
        matrix[index] = change_line(matrix[index])

        row = [line[index] for line in matrix]
        print(1)


if __name__ == '__main__':
    # 초반 행렬 선언
    matrix = [
        [1, 3, -2, 0, 2, 0, 0],
        [2, 6, -5, -2, 4, -3, -1],
        [0, 0, 5, 10, 0, 15, 5],
        [2, 6, 0, 8, 4, 18, 6]
    ]
    guess(matrix)
