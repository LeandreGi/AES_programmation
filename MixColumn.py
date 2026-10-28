"""
MixColumns and InvMixColumns steps of AES (FIPS-197, sections 5.1.3 and 5.3.3).

Each column of the state is seen as a polynomial with 4 coefficients in GF(2^8)
and is multiplied by a fixed matrix. All the additions are XOR and all the
multiplications are done with gfMultiply.

    MixColumns :            InvMixColumns :
    02 03 01 01             0E 0B 0D 09
    01 02 03 01             09 0E 0B 0D
    01 01 02 03             0D 09 0E 0B
    03 01 01 02             0B 0D 09 0E
"""

from GaloisField import gfMultiply

MIX_MATRIX = [
    [0x02, 0x03, 0x01, 0x01],
    [0x01, 0x02, 0x03, 0x01],
    [0x01, 0x01, 0x02, 0x03],
    [0x03, 0x01, 0x01, 0x02],
]

INV_MIX_MATRIX = [
    [0x0E, 0x0B, 0x0D, 0x09],
    [0x09, 0x0E, 0x0B, 0x0D],
    [0x0D, 0x09, 0x0E, 0x0B],
    [0x0B, 0x0D, 0x09, 0x0E],
]

def multiplyColumns(state, matrix) :
    """
    Multiplies each column of the state by a 4x4 matrix in GF(2^8).
    For each column c : newState[row][c] = sum over i of matrix[row][i] * state[i][c],
    the sum being a XOR and the product a gfMultiply.
    :param list state: the 4x4 AES state.
    :param list matrix: the 4x4 matrix of bytes to apply on each column.
    :return: a new state with every column multiplied by the matrix.
    """
    newState = [[0 for _ in range(4)] for _ in range(4)]
    for col in range(4) :
        for row in range(4) :
            value = 0
            for i in range(4) :
                value = value ^ gfMultiply(matrix[row][i], state[i][col])
            newState[row][col] = value
    return newState

def mixColumns(state) :
    """
    Applies MixColumns (FIPS-197, section 5.1.3) : each column is multiplied by MIX_MATRIX.
    It mixes the 4 bytes of a column so that each output byte depends on all of them.
    :param list state: the 4x4 AES state.
    :return: the mixed state.
    """
    return multiplyColumns(state, MIX_MATRIX)

def invMixColumns(state) :
    """
    Applies InvMixColumns (FIPS-197, section 5.3.3) : each column is multiplied by INV_MIX_MATRIX,
    which is the inverse of MIX_MATRIX in GF(2^8).
    :param list state: the 4x4 AES state.
    :return: the unmixed state.
    """
    return multiplyColumns(state, INV_MIX_MATRIX)
