import unittest

from GaloisField import xtime, gfMultiply


class TestXtime(unittest.TestCase) :

    def test_fips_example(self) :
        # FIPS-197, section 4.2.1 : repeated xtime on 0x57
        self.assertEqual(xtime(0x57), 0xAE)
        self.assertEqual(xtime(0xAE), 0x47)
        self.assertEqual(xtime(0x47), 0x8E)
        self.assertEqual(xtime(0x8E), 0x07)

    def test_no_reduction_when_bit_7_is_clear(self) :
        self.assertEqual(xtime(0x01), 0x02)
        self.assertEqual(xtime(0x40), 0x80)

    def test_reduction_when_bit_7_is_set(self) :
        # 0x80 * x = x^8, reduced to x^4 + x^3 + x + 1 = 0x1B
        self.assertEqual(xtime(0x80), 0x1B)

    def test_result_is_always_a_byte(self) :
        for a in range(256) :
            self.assertTrue(0 <= xtime(a) <= 255)


class TestGfMultiply(unittest.TestCase) :

    def test_fips_examples(self) :
        # FIPS-197, section 4.2 and 4.2.1
        self.assertEqual(gfMultiply(0x57, 0x83), 0xC1)
        self.assertEqual(gfMultiply(0x57, 0x13), 0xFE)

    def test_multiplying_by_2_is_xtime(self) :
        for a in range(256) :
            self.assertEqual(gfMultiply(a, 0x02), xtime(a))

    def test_neutral_and_absorbing_elements(self) :
        for a in range(256) :
            self.assertEqual(gfMultiply(a, 0x01), a)
            self.assertEqual(gfMultiply(a, 0x00), 0)

    def test_commutative_and_always_a_byte(self) :
        for a in range(256) :
            for b in range(256) :
                product = gfMultiply(a, b)
                self.assertTrue(0 <= product <= 255)
                self.assertEqual(product, gfMultiply(b, a))

    def test_distributive_over_xor(self) :
        # a * (b + c) = a * b + a * c, the addition being a XOR
        for a, b, c in [(0x57, 0x83, 0x13), (0xFF, 0x0E, 0x09), (0x02, 0x80, 0x7F)] :
            self.assertEqual(gfMultiply(a, b ^ c), gfMultiply(a, b) ^ gfMultiply(a, c))


if __name__ == "__main__" :
    unittest.main()
