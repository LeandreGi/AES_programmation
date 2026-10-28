import unittest

from ByteSub import S_BOX, INV_S_BOX, substitute, subBytes, invSubBytes


class TestByteSub(unittest.TestCase) :

    def test_known_values(self) :
        # FIPS-197, section 5.1.1 : S-Box(0x53) = 0xED
        self.assertEqual(substitute(0x53, S_BOX), 0xED)
        self.assertEqual(substitute(0x00, S_BOX), 0x63)
        self.assertEqual(substitute(0xED, INV_S_BOX), 0x53)

    def test_sbox_is_a_permutation(self) :
        # Each value from 0 to 255 must appear exactly once, otherwise no inverse exists
        values = sorted(byte for row in S_BOX for byte in row)
        self.assertEqual(values, list(range(256)))

    def test_inverse_sbox_undoes_sbox(self) :
        for x in range(256) :
            self.assertEqual(substitute(substitute(x, S_BOX), INV_S_BOX), x)

    def test_subBytes_fips_round_1(self) :
        # FIPS-197, appendix B : round 1, "Start of Round" -> "After SubBytes"
        start = [
            [0x19, 0xA0, 0x9A, 0xE9],
            [0x3D, 0xF4, 0xC6, 0xF8],
            [0xE3, 0xE2, 0x8D, 0x48],
            [0xBE, 0x2B, 0x2A, 0x08],
        ]
        expected = [
            [0xD4, 0xE0, 0xB8, 0x1E],
            [0x27, 0xBF, 0xB4, 0x41],
            [0x11, 0x98, 0x5D, 0x52],
            [0xAE, 0xF1, 0xE5, 0x30],
        ]
        self.assertEqual(subBytes(start), expected)
        self.assertEqual(invSubBytes(expected), start)


if __name__ == "__main__" :
    unittest.main()
