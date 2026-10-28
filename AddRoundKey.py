"""
AddRoundKey step of AES (FIPS-197, section 5.1.4).

The round key is made of 4 words of the expanded key, one word per column of the state.
Each word is a list of 4 bytes, and is added (XOR) to the matching column :

    state column c  =  state column c  XOR  word c

It is the only step that uses the key. XOR is its own inverse, so AddRoundKey
is also used as it is in the decryption (FIPS-197, section 5.3.4).
"""

def addRoundKey(state, roundKey) :
    """
    Applies AddRoundKey : XOR of each column of the state with the matching word of the round key.
    state[row][col] is combined with roundKey[col][row], because a word is a column.
    :param list state: the 4x4 AES state.
    :param list roundKey: the 4 words of the round key, each word being a list of 4 bytes.
    :return: a new state, the XOR of the state and the round key.
    """
    newState = [[0 for _ in range(4)] for _ in range(4)]
    for col in range(4) :
        for row in range(4) :
            newState[row][col] = state[row][col] ^ roundKey[col][row]
    return newState
