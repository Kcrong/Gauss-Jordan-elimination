from fractions import Fraction
from pprint import pprint


# 선도 원소의 index 를 찾아줌
def find_lead_element_index(line):
    # 첨가 행렬에서의 마지막 값을 유지하기 위해서 len(line)-1 으로 range 를 생성
    for index in range(len(line) - 1):
        if line[index] != 0:
            return index

    # 선도 원소가 없을 경우
    return None


# 나눗셈 결과가 정수, 실수 여부에 따라 반환
def divide_int_or_float(numerator, denominator):
    """
    :param numerator:
    :param denominator:
    :return: int or float data
    """
    result = numerator / denominator

    if result == int(result):  # 계산 결과에 소수점 아래 값이 없을 때
        return int(result)
    else:
        # 분수 값 반환
        return Fraction(int(numerator), int(denominator))


# 선도 원소를 1에 맞춰주는 함수
def change_line(line):
    lead_index = find_lead_element_index(line)
    try:
        first_one = line[lead_index]
    except TypeError:
        # 선도 원소가 없을 경우
        # (find_first_element_index 에서 None 이 넘어왔을 경우)
        return line

    else:
        # 모든 원소를 first_one 으로 나눈 리스트 반환
        return [divide_int_or_float(data, first_one) for data in line]


def line_elimination(lead_line, other_line, index):
    """
    :param index: 선도 원소 index
    :param lead_line: 선도 원소가 포함된 행
    :param other_line: 소거될 행
    :return: 소거된 후 결과 행
    """

    times = (other_line[index] / lead_line[index]) * -1  # -1 을 곱하여 음수 혹은 양수를 반대로 바꿈 (음수 -> 양수, 양수 -> 음수)

    return [int(lead * times + other) for lead, other in zip(lead_line, other_line)]


# 가우스 소거
def guess(matrix):
    # line 행
    # row 열

    # 직접적인 matrix 값을 변경하기 위해 index 로 반복
    for line_index in range(len(matrix)):
        matrix[line_index] = change_line(matrix[line_index])

        lead_element_index = find_lead_element_index(matrix[line_index])

        # 선도 원소가 없을 경우. (행의 모든 원소가 0일 경우)
        if lead_element_index is None:
            # 맨 마지막 행을 선도 원소가 없는 행으로 가져옴
            matrix[line_index] = matrix[len(matrix) - 1]

            # 마지막 행에 0 행렬을 넣음
            matrix[len(matrix) - 1] = [0] * len(matrix[0])
            # 다음 행으로 넘어감
            continue

        row = [line[lead_element_index] for line in matrix]  # 해당 Index 의 열 리스트

        for row_index in range(line_index + 1, len(row)):
            # 선도 원소가 아닌데 0이 아닌 값을 가지고 있을 경우
            if row[row_index] != 0:
                matrix[row_index] = line_elimination(matrix[line_index], matrix[row_index], lead_element_index)

    return matrix


def guess_jordan(matrix):
    matrix = guess(matrix)

    # range 에 step 인자를 직접 주는 것보다, reversed 를 이용하는 것이 더 코드가 깔끔
    for line_index in reversed(range(len(matrix))):
        lead_element_index = find_lead_element_index(matrix[line_index])

        if lead_element_index is None:
            continue

        matrix[line_index] = change_line(matrix[line_index])

        row = [line[lead_element_index] for line in matrix]

        for row_index in range(len(row)):
            if row_index == line_index:
                continue
            elif row[row_index] != 0:
                matrix[row_index] = line_elimination(matrix[line_index], matrix[row_index], lead_element_index)

    return matrix


if __name__ == '__main__':
    # 초반 행렬 선언
    matrix = [
        [1, 3, -2, 0, 2, 0, 0],
        [2, 6, -5, -2, 4, -3, -1],
        [0, 0, 5, 10, 0, 15, 5],
        [2, 6, 0, 8, 4, 18, 6]
    ]
    print("Before: ")
    pprint(matrix)

    matrix = guess_jordan(matrix)

    print("\nAfter Guess_Jordan: ")
    pprint(matrix)
