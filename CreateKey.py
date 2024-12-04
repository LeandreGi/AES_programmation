import random

hexValues = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F"]

def ByteCalculation(Byte) :
    byteValue = 0
    count = 0
    for el in reversed(Byte) :
        byteValue += int(el) * (2**count)
        count += 1
    hexValue = hexValues[byteValue]
    return hexValue

def CreateKey(nbBytes) :
    keyBits = ""
    key = ""
    for bytes in range(nbBytes//4) :
        for bits in range(4) :
            keyBits += str(random.randint(0, 1))
        key += ByteCalculation(keyBits)
        keyBits = ""
    key_temp = key
    key = ""
    for val in reversed(key_temp) :
        key += val
    return key

print(CreateKey(128))