# 선도 원소의 index 를 찾아줌
def find_lead_element_index(line):
    for index in range(len(line)):
        if line[index] != 0:
            return index

    # 선도 원소가 없을 경우
    return None


# 선도 원소를 1에 맞춰주는 함수
def change_line(line):
    try:
        first_one = line[find_lead_element_index(line)]
    except TypeError:
        # 선도 원소가 없을 경우
        # (find_first_element_index 에서 None 이 넘어왔을 경우)
        return line

    else:
        # 모든 원소에 1/first_one 을 곱한 행을 반환
        return [data * (1 / first_one) for data in line]


def line_elimination(lead_line, other_line, index):
    """
    :param index: 선도 원소 index
    :param lead_line: 선도 원소가 포함된 행
    :param other_line: 소거될 행
    :return: 소거된 후 결과 행
    """

    times = (other_line[index] / lead_line[index]) * -1  # -1 을 곱하여 음수 혹은 양수를 반대로 바꿈 (음수 -> 양수, 양수 -> 음수)

    return [(lead * times + other) for lead, other in zip(lead_line, other_line)]


# 가우스 소거
def guess(matrix):
    # line 행
    # row 열

    # 직접적인 matrix 값을 변경하기 위해 index 로 반복
    for index in range(len(matrix)):
        matrix[index] = change_line(matrix[index])

        lead_element_index = find_lead_element_index(matrix[index])

        # 선도 원소가 없을 경우. (행의 모든 원소가 0일 경우)
        if lead_element_index is None:
            # 맨 마지막 행과 위치를 바꿈
            matrix[index], matrix[len(matrix)-1] = matrix[len(matrix)-1], matrix[index]
            # 다음 행으로 넘어감
            continue

        row = [line[lead_element_index] for line in matrix]  # 해당 Index 의 열 리스트

        for row_index in range(index+1, len(row)):
            # 선도 원소가 아닌데 0이 아닌 값을 가지고 있을 경우
            if row[row_index] != 0:
                matrix[row_index] = line_elimination(matrix[index], matrix[row_index], lead_element_index)

        return matrix

if __name__ == '__main__':
    # 초반 행렬 선언
    matrix = [
        [1.0, 3.0, -2.0, 0.0, 2.0, 0.0, 0.0],
        [2.0, 6.0, -5.0, -2.0, 4.0, -3.0, -1.0],
        [0.0, 0.0, 5.0, 10.0, 0.0, 15.0, 5.0],
        [2.0, 6.0, 0.0, 8.0, 4.0, 18.0, 6.0]
    ]

    matrix = guess(matrix)
