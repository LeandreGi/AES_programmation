import unittest

from Main import cipher, invCipher, getRoundKey
from CreateKey import keyExpansion, generateKey


PLAIN_TEXT = bytes.fromhex("00112233445566778899aabbccddeeff")

# FIPS-197, appendix C : (key, expected cipher text) for the plain text above
FIPS_VECTORS = [
    # C.1 : AES-128
    ("000102030405060708090a0b0c0d0e0f",
     "69c4e0d86a7b0430d8cdb78070b4c55a"),
    # C.2 : AES-192
    ("000102030405060708090a0b0c0d0e0f1011121314151617",
     "dda97ca4864cdfe06eaf70a0ec0d7191"),
    # C.3 : AES-256
    ("000102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f",
     "8ea2b7ca516745bfeafc49904b496089"),
]


class TestGetRoundKey(unittest.TestCase) :

    def test_fips_round_keys(self) :
        # FIPS-197, appendix B : round keys 0 and 10
        words = keyExpansion(bytes.fromhex("2b7e151628aed2a6abf7158809cf4f3c"))
        self.assertEqual(bytes(sum(getRoundKey(words, 0), [])).hex(), "2b7e151628aed2a6abf7158809cf4f3c")
        self.assertEqual(bytes(sum(getRoundKey(words, 10), [])).hex(), "d014f9a8c9ee2589e13f0cc8b6630ca6")


class TestCipher(unittest.TestCase) :

    def test_fips_appendix_b(self) :
        # FIPS-197, appendix B : "Input" and "Cipher Key" give "Output"
        plainText = bytes.fromhex("3243f6a8885a308d313198a2e0370734")
        key = bytes.fromhex("2b7e151628aed2a6abf7158809cf4f3c")
        self.assertEqual(cipher(plainText, key).hex(), "3925841d02dc09fbdc118597196a0b32")

    def test_fips_appendix_c(self) :
        for key, expected in FIPS_VECTORS :
            with self.subTest(keySize=len(key) * 4) :
                self.assertEqual(cipher(PLAIN_TEXT, bytes.fromhex(key)).hex(), expected)


class TestInvCipher(unittest.TestCase) :

    def test_fips_appendix_c(self) :
        for key, cipherText in FIPS_VECTORS :
            with self.subTest(keySize=len(key) * 4) :
                self.assertEqual(invCipher(bytes.fromhex(cipherText), bytes.fromhex(key)), PLAIN_TEXT)

    def test_round_trip_with_random_keys(self) :
        message = "Hello, AES-128 !".encode()
        for nbBytes in (16, 24, 32) :
            key = generateKey(nbBytes)
            self.assertEqual(invCipher(cipher(message, key), key), message)

    def test_wrong_key_does_not_decrypt(self) :
        key = bytes.fromhex(FIPS_VECTORS[0][0])
        wrongKey = bytes(16)
        self.assertNotEqual(invCipher(cipher(PLAIN_TEXT, key), wrongKey), PLAIN_TEXT)


if __name__ == "__main__" :
    unittest.main()
