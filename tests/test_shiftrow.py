import unittest

from ShiftRow import shiftRows, invShiftRows


# Matrix 0..15 filled row by row : makes the shift easy to read
SIMPLE = [[row * 4 + col for col in range(4)] for row in range(4)]


class TestShiftRows(unittest.TestCase) :

    def test_each_row_shifted_left_by_its_index(self) :
        expected = [
            [0, 1, 2, 3],      # row 0 : not shifted
            [5, 6, 7, 4],      # row 1 : shifted by 1
            [10, 11, 8, 9],    # row 2 : shifted by 2
            [15, 12, 13, 14],  # row 3 : shifted by 3
        ]
        self.assertEqual(shiftRows(SIMPLE), expected)

    def test_fips_round_1(self) :
        # FIPS-197, appendix B : round 1, "After SubBytes" -> "After ShiftRows"
        afterSubBytes = [
            [0xD4, 0xE0, 0xB8, 0x1E],
            [0x27, 0xBF, 0xB4, 0x41],
            [0x11, 0x98, 0x5D, 0x52],
            [0xAE, 0xF1, 0xE5, 0x30],
        ]
        expected = [
            [0xD4, 0xE0, 0xB8, 0x1E],
            [0xBF, 0xB4, 0x41, 0x27],
            [0x5D, 0x52, 0x11, 0x98],
            [0x30, 0xAE, 0xF1, 0xE5],
        ]
        self.assertEqual(shiftRows(afterSubBytes), expected)
        self.assertEqual(invShiftRows(expected), afterSubBytes)

    def test_inverse_undoes_shift(self) :
        self.assertEqual(invShiftRows(shiftRows(SIMPLE)), SIMPLE)
        self.assertEqual(shiftRows(invShiftRows(SIMPLE)), SIMPLE)

    def test_input_is_not_modified(self) :
        copy = [row[:] for row in SIMPLE]
        shiftRows(SIMPLE)
        self.assertEqual(SIMPLE, copy)


if __name__ == "__main__" :
    unittest.main()
