def shiftRows(state) :
    """
    Function that applies the shift row. For each line of the state, the line is shifted on the left as much time as it's index.
    For line 0, the line is shifted 0 times, for the line 1, the line is shifted by 1, etc...
    :param list state: The 4x4 AES state that will be shifted.
    :return: The shifted state.
    """

    shiftedState = [[0 for _ in range(4)] for _ in range(4)]
    for i in range(4) :
        for el in range(4) :
            shiftedState[i][(el - i) % 4] = state[i][el]
    return shiftedState

def invShiftRows(state) :
    """
    Function that applies the inverse of shift row. For each line of the state, the line is shifted on the right as much time as it's index.
    For line 0, the line is shifted 0 times, for the line 1, the line is shifted by 1, etc...
    :param list state: The 4x4 AES state that will be shifted back.
    :return: The unshifted state.
    """

    unshiftedState = [[0 for _ in range(4)] for _ in range(4)]
    for i in range(4) :
        for el in range(4) :
            unshiftedState[i][el] = state[i][(el - i) % 4]
    return unshiftedState
