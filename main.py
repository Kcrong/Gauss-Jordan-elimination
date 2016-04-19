import re
from fractions import Fraction


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


def remove_condition(split_equation_list):
    for i in range(len(split_equation_list)):
        for condition in {'+', '/', '*', '='}:
            while True:
                try:
                    split_equation_list[i].remove(condition)
                except ValueError:
                    break

    return split_equation_list


def get_variable_dict(split_equation_list):
    all_variable = list()

    for equation in split_equation_list:
        var_num_dict = dict()
        for piece in equation[:len(equation) - 1]:
            # if piece.isnumeric() is False:  # 문자가 섞여있으면
            try:
                int_piece = int(piece)
            except ValueError:
                # 변수 (x,y,z..) 의 인덱스 값
                var_index = piece.find(re.sub("([0-9])", "", piece))

                # 각 조각에서 계수와 미지수를 가져온다.
                num_data = piece[:var_index]  # 계수 데이터

                if num_data == '':  # 계수가 1이라 생략된 경우에
                    num = 1
                else:  # 아닐 경우, int 형으로 저장
                    num = int(num_data)

                var = piece[var_index:]  # 미지수

                var_num_dict[var] = num

            else:
                equation[-1] = int(equation[-1]) - int_piece

        # 방정식 결과 값을 '$result' 라는 이름으로 dict 에 저장한다
        var_num_dict['$result'] = equation[-1]

        all_variable.append(var_num_dict)

    return all_variable


def get_all_var_name(all_variable):
    # 총 미지수 목록
    var_list = list()

    for variable in all_variable:
        var_list += list(variable.keys())
    var_list = set(var_list)  # 중복 제거
    var_list.remove('$result')

    return var_list


def equation2matrix(equation_list):
    # 연산자 단위로 식을 나눔.
    # 그 후 연산자를 모두 제거
    split_equation_list = remove_condition(
        [re.split("([+/*=])", equation.replace(" ", "")) for equation in equation_list])

    all_variable = get_variable_dict(split_equation_list)

    # 행렬 생성 부분
    matrix = list()

    all_var_name = get_all_var_name(all_variable)

    for i in range(len(equation_list)):
        line = list()
        for var_name in all_var_name:
            try:
                line.append(all_variable[i][var_name])
            except KeyError:  # 해당 미지수가 없는 식일 경우
                line.append(0)
        line.append(int(all_variable[i]['$result']))
        matrix.append(line)  # 행렬에 행 추가

    return all_var_name, matrix


def check_equation(equation):
    # 등호가 들어있고 길이가 1 보다 큰 지 확인
    return '=' in equation and len(equation) > 1


def pprint(data):
    for i in data:
        print(i)


def get_user_equation():
    equation_list = list()
    print("입력 종료는 'done' 입력")
    while True:
        equation = input("연립방정식 입력: ")

        if equation == 'done':
            break
        elif check_equation(equation) is False:
            print("잘못된 식입니다!")
        else:
            equation_list.append(equation)

    return equation_list


def find_var_result(var_names, matrix):
    result_dict = dict()

    # 행렬의 모든 값을 정수형으로 변환
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            matrix[i][j] = int(matrix[i][j])

    for line in matrix:
        for line_index in range(len(line)-1):
            if line[line_index] != 0:
                zero_count = line[:len(line)-1].count(0)
                if (len(line)-1) - zero_count == 1:
                    result_dict[var_names[line_index]] = str(line[-1])
                    continue

                for i in range(line_index+1, len(line)-1):
                    if line[i] == 0 or line[i] == '0':
                        continue
                    else:
                        if line[-1] == 0:
                            line[-1] = ''
                        tmp_result = (str(line[-1]) + str(line[i]*-1) + var_names[i]).replace('1', '')
                        result_dict[var_names[line_index]] = tmp_result
                        line[-1] = tmp_result

                break

    return result_dict

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

    print('\n\n\n')

    equation_list = get_user_equation()

    all_var_name, matrix = equation2matrix(equation_list)

    print("방정식 행렬화 결과")

    pprint(matrix)

    print("\n가우스 조던 소거 결과")

    result_matrix = guess_jordan(matrix)
    pprint(result_matrix)

    print("\n방정식 해 출력")

    result_dict = find_var_result(list(all_var_name), result_matrix)

    for key in result_dict.keys():
        print("%s = %s" % (key, result_dict[key]))
