"""
Arithmetic on bytes in the finite field GF(2^8), used by MixColumns (FIPS-197, section 4).

A byte is seen as a polynomial of degree < 8 whose coefficients are its bits :
    0x57 = 0101 0111 = x^6 + x^4 + x^2 + x + 1

- Addition is a XOR : coefficients are added modulo 2, so 1 + 1 = 0.
- Multiplication is a polynomial multiplication, reduced modulo the AES polynomial
      m(x) = x^8 + x^4 + x^3 + x + 1   (0x11B)
  so that the result always fits in one byte.
"""

AES_POLYNOMIAL = 0x11B  # x^8 + x^4 + x^3 + x + 1

def xtime(a) :
    """
    Multiplies a byte by x, i.e. by 0x02 (FIPS-197, section 4.2.1).
    It is a shift of one bit to the left. If the bit 7 was set, the result has a x^8 term
    and does not fit in a byte any more : it is then reduced by XOR with m(x).
    :param int a: a byte, between 0 and 255.
    :return: a * 0x02 in GF(2^8), between 0 and 255.
    """
    a = a << 1
    if a & 0x100 :
        a = a ^ AES_POLYNOMIAL
    return a

def gfMultiply(a, b) :
    """
    Multiplies two bytes in GF(2^8).
    b is decomposed into powers of 2 : for each bit of b set to 1, the matching
    a * x^i is added (XOR) to the result. a * x^i is obtained by repeating xtime.
    Example : 0x57 * 0x13 = 0x57 * (0x01 + 0x02 + 0x10)
                          = 0x57 ^ xtime(0x57) ^ xtime(xtime(xtime(xtime(0x57))))
    :param int a: a byte, between 0 and 255.
    :param int b: a byte, between 0 and 255.
    :return: a * b in GF(2^8), between 0 and 255.
    """
    result = 0
    while b :
        if b & 1 :
            result = result ^ a
        a = xtime(a)
        b = b >> 1
    return result
