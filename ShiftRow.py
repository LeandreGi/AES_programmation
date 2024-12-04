from calculation import printMatrix

testMatrix = [[y for y in range(i * 4, (i+1)*4)]for i in range(4)]

def shiftRow(matrix) :
    """
    Function that applies the shift row. For each line of the matrix, the line is shifted on the left as much time as it's index.
    For line 0, the line is shifted 0 times, for the line 1, the line is shifted by 1, etc...
    :param list matrix: The matrix that will be shifted.
    :return: The shifted matrix.
    """

    shiftedMatrix = [[0 for _ in range(4)]for _ in range(4)]
    for i in range(len(matrix)) :
        for el in range(4) :
            shiftedMatrix[i][el-i%4] = matrix[i][el]
    return shiftedMatrix

def reverseShiftRow(matrix) :
    """
    Function that applies the inverse of shift row. For each line of the matrix, the line is shifted on the left as much time as it's index.
    For line 0, the line is shifted 0 times, for the line 1, the line is shifted by 1, etc...
    :param list matrix: The matrix that will be shifted.
    :return: The shifted matrix.
    """

    unshiftedMatrix = [[0 for _ in range(4)]for _ in range(4)]
    for i in range(len(matrix)) :
        for el in range(4) :
            unshiftedMatrix[i][el] = matrix[i][(el-i)%4]
    return unshiftedMatrix