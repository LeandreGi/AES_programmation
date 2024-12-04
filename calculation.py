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

def hexToBinary(hex) :
    return

def reverseMatrix() :
    return

print(binaryToHex("1001"))
print(int("1001", 16))