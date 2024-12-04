"""
Main function that applies the AES algortithm
Input : Message, nbBytes
Output : Encrypted message
"""

def main(Message, nbBytes) :
    """
    Main function that executes the AES algorithm
    :param str Message: Message, the plain text, that is presented in 32 bytes, 128 bits.
    :param int nbBytes: Number of bytes with which we will execute the algorithm, 128, 192, or 256 bits.
    :return: Returns the encrypted message, the cypher text, as a 32 bytes key, 128 bits.
    """
    return EncryptedMessage