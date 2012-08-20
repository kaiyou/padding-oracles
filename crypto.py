"""
I am a cipher module
I provide very basic cipher classes and functions to generated pseudo-random
keys and perform AES CBC encryption/decryption
"""

from base64 import b64encode, b64decode
from binascii import hexlify, unhexlify
from StringIO import StringIO
from random import random

import Crypto.Cipher.AES
import Crypto.Hash.MD5

def gen_key():
    """
    I generate a secure key suitable for AES encrypting
    """
    md5 = Crypto.Hash.MD5.new()
    md5.update(str(random())+'salt')
    return md5.digest()

class AES:
    """
    I am a convenient wrapper around the pyCrypto AES API
    """
    
    def __init__(self, key):
        self.aes = Crypto.Cipher.AES.new(key, Crypto.Cipher.AES.MODE_CBC, '\x00'*16)
        
    def encrypt(self, message):
        """
        I perform AES encryption
        """
        return b64encode(self.aes.encrypt(PKCS7.encode(message)))
    
    def decrypt(self, message):
        """
        I perform AES decryption
        """
        clear = self.aes.decrypt(b64decode(message))
        return PKCS7.decode(clear)

class PKCS7:
    """
    I am a 16 bytes PKCS7 code implementation
    """
    
    def __init__(self):
        pass
    
    @staticmethod
    def decode(text):
        """
        I perform PKCS7 decoding
        """
        assert len(text) % 16 == 0
        last = text[-1]
        assert text[-ord(last):] == last * ord(last)
        return text[:-ord(last)]

    @staticmethod
    def encode(text):
        """
        I perform PKCS7 encoding
        """
        missing = 16 - len(text) % 16
        return text + chr(missing) * (missing if missing > 0 else 16)
