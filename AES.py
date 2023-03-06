# -*- coding: utf-8 -*-
"""
@author: david
"""

import numpy as np


class AES():
    def __init__(self, key):
        self.key = key  
        
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