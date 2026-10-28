"""
Key generation and key expansion of AES (FIPS-197, section 5.2).

The key expansion (or key schedule) turns the cipher key into Nb * (Nr + 1) words,
a word being a list of 4 bytes. AddRoundKey uses 4 of these words at each round.

    key size    Nk (words in the key)    Nr (rounds)    words produced
    AES-128     4                        10             44
    AES-192     6                        12             52
    AES-256     8                        14             60
"""

import secrets

from ByteSub import S_BOX, substitute
from GaloisField import xtime

NB = 4  # number of columns of the state, always 4 in AES

def generateKey(nbBytes=16) :
    """
    Generates a random cipher key.
    secrets is used instead of random : random is predictable and must never be used for a key.
    :param int nbBytes: size of the key in bytes, 16, 24 or 32 (AES-128, AES-192, AES-256).
    :return: the key, as bytes.
    """
    if nbBytes not in (16, 24, 32) :
        raise ValueError("An AES key must be 16, 24 or 32 bytes long, got " + str(nbBytes))
    return secrets.token_bytes(nbBytes)

def rotWord(word) :
    """
    Cyclic permutation of a word (FIPS-197, section 5.2) : [a0, a1, a2, a3] -> [a1, a2, a3, a0].
    :param list word: a word of 4 bytes.
    :return: the rotated word.
    """
    return word[1:] + word[:1]

def subWord(word) :
    """
    Applies the S-Box to each byte of a word (FIPS-197, section 5.2).
    :param list word: a word of 4 bytes.
    :return: the substituted word.
    """
    return [substitute(byte, S_BOX) for byte in word]

def xorWords(word1, word2) :
    """
    Adds two words in GF(2^8), byte by byte, i.e. a XOR.
    :param list word1: a word of 4 bytes.
    :param list word2: a word of 4 bytes.
    :return: the word word1 XOR word2.
    """
    return [word1[i] ^ word2[i] for i in range(4)]

def rcon(i) :
    """
    Round constant Rcon[i] = [x^(i-1), 0x00, 0x00, 0x00] (FIPS-197, section 5.2).
    x^(i-1) is computed in GF(2^8) by applying xtime i-1 times on 0x01 :
    01, 02, 04, 08, 10, 20, 40, 80, 1B, 36...
    :param int i: index of the constant, starting at 1.
    :return: the word Rcon[i].
    """
    value = 0x01
    for _ in range(i - 1) :
        value = xtime(value)
    return [value, 0x00, 0x00, 0x00]

def keyExpansion(key) :
    """
    Expands the cipher key into the key schedule, following the pseudo code of FIPS-197, figure 11.
    The first Nk words are the key itself. Then each word w[i] is w[i - Nk] XOR temp, where temp is
    w[i - 1], transformed by RotWord, SubWord and Rcon once every Nk words
    (and only by SubWord at the middle of each block of 8 words for AES-256).
    :param bytes key: the cipher key, 16, 24 or 32 bytes long.
    :return: the list of the Nb * (Nr + 1) words, each word being a list of 4 bytes.
    """
    if len(key) not in (16, 24, 32) :
        raise ValueError("An AES key must be 16, 24 or 32 bytes long, got " + str(len(key)))
    nk = len(key) // 4
    nr = nk + 6

    words = [list(key[4 * i : 4 * i + 4]) for i in range(nk)]
    for i in range(nk, NB * (nr + 1)) :
        temp = words[i - 1]
        if i % nk == 0 :
            temp = xorWords(subWord(rotWord(temp)), rcon(i // nk))
        elif nk > 6 and i % nk == 4 :
            temp = subWord(temp)
        words.append(xorWords(words[i - nk], temp))
    return words
