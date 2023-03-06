# -*- coding: utf-8 -*-
"""
@author: david
"""

import numpy as np


class AES():
    MIX_MATRIX = np.array([
        [2, 3, 1, 1],
        [1, 2, 3, 1],
        [1, 1, 2, 3],
        [3, 1, 1, 2]
    ], dtype = 'int')
    
    POLYNOMIAL = 0b100011011
    
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
        self.block = AES.MIX_MATRIX @ self.block
        

    def transform_key(self):
        pass