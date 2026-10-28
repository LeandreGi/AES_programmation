import unittest

from AddRoundKey import addRoundKey
from calculation import bytesToState, stateToBytes


def toWords(hexString) :
    """
    Splits 16 bytes written in hex into 4 words of 4 bytes.
    :param str hexString: 32 hex digits.
    :return: a list of 4 words, each word being a list of 4 bytes.
    """
    block = bytes.fromhex(hexString)
    return [list(block[4 * i : 4 * i + 4]) for i in range(4)]


class TestAddRoundKey(unittest.TestCase) :

    def test_fips_initial_round(self) :
        # FIPS-197, appendix B : "Input" XOR "Round Key Value" (round 0) = start of round 1
        state = bytesToState(bytes.fromhex("3243f6a8885a308d313198a2e0370734"))
        roundKey = toWords("2b7e151628aed2a6abf7158809cf4f3c")
        expected = bytes.fromhex("193de3bea0f4e22b9ac68d2ae9f84808")
        self.assertEqual(stateToBytes(addRoundKey(state, roundKey)), expected)

    def test_fips_round_1(self) :
        # FIPS-197, appendix B : round 1 "After MixColumns" XOR round key 1 = start of round 2
        state = bytes.fromhex("046681e5e0cb199a48f8d37a2806264c")
        roundKey = toWords("a0fafe1788542cb123a339392a6c7605")
        expected = bytes.fromhex("a49c7ff2689f352b6b5bea43026a5049")
        self.assertEqual(stateToBytes(addRoundKey(bytesToState(state), roundKey)), expected)

    def test_fips_last_round(self) :
        # FIPS-197, appendix B : round 10 "After ShiftRows" XOR round key 10 = "Output"
        # (the matrix of the document is read column by column)
        state = bytes.fromhex("e9317db5cb322c723d2e895faf090794")
        roundKey = toWords("d014f9a8c9ee2589e13f0cc8b6630ca6")
        expected = bytes.fromhex("3925841d02dc09fbdc118597196a0b32")
        self.assertEqual(stateToBytes(addRoundKey(bytesToState(state), roundKey)), expected)

    def test_applying_twice_gives_back_the_state(self) :
        # XOR is its own inverse : (s ^ k) ^ k = s
        state = bytesToState(bytes.fromhex("3243f6a8885a308d313198a2e0370734"))
        roundKey = toWords("2b7e151628aed2a6abf7158809cf4f3c")
        self.assertEqual(addRoundKey(addRoundKey(state, roundKey), roundKey), state)

    def test_zero_key_changes_nothing(self) :
        state = bytesToState(bytes(range(16)))
        zeroKey = [[0, 0, 0, 0] for _ in range(4)]
        self.assertEqual(addRoundKey(state, zeroKey), state)

    def test_input_is_not_modified(self) :
        state = bytesToState(bytes(range(16)))
        copy = [row[:] for row in state]
        addRoundKey(state, toWords("2b7e151628aed2a6abf7158809cf4f3c"))
        self.assertEqual(state, copy)


if __name__ == "__main__" :
    unittest.main()
