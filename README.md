<h1>AES algorithm</h1>

Educational implementation of the AES (Advanced Encryption Standard) block cipher in Python,
written step by step to understand and explain each transformation.
It follows the official standard **FIPS-197** and is checked against its test vectors.

Only the Python standard library is used : no cryptography library.
This code is for learning purposes and must not be used to protect real data.

<h2>Usage</h2>

    python Main.py

encrypts and decrypts the example of FIPS-197 appendix C.1, then a 16-byte message with a random key.

    from Main import cipher, invCipher
    from CreateKey import generateKey

    key = generateKey(16)                     # 16, 24 or 32 bytes : AES-128, AES-192, AES-256
    cipherText = cipher(b"Hello, AES-128 !", key)
    plainText = invCipher(cipherText, key)

Run the tests from the root of the repository :

    python -m unittest discover -s tests -v

<h2>AES's functioning</h2>

AES encrypts a block of 16 bytes, seen as a 4x4 matrix of bytes called the **state**,
filled column by column. The number of rounds depends on the key size :
10 rounds for a 128-bit key, 12 for 192 bits, 14 for 256 bits.

- ***Key expansion*** : the cipher key is expanded into one round key per round, plus one.
- ***Initial key addition*** : the state is combined with the first round key (the cipher key itself).

Then, for each round of the algorithm, except the last one, we do :
- ***Byte Substitution***
- ***Shift Row***
- ***Mix Columns***
- ***Key addition layer***

The last round is the same, without Mix Columns.
Decryption applies the inverse of each step, in the reverse order, with the round keys from the last to the first.

<h2>Byte Substitution</h2>

Each byte of the state is replaced by another byte, read in a fixed table called the **S-Box** :
the 4 high bits give the row, the 4 low bits give the column.
It is the only non-linear step of AES : it prevents an attacker from describing the cipher with simple equations.
Decryption uses the inverse S-Box.

<h2>Shift Row</h2>

Each row of the state is shifted to the left by its index : row 0 is not shifted, row 1 by one byte,
row 2 by two bytes, row 3 by three bytes.
The bytes of a column are spread over the 4 columns, so that the columns do not stay independent.

<h2>Mix Columns</h2>

Each column is multiplied by a fixed matrix, in the finite field GF(2^8) :
the addition is a XOR, the multiplication is done modulo the polynomial x^8 + x^4 + x^3 + x + 1.
Each output byte depends on the 4 bytes of the column.
With Shift Row, this gives the **diffusion** : after a few rounds, each byte of the cipher text depends on all the bytes of the plain text.

<h2>Key addition layer</h2>

The state is combined with the round key by a XOR, byte by byte.
It is the only step that uses the key : all the other steps are public and could be undone by anyone.
XOR is its own inverse, so the same step is used to decrypt.

<h2>Key expansion</h2>

The cipher key is split into words of 4 bytes, and new words are computed from the previous ones
until there are enough for every round (44 words for AES-128).
Every few words, the word is rotated (RotWord), passed through the S-Box (SubWord)
and combined with a round constant (Rcon), so that each round key is different and non-linearly linked to the key.

<h2>Project structure</h2>

| File | Content |
|---|---|
| `calculation.py` | Conversions between a block of 16 bytes and the state |
| `ByteSub.py` | Byte Substitution and its inverse, S-Box |
| `ShiftRow.py` | Shift Row and its inverse |
| `GaloisField.py` | Arithmetic in GF(2^8) |
| `MixColumn.py` | Mix Columns and its inverse |
| `AddRoundKey.py` | Key addition layer |
| `CreateKey.py` | Key generation and key expansion |
| `Main.py` | Full encryption and decryption of a block |
| `tests/` | Unit tests, based on the FIPS-197 test vectors |

<h2>Limits</h2>

- Only one block of 16 bytes is encrypted at a time. A longer message would need padding and a mode of operation (CBC, CTR...).
- The code favours readability over speed and is not protected against side-channel attacks.

<h2>Reference</h2>

NIST, *FIPS-197 : Advanced Encryption Standard (AES)*.
