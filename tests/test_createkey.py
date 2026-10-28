import unittest

from CreateKey import generateKey, rotWord, subWord, rcon, keyExpansion


def toHex(word) :
    """
    Writes a word as 8 hex digits, like in FIPS-197 appendix A.
    :param list word: a word of 4 bytes.
    :return: the word in hex.
    """
    return bytes(word).hex()


class TestGenerateKey(unittest.TestCase) :

    def test_sizes(self) :
        for nbBytes in (16, 24, 32) :
            key = generateKey(nbBytes)
            self.assertIsInstance(key, bytes)
            self.assertEqual(len(key), nbBytes)

    def test_default_is_aes_128(self) :
        self.assertEqual(len(generateKey()), 16)

    def test_two_keys_are_different(self) :
        self.assertNotEqual(generateKey(), generateKey())

    def test_invalid_size(self) :
        with self.assertRaises(ValueError) :
            generateKey(10)


class TestKeyExpansionSteps(unittest.TestCase) :

    def test_fips_first_word(self) :
        # FIPS-197, appendix A.1 : i = 4, temp = w[3] = 09cf4f3c
        temp = [0x09, 0xCF, 0x4F, 0x3C]
        self.assertEqual(toHex(rotWord(temp)), "cf4f3c09")
        self.assertEqual(toHex(subWord(rotWord(temp))), "8a84eb01")
        self.assertEqual(toHex(rcon(1)), "01000000")

    def test_rcon_values(self) :
        # FIPS-197, appendix A.1 : Rcon[1] to Rcon[10]
        expected = [0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1B, 0x36]
        self.assertEqual([rcon(i)[0] for i in range(1, 11)], expected)

    def test_input_is_not_modified(self) :
        word = [0x09, 0xCF, 0x4F, 0x3C]
        rotWord(word)
        subWord(word)
        self.assertEqual(word, [0x09, 0xCF, 0x4F, 0x3C])


class TestKeyExpansion(unittest.TestCase) :

    def test_fips_aes_128(self) :
        # FIPS-197, appendix A.1
        words = keyExpansion(bytes.fromhex("2b7e151628aed2a6abf7158809cf4f3c"))
        self.assertEqual(len(words), 44)
        self.assertEqual(toHex(words[0]), "2b7e1516")
        self.assertEqual(toHex(words[3]), "09cf4f3c")
        self.assertEqual([toHex(w) for w in words[4:8]], ["a0fafe17", "88542cb1", "23a33939", "2a6c7605"])
        self.assertEqual([toHex(w) for w in words[40:44]], ["d014f9a8", "c9ee2589", "e13f0cc8", "b6630ca6"])

    def test_fips_aes_192(self) :
        # FIPS-197, appendix A.2
        words = keyExpansion(bytes.fromhex("8e73b0f7da0e6452c810f32b809079e562f8ead2522c6b7b"))
        self.assertEqual(len(words), 52)
        self.assertEqual(toHex(words[6]), "fe0c91f7")
        self.assertEqual(toHex(words[51]), "01002202")

    def test_fips_aes_256(self) :
        # FIPS-197, appendix A.3
        words = keyExpansion(bytes.fromhex("603deb1015ca71be2b73aef0857d77811f352c073b6108d72d9810a30914dff4"))
        self.assertEqual(len(words), 60)
        self.assertEqual(toHex(words[8]), "9ba35411")
        self.assertEqual(toHex(words[59]), "706c631e")

    def test_invalid_key_size(self) :
        with self.assertRaises(ValueError) :
            keyExpansion(bytes(10))


if __name__ == "__main__" :
    unittest.main()
