# -*- coding: utf-8 -*-
"""
@authors: david & guille
"""

import numpy as np

def ROTL8(x, shift):
    return ((x) << (shift)) | ((x) >> (8 - (shift)))

class AES():
    def __init__(self, key):
        self.key = key
        self.make_sbox()
        
    def transform_block(self, block, rounds):
        self.key_i = self.key.copy()
        self.block = block
        self.add_round_key()
        for _ in range(rounds - 1):
            self.byte_sub()
            self.shift_row()
            self.mix_column()
            self.add_round_key()
        self.byte_sub()
        self.shift_row()
        self.add_round_key()
        return self.block
    
    def add_round_key(self):
        self.transform_key()
        self.block = self.block ^ self.key_i
        
    def byte_sub(self):
        # The goal of this function is to perform the byte substitution 
        # (hence the name) of each element in the message block, using the
        # corresponding elements of the substitution bytes matrix.
        
        pass
    
    def shift_row(self):
        pass
    
    def mix_column(self):
        # Polynomial reduction / capping the result
        poly = 0b100011011
        cap = lambda num: num ^ poly if num >> 8 else num
        
        # Multiplication functions
        x1 = lambda num: num
        x2 = lambda num: cap(num << 1)
        x3 = lambda num: x2(num) ^ num
        mix = np.array([
            [x2, x3, x1, x1],
            [x1, x2, x3, x1],
            [x1, x1, x2, x3],
            [x3, x1, x1, x2]
        ])
        
        # Matrix multiplication
        result = np.zeros((4, 4), dtype='int')
        for i in range(4):
            for j in range(4):
                for k in range(4):
                    result[i,j] ^= mix[i,k](self.block[k,j])
        
        # Save result
        self.block = result

    def transform_key(self):
        pass
    
    def make_sbox(self):
        # Code adapted from Wikipedia:
            # https://en.wikipedia.org/wiki/Rijndael_S-box
        p = 1
        q = 1
        firstTime = True
        sbox = np.zeros((256), dtype=np.ubyte)
        
        while p != 1 or firstTime:
            # multiply p by 3
            p = p ^ (p << 1) ^ (0x1B if (p & 0x80) else 0)
            
            # divide q by 3 (equals multiplication by 0xf6)
            q ^= q << 1
            q ^= q << 2
            q ^= q << 4
            q ^= 0x09 if q & 0x80 else 0

            
            # compute the affine transformation
            xformed = q ^ ROTL8(q, 1) ^ ROTL8(q, 2) ^ ROTL8(q, 3) ^ ROTL8(q, 4);
            
            sbox[p] = xformed ^ 0x63
            firstTime = False
        
        # 0 is a special case since it has no inverse
        sbox[0] = 0x63;
        
        self.sbox=sbox
        