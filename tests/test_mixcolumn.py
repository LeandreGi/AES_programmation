import unittest

from MixColumn import mixColumns, invMixColumns, MIX_MATRIX, INV_MIX_MATRIX
from GaloisField import gfMultiply


# FIPS-197, appendix B : round 1, "After ShiftRows"
AFTER_SHIFT_ROWS = [
    [0xD4, 0xE0, 0xB8, 0x1E],
    [0xBF, 0xB4, 0x41, 0x27],
    [0x5D, 0x52, 0x11, 0x98],
    [0x30, 0xAE, 0xF1, 0xE5],
]

# FIPS-197, appendix B : round 1, "After MixColumns"
AFTER_MIX_COLUMNS = [
    [0x04, 0xE0, 0x48, 0x28],
    [0x66, 0xCB, 0xF8, 0x06],
    [0x81, 0x19, 0xD3, 0x26],
    [0xE5, 0x9A, 0x7A, 0x4C],
]


class TestMixColumns(unittest.TestCase) :

    def test_fips_round_1(self) :
        self.assertEqual(mixColumns(AFTER_SHIFT_ROWS), AFTER_MIX_COLUMNS)

    def test_inverse_fips_round_1(self) :
        self.assertEqual(invMixColumns(AFTER_MIX_COLUMNS), AFTER_SHIFT_ROWS)

    def test_matrices_are_inverse(self) :
        # MIX_MATRIX * INV_MIX_MATRIX must be the identity matrix in GF(2^8)
        for row in range(4) :
            for col in range(4) :
                value = 0
                for i in range(4) :
                    value = value ^ gfMultiply(MIX_MATRIX[row][i], INV_MIX_MATRIX[i][col])
                self.assertEqual(value, 1 if row == col else 0)

    def test_round_trip(self) :
        state = [[(row * 4 + col) * 17 % 256 for col in range(4)] for row in range(4)]
        self.assertEqual(invMixColumns(mixColumns(state)), state)
        self.assertEqual(mixColumns(invMixColumns(state)), state)

    def test_input_is_not_modified(self) :
        copy = [row[:] for row in AFTER_SHIFT_ROWS]
        mixColumns(AFTER_SHIFT_ROWS)
        invMixColumns(AFTER_SHIFT_ROWS)
        self.assertEqual(AFTER_SHIFT_ROWS, copy)


if __name__ == "__main__" :
    unittest.main()
