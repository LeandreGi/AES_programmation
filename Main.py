"""
Full AES : encryption and decryption of one block of 16 bytes (FIPS-197, sections 5.1 and 5.3).

    cipher :                             invCipher :
    AddRoundKey (round 0)                AddRoundKey (round Nr)
    for round 1 to Nr - 1 :              for round Nr - 1 down to 1 :
        SubBytes                             InvShiftRows
        ShiftRows                            InvSubBytes
        MixColumns                           AddRoundKey
        AddRoundKey                          InvMixColumns
    SubBytes                             InvShiftRows
    ShiftRows                            InvSubBytes
    AddRoundKey (round Nr)               AddRoundKey (round 0)

The last round has no MixColumns. Nr is 10, 12 or 14 for a key of 16, 24 or 32 bytes.
"""

from calculation import bytesToState, stateToBytes
from ByteSub import subBytes, invSubBytes
from ShiftRow import shiftRows, invShiftRows
from MixColumn import mixColumns, invMixColumns
from AddRoundKey import addRoundKey
from CreateKey import keyExpansion, generateKey, NB

def getRoundKey(words, round) :
    """
    Extracts the round key of a round from the key schedule : the 4 words w[4 * round] to w[4 * round + 3].
    :param list words: the key schedule, as returned by keyExpansion.
    :param int round: the number of the round, from 0 to Nr.
    :return: the 4 words of the round key.
    """
    return words[NB * round : NB * (round + 1)]

def cipher(block, key) :
    """
    Encrypts one block of 16 bytes (FIPS-197, section 5.1, figure 5).
    :param bytes block: the plain text, 16 bytes.
    :param bytes key: the cipher key, 16, 24 or 32 bytes.
    :return: the cipher text, 16 bytes.
    """
    words = keyExpansion(key)
    nr = len(words) // NB - 1

    state = bytesToState(block)
    state = addRoundKey(state, getRoundKey(words, 0))
    for round in range(1, nr) :
        state = subBytes(state)
        state = shiftRows(state)
        state = mixColumns(state)
        state = addRoundKey(state, getRoundKey(words, round))
    state = subBytes(state)
    state = shiftRows(state)
    state = addRoundKey(state, getRoundKey(words, nr))
    return stateToBytes(state)

def invCipher(block, key) :
    """
    Decrypts one block of 16 bytes (FIPS-197, section 5.3, figure 12).
    The steps of cipher are undone in the reverse order, with the round keys from the last to the first.
    :param bytes block: the cipher text, 16 bytes.
    :param bytes key: the cipher key used to encrypt, 16, 24 or 32 bytes.
    :return: the plain text, 16 bytes.
    """
    words = keyExpansion(key)
    nr = len(words) // NB - 1

    state = bytesToState(block)
    state = addRoundKey(state, getRoundKey(words, nr))
    for round in range(nr - 1, 0, -1) :
        state = invShiftRows(state)
        state = invSubBytes(state)
        state = addRoundKey(state, getRoundKey(words, round))
        state = invMixColumns(state)
    state = invShiftRows(state)
    state = invSubBytes(state)
    state = addRoundKey(state, getRoundKey(words, 0))
    return stateToBytes(state)

if __name__ == "__main__" :
    # Example of FIPS-197, appendix C.1 (AES-128)
    plainText = bytes.fromhex("00112233445566778899aabbccddeeff")
    key = bytes.fromhex("000102030405060708090a0b0c0d0e0f")
    cipherText = cipher(plainText, key)
    print("FIPS-197 appendix C.1")
    print("  plain text  :", plainText.hex())
    print("  key         :", key.hex())
    print("  cipher text :", cipherText.hex(), "(expected 69c4e0d86a7b0430d8cdb78070b4c55a)")
    print("  decrypted   :", invCipher(cipherText, key).hex())

    # A message of exactly 16 bytes, with a random key
    message = "Hello, AES-128 !".encode()
    key = generateKey(16)
    cipherText = cipher(message, key)
    print("Random key")
    print("  message     :", message.decode())
    print("  key         :", key.hex())
    print("  cipher text :", cipherText.hex())
    print("  decrypted   :", invCipher(cipherText, key).decode())
