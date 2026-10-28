import unittest

from calculation import bytesToState, stateToBytes


# Input block of FIPS-197, appendix B
FIPS_INPUT = bytes.fromhex("3243f6a8885a308d313198a2e0370734")


class TestStateConversion(unittest.TestCase) :

    def test_bytesToState_fills_column_by_column(self) :
        # Expected state as printed in FIPS-197, appendix B
        expected = [
            [0x32, 0x88, 0x31, 0xE0],
            [0x43, 0x5A, 0x31, 0x37],
            [0xF6, 0x30, 0x98, 0x07],
            [0xA8, 0x8D, 0xA2, 0x34],
        ]
        self.assertEqual(bytesToState(FIPS_INPUT), expected)

    def test_round_trip(self) :
        self.assertEqual(stateToBytes(bytesToState(FIPS_INPUT)), FIPS_INPUT)

    def test_wrong_length_is_rejected(self) :
        with self.assertRaises(ValueError) :
            bytesToState(b"too short")


if __name__ == "__main__" :
    unittest.main()
