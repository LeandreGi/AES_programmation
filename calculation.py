"""
Utility functions shared by the AES steps.

The AES "state" is a 4x4 matrix of bytes, each byte being an int between 0 and 255.
It is filled column by column (FIPS-197, section 3.4) :

    input bytes : b0 b1 b2 ... b15

    state :  b0  b4  b8  b12
             b1  b5  b9  b13
             b2  b6  b10 b14
             b3  b7  b11 b15

so state[row][col] = block[row + 4 * col].
"""

hexValues = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F"]

def binaryToHex(Byte) :
    """
    Converts a block of 4 bits in hex.
    :param str Byte: a block of 4 bits.
    :return: a hex value.
    """
    byteValue = 0
    count = 0
    for el in reversed(Byte) :
        byteValue += int(el) * (2**count)
        count += 1
    hexValue = hexValues[byteValue]
    return hexValue

def bytesToState(block) :
    """
    Converts a block of 16 bytes into the AES state, filled column by column.
    :param bytes block: the 16 bytes to convert.
    :return: a 4x4 matrix (list of 4 rows) of ints between 0 and 255.
    """
    if len(block) != 16 :
        raise ValueError("An AES block must contain exactly 16 bytes, got " + str(len(block)))
    return [[block[row + 4 * col] for col in range(4)] for row in range(4)]

def stateToBytes(state) :
    """
    Converts the AES state back into a block of 16 bytes, reading it column by column.
    :param list state: a 4x4 matrix of ints between 0 and 255.
    :return: the 16 bytes of the block.
    """
    return bytes(state[row][col] for col in range(4) for row in range(4))

def printMatrix(matrix) :
    """
    Prints a matrix of bytes, each byte displayed as 2 hex digits.
    :param list matrix: a matrix of ints between 0 and 255.
    """
    for row in matrix :
        print(" ".join(format(el, "02X") for el in row))
