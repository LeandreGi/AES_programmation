import random
from calculation import binaryToHex

def CreateKey(nbBytes) :
    keyBits = ""
    key = ""
    for bytes in range(nbBytes//4) :
        for bits in range(4) :
            keyBits += str(random.randint(0, 1))
        key += binaryToHex(keyBits)
        keyBits = ""
    key_temp = key
    key = ""
    for val in reversed(key_temp) :
        key += val
    return key

print(CreateKey(128))